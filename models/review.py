#!/usr/bin/python3
'''review model'''
from models.base_model import BaseModel


class Review(BaseModel):
    '''review Class declaration'''
    place_id = ""
    user_id = ""
    text = ""
