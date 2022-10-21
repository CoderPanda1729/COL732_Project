from app import app
from model.assignment_model import AssignmentModel
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


@app.route("/getAssLink/<course_id>/<ass_id>",methods=["GET"])
def getAssignment(course_id,ass_id):
    if(process_json()!='Content-Type not supported!'):
        obj=AssignmentModel()
        return obj.assignment_get(process_json(), course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/uploadAssPdf/<course_id>/<ass_id>",methods=["POST"])
def uploadAssignmentPdf(course_id,ass_id):
    if(process_binary()!='Content-Type not supported!'):
        obj=AssignmentModel()
        return obj.assignment_upload_pdf(process_binary(), course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/updateAss/<course_id>/<ass_id>",methods=["POST"])
def updateAssignment(course_id,ass_id):
    if(process_json()!='Content-Type not supported!'):
        obj=AssignmentModel()
        return obj.assignment_update(process_json(), course_id, ass_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)
