from app import app
from model.name_model import NameModel
from flask import request
from flask import make_response

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
        obj=nameModel()
        return obj.name_get(json)
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)
