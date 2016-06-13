import importlib
import os

SCRIPT_DIR = os.path.dirname(__file__)

registered_handlers = {}

for filename in os.listdir(SCRIPT_DIR):

    if not filename.lower().endswith('.py'):
        continue

    if '__init__' in filename.lower():
        continue

    modname, ext = os.path.splitext(filename)
    mod = importlib.import_module('.%s' % modname, __package__)
