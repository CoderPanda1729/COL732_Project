from app import app
from model.activities_model import activities_model
from flask import request
from flask import make_response
from .utils import *


@app.route("/recordActivities/<entry_num>/<course_id>/<assign_id>/<operation>", methods = ["GET"])
def recordActivities(entry_num,course_id, assign_id, operation):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_num, role):
        return make_response({'format':" 'Invalid token!'"},404)

    obj = activities_model()
    obj.record_activity(entry_num,course_id, assign_id, operation)
    return make_response({'status': 'activity added'}, 201)

@app.route("/getActivityRecords/<entry_num>/<course_id>/<assign_id>", methods = ["GET"])
def getActivityRecords(entry_num,course_id, assign_id):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_num, role):
        return make_response({'format':" 'Invalid token!'"},404)

    obj = activities_model()
    l = obj.get_records(entry_num,course_id, assign_id)
    return make_response({assign_id: l, 'status': 'returned'}, 201)







