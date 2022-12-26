from . import db
from flask_login import UserMixin

#setting up a relationship (foreign key)
#user_id=db.Column(db.Integer,db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(500))
    first_name=db.Column(db.String(150))
    #notes=db.relationship('Note')