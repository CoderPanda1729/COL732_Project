from app import app
from model.activities_model import activities_model
from flask import request
from flask import make_response
from .utils import *


@app.route("/recordActivities/<entry_num>/<assign_id>/<operation>", methods = ["GET"])
def recordActivities(entry_num, assign_id, operation):
    token, role = request.headers['token'], request.headers['role']
    if not isValidToken(token, entry_num, role):
        return make_response({'format':" 'Invalid token!'"},404)

    obj = activities_model()
    obj.record_activity(entry_num, assign_id, operation)
    return make_response({'status': 'activity added'}, 201)

@app.route("/getActivityRecords/<entry_num>/<assign_id>", methods = ["GET"])
def getActivityRecords(entry_num, assign_id):
    token = request.headers['token']
    role=request.headers['role']
    if not isValidToken(token, entry_num, role):
        return make_response({'format':" 'Invalid token!'"},404)

    obj = activities_model()
    # todo : check this 
    # print(obj.get_records(entry_num, assign_id).json)
    try:
        l = obj.get_records(entry_num, assign_id).json['record']
        return make_response({assign_id: l, 'status': 'returned'}, 201)
    except: 
        return make_response({'status': 'Error'}, 404)
    






