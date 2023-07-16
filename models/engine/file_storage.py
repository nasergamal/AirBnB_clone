#!/usr/bin/python3
'''data storage handler'''
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from datetime import datetime


class FileStorage:
    '''file storage class.
        update database after each change
    '''
    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        '''No initiation'''
        pass

    def all(self):
        '''return all stored instances details'''
        return FileStorage.__objects

    def new(self, obj):
        '''add new instance to objects attribute'''
        k = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[k] = obj

    def save(self):
        '''save data to file'''
        s = {}
        for k, v in self.__objects.items():
            s[k] = v.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(s, f)

    def reload(self):
        '''restore data from file'''
        try:
            ds = {}
            with open(FileStorage.__file_path, "r") as f:
                ds = json.loads(f.read())
            for k, v in ds.items():
                FileStorage.__objects[k] = eval(v["__class__"])(**v)
        except Exception as e:
            pass

    def idexist(self, arg):
        '''check if an id exist'''
        if arg in FileStorage.__objects:
            return FileStorage.__objects[arg]
        return None

    def remove(self, arg):
        '''remove instance using id'''
        if arg in FileStorage.__objects:
            del FileStorage.__objects[arg]
            self.save()
            return True
        return False

    def getall(self, arg=""):
        '''return a list of all instances in a class'''
        li = []
        for k, v in FileStorage.__objects.items():
            if k.startswith(arg):
                li.append(str(FileStorage.__objects[k]))
        return li

    def update(self, i, arg):
        '''update/add an attribute using instance id'''
        try:
            t = type(FileStorage.__objects[i].__dict__[arg[2]])
            FileStorage.__objects[i].__dict__[arg[2]] = t(arg[3])
        except KeyError:
            FileStorage.__objects[i].__dict__[arg[2]] = arg[3]
        FileStorage.__objects[i].updated_at = datetime.utcnow()
        self.save()
