from init import db, marsh, patient_schema, patients_schema, Patient

def createPatient(_name, _age, _height, _weight):
    patient = Patient.query.filter_by(name=_name).first()
    if patient is None:
        new_patient = Patient(_name, _age, _height, _weight)
        db.session.add(new_patient)
        db.session.commit()
        data = patient_schema.dump(new_patient).data
        response = 200
    else:
        response = 201
    return response

def list():
    patients = Patient.query.all()
    return patients

def getPatient(id):
    patient = Patient.query.get(id)
    if patient is None:
        response = None
    else:
        response = patient
    return response

def modifyPatient(id, _name, _age, _height, _weight):
    patient = Patient.query.get(id)
    patient.name = _name
    patient.age = _age
    patient.height = _height
    patient.weight = _weight

    db.session.commit()
    return 200

def deletePatient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return 200
