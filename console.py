#!/usr/bin/python3
"""the console program for AirBnB."""

import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import json
import re

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review
}


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter.

        Attributes:
            prompt (str): The command prompt.
    """

    prompt = "(hbnb) "

    @staticmethod
    def parseLine(line):
        """parses the input line into tokens

        :param line: the arguments of the command.
        """
        return list(line.split())

    def countInstance(self, cls_name):
        """countInstance: counts the number of instances for a specific obj.

        Usage: <Class name>.count()
        """
        storage_dic = storage.all()
        counter = 0
        if cls_name not in classes.keys():
            print("** class doesn't exist **")
            return
        for key in storage_dic.keys():
            matching = re.search(r"^({})\..+".format(cls_name), key)
            if matching:
                counter += 1
        print(counter)

    def emptyline(self):
        """emptyline and enter does nothing anymore.
        """
        pass

    def default(self, line):
        """default.

        overrides the default behavior of cmd
        """
        cmd_methods = {
            "all": self.do_all,
            "create": self.do_create,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
            "count": self.countInstance
        }
        if "{" not in line:
            matching = re.search(
                r"(\w+)\.(\w+)\(['\"]?(.*?)?['\"]?(?:, (.*?))?(?:, (.*?))?\)",
                line)
            if matching:
                if matching.group(2) in cmd_methods:
                    call = cmd_methods[matching.group(2)]
                    if not matching.group(3):
                        call(matching.group(1))
                    elif not matching.group(4):
                        args = matching.group(1) + " " + matching.group(3)
                        call(args)
                    elif not matching.group(5):
                        args = matching.group(
                            1) + " " + matching.group(3) +\
                            " " + matching.group(4)
                        call(args)
                    else:
                        args = matching.group(
                            1) + " " + matching.group(3) + " " +\
                            matching.group(4) + " " + matching.group(5)
                        call(args)
                else:
                    print(f"*** Unknown syntax: {line}")
            else:
                print(f"*** Unknown syntax: {line}")
        else:
            matching = re.search(r"(\w+)\.(\w+)\((.*?)?(?:, )(.*?)?\)", line)
            if matching:
                if matching.group(2) in cmd_methods:
                    call = cmd_methods[matching.group(2)]
                    args = matching.group(
                        1) + " " + matching.group(3) + " " +\
                        matching.group(4)
                    call(args)
                else:
                    print(f"*** Unknown syntax: {line}")
            else:
                print(f"*** Unknown syntax: {line}")

    def do_quit(self, line):
        """Quit command to exit the program.
        """
        return True

    def do_EOF(self, line):
        """(Ctrl+D): Exit the program.
        """
        print("")
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel

        Usage: create <Class_name> <Class_id>
        """

        token = HBNBCommand.parseLine(line)
        if token == []:
            print("** class name missing **")
        elif token[0] in classes.keys():
            new_cls = classes[token[0]]()
            print(new_cls.id)
            new_cls.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation of an instance

        Usage: show <Class_name> <Class_id>
        """
        token = HBNBCommand.parseLine(line)
        obj_dic = storage.all()
        if token == []:
            print("** class name missing **")
        elif token[0] not in classes.keys():
            print("** class doesn't exist **")
        elif len(token) == 1:
            print("** instance id missing **")
        elif f"{token[0]}.{token[1]}" not in obj_dic:
            print("** no instance found **")
        else:
            print(obj_dic["{}.{}".format(token[0], token[1])])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id

        Usage: destroy <Class_name> <Class_id>
        """
        token = HBNBCommand.parseLine(line)
        obj_dic = storage.all()
        if token == []:
            print("** class name missing **")
        elif token[0] not in classes.keys():
            print("** class doesn't exist **")
        elif len(token) == 1:
            print("** instance id missing **")
        elif f"{token[0]}.{token[1]}" not in obj_dic:
            print("** no instance found **")
        else:
            dest_cls = f"{token[0]}.{token[1]}"
            for key in obj_dic.keys():
                if dest_cls == key:
                    break
            del obj_dic[dest_cls]
            storage.save()

    def do_all(self, line):
        """do_all.
            Prints all string representation of all\
instances based or not on the class name

        Usage: all <Class_name(optional)>
        """
        all_dic = []
        obj_dic = storage.all()
        token = HBNBCommand.parseLine(line)
        if len(token) > 0 and token[0] not in classes.keys():
            print("** class doesn't exist **")
        elif len(token) > 0 and token[0] in classes.keys():
            for obj in obj_dic.values():
                if token[0] == obj.__class__.__name__:
                    all_dic.append(obj.__str__())
            print(all_dic)
        else:
            for obj in obj_dic.values():
                all_dic.append(obj.__str__())
            print(all_dic)

    def do_update(self, line):
        """Updates an instance based on the class name and id

        Usage: Update <Class_name> <Class_id> <attribute> <value>
        """
        obj_dic = storage.all()
        if "{" not in line:
            token = HBNBCommand.parseLine(line)
            if token == []:
                print("** class name missing **")
            elif token[0] not in classes.keys():
                print("** class doesn't exist **")
            elif len(token) == 1:
                print("** instance id missing **")
            elif f"{token[0]}.{token[1]}" not in obj_dic:
                print("** no instance found **")
            elif len(token) == 2:
                print("** attribute name missing **")
            elif len(token) == 3:
                print("** value missing **")
            else:
                update_dic = obj_dic["{}.{}".format(token[0], token[1])]
                if token[2] in update_dic.__dict__:
                    attrtype = type(update_dic.__dict__[token[2]])
                    setattr(update_dic, token[2], attrtype(token[3]))
                else:
                    setattr(update_dic, token[2], token[3])
                storage.save()
        else:
            cls_name = re.findall(r"^(\w+)", line)
            cls_id = re.findall(r"\s+['\"]?((\w+-){4}\w+)['\"]?", line)
            cls_dic_raw = re.findall(r"({.*})", line)
            cls_dic = cls_dic_raw[0].replace("'", "\"")
            if not cls_name:
                print("** class name missing **")
            elif cls_name[0] not in classes.keys():
                print("** class doesn't exist **")
            elif cls_id == []:
                print("** instance id missing **")
            elif f"{cls_name[0]}.{cls_id[0][0]}" not in obj_dic:
                print("** no instance found **")
            else:
                update_dic = obj_dic["{}.{}".format(
                    cls_name[0], cls_id[0][0])]
                try:
                    add_dic = json.loads(cls_dic)
                except json.JSONDecodeError:
                    print("** invalid syntax")
                    return
                for add_key, add_value in add_dic.items():
                    if add_key in update_dic.__dict__:
                        attrtype = type(update_dic.__dict__[add_key])
                        setattr(update_dic, add_key, attrtype(add_value))
                    else:
                        setattr(update_dic, add_key, add_value)
                storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
