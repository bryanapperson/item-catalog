#!/usr/bin/env python
"""Instance specific configuration for item catalog."""

DEBUG = True  # Turns on debugging features in Flask
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Extra overhead
SQLALCHEMY_DATABASE_URI = 'sqlite:///item_catalog.db'
