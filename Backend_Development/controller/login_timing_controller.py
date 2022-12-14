from app import app
from model.login_timing_model import login_timing_model
from flask import request
from flask import make_response
from .utils import *

# def process_json():
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         json = request.json
#         return json
#     else:
#         return 'Content-Type not supported!'

@app.route("/getVM/<string:entry_no>/<string:course_id>/<string:assignment_id>", methods = ["GET"])
def getVM(entry_no, course_id, assignment_id):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},404)

    obj = login_timing_model()
    session_id = obj.start_vm(entry_no, course_id, assignment_id)
    return make_response({'session_id': session_id, "status" : "time added"}, 201)

@app.route("/resumeVM/<string:entry_no>/<string:course_id>/<string:assignment_id>", methods = ["GET"])
def resumeVM(entry_no, course_id, assignment_id):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},404)    
    obj = login_timing_model()
    session_id = obj.start_vm(entry_no, course_id, assignment_id)
    return make_response({'session_id': session_id, "status" : "time added"}, 201)

@app.route("/pauseVM/<int:session_id>/<string:entry_no>/<string:course_id>/<string:assignment_id>", methods = ["GET"])
def pauseVM(session_id, entry_no, course_id, assignment_id):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},404)    
    obj = login_timing_model()
    obj.stop_vm(session_id, entry_no, course_id, assignment_id)
    return make_response({"status" : "time added"}, 201)


@app.route("/stopVM/<int:session_id>/<string:entry_no>/<string:course_id>/<string:assignment_id>", methods = ["GET"])
def stopVM(session_id, entry_no, course_id, assignment_id):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},404)    
    obj = login_timing_model()
    obj.stop_vm(session_id, entry_no, course_id, assignment_id)
    return make_response({"status" : "time added"}, 201)

