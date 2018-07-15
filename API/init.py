from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = __name__
server = Flask(app)

basedir = os.path.abspath(os.path.dirname(__file__))
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'context.sqlite')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(server)
marsh = Marshmallow(server)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(10), unique = False)
    group = db.Column(db.String(80), unique = False)

    def __init__(self, username, password, group):
        self.username = username
        self.password = password
        self.group = group

class UserSchema(marsh.Schema):
    class Meta:
        field = ('id', 'username', 'password', 'group')

user_schema = UserSchema()
users_schema = UserSchema(many = True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = False)
    age = db.Column(db.String(80), unique = False)
    height = db.Column(db.String(80), unique = False)
    weight = db.Column(db.String(80), unique = False)
    group = db.Column(db.String(80), unique = False)
    genotype = db.Column(db.String(80), unique = False)

    def __init__(self, name, age, height, weight, group, genotype):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.group = group
        self.genotype = genotype

class PatientSchema(marsh.Schema):
    class Meta:
        field = ('id', 'name', 'age', 'height', 'weight', 'group', 'genotype')

patient_schema = PatientSchema()
patients_schema = PatientSchema(many = True)
