from flask import Flask, request, jsonify
import bcrypt
from init import db, marsh, patient_schema, patients_schema, Patient

def addPatient(_name, _age, _gender, _height, _weight, _blood_group, _genotype):
    name = _name
    age = _age
    gender = _gender
    height = _height
    weight = _weight
    blood_group = _blood_group
    genotype = _genotype

    new_patient = Patient(name, age, gender, height, weight, blood_group, genotype)

    db.session.add(new_patient)
    db.session.commit()

    _patient = patient_schema.dump(new_patient).data
    return _patient

def listPatients():
    patients = Patient.query.all()
    result = patients_schema.dump(patients).data
    return result

def getPatient(id):
    patient = Patient.query.get(id)
    return patient_schema.dump(patient).data

def editPatient(id, name, age, gender, height, weight, blood_group, genotype):
    patient = Patient.query.get(id)
    patient.name = name
    patient.age = age
    patient.gender = gender
    patient.height = height
    patient.weight = weight
    patient.blood_group = blood_group
    patient.genotype = genotype
    db.session.commit()
    _patient = patient_schema.dump(patient).data
    return _patient

def deletePatient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return 200