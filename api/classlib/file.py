import json


class File:
    def __init__(self, id=None, name=None, path=None, cksum=None):
        self.id = id  # Ussing a UUID for the id
        self.name = name
        self.path = path
        self.cksum = cksum

    @staticmethod
    def fromjson(obj):
    	pass

