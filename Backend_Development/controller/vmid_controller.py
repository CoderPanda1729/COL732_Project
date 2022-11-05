from app import app
from model.vmid_model import VmidModel
from flask import request
from flask import make_response
from .utils import *


def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

def process_binary():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/octet-stream'):
        return request.data
    else:
        return 'Content-Type not supported!'


@app.route("/getVM/<entry_number>/<course_id>/<ass_id>",methods=["GET"])
def get_VM(entry_no,course_id,ass_id):
    if(process_json()!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=VmidModel()
        return obj.get_vm(entry_no,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/getVM/<entry_number>/<course_id>/<ass_id>",methods=["POST"])
def create_VM(entry_number,course_id,ass_id):
    if(process_json()!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_number, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=VmidModel()
        data = process_json()
        if 'iso_path' not in data:
            return obj.create_vm(entry_number,course_id, ass_id)
        else:
            return obj.create_vm(entry_number,course_id, ass_id, data['iso_path'])
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/getVM/<entry_number>/<course_id>/<ass_id>",methods=["GET"])
def start_VM(entry_number,course_id,ass_id):
    if(process_json()!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_number, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=VmidModel()
        return obj.start_vm(entry_number,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/resumeVM/<entry_number>/<course_id>/<ass_id>",methods=["POST"])
def resume_VM(entry_no,course_id,ass_id):
    json=process_json()
    if(json!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=VmidModel()
        return obj.resume_vm(entry_no ,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/pauseVM/<entry_number>/<course_id>/<ass_id>",methods=["POST"])
def pause_VM(entry_no,course_id,ass_id):
    json=process_json()
    if(json!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=VmidModel()
        return obj.pause_vm(entry_no ,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)


@app.route("/getPlagReport/<entry_number>/<course_id>/<ass_id>",methods=["GET"])
def getPlagReport(entry_no,course_id,ass_id):
    json=process_binary()
    if(json!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)

        obj=VmidModel()
        return obj.get_plag_report(json,entry_no ,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)


@app.route("/getTree/<entry_number>/<course_id>/<assignment_id>",methods=["GET"])
def getTree(entry_no,course_id,assignment_id):
    json=process_json()
    if(json!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=VmidModel()
        return obj.get_tree(entry_no,course_id,assignment_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/fork/<entry_number>/<course_id>/<assignment_id>/<parent_version>/<new_version_name>",methods=["POST"])
def fork(entry_no,course_id,assignment_id,parent_version,new_version_name):
    json=process_json()
    if(json!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=VmidModel()
        return obj.fork(entry_no, course_id, assignment_id,parent_version,new_version_name)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/delete/<entry_number>/<course_id>/<assignment_id>/<version>",methods=["POST"])
def delete(entry_no,course_id,assignment_id,version):
    json=process_json()
    if(json!='Content-Type not supported!'):
        token, role = request.headers['token'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=VmidModel()
        return obj.delete_query(entry_no,course_id,assignment_id,version)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

