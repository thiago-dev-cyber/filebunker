import os, sys, inspect

# Get a directory ROOT 
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR))

# Adding a ROOT directory a sys.path
sys.path.append(ROOT)
os.environ["ROOT"] = ROOT


from api.classlib.db import DataBase
from api.classlib.jsonhelp import JsonHelp

#JsonHelp.create_config_file(config_file_name="1.json", password="Thiagoak103")

salt, iv, key, data = JsonHelp.decrypt_file(file_path='data/1.json', password="Thiagoak103")
db = DataBase(data, salt, iv, key)
#db.db["paths"]["/home/usr/Downloads"] = {"teste.txt":"Teucu"}
#db.save()
