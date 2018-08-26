from flask import Flask, request, jsonify
import bcrypt
from init import db, marsh, test_schema, tests_schema, Test

def addTest(_patient_id, _timestamp, _result):
    patient_id = _patient_id
    timestamp = _timestamp
    result = _result

    new_test = Test(patient_id, timestamp, result)

    db.session.add(new_test)
    db.session.commit()
    return 200

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