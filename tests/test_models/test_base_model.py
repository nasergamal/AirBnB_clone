#!/usr/bin/python3
'''unit tests for BaseModel Class'''
import unittest
from datetime import datetime
from models.base_model import BaseModel
from time import sleep
import os


class Test_BaseModelinit(unittest.TestCase):
    '''test cases for Basemodel instantiation'''
    def test_uuid4(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertIsInstance(bm1, BaseModel)
        self.assertTrue(hasattr(bm1, "id"))

    def test_unique_id(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)
        self.assertIsInstance(bm1.id, str)

    def test_types(self):
        bm1 = BaseModel()
        self.assertEqual(BaseModel, type(BaseModel()))
        self.assertIsInstance(bm1.id, str)
        self.assertIsInstance(bm1.created_at, datetime)
        self.assertIsInstance(bm1.updated_at, datetime)

    def test_creation_timedif(self):
        bm1 = BaseModel()
        sleep(0.01)
        bm2 = BaseModel()
        self.assertLess(bm1.created_at, bm2.created_at)

    def test_update_timedif(self):
        bm1 = BaseModel()
        sleep(0.01)
        bm2 = BaseModel()
        self.assertLess(bm1.updated_at, bm2.updated_at)

    def test_created_at(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertTrue(hasattr(bm1, "created_at"))
        self.assertIsInstance(bm1.created_at, datetime)

    def test_updated_at(self):
        bm1 = BaseModel()
        self.assertTrue(hasattr(bm1, "updated_at"))
        self.assertIsInstance(bm1.updated_at, datetime)

    def test_str(self):
        bm1 = BaseModel()
        text = f'[{type(bm1).__name__}] ({bm1.id})'
        self.assertIn(text, bm1.__str__())
        self.assertIn(f"'created_at': {repr(bm1.created_at)}", bm1.__str__())
        self.assertIn(f"'updated_at': {repr(bm1.updated_at)}", bm1.__str__())

    def test_kwargs(self):
        time = datetime.now()
        bm = BaseModel(id="9999999999", created_at=time.isoformat(),
                       updated_at=time.isoformat())
        self.assertEqual(bm.id, "9999999999")
        self.assertEqual(bm.created_at, time)
        self.assertEqual(bm.updated_at, time)

    def test_no_kwargs(self):
        with self.assertRaises(TypeError):
            bm1 = BaseModel(id=None, created_at=None, updated_at=None)


class Test_BaseModel_to_dict(unittest.TestCase):
    """unittests for to_dict method"""
    def test_dict(self):
        bm1 = BaseModel()
        self.assertIsInstance(bm1.to_dict(), dict)

    def test_to_dict_content(self):
        bm1 = BaseModel()
        self.assertIn("__class__", bm1.to_dict())
        self.assertIn("id", bm1.to_dict())
        self.assertIn("created_at", bm1.to_dict())
        self.assertIn("updated_at", bm1.to_dict())

    def test_to_dict_timeformat(self):
        bm1 = BaseModel()
        timec = bm1.created_at.isoformat()
        timeu = bm1.updated_at.isoformat()
        self.assertEqual(timec, bm1.to_dict()["created_at"])
        self.assertEqual(timeu, bm1.to_dict()["updated_at"])

    def test_to_dict_timetype(self):
        bm1 = BaseModel()
        self.assertIsInstance(bm1.to_dict()["created_at"], str)
        self.assertIsInstance(bm1.to_dict()["updated_at"], str)

    def test_to_dict_all(self):
        bm1 = BaseModel()
        di = {"__class__": "BaseModel", "id": f"{bm1.id}",
              "created_at": bm1.created_at.isoformat(),
              "updated_at": bm1.updated_at.isoformat()}
        self.assertDictEqual(di, bm1.to_dict())

    def test_to_dict_random_addition(self):
        bm1 = BaseModel()
        bm1.name = "Walter"
        bm1.interest = "science"
        self.assertIn("name", bm1.to_dict())
        self.assertIn("interest", bm1.to_dict())

    def test_to_dict_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict("Take it")

    def test_creation_fromdict(self):
        bm1 = BaseModel()
        copy = bm1.to_dict()
        del bm1
        bm1 = BaseModel(**copy)
        self.assertDictEqual(copy, bm1.to_dict())


class Test_BaseModel_save(unittest.TestCase):
    '''unit tests for save method'''
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

    def test_update(self):
        bm1 = BaseModel()
        time = bm1.updated_at
        sleep(0.01)
        bm1.save()
        self.assertNotEqual(bm1.updated_at, time)

    def test_2_update(self):
        bm1 = BaseModel()
        time = bm1.updated_at
        sleep(0.01)
        bm1.save()
        time2 = bm1.updated_at
        sleep(0.01)
        bm1.save()
        self.assertNotEqual(bm1.updated_at, time)
        self.assertNotEqual(bm1.updated_at, time2)
        self.assertLess(time, bm1.updated_at)

    def test_savefile(self):
        bm1 = BaseModel()
        bm1.save()
        with open("file.json", "r") as f:
            self.assertIn(f"{type(bm1).__name__}.{bm1.id}", f.read())

    def test_save_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save("Save it")
