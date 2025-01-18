import inspect
import os
import sys


# Get a directory ROOT
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR))

# Adding a ROOT directory a sys.path
sys.path.append(ROOT)
os.environ['ROOT'] = ROOT


from api.classlib.db import DataBase
from api.classlib.jsonhelp import JsonHelp


# JsonHelp.create_config_file(config_file_name="1.json", password="")

salt, iv, key, data = JsonHelp.decrypt_file(file_path='data/1.json', password='12344')
db = DataBase(data, salt, iv, key)
# db.db["paths"]["/home/usr/Downloads"] = {"teste.txt":"Teu Ceu"}
# db.save()
