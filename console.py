#!/usr/bin/python3
'''entry point of the command interpreter'''
import cmd
import sys
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import re
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    '''hbnb cmd class'''
    prompt = "(hbnb) "
    ms = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]

    def onecmd(self, line):
        '''modified onecmd'''
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if cmd == '':
            return self.default(line)
        else:
            try:
                if "." in line:
                    f, c = line.split(".")
                    x = re.search(r'(.*)\(', c)
                    func = getattr(self, 'do_' + x[1])
                    i = re.search(r'\((.*?)\)', c)
                    if i[1]:
                        f = f + ' ' + i[1]
                    return func(f)
            except Exception as e:
                pass
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)

    def do_EOF(self, arg):
        '''Close file'''
        return True

    def do_quit(self, arg):
        '''Quit command to exit the program'''
        return True

    def emptyline(self):
        return

    def do_create(self, arg):
        '''create a new instace of given class'''
        if not arg:
            print("** class name missing **")
        elif arg not in HBNBCommand.ms:
            print("** class doesn't exist **")
        else:
            x = eval(arg)()
            print(x.id)
            x.save()

    def do_show(self, arg):
        '''show instance details given class and id'''
        arg = arg.replace("\"", "")
        a = list(arg.split())
        if not a:
            print("** class name missing **")
        elif a[0] not in HBNBCommand.ms:
            print("** class doesn't exist **")
        elif len(a) < 2:
            print("** instance id missing **")
        else:
            k = f"{a[0]}.{a[1]}"
            k = storage.idexist(k)
            if k:
                print(k)
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        '''delete instance by id and class'''
        arg = arg.replace("\"", "")
        a = list(arg.split())
        if not a:
            print("** class name missing **")
        elif a[0] not in HBNBCommand.ms:
            print("** class doesn't exist **")
        elif len(a) < 2:
            print("** instance id missing **")
        else:
            k = f"{a[0]}.{a[1]}"
            k = storage.remove(k)
            if not k:
                print("** no instance found **")

    def do_all(self, arg):
        '''show all instance of required class'''
        if arg and arg not in HBNBCommand.ms:
            print("** class doesn't exist **")
        else:
            li = storage.getall(arg)
            print(li)

    def do_update(self, arg):
        '''update an instance attribute'''
        a = parse(arg)
        if not a:
            print("** class name missing **")
            return
        elif a[0] not in HBNBCommand.ms:
            print("** class doesn't exist **")
            return
        elif len(a) < 2:
            print("** instance id missing **")
            return
        k = f"{a[0]}.{a[1]}"
        if not storage.idexist(k):
            print("** no instance found **")
            return
        elif len(a) < 3:
            print("** attribute name missing **")
            return
        elif len(a) == 3:
            if type(a[2]) != dict:
                print("** value missing **")
                return
        if type(a[2]) != dict and a[2] in "id created_at updated_at":
            return
        if len(a) > 3:
            storage.update(k, a)
        else:
            objall = storage.all()
            obj = objall[f"{a[0]}.{a[1]}"]
            for k, v in a[2].items():
                if k not in "id created_at updated_at":
                    try:
                        t = type(obj.__class__.__dict__[k])
                        obj.__dict__[k] = t(v)
                    except KeyError:
                        obj.__dict__[k] = v
            obj.__dict__['updated_at'] = datetime.utcnow()
            storage.save()

    def do_count(self, arg):
        '''return number of instance in given class'''
        a = list(arg.split())
        if not a:
            print("** class name missing **")
            return
        elif a[0] not in HBNBCommand.ms:
            print("** class doesn't exist **")
            return
        x = storage.all()
        c = 0
        for k in x.keys():
            if k.startswith(a[0]):
                c += 1
        print(c)


def parse(arg):
    '''parses text for excution'''
    di = re.search(r"\{(.*)\}", arg)
    if di:
        narg = arg[:di.span()[0]]
        narg = narg.replace("\"", "")
        narg = narg.replace(",", "")
        di = eval(di.group())
        narg = list(narg.split())
        narg.append(di)
        arg = narg
    else:
        arg = arg.replace("'", "")
        arg = arg.replace("\"", "")
        arg = arg.replace(",", "")
        arg = list(arg.split())
    return arg


if __name__ == '__main__':
    HBNBCommand().cmdloop()
