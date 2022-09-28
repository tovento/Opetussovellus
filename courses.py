from db import db
import users

def newcourse(name, teacher_id):
    sql = "INSERT INTO Courses (name, teacher_id) VALUES " \
          "(:name, :teacher_id) RETURNING id"
    result = db.session.execute(sql, {"name":name, "teacher_id":teacher_id})
    course_id = result.fetchone()[0]
    db.session.commit()
    return course_id

def coursepage(id):
    sql = "SELECT id, question FROM Tasks WHERE course_id=:id"
    result = db.session.execute(sql, {"id":id})
    tasks = result.fetchall()
    sql = "SELECT name, teacher_id FROM Courses WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    course = result.fetchone()
    name = course[0]
    teacher_id = course[1]
    return (tasks, name, teacher_id)

def coursename(course_id):
    sql = "SELECT name FROM Courses WHERE id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    course_name = result.fetchone()[0]
    return course_name

def newtask(course_id, question, choices, correct_choice):
    sql = "INSERT INTO Tasks (course_id, question)" \
          "VALUES (:course_id, :question) RETURNING id"
    result = db.session.execute(sql, {"course_id":course_id, "question":question})
    task_id = result.fetchone()[0]
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

