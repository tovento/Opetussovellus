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
        return render_template("error.html", message=
                               "Virheellinen käyttäjätunnus tai salasana.")

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
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("error.html", message=
                               "Salasanat eivät ole identtiset.")
    if "teacher" in request.form:
        teacher = True
    else:
        teacher = False
    
    if users.register(username, password1, teacher):
        return redirect("/")
    else:
        return render_template("error.html", message=
                               "Rekisteröinnissä tapahtui virhe.")

@app.route("/newcourse", methods=["GET", "POST"])
def newcourse():
    if request.method == "GET":
        return render_template("newcourse.html")
    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        teacher_id = session["id"]
        course_id = courses.newcourse(name, teacher_id)
        return redirect(f"/coursepage/{course_id}")

@app.route("/coursepage/<int:id>")
def coursepage(id):
    tasks, name, teacher_id = courses.coursepage(id)

    user_id = users.user_id()
    completed_tasks = courses.completed_tasks(user_id, id)
    return render_template("coursepage.html", id=id, tasks=tasks,
                           name=name, teacher_id=teacher_id,
                           completed_tasks=completed_tasks)

@app.route("/newtask/<int:course_id>")
def newtask(course_id):
    course_name = courses.coursename(course_id)
    return render_template("newtask.html", course_id=course_id,
                            course_name=course_name)

@app.route("/create/", methods=["POST"])
def create():
    users.check_csrf()

    question = request.form["question"]
    course_id = request.form["course_id"]
    choices = request.form.getlist("choice")
    if "correct" in request.form:
        correct_choice = request.form["correct"]
    else:
        return render_template("error.html", message="Oikea vastaus puuttuu.",
                course_id=course_id)

    courses.newtask(course_id, question, choices, correct_choice)
    return render_template("create.html", course_id=course_id)

@app.route("/task/<int:course_id>/<int:id>")
def task(course_id, id):
    question = courses.task_question(id)
    choices = courses.task_choices(id)
    return render_template("task.html", id=id, question=question,
            choices=choices, course_id=course_id)

@app.route("/answer", methods= ["POST"])
def answer():
    users.check_csrf()
    task_id = request.form["id"]
    user_id = users.user_id()
    if "answer" in request.form:
        choice_id = request.form["answer"]
    else:
        course_id = courses.courseid_from_task(task_id)
        return render_template("error.html", message="Vastaus puuttuu.",
                               course_id=course_id)

    answer_id = courses.submit_answer(task_id, user_id, choice_id)
    return redirect(f"/result/{task_id}/{answer_id}")

@app.route("/result/<int:task_id>/<int:answer_id>", methods = ["GET"])
def result(task_id, answer_id):
    user_id = users.user_id()
    student_id = courses.studentid_from_answer(answer_id)

    if user_id != student_id:
        return render_template("error.html", message=
                               "Sinulla ei ole oikeutta katsella tätä sivua.")

    correct = courses.check_answer(answer_id)
    course_id = courses.courseid_from_answer(answer_id)

    if correct:
        courses.complete_task(user_id, task_id)

    return render_template("result.html", result_id=answer_id, correct=correct,
                           course_id=course_id)

@app.route("/delete/<int:course_id>/<int:task_id>")
def delete(course_id, task_id):
    user_id = users.user_id()
    if session["teacher"]:
        course_teacher = courses.course_teacher(course_id)
        if course_teacher == user_id:
            course_name = courses.coursename(course_id)
            task_question = courses.task_question(task_id)
            return render_template("delete.html", course_name=course_name,
                            course_id=course_id, task_question=task_question,
                            task_id=task_id)
    return render_template("error.html", message=
                           "Sinulla ei ole oikeutta katsella tätä sivua.")

@app.route("/deleted/<int:course_id>/<int:task_id>", methods=["POST"])
def deleted(course_id, task_id):
    users.check_csrf()

    no_yes = request.form["no_yes"]
    if no_yes == "yes":
        if not courses.delete_task(task_id):
            return render_template("error.html",
                        message="Tehtävän poistaminen ei onnistunut.")

    return render_template("deleted.html", course_id=course_id,
                           no_yes=no_yes)
