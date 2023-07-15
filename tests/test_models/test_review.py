#!/usr/bin/python3
'''unit tests for Review Class'''
import unittest
from datetime import datetime
from models.review import Review
from time import sleep
import os


class Test_Reviewinit(unittest.TestCase):
    '''test cases for Reviewinstantiation'''
    def test_place_id_is_str(self):
        self.assertEqual(str, type(Review.place_id))

    def test_user_id_is_str(self):
        self.assertEqual(str, type(Review.user_id))

    def test_text_is_str(self):
        self.assertEqual(str, type(Review.text))

    def test_uuid4(self):
        rev1 = Review()
        rev2 = Review()
        self.assertIsInstance(rev1, Review)
        self.assertTrue(hasattr(rev1, "id"))
        self.assertNotEqual(rev1.id, rev2.id)
        self.assertIsInstance(rev1.id, str)

    def test_types(self):
        rev1 = Review()
        self.assertIsInstance(rev1.id, str)
        self.assertIsInstance(rev1.created_at, datetime)
        self.assertIsInstance(rev1.updated_at, datetime)

    def test_creation_timedif(self):
        rev1 = Review()
        sleep(0.01)
        rev2 = Review()
        self.assertNotEqual(rev1.created_at, rev2.created_at)

    def test_update_timedif(self):
        rev1 = Review()
        sleep(0.01)
        rev2 = Review()
        self.assertNotEqual(rev1.updated_at, rev2.updated_at)

    def test_created_at(self):
        rev1 = Review()
        rev2 = Review()
        self.assertTrue(hasattr(rev1, "created_at"))
        self.assertIsInstance(rev1.created_at, datetime)

    def test_updated_at(self):
        rev1 = Review()
        self.assertTrue(hasattr(rev1, "updated_at"))
        self.assertIsInstance(rev1.updated_at, datetime)

    def test_str(self):
        rev1 = Review()
        text = f'[{type(rev1).__name__}] ({rev1.id})'
        self.assertIn(text, rev1.__str__())
        self.assertIn(f"'created_at': {repr(rev1.created_at)}", rev1.__str__())
        self.assertIn(f"'updated_at': {repr(rev1.updated_at)}", rev1.__str__())

    def test_kwargs(self):
        time = datetime.now()
        rev = Review(id="9999999999", created_at=time.isoformat(),
                     updated_at=time.isoformat())
        self.assertEqual(rev.id, "9999999999")
        self.assertEqual(rev.created_at, time)
        self.assertEqual(rev.updated_at, time)

    def test_no_kwargs(self):
        with self.assertRaises(TypeError):
            rev1 = Review(id=None, created_at=None, updated_at=None)


class Test_Review_to_dict(unittest.TestCase):
    """unittests for to_dict method"""
    def test_dict(self):
        rev1 = Review()
        self.assertIsInstance(rev1.to_dict(), dict)

    def test_to_dict_content(self):
        rev1 = Review()
        self.assertIn("__class__", rev1.to_dict())
        self.assertIn("id", rev1.to_dict())
        self.assertIn("created_at", rev1.to_dict())
        self.assertIn("updated_at", rev1.to_dict())

    def test_to_dict_timeformat(self):
        rev1 = Review()
        timec = rev1.created_at.isoformat()
        timeu = rev1.updated_at.isoformat()
        self.assertEqual(timec, rev1.to_dict()["created_at"])
        self.assertEqual(timeu, rev1.to_dict()["updated_at"])

    def test_to_dict_timetype(self):
        rev1 = Review()
        self.assertIsInstance(rev1.to_dict()["created_at"], str)
        self.assertIsInstance(rev1.to_dict()["updated_at"], str)

    def test_to_dict_all(self):
        rev1 = Review()
        di = {"__class__": "Review", "id": f"{rev1.id}",
              "created_at": rev1.created_at.isoformat(),
              "updated_at": rev1.updated_at.isoformat()}
        self.assertDictEqual(di, rev1.to_dict())

    def test_to_dict_random_addition(self):
        rev1 = Review()
        rev1.name = "Walter"
        rev1.interest = "science"
        self.assertIn("name", rev1.to_dict())
        self.assertIn("interest", rev1.to_dict())

    def test_to_dict_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.to_dict("Take it")

    def test_creation_fromdict(self):
        rev1 = Review()
        copy = rev1.to_dict()
        del rev1
        rev1 = Review(**copy)
        self.assertDictEqual(copy, rev1.to_dict())


class Test_Review_save(unittest.TestCase):
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
        rev1 = Review()
        time = rev1.updated_at
        sleep(0.01)
        rev1.save()
        self.assertNotEqual(rev1.updated_at, time)

    def test_2_update(self):
        rev1 = Review()
        time = rev1.updated_at
        sleep(0.01)
        rev1.save()
        time2 = rev1.updated_at
        sleep(0.01)
        rev1.save()
        self.assertNotEqual(rev1.updated_at, time)
        self.assertNotEqual(rev1.updated_at, time2)
        self.assertLess(time, rev1.updated_at)

    def test_savefile(self):
        rev1 = Review()
        rev1.save()
        with open("file.json", "r") as f:
            self.assertIn(f"{type(rev1).__name__}.{rev1.id}", f.read())

    def test_save_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.save("Save it")
