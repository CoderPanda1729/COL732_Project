from app import app
from model.course_model import course_model
from model.name_model import NameModel
from flask import make_response
from flask import request
from utils import *

@app.route("/getCourses/<string:entry_no>/<string:role>", methods=["GET"])
def get_courses(entry_no, role):
    token, entry_no, role = request.headers['token'], request.args.get('entry_no'), request.args.get('role')
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},404)
    obj = course_model()
    courses = obj.get_course_model(entry_no, role)
    return make_response({"courses" : courses}, 201) 

@app.route("/setCourses/<string:entry_no>/<string:role>/<string:course_id>", methods=["GET"])
def set_courses(entry_no, role, course_id):
    obj = course_model()
    obj.set_course_model(entry_no, role, course_id)
    return make_response({"status" : "course added"}, 201)


@app.route("/getAllMembers/<course_id>")
def getMembers(course_id):
    obj = course_model()
    mems = obj.getAllMembers(course_id)
    obj2 = NameModel()
    names = [obj2.name_get(e['entry_no']) for e in mems]
    res = [{'name':names[i],'entry_no':mems[i]['entry_no'], 'role':mems[i]['role']} for i in range(len(names)) ]
    return make_response({'members':res}, 201)

@app.route('/removeMember/<string:entry_no>/<string:role>/<string:course_id>')
def removeMember(entry_no, role, course_id):
    obj = course_model()
    obj.removeMember(entry_no,role,course_id)
    return make_response({'status':'success'},201)