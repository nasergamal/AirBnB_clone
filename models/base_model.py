#!/usr/bin/python3
'''Base model class for airbnb'''
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    '''Base class for other models'''
    def __init__(self, *args, **kwargs):
        '''
        intiating class
        '''
        if len(kwargs) == 0:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)
        else:
            if '__class__' in kwargs:
                kwargs.pop('__class__')
            for k, v in kwargs.items():
                self.__dict__[k] = v
            self.created_at = datetime.fromisoformat(self.created_at)
            self.updated_at = datetime.fromisoformat(self.updated_at)

    def __str__(self):
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        '''save changes to device and update updated_at attribute'''
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        '''return a dictionary containing all keys/values
           of __dict__ of the instance
        '''
        di = self.__dict__.copy()
        di['__class__'] = type(self).__name__
        di['created_at'] = self.created_at.isoformat()
        di['updated_at'] = self.updated_at.isoformat()
        return di


'''    def to_dict(self):
        di = {}
        di['__class__'] = type(self).__name__

        for i, k in self.__dict__.items():
            if i == "created_at" or i == "updated_at":
                di[i] = k.isoformat()
                continue
            di[i] = k
        return di
    '''
