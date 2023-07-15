#!/usr/bin/python3
'''unit tests for Amenity Class'''
import unittest
from datetime import datetime
from models.amenity import Amenity
from time import sleep
import os


class Test_Amenityinit(unittest.TestCase):
    '''test cases for Amenity instantiation'''
    def test_name_is_str(self):
        self.assertEqual(str, type(Amenity.name))

    def test_uuid4(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertIsInstance(am1, Amenity)
        self.assertTrue(hasattr(am1, "id"))
        self.assertNotEqual(am1.id, am2.id)
        self.assertIsInstance(am1.id, str)

    def test_types(self):
        am1 = Amenity()
        self.assertIsInstance(am1.id, str)
        self.assertIsInstance(am1.created_at, datetime)
        self.assertIsInstance(am1.updated_at, datetime)

    def test_creation_timedif(self):
        am1 = Amenity()
        sleep(0.01)
        am2 = Amenity()
        self.assertNotEqual(am1.created_at, am2.created_at)

    def test_update_timedif(self):
        am1 = Amenity()
        sleep(0.01)
        am2 = Amenity()
        self.assertNotEqual(am1.updated_at, am2.updated_at)

    def test_created_at(self):
        am1 = Amenity()
        am2 = Amenity()
        self.assertTrue(hasattr(am1, "created_at"))
        self.assertIsInstance(am1.created_at, datetime)

    def test_updated_at(self):
        am1 = Amenity()
        self.assertTrue(hasattr(am1, "updated_at"))
        self.assertIsInstance(am1.updated_at, datetime)

    def test_str(self):
        am1 = Amenity()
        text = f'[{type(am1).__name__}] ({am1.id})'
        self.assertIn(text, am1.__str__())
        self.assertIn(f"'created_at': {repr(am1.created_at)}", am1.__str__())
        self.assertIn(f"'updated_at': {repr(am1.updated_at)}", am1.__str__())

    def test_kwargs(self):
        time = datetime.now()
        am = Amenity(id="9999999999", created_at=time.isoformat(),
                     updated_at=time.isoformat())
        self.assertEqual(am.id, "9999999999")
        self.assertEqual(am.created_at, time)
        self.assertEqual(am.updated_at, time)

    def test_no_kwargs(self):
        with self.assertRaises(TypeError):
            am1 = Amenity(id=None, created_at=None, updated_at=None)


class Test_Amenity_to_dict(unittest.TestCase):
    """unittests for to_dict method"""
    def test_dict(self):
        am1 = Amenity()
        self.assertIsInstance(am1.to_dict(), dict)

    def test_to_dict_content(self):
        am1 = Amenity()
        self.assertIn("__class__", am1.to_dict())
        self.assertIn("id", am1.to_dict())
        self.assertIn("created_at", am1.to_dict())
        self.assertIn("updated_at", am1.to_dict())

    def test_to_dict_timeformat(self):
        am1 = Amenity()
        timec = am1.created_at.isoformat()
        timeu = am1.updated_at.isoformat()
        self.assertEqual(timec, am1.to_dict()["created_at"])
        self.assertEqual(timeu, am1.to_dict()["updated_at"])

    def test_to_dict_timetype(self):
        am1 = Amenity()
        self.assertIsInstance(am1.to_dict()["created_at"], str)
        self.assertIsInstance(am1.to_dict()["updated_at"], str)

    def test_to_dict_all(self):
        am1 = Amenity()
        di = {"__class__": "Amenity", "id": f"{am1.id}",
              "created_at": am1.created_at.isoformat(),
              "updated_at": am1.updated_at.isoformat()}
        self.assertDictEqual(di, am1.to_dict())

    def test_to_dict_random_addition(self):
        am1 = Amenity()
        am1.name = "Walter"
        am1.interest = "science"
        self.assertIn("name", am1.to_dict())
        self.assertIn("interest", am1.to_dict())

    def test_to_dict_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict("Take it")

    def test_creation_fromdict(self):
        am1 = Amenity()
        copy = am1.to_dict()
        del am1
        am1 = Amenity(**copy)
        self.assertDictEqual(copy, am1.to_dict())


class Test_Amenity_save(unittest.TestCase):
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
        am1 = Amenity()
        time = am1.updated_at
        sleep(0.01)
        am1.save()
        self.assertNotEqual(am1.updated_at, time)

    def test_2_update(self):
        am1 = Amenity()
        time = am1.updated_at
        sleep(0.01)
        am1.save()
        time2 = am1.updated_at
        sleep(0.01)
        am1.save()
        self.assertNotEqual(am1.updated_at, time)
        self.assertNotEqual(am1.updated_at, time2)
        self.assertLess(time, am1.updated_at)

    def test_savefile(self):
        am1 = Amenity()
        am1.save()
        with open("file.json", "r") as f:
            self.assertIn(f"{type(am1).__name__}.{am1.id}", f.read())

    def test_save_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.save("Save it")
