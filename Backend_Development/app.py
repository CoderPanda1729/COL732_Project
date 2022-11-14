from flask import Flask

import sys
app=Flask(__name__)


from controller import *
# app.run(ssl_context='adhoc')