from app import app
from model.submission_table import SubmissionModel
from flask import request
from flask import make_response

def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

@app.route("/getSubmission/<entry_no>/<course_id>/<assignment_id>",methods=["GET"])
def getSubmission(entry_no, course_id,assignment_id):
    if(process_json()!='Content-Type not supported!'):
        obj=SubmissionModel()
        return obj.submission_get(process_json(), entry_no, course_id, assignment_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/getAllSubmissions/<course_id>/<assignment_id>",methods=["GET"])
def getAllSubmissions(course_id,assignment_id):
    obj=SubmissionModel()
    return obj.submission_get_all(process_json(), course_id, assignment_id)      

@app.route("/uploadSubmission/<entry_no>/<course_id>/<assignment_id>",methods=["POST"])
def uploadSubmission(entry_no, course_id,assignment_id, status, submission_time, marks, plag_path):
    if(process_json()!='Content-Type not supported!'):
        obj=SubmissionModel()
        return obj.submission_upload(process_json(), entry_no, course_id, assignment_id, status, submission_time, marks, plag_path)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/updateSubmission/<entry_no>/<course_id>/<assignment_id>",methods=["POST"])
def updateSubmission(entry_no, course_id,assignment_id):
    if(process_json()!='Content-Type not supported!'):
        obj=SubmissionModel()
        return obj.submission_update(process_json(), entry_no, course_id, assignment_id)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route('/studentSubmit', methods = ['POST'])
def studentSubmit():
    data = process_json()
    if(data!='Content-Type not supported!'):
        obj=SubmissionModel()
        return obj.studentSubmit(data)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},400)

@app.route('/grade/<course_id>/<asmt_id>/<entry_no>')
def grade(course_id, asmt_id,entry_no):
    #TODO execute the checker script and return marks enable the plag report
    pass

@app.route('/downloadAsmt/<course_id>/<asmt_id>/<entry_no>')
def downloadSubmission():
    '''
    This is only possible when the file has been extracted out of the vm -> after grade
    '''
    pass

@app.route('/downloadPlagReport/<course_id>/<asmt_id>/<entry_no>')
def downloadPlagReport(course_id, asmt_id, entry_no):
    '''
    '''
    pass