#!/usr/bin/python3
'''Unit tests for Console'''
import os
import unittest
from unittest.mock import patch
from models import storage
from console import HBNBCommand
from io import StringIO


class Test_console_basics(unittest.TestCase):
    '''unittests for console's  ????????????????'''

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
        c = "Close file"
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(c, f.getvalue().strip())
