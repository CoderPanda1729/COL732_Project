from app import app
from model.marks_model import marksModel
from flask import request
from flask import make_response

def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

@app.route("/submit/<course_id>/<asmt_id>/<entry_no>/<time>",methods=["GET"])
def submit(course_id, asmt_id, entry_no, submission_time):
    if(process_json()!='Content-Type not supported!'):
        obj = marksModel()
        return obj.submit(course_id, asmt_id, entry_no, submission_time)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/setMarks/<course_id>/<asmt_id>/<entry_no>", methods=["POST"])
def set_marks(course_id, asmt_id, entry_no):
    if(process_json()!='Content-Type not supported!'):
        marks, remark = float(request.headers['marks']), request.headers['remark']
        obj = marksModel()
        return obj.setMarks(course_id, asmt_id, entry_no, marks, remark)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/getMarks/<course_id>/<asmt_id>/<entry_no>",methods=["GET"])
def get_marks(course_id, asmt_id, entry_no):
    if(process_json()!='Content-Type not supported!'):
        obj = marksModel()
        return obj.getMarks(course_id, asmt_id, entry_no)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/getAllMarks/<course_id>/<asmt_id>",methods=["GET"])
def get_all_marks(course_id, asmt_id):
    if(process_json()!='Content-Type not supported!'):
        obj = marksModel()
        return obj.getAllMarks(course_id, asmt_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/runAutoGrader/<course_id>/<asmt_id>",methods=["GET"])
def run_auto_grader(course_id, asmt_id):
    if(process_json()!='Content-Type not supported!'):
        entry_no = request.headers['entry_no']
        auto_marks =  request.headers['auto_marks']
        plag_pts = request.headers['plag_pts']
        obj = marksModel()
        return obj.runAutoGrader(course_id, asmt_id, entry_no, auto_marks, plag_pts)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)
