#!/usr/bin/python3
'''unit tests for User Class'''
import unittest
from datetime import datetime
from models.user import User
from time import sleep
import os


class Test_Userinit(unittest.TestCase):
    '''test cases for Basemodel instantiation'''
    def test_email_is_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_uuid4(self):
        us1 = User()
        us2 = User()
        self.assertIsInstance(us1, User)
        self.assertTrue(hasattr(us1, "id"))
        self.assertNotEqual(us1.id, us2.id)
        self.assertIsInstance(us1.id, str)

    def test_types(self):
        us1 = User()
        self.assertEqual(User, type(User()))
        self.assertIsInstance(us1.id, str)
        self.assertIsInstance(us1.created_at, datetime)
        self.assertIsInstance(us1.updated_at, datetime)

    def test_creation_timedif(self):
        us1 = User()
        sleep(0.01)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)

    def test_update_timedif(self):
        us1 = User()
        sleep(0.01)
        us2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def test_created_at(self):
        us1 = User()
        us2 = User()
        self.assertTrue(hasattr(us1, "created_at"))
        self.assertIsInstance(us1.created_at, datetime)

    def test_updated_at(self):
        us1 = User()
        self.assertTrue(hasattr(us1, "updated_at"))
        self.assertIsInstance(us1.updated_at, datetime)

    def test_str(self):
        us1 = User()
        text = f'[{type(us1).__name__}] ({us1.id})'
        self.assertIn(text, us1.__str__())
        self.assertIn(f"'created_at': {repr(us1.created_at)}", us1.__str__())
        self.assertIn(f"'updated_at': {repr(us1.updated_at)}", us1.__str__())

    def test_kwargs(self):
        time = datetime.now()
        us = User(id="9999999999", created_at=time.isoformat(),
                  updated_at=time.isoformat())
        self.assertEqual(us.id, "9999999999")
        self.assertEqual(us.created_at, time)
        self.assertEqual(us.updated_at, time)

    def test_no_kwargs(self):
        with self.assertRaises(TypeError):
            us1 = User(id=None, created_at=None, updated_at=None)


class Test_User_to_dict(unittest.TestCase):
    """unittests for to_dict method"""
    def test_dict(self):
        us1 = User()
        self.assertIsInstance(us1.to_dict(), dict)

    def test_to_dict_content(self):
        us1 = User()
        self.assertIn("__class__", us1.to_dict())
        self.assertIn("id", us1.to_dict())
        self.assertIn("created_at", us1.to_dict())
        self.assertIn("updated_at", us1.to_dict())

    def test_to_dict_timeformat(self):
        us1 = User()
        timec = us1.created_at.isoformat()
        timeu = us1.updated_at.isoformat()
        self.assertEqual(timec, us1.to_dict()["created_at"])
        self.assertEqual(timeu, us1.to_dict()["updated_at"])

    def test_to_dict_timetype(self):
        us1 = User()
        self.assertIsInstance(us1.to_dict()["created_at"], str)
        self.assertIsInstance(us1.to_dict()["updated_at"], str)

    def test_to_dict_all(self):
        us1 = User()
        di = {"__class__": "User", "id": f"{us1.id}",
              "created_at": us1.created_at.isoformat(),
              "updated_at": us1.updated_at.isoformat()}
        self.assertDictEqual(di, us1.to_dict())

    def test_to_dict_random_addition(self):
        us1 = User()
        us1.name = "Walter"
        us1.interest = "science"
        self.assertIn("name", us1.to_dict())
        self.assertIn("interest", us1.to_dict())

    def test_to_dict_arg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict("Take it")

    def test_creation_fromdict(self):
        us1 = User()
        copy = us1.to_dict()
        del us1
        us1 = User(**copy)
        self.assertDictEqual(copy, us1.to_dict())


class Test_User_save(unittest.TestCase):
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
        us1 = User()
        time = us1.updated_at
        sleep(0.01)
        us1.save()
        self.assertNotEqual(us1.updated_at, time)

    def test_2_update(self):
        us1 = User()
        time = us1.updated_at
        sleep(0.01)
        us1.save()
        time2 = us1.updated_at
        sleep(0.01)
        us1.save()
        self.assertNotEqual(us1.updated_at, time)
        self.assertNotEqual(us1.updated_at, time2)
        self.assertLess(time, us1.updated_at)

    def test_savefile(self):
        us1 = User()
        us1.save()
        with open("file.json", "r") as f:
            self.assertIn(f"{type(us1).__name__}.{us1.id}", f.read())

    def test_save_arg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save("Save it")
