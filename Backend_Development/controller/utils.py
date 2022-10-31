from app import app
from model.assignment_model import AssignmentModel
from flask import request
from flask import make_response
import jwt
from configs.config import server_config

def decode_auth_token(s):
    try:
        payload = jwt.decode(s, server_config['SECRET_KEY'],algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def isValidToken(s, entry_num, role):
    print("yoy ", type(s), s)
    st=decode_auth_token(str(s))
    print(st, entry_num+"#"+role)
    return st == entry_num+"#"+role
