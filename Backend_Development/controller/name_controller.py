from app import app
from model.name_model import NameModel
from flask import request
from flask import make_response
from utils import *

def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'

@app.route("/getName/<entryNumber>",methods=["GET"])
def getName():
    json = process_json()
    if(json != 'Content-Type not supported!'):
        token, entry_no, role = request.headers['token'], request.args.get('entry_no'), request.args.get('role')
        if not isValidToken(token, entry_no, role):
            return make_response({'format':" 'Invalid token!'"},404)        
        obj=NameModel()
        return obj.name_get(json)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)
