from flask import Flask, jsonify, request, make_response, current_app
import user, patient as patient, json
from init import server
from functools import update_wrapper
from datetime import timedelta

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, list):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, list):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@server.route("/")
@crossdomain(origin="*")
def welcome():
    response = jsonify(message = "Medical Imaging: Breast Cancer Server", code = 200)
    response.status_code = 200
    return response

@server.route("/user/signup", methods=["POST"])
@crossdomain(origin="*")
def signup():
    username = request.form.get('username')
    password = request.form.get('hash')
    group = request.form.get('group')

    process = user.createUser(username, password, group)
    if process is 200:
        response = jsonify(message = True, code = 200)
        response.status_code = 200
    elif process is 201:
        response = jsonify(message = False, code = 201)
        response.status_code = 201
    else:
        response = jsonify(message = False, code = 500, data = "Error occured. Please try again")
        response.status_code = 500
    return response

@server.route("/user/login", methods=["POST"])
@crossdomain(origin="*")
def login():
    username = request.form.get('username')
    password = request.form.get('hash')
    process = user.checkUser(username, password)

    if process is None:
        response = jsonify(message=False, code = 404, data = "Username or password incorrect")
        response.status_code = 404
    else:
        data = [{'username': process.username, 'group': process.group}]
        response = jsonify(message=True, code = 200, data = data)
        response.status_code = 200
    return response

@server.route("/user/check_group", methods=["POST"])
@crossdomain(origin="*")
def checkGroup():
    group = request.form.get('group')
    users = user.checkGroup(group)
    
    user_array = []

    for _user in users:
        data = {'username': _user.username, 'group': _user.group}
        user_array.append(data)
        
    response = jsonify(message=True, code = 200, data = user_array)
    response.status_code = 200

    return response

@server.route("/user/list", methods=["GET"])
@crossdomain(origin="*")
def listUsers():
    users = user.list()
    user_array = []

    for _user in users:
        data = {'username': _user.username, 'group': _user.group, 'id': _user.id}
        user_array.append(data)
    response = jsonify(message=True, code = 200, data = user_array)
    response.status_code = 200
    return response

@server.route("/user/single", methods=["POST"])
@crossdomain(origin="*")
def singleUser():
    id = request.form.get('id')
    process = user.getUser(id)

    if process is None:
        response = jsonify(message=True, code = 200, data = [])
        response.status_code = 200
    else:
        _array = []
        data = {'username': process.username, 'group': process.group}
        _array.append(data)
        response = jsonify(message=True, code = 200, data = _array)
        response.status_code = 200
    return response

@server.route("/user/modify", methods=["POST"])
@crossdomain(origin="*")
def modifyUser():
    id = request.form.get('id')
    group = request.form.get('group')
    process = user.modifyUser(id, group)

    if process is 200:
        response = jsonify(message=True, code = 200, data="User modified")
        response.status_code = 200
    return response

@server.route("/user/delete", methods=["POST"])
@crossdomain(origin="*")
def deleteUser():
    id = request.form.get('id')
    process = user.deleteUser(id)

    if process is 200:
        response = jsonify(message=True, code = 200, data="User deleted")
        response.status_code = 200
    return response

@server.route("/patient/create", methods=["POST"])
@crossdomain(origin="*")
def createPatient():
    name = request.form.get('name')
    age = request.form.get('age')
    height = request.form.get('height')
    weight = request.form.get('weight')
    group = request.form.get('group')
    genotype = request.form.get('genotype')

    process = patient.createPatient(name, age, height, weight, group, genotype)
    if process is 200:
        response = jsonify(message = True, code = 200)
        response.status_code = 200
    elif process is 201:
        response = jsonify(message = False, code = 201)
        response.status_code = 201
    else:
        response = jsonify(message = False, code = 500, data = "Error occured. Please try again")
        response.status_code = 500
    return response

@server.route("/patient/list", methods=["GET"])
@crossdomain(origin="*")
def listPatients():
    patients = patient.list()
    patient_array = []

    for _patient in patients:
        data = {'name': _patient.name, 'age': _patient.age, 'height': _patient.height, 'weight': _patient.weight, 'id': _patient.id}
        patient_array.append(data)
    response = jsonify(message=True, code = 200, data = patient_array)
    response.status_code = 200
    return response

@server.route("/patient/single", methods=["POST"])
@crossdomain(origin="*")
def singlePatient():
    id = request.form.get('id')
    process = patient.getPatient(id)

    if process is None:
        response = jsonify(message=True, code = 200, data = [])
        response.status_code = 200
    else:
        _array = []
        data = {
            'name': process.name, 'age': process.age, 
            'height': process.height, 'weight': process.weight, 
            'id': process.id, 'group': process.group, 'genotype': process.genotype
            }
        _array.append(data)
        response = jsonify(message=True, code = 200, data = _array)
        response.status_code = 200
    return response

@server.route("/patient/modify", methods=["POST"])
@crossdomain(origin="*")
def modifyPatient():
    id = request.form.get('id')
    name = request.form.get('name')
    age = request.form.get('age')
    height = request.form.get('height')
    weight = request.form.get('weight')
    group = request.form.get('group')
    genotype = request.form.get('genotype')
    process = patient.modifyPatient(id, name, age, height, weight, group, genotype)

    if process is 200:
        response = jsonify(message=True, code = 200, data="Patient modified")
        response.status_code = 200
    return response

@server.route("/patient/delete", methods=["POST"])
@crossdomain(origin="*")
def deletePatient():
    id = request.form.get('id')
    process = patient.deletePatient(id)

    if process is 200:
        response = jsonify(message=True, code = 200, data="Patient deleted")
        response.status_code = 200
    return response

if __name__ == '__main__':
    server.run('0.0.0.0', port=2701, debug=True)