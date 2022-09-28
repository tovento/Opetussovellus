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
    sql = "SELECT id, name FROM Courses"
    result = db.session.execute(sql)
    courses = result.fetchall()
    return render_template("index.html", courses=courses)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password, teacher FROM Users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        #TODO: invalid username
        pass
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["teacher"] = user.teacher
            session["id"] = user.id
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
        teacher = True
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

@app.route("/newtask/<int:course_id>")
def newtask(course_id):
    sql = "SELECT name FROM Courses WHERE id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    course_name = result.fetchone()[0]
    return render_template("newtask.html", course_id=course_id,
            course_name=course_name)

@app.route("/create", methods=["POST"])
def create():
    question = request.form["question"]
    course_id = request.form["course_id"]
    sql = "INSERT INTO Tasks (course_id, question)" \
          "VALUES (:course_id, :question) RETURNING id"
    result = db.session.execute(sql, {"course_id":course_id, "question":question})
    task_id = result.fetchone()[0]
    choices = request.form.getlist("choice")
    correct_choice = request.form["correct"]
    for i in range(len(choices)):
        if choices[i] != "":
            correct = i == int(correct_choice)
            sql = "INSERT INTO Choices (task_id, choice, correct) " \
                    "VALUES (:task_id, :choice, :correct)"
            db.session.execute(sql,
                               {"task_id":task_id,
                               "choice":choices[i],
                               "correct":correct})
    db.session.commit()
    return render_template("create.html", course_id=course_id)

@app.route("/newcourse")
def newcourse():
    return render_template("newcourse.html")

@app.route("/createcourse", methods=["POST"])
def createcourse():
    name = request.form["name"]
    teacher_id = session["id"]
    sql = "INSERT INTO Courses (name, teacher_id) VALUES " \
          "(:name, :teacher_id) RETURNING id"
    result = db.session.execute(sql, {"name":name, "teacher_id":teacher_id})
    course_id = result.fetchone()[0]
    db.session.commit()
    return redirect(f"/coursepage/{course_id}")

@app.route("/coursepage/<int:id>")
def coursepage(id):
    sql = "SELECT id, question FROM Tasks WHERE course_id=:id"
    result = db.session.execute(sql, {"id":id})
    tasks = result.fetchall()
    sql = "SELECT name, teacher_id FROM Courses WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    course = result.fetchone()
    name = course[0]
    teacher_id = course[1]
    return render_template("coursepage.html", id=id, tasks=tasks,
                           name=name, teacher_id=teacher_id)

@app.route("/task/<int:id>")
def task(id):
    sql = "SELECT question FROM Tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    question = result.fetchone()[0]
    sql = "SELECT id, choice FROM Choices WHERE task_id=:id"
    result = db.session.execute(sql, {"id":id})
    choices = result.fetchall()
    return render_template("task.html", id=id, question=question,
            choices=choices)

@app.route("/answer", methods= ["POST"])
def answer():
    task_id = request.form["id"]
    student_id = session["id"]
    if "answer" in request.form:
        choice_id = request.form["answer"]
        sql = "INSERT INTO Answers (task_id, student_id, choice_id) " \
              "VALUES (:task_id, :student_id, :choice_id)"
        db.session.execute(sql,
                           {"task_id":task_id,
                           "student_id":student_id,
                           "choice_id":choice_id})
        db.session.commit()
    return redirect("/") #JONNEKIN
