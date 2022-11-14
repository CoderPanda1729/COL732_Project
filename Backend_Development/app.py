from flask import Flask
from flask_cors import CORS
import sys
app=Flask(__name__)
CORS(app)

from controller import *
