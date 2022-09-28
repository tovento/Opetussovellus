from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password, teacher FROM Users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["teacher"] = user.teacher
            session["id"] = user.id
            return True
        else:
            return False

def logout():
    del session["username"]

def register(username, password, teacher):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username, password, teacher) " \
              "VALUES (:username, :password, :teacher)"
        db.session.execute(
                sql, {"username":username, "password":hash_value,
                "teacher": teacher})
        db.session.commit()
    except:
        return False
    return True

