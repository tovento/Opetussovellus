from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM Users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        #TODO: invalid username
        pass
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            #TODO: invalid password
            pass

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registration", methods=["POST"])
def registration():
    username = request.form["username"]
    password = request.form["password"]
    if "teacher" in request.form:
        teacher = request.form["teacher"]
    else:
        teacher = False
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO Users (username, password, teacher) " \
          "VALUES (:username, :password, :teacher)"
    db.session.execute(
            sql, {"username":username, "password":hash_value,
            "teacher": teacher})
    db.session.commit()
    #TODO: check username doesn't exist
    #TODO: Info on successful registration
    return redirect("/")
