import bcrypt
from init import db, marsh, user_schema, users_schema, User

def createUser(_username, _password, _group):
    user = User.query.filter_by(username=_username).first()
    if user is None:
        username = _username
        password = bcrypt.hashpw(_password.encode('utf8'), bcrypt.gensalt())
        group = _group

        new_user = User(username, password, group)

        db.session.add(new_user)
        db.session.commit()
        data = user_schema.dump(new_user).data
        response = 200
    else:
        response = 201
    return response

def checkUser(_username, _password):
    user = User.query.filter_by(username=_username).first()
    passwordCheck = bcrypt.checkpw(_password.encode('utf8'), user.password);
    if passwordCheck == True:
        response = user
    else:
        response = None
    return response

def checkGroup(_group):
    users = User.query.filter_by(group=_group).all()
    return users

def list():
    users = User.query.all()
    return users

def getUser(id):
    user = User.query.get(id)
    if user is None:
        response = None
    else:
        response = user
    return response

def modifyUser(id, _group):
    user = User.query.get(id)
    username = user.username
    hash = user.password

    user.username = username
    user.password = hash
    user.group = _group

    db.session.commit()
    return 200

def deleteUser(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return 200
