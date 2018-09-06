from flask import Flask, request, jsonify
import bcrypt
from init import db, marsh, test_schema, tests_schema, Test

def addTest(_patient_id, _timestamp, _result, _confidence, _img):
    patient_id = _patient_id
    timestamp = _timestamp
    result = _result
    image = _img
    confidence = _confidence

    new_test = Test(patient_id, timestamp, result, confidence, image)
    db.session.add(new_test)
    db.session.commit()
    result = test_schema.dump(new_test).data
    return result

def listTest():
    tests = Test.query.all()
    result = tests_schema.dump(tests).data
    return result

def positiveTest():
    tests = Test.query.filter_by(result="positive").all()
    result = tests_schema.dump(tests).data
    return result
    
def negativeTest():
    tests = Test.query.filter_by(result="negative").all()
    result = tests_schema.dump(tests).data
    return result

def getTest(id):
    test = Test.query.get(id)
    result = test_schema.dump(test).data
    return result

def getPatientTest(id):
    test = Test.query.filter_by(patient_id=id).all()
    result = tests_schema.dump(test).data
    return result