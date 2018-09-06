from flask import Flask, request, jsonify
import bcrypt
from init import db, marsh, user_schema, users_schema, User

def createUser(_username, _password, _group):
    username = _username
    password = bcrypt.hashpw(_password.encode('utf8'), bcrypt.gensalt())
    group = _group

    new_user = User(username, password, group)

    db.session.add(new_user)
    db.session.commit()
    return 200

def checkUser(_username, _password):
    user = User.query.filter_by(username=_username).first()
    if user == None:
        response = None
    else:
        passwordCheck = bcrypt.checkpw(_password.encode('utf8'), user.password)
        if passwordCheck == True:
            response = user
        else:
            response = None
    return response

def listUsers():
    users = User.query.all()
    result = users_schema.dump(users).data
    return result

def deleteUser(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return 200