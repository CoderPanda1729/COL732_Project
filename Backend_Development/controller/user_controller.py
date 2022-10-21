from app import app
from model.user_model import user_model
from flask import request
from flask import make_response



def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'


@app.route("/user/signup", methods=["POST"])
def signup():
    
    if(process_json()!='Content-Type not supported!'):
        obj=user_model()
        return obj.user_signup_model(process_json())
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)
        

@app.route("/user/login",methods=["POST"])
def login():

    if(process_json()!='Content-Type not supported!'):
        obj=user_model()
        return obj.user_login_model(process_json())
        
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

@app.route("/user/forgotPassword",methods=["POST"])
def forgotPassword():

    if(process_json()!='Content-Type not supported!'):
        obj=user_model()
        return obj.user_forgot_password_model(process_json())
        
    else:
        return make_response({'format':" 'Content-Type not supported!'"},404)

    
