#!/usr/bin/python3
"""__init__ magic method for models directory"""
from models.engine.file_storage import FileStorage as FS


storage = FS()
storage.reload()
