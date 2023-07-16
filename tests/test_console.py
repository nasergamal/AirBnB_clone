#!/usr/bin/python3
'''Unit tests for Console'''
import os
import unittest
from unittest.mock import patch
from models import storage
from console import HBNBCommand
from io import StringIO
from models.engine.file_storage import FileStorage


class Test_console_basics(unittest.TestCase):
    '''unittests for console's basic functions'''

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_help(self):
        c = "Documented commands (type help <topic>):\n"
        c += "========================================\n"
        c += "EOF  all  count  create  destroy  help  quit  show  update"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(c, f.getvalue().strip())

    def test_help_quit(self):
        c = "Quit command to exit the program"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(c, f.getvalue().strip())

    def test_help_EOF(self):
        c = "Close file"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(c, f.getvalue().strip())

    def test_help_all(self):
        c = "show all instance of required class"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(c, f.getvalue().strip())

    def test_help_count(self):
        c = "return number of instance in given class"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(c, f.getvalue().strip())

    def test_help_create(self):
        c = "create a new instace of given class"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(c, f.getvalue().strip())

    def test_help_destroy(self):
        c = "delete instance by id and class"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(c, f.getvalue().strip())

    def test_help_show(self):
        c = "show instance details given class and id"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(c, f.getvalue().strip())

    def test_help_update(self):
        c = "update an instance attribute"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(c, f.getvalue().strip())

    def test_emptyline(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", f.getvalue().strip())


class Test_console_create_show_methods(unittest.TestCase):
    '''unit tests for console's create and show methods'''
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "fil.json")
        except IOError:
            pass
        storage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("fil.json", "file.json")
        except IOError:
            pass

    def test_create_method_no_arg(self):
        output = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(output, f.getvalue().strip())

    def test_create_method_wrong_model(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create model"))
            self.assertEqual(output, f.getvalue().strip())

    def test_create_method_normal(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            output = f.getvalue().strip()
            self.assertIn(f"BaseModel.{output}", storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            output = f.getvalue().strip()
            self.assertIn(f"User.{output}", storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            output = f.getvalue().strip()
            self.assertIn(f"State.{output}", storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            output = f.getvalue().strip()
            self.assertIn(f"City.{output}", storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            output = f.getvalue().strip()
            self.assertIn(f"Amenity.{output}", storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            output = f.getvalue().strip()
            self.assertIn(f"Place.{output}", storage.all().keys())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            output = f.getvalue().strip()
            self.assertIn(f"Review.{output}", storage.all().keys())

    def test_show_method_no_arg(self):
        output = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(output, f.getvalue().strip())

    def test_show_method_wrong_model(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show model"))
            self.assertEqual(output, f.getvalue().strip())

    def test_show_method_wrong_model2(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("model.show()"))
            self.assertEqual(output, f.getvalue().strip())

    def test_show_method_no_id(self):
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(output, f.getvalue().strip())

    def test_show_method_no_id2(self):
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(output, f.getvalue().strip())

    def test_show_method_wrong_id(self):
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 123"))
            self.assertEqual(output, f.getvalue().strip())

    def test_show_method_wrong_id2(self):
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show('123')"))
            self.assertEqual(output, f.getvalue().strip())

    def test_show_method_normal(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"show BaseModel {output}"))
            obj = storage.all()[f"BaseModel.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"show User {output}"))
            obj = storage.all()[f"User.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"show State {output}"))
            obj = storage.all()[f"State.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"show City {output}"))
            obj = storage.all()[f"City.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"show Amenity {output}"))
            obj = storage.all()[f"Amenity.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"show Place {output}"))
            obj = storage.all()[f"Place.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"show Review {output}"))
            obj = storage.all()[f"Review.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())

    def test_show_method_normal2(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"BaseModel.show({output})"))
            obj = storage.all()[f"BaseModel.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"User.show({output})"))
            obj = storage.all()[f"User.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"State.show({output})"))
            obj = storage.all()[f"State.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"City.show({output})"))
            obj = storage.all()[f"City.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"Amenity.show({output})"))
            obj = storage.all()[f"Amenity.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"Place.show({output})"))
            obj = storage.all()[f"Place.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"Review.show({output})"))
            obj = storage.all()[f"Review.{output}"]
            self.assertEqual(obj.__str__(), f.getvalue().strip())


class Test_console_destroy_all_methods(unittest.TestCase):
    '''unit tests for console's destroy and all methods'''
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "fil.json")
        except IOError:
            pass
        storage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("fil.json", "file.json")
        except IOError:
            pass

    def test_destroy_method_no_arg(self):
        output = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(output, f.getvalue().strip())

    def test_destroy_method_wrong_model(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy model"))
            self.assertEqual(output, f.getvalue().strip())

    def test_destroy_method_wrong_model2(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("model.destroy()"))
            self.assertEqual(output, f.getvalue().strip())

    def test_destroy_method_no_id(self):
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(output, f.getvalue().strip())

    def test_destroy_method_no_id2(self):
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(output, f.getvalue().strip())

    def test_destroy_method_wrong_id(self):
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 123"))
            self.assertEqual(output, f.getvalue().strip())

    def test_destroy_method_wrong_id2(self):
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = "BaseModel.destroy('123')"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(output, f.getvalue().strip())

    def test_show_method_normal(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"BaseModel.{output}"]
            cmd = f"destroy BaseModel {output}"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertNotIn(f"BaseModel.{output}", storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"User.{output}"]
            self.assertFalse(HBNBCommand().onecmd(f"destroy User {output}"))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"State.{output}"]
            self.assertFalse(HBNBCommand().onecmd(f"destroy State {output}"))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"City.{output}"]
            self.assertFalse(HBNBCommand().onecmd(f"destroy City {output}"))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"Amenity.{output}"]
            self.assertFalse(HBNBCommand().onecmd(f"destroy Amenity {output}"))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"Place.{output}"]
            self.assertFalse(HBNBCommand().onecmd(f"destroy Place {output}"))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"Review.{output}"]
            self.assertFalse(HBNBCommand().onecmd(f"destroy Review {output}"))
            self.assertNotIn(obj, storage.all().values())

    def test_destroy_method_normal(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"BaseModel.{output}"]
            cmd = f'BaseModel.destroy("{output}")'
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"User.{output}"]
            self.assertFalse(HBNBCommand().onecmd(f'User.destroy("{output}")'))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"State.{output}"]
            cmd = f'State.destroy("{output}")'
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"City.{output}"]
            self.assertFalse(HBNBCommand().onecmd(f'City.destroy("{output}")'))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"Amenity.{output}"]
            cmd = f'Amenity.destroy("{output}")'
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"Place.{output}"]
            cmd = f'Place.destroy("{output}")'
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertNotIn(obj, storage.all().values())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            obj = storage.all()[f"Review.{output}"]
            cmd = f'Review.destroy("{output}")'
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertNotIn(obj, storage.all().values())

    def test_all_wrong_model(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all model"))
            self.assertEqual(output, f.getvalue().strip())

    def test_all_normal(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("create State")
            HBNBCommand().onecmd("create City")
            HBNBCommand().onecmd("create Amenity")
            HBNBCommand().onecmd("create Place")
            HBNBCommand().onecmd("create Review")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", f.getvalue().strip())
            self.assertIn("User", f.getvalue().strip())
            self.assertIn("State", f.getvalue().strip())
            self.assertIn("Place", f.getvalue().strip())
            self.assertIn("City", f.getvalue().strip())
            self.assertIn("Amenity", f.getvalue().strip())
            self.assertIn("Review", f.getvalue().strip())

    def test_all_one_class(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", f.getvalue().strip())
            self.assertNotIn("BaseModel", f.getvalue().strip())

    def test_all_one_class2(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            output = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", f.getvalue().strip())
            self.assertNotIn("Review", f.getvalue().strip())


class Test_console_update_method(unittest.TestCase):
    '''unit tests for console's update method'''
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "fil.json")
        except IOError:
            pass
        storage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("fil.json", "file.json")
        except IOError:
            pass

    def test_update_method_no_arg(self):
        output = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_wrong_model(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update model"))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_wrong_model2(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("model.update()"))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_no_id(self):
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_no_id2(self):
        output = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_wrong_id(self):
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 123"))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_wrong_id2(self):
        output = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update('123')"))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_missing_attname(self):
        output = "** attribute name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            out = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(f"update BaseModel {out}"))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_missing_attname2(self):
        output = "** attribute name missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            out = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = f"BaseModel.update('{out}')"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_missing_attname(self):
        output = "** value missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            out = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = f"update BaseModel {out} attname"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_missing_attname2(self):
        output = "** value missing **"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            out = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = f"BaseModel.update('{out}', 'attname')"
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(output, f.getvalue().strip())

    def test_update_method_normal1(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            out = f.getvalue().strip()
        cmd = f"update BaseModel {out} attname attvalue"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        self.assertIn('attname', storage.all()[f'BaseModel.{out}'].__dict__)

    def test_update_method_normal2(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            out = f.getvalue().strip()
        cmd = f'BaseModel.update("{out}", "attname", "attvalue")'
        self.assertFalse(HBNBCommand().onecmd(cmd))
        self.assertIn('attname', storage.all()[f'BaseModel.{out}'].__dict__)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            out = f.getvalue().strip()
        cmd = f"User.update('{out}', 'attname', 'attvalue')"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        self.assertIn('attname', storage.all()[f'User.{out}'].__dict__)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            out = f.getvalue().strip()
        cmd = f"State.update('{out}', 'attname', 'attvalue')"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        self.assertIn('attname', storage.all()[f'State.{out}'].__dict__)

    def test_update_method_dict(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            out = f.getvalue().strip()
        cmd = f'BaseModel.update("{out}"'
        cmd += ", {'attname': 'attvalue', 'nameofatt': 'valueofatt'})"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        self.assertIn('attname', storage.all()[f'BaseModel.{out}'].__dict__)
        self.assertIn('nameofatt', storage.all()[f'BaseModel.{out}'].__dict__)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            out = f.getvalue().strip()
        cmd = f'User.update("{out}"'
        cmd += ", {'attname': 'attvalue', 'nameofatt': 'valueofatt'})"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        self.assertIn('attname', storage.all()[f'User.{out}'].__dict__)
        self.assertIn('nameofatt', storage.all()[f'User.{out}'].__dict__)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            out = f.getvalue().strip()
        cmd = f'State.update("{out}"'
        cmd += ", {'attname': 'attvalue', 'nameofatt': 'valueofatt'})"
        self.assertFalse(HBNBCommand().onecmd(cmd))
        self.assertIn('attname', storage.all()[f'State.{out}'].__dict__)
        self.assertIn('nameofatt', storage.all()[f'State.{out}'].__dict__)


class Test_instance_count(unittest.TestCase):
    '''unit tests for console's update method'''
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "fil.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("fil.json", "file.json")
        except IOError:
            pass

    def test_count_method_wrong_model(self):
        output = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("count model"))
            self.assertEqual(output, f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("model.count()"))
            self.assertEqual(output, f.getvalue().strip())

    def test_count(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count BaseModel")
            self.assertEqual('4', f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count User")
            self.assertEqual('3', f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            HBNBCommand().onecmd("create State")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count State")
            self.assertEqual('2', f.getvalue().strip())

    def test_count2(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create BaseModel")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.count()")
            self.assertEqual('4', f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("create User")
            HBNBCommand().onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.count()")
            self.assertEqual('3', f.getvalue().strip())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            HBNBCommand().onecmd("create State")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("State.count()")
            self.assertEqual('2', f.getvalue().strip())
