from email.policy import default
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/img/49468"


class Pet(db.Model):

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(33), nullable = False)
    species = db.Column(db.String(33), nullable = False)
    image_URL = db.Column(db.String, default = DEFAULT_IMAGE_URL)
    age = db.Column(db.Integer)
    notes = db.Column(db.String)
    available = db.Column(db.Boolean, nullable = False, default = True)

    def image_url(self):
        """returns image for a pet"""

        return self.image_URL or DEFAULT_IMAGE_URL

def connect_db(app):

    db.app = app
    db.init_app(app)


    