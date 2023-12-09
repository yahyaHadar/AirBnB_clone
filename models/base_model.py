#!/usr/env/python3
"""clase BaseModel"""

from datetime import datetime
import models
import uuid


class BaseModel:
    """class BaseModel
        Represent all the common functionalities of the classes in the project.
        """

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

            Args:
                *args (any): Unused.
                **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    self.__dict__[key] = datetime.strptime(
                        value, '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def __str__(self):
        """Return the print/str representation of the BaseModel instance.
            [<class name>] (<self.id>) <self.__dict__>"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the updated_at to the current time"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary of the BaseModel

            to represent the class name of the object
            the key/value pair of __class__ is included"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
