#!/usr/bin/python3
'''unit tests for Place Class'''
import unittest
from datetime import datetime
from models.place import Place
from time import sleep
import os


class Test_Placeinit(unittest.TestCase):
    '''test cases for Place instantiation'''
    def test_city_id_is_str(self):
        self.assertEqual(str, type(Place.city_id))

    def test_user_id_is_str(self):
        self.assertEqual(str, type(Place.user_id))

    def test_name_is_str(self):
        self.assertEqual(str, type(Place.name))

    def test_description_is_str(self):
        self.assertEqual(str, type(Place.description))

    def test_number_rooms_is_int(self):
        self.assertEqual(int, type(Place.number_rooms))

    def test_number_rooms_is_int(self):
        self.assertEqual(int, type(Place.number_rooms))

    def test_number_bathrooms_is_int(self):
        self.assertEqual(int, type(Place.number_bathrooms))

    def test_max_guest_is_int(self):
        self.assertEqual(int, type(Place.max_guest))

    def test_price_by_night_is_int(self):
        self.assertEqual(int, type(Place.price_by_night))

    def test_latitude_is_float(self):
        self.assertEqual(float, type(Place.latitude))

    def test_longitude_is_float(self):
        self.assertEqual(float, type(Place.longitude))

    def test_amenity_ids_is_list(self):
        self.assertEqual(list, type(Place.amenity_ids))

    def test_uuid4(self):
        pl1 = Place()
        pl2 = Place()
        self.assertIsInstance(pl1, Place)
        self.assertTrue(hasattr(pl1, "id"))
        self.assertNotEqual(pl1.id, pl2.id)
        self.assertIsInstance(pl1.id, str)

    def test_types(self):
        pl1 = Place()
        self.assertIsInstance(pl1.id, str)
        self.assertIsInstance(pl1.created_at, datetime)
        self.assertIsInstance(pl1.updated_at, datetime)

    def test_creation_timedif(self):
        pl1 = Place()
        sleep(0.01)
        pl2 = Place()
        self.assertNotEqual(pl1.created_at, pl2.created_at)

    def test_update_timedif(self):
        pl1 = Place()
        sleep(0.01)
        pl2 = Place()
        self.assertNotEqual(pl1.updated_at, pl2.updated_at)

    def test_created_at(self):
        pl1 = Place()
        pl2 = Place()
        self.assertTrue(hasattr(pl1, "created_at"))
        self.assertIsInstance(pl1.created_at, datetime)

    def test_updated_at(self):
        pl1 = Place()
        self.assertTrue(hasattr(pl1, "updated_at"))
        self.assertIsInstance(pl1.updated_at, datetime)

    def test_str(self):
        pl1 = Place()
        text = f'[{type(pl1).__name__}] ({pl1.id})'
        self.assertIn(text, pl1.__str__())
        self.assertIn(f"'created_at': {repr(pl1.created_at)}", pl1.__str__())
        self.assertIn(f"'updated_at': {repr(pl1.updated_at)}", pl1.__str__())

    def test_kwargs(self):
        time = datetime.now()
        pl = Place(id="9999999999", created_at=time.isoformat(),
                   updated_at=time.isoformat())
        self.assertEqual(pl.id, "9999999999")
        self.assertEqual(pl.created_at, time)
        self.assertEqual(pl.updated_at, time)

    def test_no_kwargs(self):
        with self.assertRaises(TypeError):
            pl1 = Place(id=None, created_at=None, updated_at=None)


class Test_Place_to_dict(unittest.TestCase):
    """unittests for to_dict method"""
    def test_dict(self):
        pl1 = Place()
        self.assertIsInstance(pl1.to_dict(), dict)

    def test_to_dict_content(self):
        pl1 = Place()
        self.assertIn("__class__", pl1.to_dict())
        self.assertIn("id", pl1.to_dict())
        self.assertIn("created_at", pl1.to_dict())
        self.assertIn("updated_at", pl1.to_dict())

    def test_to_dict_timeformat(self):
        pl1 = Place()
        timec = pl1.created_at.isoformat()
        timeu = pl1.updated_at.isoformat()
        self.assertEqual(timec, pl1.to_dict()["created_at"])
        self.assertEqual(timeu, pl1.to_dict()["updated_at"])

    def test_to_dict_timetype(self):
        pl1 = Place()
        self.assertIsInstance(pl1.to_dict()["created_at"], str)
        self.assertIsInstance(pl1.to_dict()["updated_at"], str)

    def test_to_dict_all(self):
        pl1 = Place()
        di = {"__class__": "Place", "id": f"{pl1.id}",
              "created_at": pl1.created_at.isoformat(),
              "updated_at": pl1.updated_at.isoformat()}
        self.assertDictEqual(di, pl1.to_dict())

    def test_to_dict_random_addition(self):
        pl1 = Place()
        pl1.name = "Walter"
        pl1.interest = "science"
        self.assertIn("name", pl1.to_dict())
        self.assertIn("interest", pl1.to_dict())

    def test_to_dict_arg(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.to_dict("Take it")

    def test_creation_fromdict(self):
        pl1 = Place()
        copy = pl1.to_dict()
        del pl1
        pl1 = Place(**copy)
        self.assertDictEqual(copy, pl1.to_dict())


class Test_Place_save(unittest.TestCase):
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
        pl1 = Place()
        time = pl1.updated_at
        sleep(0.01)
        pl1.save()
        self.assertNotEqual(pl1.updated_at, time)

    def test_2_update(self):
        pl1 = Place()
        time = pl1.updated_at
        sleep(0.01)
        pl1.save()
        time2 = pl1.updated_at
        sleep(0.01)
        pl1.save()
        self.assertNotEqual(pl1.updated_at, time)
        self.assertNotEqual(pl1.updated_at, time2)
        self.assertLess(time, pl1.updated_at)

    def test_savefile(self):
        pl1 = Place()
        pl1.save()
        with open("file.json", "r") as f:
            self.assertIn(f"{type(pl1).__name__}.{pl1.id}", f.read())

    def test_save_arg(self):
        pl = Place()
        with self.assertRaises(TypeError):
            pl.save("Save it")
