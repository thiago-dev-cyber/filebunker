import inspect
import os
import sys

from dotenv import load_dotenv


load_dotenv()

# Get a directory ROOT
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR))

# Adding a ROOT directory a sys.path
sys.path.append(ROOT)
os.environ['ROOT'] = ROOT

from api.classlib.db import DataBase
from api.classlib.menu import Manager


# JsonHelp.create_config_file(config_file_name='1.json', password='1234')

db = DataBase.load_db('data/1.json', '1234')
# Manager.add_path('/home/thi/Downloads', db)

# print(db.db)


Manager.reload_files(db)
file = Manager._load_file('/home/thi/Downloads/password.txt')

print(file)
email = os.getenv('email')
password = os.getenv('password')
# m = ConnectMega(email, password)
# m.start()
# print(Manager._list_files("/home/user/Downloads"))
# db.save()
