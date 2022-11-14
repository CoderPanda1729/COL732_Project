from app import app
from model.assignment_model import AssignmentModel
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
    

@app.route('/createAss',methods=['POST'])
def createAssignment():
    if(process_json()!='Content-Type not supported!'):
        token, entry_no, role = request.headers['token'], request.headers['entry_no'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)
        
        obj=AssignmentModel()
        return obj.assignment_create(process_json())
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/updateAss",methods=["POST"])
def updateAssignment():
    #receive the assignment json
    #contains {start_time,end_time,pdfLink,VMID}   
    if(process_json()!='Content-Type not supported!'):
        token, entry_no, role = request.headers['token'], request.headers['entry_no'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)
        obj=AssignmentModel()
        return obj.assignment_update(process_json())
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)


@app.route("/getAllAss/<course_id>")
def getAllAss(course_id):
    obj=AssignmentModel()
    return obj.getAllAss(course_id)

@app.route("/getAss/<course_id>/<asmt_id>")
def getAsmt(course_id, asmt_id):
    obj = AssignmentModel()
    return obj.assignment_get(course_id, asmt_id)