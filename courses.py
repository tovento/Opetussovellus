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

def courseid(answer_id):
    sql = "SELECT C.id FROM Courses C, Tasks T, Choices Ch, Answers A " \
          "WHERE A.id=:answer_id AND A.choice_id=Ch.id AND Ch.task_id=T.id " \
          "AND T.course_id=C.id"
    result = db.session.execute(sql, {"answer_id":answer_id})
    course_id = result.fetchone()[0]
    return course_id

def course_teacher(course_id):
    sql = "SELECT teacher_id FROM Courses WHERE id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    course_teacher = result.fetchone()[0]
    return course_teacher

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

def task_question(id):
    sql = "SELECT question FROM Tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    question = result.fetchone()[0]
    return question

def task_choices(id):
    sql = "SELECT id, choice FROM Choices WHERE task_id=:id"
    result = db.session.execute(sql, {"id":id})
    choices = result.fetchall()
    return  choices

def submit_answer(task_id, student_id, choice_id):
    sql = "INSERT INTO Answers (student_id, choice_id) " \
          "VALUES (:student_id, :choice_id) RETURNING id"
    result = db.session.execute(sql,
                                {"student_id":student_id,
                                "choice_id":choice_id})
    answer_id = result.fetchone()[0]
    db.session.commit()
    return answer_id

def check_answer(answer_id):
    sql = "SELECT C.correct FROM Choices C, Answers A " \
          "WHERE A.id=:answer_id AND A.choice_id=C.id"
    result = db.session.execute(sql, {"answer_id":answer_id})
    correct = result.fetchone()[0]
    return correct

def complete_task(student_id, task_id):
    sql = "INSERT INTO Completions (student_id, task_id) " \
          "VALUES (:student_id, :task_id)"
    db.session.execute(sql, {"student_id":student_id, "task_id":task_id})
    db.session.commit()

def completed_tasks(user_id, course_id):
    sql = "SELECT C.task_id, T.question FROM Completions C, Tasks T "\
          "WHERE C.student_id=:user_id AND T.course_id=:course_id " \
          "AND T.id=C.task_id"
    result = db.session.execute(sql,
                                {"user_id":user_id,
                                "course_id":course_id})
    completed_tasks = result.fetchall()
    return completed_tasks

def delete_task(task_id):
    try:
        sql = "DELETE FROM Tasks WHERE id=:task_id"
        db.session.execute(sql, {"task_id":task_id})
        db.session.commit()
    except:
        return False
    return True
