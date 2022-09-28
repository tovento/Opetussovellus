from app import app
from db import db
from flask import render_template, redirect, request, session
import users, courses

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
    if users.login(username, password):
        return redirect("/")
    else:
        #TODO
        pass

@app.route("/logout")
def logout():
    users.logout()
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
    
    # TODO: check 2 passwords match
    if users.register(username, password, teacher):
        return redirect("/")
    else:
        #TODO: check username doesn't exist
        #TODO: Info on successful registration
        pass

@app.route("/newcourse", methods=["GET", "POST"])
def newcourse():
    if request.method == "GET":
        return render_template("newcourse.html")
    if request.method == "POST":
        name = request.form["name"]
        teacher_id = session["id"]
        course_id = courses.newcourse(name, teacher_id)
        return redirect(f"/coursepage/{course_id}")

@app.route("/coursepage/<int:id>")
def coursepage(id):
    tasks, name, teacher_id = courses.coursepage(id)
    return render_template("coursepage.html", id=id, tasks=tasks,
                           name=name, teacher_id=teacher_id)

@app.route("/newtask/<int:course_id>")
def newtask(course_id):
    course_name = courses.coursename(course_id)
    return render_template("newtask.html", course_id=course_id,
                            course_name=course_name)

@app.route("/create/", methods=["POST"])
def create():
    question = request.form["question"]
    course_id = request.form["course_id"]
    choices = request.form.getlist("choice")
    correct_choice = request.form["correct"]

    courses.newtask(course_id, question, choices, correct_choice)
    return render_template("create.html", course_id=course_id)

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
