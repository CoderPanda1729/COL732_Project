import imp
from app import app
from model.course_model import course_model
from model.name_model import NameModel
from flask import make_response, request
from .utils import *

# please don't remove 
@app.route("/ping", methods=["GET"])
def ping():
    print("running")
    return make_response({"status" : "running"}, 200)

@app.route("/getCourses/<string:entry_no>/<string:role>", methods=["GET"])
def get_courses(entry_no, role):
    token = request.headers['token']
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},404)    
    obj = course_model()
    courses = obj.get_course_model(entry_no, role)
    return make_response({"courses" : courses}, 201) 

@app.route("/setCourses/<string:entry_no>/<string:role>/<string:course_id>", methods=["GET"])
def set_courses(entry_no, role, course_id):
    token = request.headers['token']
    entry = request.headers['entry_no']
    Role = request.headers['role']
    if not isValidToken(token, entry, Role):
        print('INVALID TOKEN')
        return make_response({'format':" 'Invalid token!'"},404)      
    obj = course_model()
    print(entry_no)
    obj.set_course_model(entry_no, role, course_id)
    return make_response({"status" : "course added"}, 201)


@app.route("/getAllMembers/<course_id>")
def getMembers(course_id):
    token = request.headers['token']
    entry = request.headers['entry_no']
    Role = request.headers['role']
    if not isValidToken(token, entry, Role):
        print('INVALID TOKEN')
        return make_response({'format':" 'Invalid token!'"},404)  
    obj = course_model()
    mems = obj.getAllMembers(course_id)
    obj2 = NameModel()
    names = [obj2.name_get(e['entry_no']) for e in mems]
    res = [{'name':names[i],'entry_no':mems[i]['entry_no'], 'role':mems[i]['role']} for i in range(len(names)) ]
    return make_response({'members':res}, 201)

@app.route('/removeMember/<string:entry_no>/<string:role>/<string:course_id>')
def removeMember(entry_no, role, course_id):
    token = request.headers['token']
    entry = request.headers['entry_no']
    Role = request.headers['role']
    if not isValidToken(token, entry, Role):
        print('INVALID TOKEN')
        return make_response({'format':" 'Invalid token!'"},404) 
    obj = course_model()
    obj.removeMember(entry_no,role,course_id)
    return make_response({'status':'success'},201)