from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = __name__
server = Flask(app)

basedir = os.path.abspath(os.path.dirname(__file__))
#server.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bcmis.sqlite')
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
        fields = ('id', 'username', 'password', 'group')

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    blood_group = db.Column(db.String(80))
    genotype = db.Column(db.String(80))

    def __init__(self, name, age, gender, height, weight, blood_group, genotype):
        self.name = name
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.blood_group = blood_group
        self.genotype = genotype

class PatientSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'gender', 'height', 'weight', 'blood_group', 'genotype')

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    confidence = db.Column(db.Float)
    result = db.Column(db.String(80))
    image = db.Column(db.String(80))

    def __init__(self, patient_id, timestamp, result, confidence, image):
        self.patient_id = patient_id
        self.timestamp = timestamp
        self.result = result
        self.confidence = confidence
        self.image = image

class TestSchema(marsh.Schema):
    class Meta:
        fields = ('id', 'patient_id', 'timestamp', 'result', 'confidence', 'image')

user_schema = UserSchema()
users_schema = UserSchema(many = True)

patient_schema = PatientSchema()
patients_schema = PatientSchema(many = True)

test_schema = TestSchema()
tests_schema = TestSchema(many = True)