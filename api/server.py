import os
from flask import Flask, jsonify, request, make_response, current_app, redirect, url_for, send_from_directory
import user, patient, test
from init import server
from functools import update_wrapper
from datetime import timedelta
from werkzeug.utils import secure_filename
from model import test as cnn

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower in ALLOWED_EXTENSIONS

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

@server.route("/upload", methods=['POST', 'GET'])
@crossdomain(origin="*")
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify(code = 400, message = "No image in request")
        file = request.files['image']
        if file.filename == '':
            return jsonify(code = 400, message = "No image in request")
        if file.filename != '':
            if "class" in file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
                return jsonify(code = 200, message = "Uploading done!", filename = filename)
            else:
                return jsonify(code = 400, message = "Image is not that of a biopsy slide!")
        else: 
            return jsonify(message = "Uploading failed!")

@server.route("/upload/<filename>")
@crossdomain(origin="*")
def uploaded_file(filename):
    return send_from_directory(server.config['UPLOAD_FOLDER'], filename)

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

    if process != None:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    else:
        response = jsonify(message = False, code = 500, data = "Error occured. Please try again")
        response.status_code = 500
    return response

@server.route("/user/list", methods=["GET"])
@crossdomain(origin="*")
def listUsers():
    response = user.listUsers()

    if response == []:
        response = jsonify(message = False, code = 200, data = [])
        response.status_code = 200
    else:
        response = jsonify(message = True, code = 200, data = response)
        response.status_code = 200
    return response

@server.route("/user/delete", methods=["POST"])
@crossdomain(origin="*")
def deleteUser():
    id = request.form.get('id')
    process = user.deleteUser(id)
    
    if process == 200:
        response = jsonify(message = True, code = 200)
        response.status_code = 200
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

    if process != None:
        data = [{'username': process.username, 'group': process.group}]
        response = jsonify(message=True, code = 200, data = data)
        response.status_code = 200
    else:
        response = jsonify(message=False, code = 404, data = "Username or password incorrect")
        response.status_code = 404
    return response

@server.route("/patient/create", methods=["POST"])
@crossdomain(origin="*")
def createPatient():
    name = request.form.get('name')
    age = request.form.get('age')
    height = request.form.get('height')
    weight = request.form.get('weight')
    gender = request.form.get('gender')
    blood_group = request.form.get('blood_group')
    genotype = request.form.get('genotype')

    process = patient.addPatient(name, age, gender, height, weight, blood_group, genotype)
    if process != None:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    else:
        response = jsonify(message = False, code = 500, data = "Error occured. Please try again")
        response.status_code = 500
    return response

@server.route("/patient/list", methods=["GET"])
@crossdomain(origin="*")
def listPatients():
    process = patient.listPatients()
    if process == []:
        response = jsonify(message = True, code = 200, data = [])
        response.status_code = 200
    else:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    return response

@server.route("/patient/read", methods=["POST"])
@crossdomain(origin="*")
def getPatient():
    id = request.form.get('id')
    process = patient.getPatient(id)

    if process == None or process == [] or process == {}:
        response = jsonify(message = True, code = 200, data = [])
        response.status_code = 200
    else:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    return response

@server.route("/patient/update", methods=["POST"])
@crossdomain(origin="*")
def editPatient():
    id = request.form.get('id')
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    height = request.form.get('height')
    weight = request.form.get('weight')
    blood_group = request.form.get('blood_group')
    genotype = request.form.get('genotype')

    process = patient.editPatient(id, name, age, gender, height, weight, blood_group, genotype)

    if process != None:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    else:
        response = jsonify(message = False, code = 500, data = "Error occured. Please try again")
        response.status_code = 500
    return response

@server.route("/patient/delete", methods=["POST"])
@crossdomain(origin="*")
def deletePatient():
    id = request.form.get('id')
    process = patient.deletePatient(id)
    
    if process == 200:
        response = jsonify(message = True, code = 200)
        response.status_code = 200
    else:
        response = jsonify(message = False, code = 500, data = "Error occured. Please try again")
        response.status_code = 500
    return response

@server.route("/test/list", methods=["GET"])
@crossdomain(origin="*")
def listTest():
    process = test.listTest()
    if process == []:
        response = jsonify(message = True, code = 200, data = [])
        response.status_code = 200
    else:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    return response

@server.route("/test/read", methods=["POST"])
@crossdomain(origin="*")
def getTest():
    id = request.form.get('id')
    process = test.getTest(id)

    if process == None or process == [] or process == {}:
        response = jsonify(message = True, code = 200, data = [])
        response.status_code = 200
    else:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    return response

@server.route("/test/read_by_patient", methods=["POST"])
@crossdomain(origin="*")
def getPatientTest():
    patient_id = request.form.get('patient_id')
    process = test.getPatientTest(patient_id)

    if process == None or process == [] or process == {}:
        response = jsonify(message = True, code = 200, data = [])
        response.status_code = 200
    else:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    return response

@server.route("/test/positive", methods=["GET"])
@crossdomain(origin="*")
def positiveTests():
    process = test.positiveTest()
    if process == []:
        response = jsonify(message = True, code = 200, data = [])
        response.status_code = 200
    else:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    return response

@server.route("/test/negative", methods=["GET"])
@crossdomain(origin="*")
def negativeTests():
    process = test.negativeTest()
    if process == []:
        response = jsonify(message = True, code = 200, data = [])
        response.status_code = 200
    else:
        response = jsonify(message = True, code = 200, data = process)
        response.status_code = 200
    return response

@server.route("/test/run", methods=["POST"])
@crossdomain(origin="*")
def diagnosis():
    patient_id = request.form.get('patient_id')
    timestamp = request.form.get('timestamp')
    image = request.form.get('img')
    if 'image' not in request.files:
        return jsonify(code = 400, message = "No image in request")
    file = request.files['image']
    if file.filename == '':
        return jsonify(code = 400, message = "No image in request")
    if file.filename != '':
        res = cnn.predict(file)
        #print(res)
        process = test.addTest(patient_id, timestamp, res['response'], res['accuracy'], image)
        return jsonify(code = 200, data = process)

if __name__ == '__main__':
    server.run('0.0.0.0', port=2701, debug=True)