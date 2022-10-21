from app import app
from model.course_model import course_model
from flask import make_response

@app.route("/getCourses/<string:entry_no>/<string:role>", methods=["GET"])
def get_courses(entry_no, role):
    obj = course_model()
    courses = obj.get_course_model(entry_no, role)
    return make_response({"courses" : courses}, 201) 

@app.route("/setCourses/<string:entry_no>/<string:role>/<string:course_id>", methods=["GET"])
def set_courses(entry_no, role, course_id):
    obj = course_model()
    obj.set_course_model(entry_no, role, course_id)
    return make_response({"status" : "course added"}, 201)
