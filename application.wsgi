import os
import sys

venvPath = os.path.join(os.path.dirname(__file__), "venv/bin/activate_this.py")
execfile(venvPath, { "__file__": venvPath })

sys.path.insert(0, os.path.dirname(__file__))

from application import app as application
