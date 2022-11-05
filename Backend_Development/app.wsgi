from multiprocessing.dummy import active_children
import sys
sys.path.insert(0, "/home/col732_gautam/COL732_Project/Backend_Development")

activate_this = "/home/col732_gautam/COL732/bin/activate_this.py"
with open(activate_this) as infile:
    exec(infile.read(), dict(__file__=activate_this))

from app import app as application
