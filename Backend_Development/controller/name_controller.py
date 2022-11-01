from app import app
from model.name_model import NameModel
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

@app.route("/getName/<entryNumber>",methods=["GET"])
def getName(entryNumber):
    json = process_json()
    if(json != 'Content-Type not supported!'):
        token, entry_no, role = request.headers['token'], request.headers['entry_no'], request.headers['role']
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)        
        obj=NameModel()
        return obj.name_get(entryNumber)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)
