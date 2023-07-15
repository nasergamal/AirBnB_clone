#!/usr/bin/python3
'''unit tests for State Class'''
import unittest
from datetime import datetime
from models.state import State
from time import sleep
import os


class Test_Stateinit(unittest.TestCase):
    '''test cases for State instantiation'''
    def test_name_is_str(self):
        self.assertEqual(str, type(State.name))

    def test_uuid4(self):
        st1 = State()
        st2 = State()
        self.assertIsInstance(st1, State)
        self.assertTrue(hasattr(st1, "id"))
        self.assertNotEqual(st1.id, st2.id)
        self.assertIsInstance(st1.id, str)

    def test_types(self):
        st1 = State()
        self.assertIsInstance(st1.id, str)
        self.assertIsInstance(st1.created_at, datetime)
        self.assertIsInstance(st1.updated_at, datetime)

    def test_creation_timedif(self):
        st1 = State()
        sleep(0.01)
        st2 = State()
        self.assertNotEqual(st1.created_at, st2.created_at)

    def test_update_timedif(self):
        st1 = State()
        sleep(0.01)
        st2 = State()
        self.assertNotEqual(st1.updated_at, st2.updated_at)

    def test_created_at(self):
        st1 = State()
        st2 = State()
        self.assertTrue(hasattr(st1, "created_at"))
        self.assertIsInstance(st1.created_at, datetime)

    def test_updated_at(self):
        st1 = State()
        self.assertTrue(hasattr(st1, "updated_at"))
        self.assertIsInstance(st1.updated_at, datetime)

    def test_str(self):
        st1 = State()
        text = f'[{type(st1).__name__}] ({st1.id})'
        self.assertIn(text, st1.__str__())
        self.assertIn(f"'created_at': {repr(st1.created_at)}", st1.__str__())
        self.assertIn(f"'updated_at': {repr(st1.updated_at)}", st1.__str__())

    def test_kwargs(self):
        time = datetime.now()
        st = State(id="9999999999", created_at=time.isoformat(),
                   updated_at=time.isoformat())
        self.assertEqual(st.id, "9999999999")
        self.assertEqual(st.created_at, time)
        self.assertEqual(st.updated_at, time)

    def test_no_kwargs(self):
        with self.assertRaises(TypeError):
            st1 = State(id=None, created_at=None, updated_at=None)


class Test_State_to_dict(unittest.TestCase):
    """unittests for to_dict method"""
    def test_dict(self):
        st1 = State()
        self.assertIsInstance(st1.to_dict(), dict)

    def test_to_dict_content(self):
        st1 = State()
        self.assertIn("__class__", st1.to_dict())
        self.assertIn("id", st1.to_dict())
        self.assertIn("created_at", st1.to_dict())
        self.assertIn("updated_at", st1.to_dict())

    def test_to_dict_timeformat(self):
        st1 = State()
        timec = st1.created_at.isoformat()
        timeu = st1.updated_at.isoformat()
        self.assertEqual(timec, st1.to_dict()["created_at"])
        self.assertEqual(timeu, st1.to_dict()["updated_at"])

    def test_to_dict_timetype(self):
        st1 = State()
        self.assertIsInstance(st1.to_dict()["created_at"], str)
        self.assertIsInstance(st1.to_dict()["updated_at"], str)

    def test_to_dict_all(self):
        st1 = State()
        di = {"__class__": "State", "id": f"{st1.id}",
              "created_at": st1.created_at.isoformat(),
              "updated_at": st1.updated_at.isoformat()}
        self.assertDictEqual(di, st1.to_dict())

    def test_to_dict_random_addition(self):
        st1 = State()
        st1.name = "Walter"
        st1.interest = "science"
        self.assertIn("name", st1.to_dict())
        self.assertIn("interest", st1.to_dict())

    def test_to_dict_arg(self):
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict("Take it")

    def test_creation_fromdict(self):
        st1 = State()
        copy = st1.to_dict()
        del st1
        st1 = State(**copy)
        self.assertDictEqual(copy, st1.to_dict())


class Test_State_save(unittest.TestCase):
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
        st1 = State()
        time = st1.updated_at
        sleep(0.01)
        st1.save()
        self.assertNotEqual(st1.updated_at, time)

    def test_2_update(self):
        st1 = State()
        time = st1.updated_at
        sleep(0.01)
        st1.save()
        time2 = st1.updated_at
        sleep(0.01)
        st1.save()
        self.assertNotEqual(st1.updated_at, time)
        self.assertNotEqual(st1.updated_at, time2)
        self.assertLess(time, st1.updated_at)

    def test_savefile(self):
        st1 = State()
        st1.save()
        with open("file.json", "r") as f:
            self.assertIn(f"{type(st1).__name__}.{st1.id}", f.read())

    def test_save_arg(self):
        st = State()
        with self.assertRaises(TypeError):
            st.save("Save it")
