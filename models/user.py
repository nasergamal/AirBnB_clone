#!/usr/bin/python3
'''user model'''
from models.base_model import BaseModel


class User(BaseModel):
    '''User class declaration'''
    email = ""
    password = ""
    first_name = ""
    last_name = ""
