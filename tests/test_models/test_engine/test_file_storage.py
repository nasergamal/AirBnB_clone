#!/usr/bin/python3
'''unit tests for FileStorage Class'''
import unittest
from datetime import datetime
from models import storage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import models
import os
import json


class Test_FileStorage_init(unittest.TestCase):
    '''FileStorage Class Unittests'''
    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class Test_FileStorage(unittest.TestCase):
    '''Check Basic attributes of FileStorage Class'''
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "fil.json")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("fil.json")
        except IOError:
            pass
        try:
            os.rename("fil.json", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_new_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_type(self):
        bm1 = BaseModel()
        bm1.save()
        with open("file.json", "r") as f:
            self.assertIsInstance(f.read(), str)

    def test_content(self):
        bm1 = BaseModel()
        us1 = models.user.User()
        st1 = models.state.State()
        cy1 = models.city.City()
        am1 = models.amenity.Amenity()
        pl1 = models.place.Place()
        rev1 = models.review.Review()
        allobj = storage.all()
        storage.new(bm1)
        storage.new(us1)
        storage.new(st1)
        storage.new(cy1)
        storage.new(am1)
        storage.new(pl1)
        storage.new(rev1)
        storage.save()
        with open("file.json", "r") as f:
            content = f.read()
        self.assertIn(f"{type(bm1).__name__}.{bm1.id}", content)
        self.assertIn(f"{type(us1).__name__}.{us1.id}", content)
        self.assertIn(f"{type(st1).__name__}.{st1.id}", content)
        self.assertIn(f"{type(cy1).__name__}.{cy1.id}", content)
        self.assertIn(f"{type(am1).__name__}.{am1.id}", content)
        self.assertIn(f"{type(pl1).__name__}.{pl1.id}", content)
        self.assertIn(f"{type(rev1).__name__}.{rev1.id}", content)

    def test_all(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        bm3 = BaseModel()
        allobj = storage.all()
        self.assertIn(f"{type(bm1).__name__}.{bm1.id}", allobj)
        self.assertIn(f"{type(bm3).__name__}.{bm2.id}", allobj)
        self.assertIn(f"{type(bm3).__name__}.{bm3.id}", allobj)

    def test_all_type(self):
        allobj = storage.all()
        self.assertEqual(type(allobj), dict)

    def test_all_arg(self):
        with self.assertRaises(TypeError):
            storage.all("bark and no action")

    def test_new(self):
        bm1 = BaseModel()
        us1 = models.user.User()
        st1 = models.state.State()
        cy1 = models.city.City()
        am1 = models.amenity.Amenity()
        pl1 = models.place.Place()
        rev1 = models.review.Review()
        storage.new(bm1)
        storage.new(us1)
        storage.new(st1)
        storage.new(cy1)
        storage.new(am1)
        storage.new(pl1)
        storage.new(rev1)
        allobj = storage.all()
        self.assertIn(f"{type(bm1).__name__}.{bm1.id}", allobj.keys())
        self.assertIn(f"{type(us1).__name__}.{us1.id}", allobj.keys())
        self.assertIn(f"{type(st1).__name__}.{st1.id}", allobj.keys())
        self.assertIn(f"{type(cy1).__name__}.{cy1.id}", allobj.keys())
        self.assertIn(f"{type(am1).__name__}.{am1.id}", allobj.keys())
        self.assertIn(f"{type(pl1).__name__}.{pl1.id}", allobj.keys())
        self.assertIn(f"{type(rev1).__name__}.{rev1.id}", allobj.keys())
        self.assertIn(bm1, allobj.values())
        self.assertIn(us1, allobj.values())
        self.assertIn(st1, allobj.values())
        self.assertIn(cy1, allobj.values())
        self.assertIn(am1, allobj.values())
        self.assertIn(pl1, allobj.values())
        self.assertIn(rev1, allobj.values())

    def test_reload_arg(self):
        with self.assertRaises(TypeError):
            storage.reload("ed and ready to fire")
