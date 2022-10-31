from app import app
from model.assignment_model import AssignmentModel
from flask import request
from flask import make_response
import jwt

def decode_auth_token(s):
    try:
        payload = jwt.decode(s, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def isValidToken(s, entry_num, role):
    return decode_auth_token(s) == entry_num+"#"+role
