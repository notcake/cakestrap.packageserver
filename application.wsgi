import logging
import os
import sys

# Logging
logging.basicConfig(stream = sys.stderr)

# Virtual environment
venvPath = os.path.join(os.path.dirname(__file__), "venv/bin/activate_this.py")
execfile(venvPath, { "__file__": venvPath })

# Import paths
sys.path.insert(0, os.path.dirname(__file__))

# LETSDODIS
from application import app as application
