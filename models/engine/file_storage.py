#!/usr/bin/python3
"""serializes instances to a JSON file and
    deserializes JSON file to instances
    """
import json as j
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """FileStorage: a way to store the objects created."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """all returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """new: sets in __objects the obj with key clsName.id.

        :param obj: the object
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """save: serializes __objects to the JSON file."""
        obj_dic = FileStorage.__objects
        all_obj = {obj: obj_dic[obj].to_dict() for obj in obj_dic.keys()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            j.dump(all_obj, f)

    def reload(self):
        """reload: Deserialize the JSON file\
__file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                obj_dic = j.load(f)
                for obj in obj_dic.values():
                    clsName = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(clsName)(**obj))
        except FileNotFoundError:
            return
