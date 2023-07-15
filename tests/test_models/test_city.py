#!/usr/bin/python3
'''unit tests for City Class'''
import unittest
from datetime import datetime
from models.city import City
from time import sleep
import os


class Test_Cityinit(unittest.TestCase):
    '''test cases for City instantiation'''
    def test_name_is_str(self):
        self.assertEqual(str, type(City.name))

    def test_stateid_is_str(self):
        self.assertEqual(str, type(City.state_id))

    def test_uuid4(self):
        cy1 = City()
        cy2 = City()
        self.assertIsInstance(cy1, City)
        self.assertTrue(hasattr(cy1, "id"))
        self.assertNotEqual(cy1.id, cy2.id)
        self.assertIsInstance(cy1.id, str)

    def test_types(self):
        cy1 = City()
        self.assertIsInstance(cy1.id, str)
        self.assertIsInstance(cy1.created_at, datetime)
        self.assertIsInstance(cy1.updated_at, datetime)

    def test_creation_timedif(self):
        cy1 = City()
        sleep(0.01)
        cy2 = City()
        self.assertNotEqual(cy1.created_at, cy2.created_at)

    def test_update_timedif(self):
        cy1 = City()
        sleep(0.01)
        cy2 = City()
        self.assertNotEqual(cy1.updated_at, cy2.updated_at)

    def test_created_at(self):
        cy1 = City()
        cy2 = City()
        self.assertTrue(hasattr(cy1, "created_at"))
        self.assertIsInstance(cy1.created_at, datetime)

    def test_updated_at(self):
        cy1 = City()
        self.assertTrue(hasattr(cy1, "updated_at"))
        self.assertIsInstance(cy1.updated_at, datetime)

    def test_str(self):
        cy1 = City()
        text = f'[{type(cy1).__name__}] ({cy1.id})'
        self.assertIn(text, cy1.__str__())
        self.assertIn(f"'created_at': {repr(cy1.created_at)}", cy1.__str__())
        self.assertIn(f"'updated_at': {repr(cy1.updated_at)}", cy1.__str__())

    def test_kwargs(self):
        time = datetime.now()
        cy = City(id="9999999999", created_at=time.isoformat(),
                  updated_at=time.isoformat())
        self.assertEqual(cy.id, "9999999999")
        self.assertEqual(cy.created_at, time)
        self.assertEqual(cy.updated_at, time)

    def test_no_kwargs(self):
        with self.assertRaises(TypeError):
            cy1 = City(id=None, created_at=None, updated_at=None)


class Test_City_to_dict(unittest.TestCase):
    """unittests for to_dict method"""
    def test_dict(self):
        cy1 = City()
        self.assertIsInstance(cy1.to_dict(), dict)

    def test_to_dict_content(self):
        cy1 = City()
        self.assertIn("__class__", cy1.to_dict())
        self.assertIn("id", cy1.to_dict())
        self.assertIn("created_at", cy1.to_dict())
        self.assertIn("updated_at", cy1.to_dict())

    def test_to_dict_timeformat(self):
        cy1 = City()
        timec = cy1.created_at.isoformat()
        timeu = cy1.updated_at.isoformat()
        self.assertEqual(timec, cy1.to_dict()["created_at"])
        self.assertEqual(timeu, cy1.to_dict()["updated_at"])

    def test_to_dict_timetype(self):
        cy1 = City()
        self.assertIsInstance(cy1.to_dict()["created_at"], str)
        self.assertIsInstance(cy1.to_dict()["updated_at"], str)

    def test_to_dict_all(self):
        cy1 = City()
        di = {"__class__": "City", "id": f"{cy1.id}",
              "created_at": cy1.created_at.isoformat(),
              "updated_at": cy1.updated_at.isoformat()}
        self.assertDictEqual(di, cy1.to_dict())

    def test_to_dict_random_addition(self):
        cy1 = City()
        cy1.name = "Walter"
        cy1.interest = "science"
        self.assertIn("name", cy1.to_dict())
        self.assertIn("interest", cy1.to_dict())

    def test_to_dict_arg(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict("Take it")

    def test_creation_fromdict(self):
        cy1 = City()
        copy = cy1.to_dict()
        del cy1
        cy1 = City(**copy)
        self.assertDictEqual(copy, cy1.to_dict())


class Test_City_save(unittest.TestCase):
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
        cy1 = City()
        time = cy1.updated_at
        sleep(0.01)
        cy1.save()
        self.assertNotEqual(cy1.updated_at, time)

    def test_2_update(self):
        cy1 = City()
        time = cy1.updated_at
        sleep(0.01)
        cy1.save()
        time2 = cy1.updated_at
        sleep(0.01)
        cy1.save()
        self.assertNotEqual(cy1.updated_at, time)
        self.assertNotEqual(cy1.updated_at, time2)
        self.assertLess(time, cy1.updated_at)

    def test_savefile(self):
        cy1 = City()
        cy1.save()
        with open("file.json", "r") as f:
            self.assertIn(f"{type(cy1).__name__}.{cy1.id}", f.read())

    def test_save_arg(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.save("Save it")
