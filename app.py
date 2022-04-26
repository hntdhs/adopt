from crypt import methods
from flask import Flask, url_for, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful; however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.route("/")
def list_all_pets():
    """shows a page listing all pets in database"""

    pets = Pet.query.all()
    return render_template("pet_list.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """add new pet to database"""

    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        # list comprehension that's taking all data from the form except the csrf token
        new_pet = Pet(**data)
        # new_pet = Pet(name=form.name.data, age=form.age.data, ...)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect(url_for('list_all_pets'))

    else:
        # re-present form for editing
        return render_template("add_pet_form.html", form=form)

@app.route("/<int:pet_id>", methods=["GET", "POST"])
# Why is the URL not edit/<int:pet_id>? - could do it that way but it's implied that it's for editing if you do it like this
def edit_pet(pet_id):
    """edit existing pet in database"""
    
    pet = Pet.query_or_404(pet_id)
    form = EditPetForm(obj=pet)
    # why does it pass in obj=pet as opposed to just pet?
    # obj=None is default for obj

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.image_url = form.image_url.data
        db.session.commit()
        flash(f"{pet.name} updated")
        return redirect(url_for('list_pets'))
        # why url_for and not just the Flask route? - b/c redirect, it expects a string

        # Why is this different from the route immediately above where we saved all the data to a variable to a variable called new_pet using new_pet = Pet(**data)? Could we do something like edited_pet = Pet(**data) and commit that?

    else:
        """form didn't validate so this brings it up again to try again"""
        return render_template("pet_edit_form.html", form=form, pet=pet)

# @app.route("/api/pets/<int:pet_id>", methods=['GET'])
# def api_get_pet(pet_id):
#     """Return basic info about pet in JSON."""

#     pet = Pet.query.get_or_404(pet_id)
#     info = {"name": pet.name, "age": pet.age}

#     return jsonify(info)