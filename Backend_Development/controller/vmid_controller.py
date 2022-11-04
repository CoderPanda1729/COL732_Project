from app import app
from model.VMID_model import VmidModel
from flask import request, send_file
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


@app.route("/startFresh/<entry_no>/<course_id>/<ass_id>",methods=["GET",'POST'])
def startFresh(entry_no,course_id,ass_id):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},401)
    obj=VmidModel()
    return obj.start_fresh(entry_no,course_id, ass_id)#iso hardcoded in function

@app.route("/saveTemplate/<entry_no>/<course_id>/<ass_id>",methods=["GET"])
def saveTemplate(entry_no,course_id,ass_id):
    entry,token, role = request.headers['entry_no'],request.headers['token'], request.headers['role']
    if not isValidToken(token, entry, role):
        return make_response({'format':" 'Invalid token!'"},401)
    obj=VmidModel()
    return obj.save_template(entry_no,course_id, ass_id)

@app.route("/startTemplate/<entry_no>/<course_id>/<ass_id>",methods=["GET"])
def startTemplate(entry_no,course_id,ass_id):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},404)
    obj=VmidModel()
    return obj.start_template(entry_no,course_id, ass_id)

@app.route("/resumeVM/<entry_no>/<course_id>/<asmt_id>",methods=["GET"])
def resume_VM(entry_no,course_id,asmt_id):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_no, role):
        return make_response({'format':" 'Invalid token!'"},401)
    obj=VmidModel()
    #TODO get ISO from the assignment table, applicable when other teams can support different images
    return obj.resume_vm(entry_no ,course_id, asmt_id,'')#currently ISO is hardcoded in function

@app.route("/pauseVM/<entry_no>/<course_id>/<asmt_id>",methods=["GET"])
def pause_VM(entry_no,course_id,asmt_id):
    token, role, entry = request.headers['token'], request.headers['role'], request.headers['entry_no']
    if not isValidToken(token, entry, role):
        return make_response({'format':" 'Invalid token!'"},401)
    obj=VmidModel()
    return obj.pause_vm(entry_no ,course_id, asmt_id)

@app.route("/getISOs")
def getISOs():
    '''
    #TODO read from the ../images folder and specify the ISOs available,
    currently hardcoded
    '''
    return [{'ISO':'bzimage-hello-busybox'}]

@app.route('/downloadCheck')
def download():
    path = "utils.py"
    return send_file(path, as_attachment=True)
