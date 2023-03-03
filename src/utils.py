from datetime import datetime

from config import Config
from .database import Database

def log(uid, message):
    print("[%s] [%s] %s" % (f"{datetime.now():%Y-%m-%d %H:%M:%S}", uid, message))

class Interfaces:
    database = Database(Config.mongo_credentials, 'players')
    world = Database(Config.mongo_credentials, 'world')
    objects = Database(Config.mongo_credentials, 'objects')