from app import app
from model.vmid_model import VmidModel
from flask import request
from flask import make_response

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
def get_VM(entry_number,course_id,ass_id):
    if(process_json()!='Content-Type not supported!'):
        obj=VmidModel()
        return obj.get_vm(entry_number,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/getVM/<entry_number>/<course_id>/<ass_id>",methods=["POST"])
def create_VM(entry_number,course_id,ass_id):
    if(process_json()!='Content-Type not supported!'):
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
        obj=VmidModel()
        return obj.start_vm(entry_number,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/resumeVM/<entry_number>/<course_id>/<ass_id>",methods=["POST"])
def resume_VM(entry_number,course_id,ass_id):
    json=process_json()
    if(json!='Content-Type not supported!'):
        obj=VmidModel()
        return obj.resume_vm(entry_number ,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/pauseVM/<entry_number>/<course_id>/<ass_id>",methods=["POST"])
def pause_VM(entry_number,course_id,ass_id):
    json=process_json()
    if(json!='Content-Type not supported!'):
        obj=VmidModel()
        return obj.pause_vm(entry_number ,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)


@app.route("/getPlagReport/<entry_number>/<course_id>/<ass_id>",methods=["GET"])
def getPlagReport(entry_number,course_id,ass_id):
    json=process_binary()
    if(json!='Content-Type not supported!'):
        obj=VmidModel()
        return obj.get_plag_report(json,entry_number ,course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)
