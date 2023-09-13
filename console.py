#!/usr/bin/python3
"""console"""
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import models
import cmd
import shlex
import re


class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "

    def precmd(self, line):
        """modify user input"""
        """User.all() -> all User"""
        line  = re.sub(r"\(\)$", "", line)
        args = line.split('.')
        if len(args) == 2:
            return f"{args[1]} {args[0]}"
        return line



    def do_create(self, line):
        """creates a new instance of BaseModel"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        cls_name = args[0]
        classes = {"User": User, "BaseModel": BaseModel, "State": State,
                    "City": City, "Amenity": Amenity, "Place": Place,
                     "Review": Review}
        if cls_name not in classes:
            print("** class doesn't exist **")
            return
        obj = classes[cls_name]()
        models.storage.save()
        print(obj.id)

    def do_show(self, line):
        """Prints the str rep of an instance based
        on the class name and id"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        cls_name = args[0]
        classes = ["User", "BaseModel", "State", "City", "Amenity",
                    "Place", "Review"]
        if cls_name not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        id = args[1]
        ##getting the list of all objects
        dictionary = storage.all()
        key = f"{cls_name}.{id}"
        if key in dictionary:
            ##dictionary[key] is an object
            print(dictionary[key])
        else:
            print("** no instance found **")
            return

    def do_destroy(self, line):
        """Deletes an instance based on the
        class name and id"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return
        cls_name = args[0]
        classes = ["User", "BaseModel", "State", "City", "Amenity",
                    "Place", "Review"]
        if cls_name not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        ##getting the list of all objects
        id = args[1]
        dictionary = storage.all()
        key = f"{cls_name}.{id}"
        if key in dictionary:
            ##dictionary[key] is the object
            del(dictionary[key])
            ##now delete the key from the dictionary
            storage.save()
        else:
            print("** no instance found **")
            return

    def do_all(self, line):
        """Prints all string representation of
        all instances based or not on the class name"""
        args = line.split()
        if len(args) == 1:
            cls_name = args[0]
            classes = ["User", "BaseModel", "State", "City", "Amenity",
                        "Place", "Review"]
            if cls_name not in classes:
                print("** class doesn't exist **")
                return
            ##getting the list of all objects
            dictionary = storage.all()
            for key in dictionary:
                ##dictionary[key] is an object
                if dictionary[key].__class__.__name__ == cls_name:
                    print(dictionary[key])
        else:
            dictionary = storage.all()
            for key in dictionary:
                print(dictionary[key])
    
    def do_update(self, line):
        """updates obj
        update <class name> <id> <attribute name> "<attribute value>"""

        args = shlex.split(line)
        if not args:
            print("** class name missing **")
            return
        cls_name = args[0]
        cls_list = ["User", "BaseModel", "State", "City", "Amenity",
                     "Place", "Review"]
        if cls_name not in cls_list:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
        id = args[1]
        dictionary = storage.all()
        key = f"{cls_name}.{id}"
        if key not in dictionary:
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        obj = dictionary[key]
        attr = args[2]
        val = args[3]
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if type(value) is int:
                setattr(obj, attr, int(val))
            elif type(value) is float:
                setattr(obj, attr, float(val))
            else:
                setattr(obj, attr, val)
        else:
            setattr(obj, attr, val)
        obj.save()
        
    
    def do_EOF(self, line):
        """quit the program"""
        return True
    
    def do_quit(self, line):
        """quit the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
