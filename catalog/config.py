#!/usr/bin/env python
"""This file can be used for configuration overrides.

Values specified here will override values set in the parent directory's
config.py.
"""

DEBUG = False  # Disable debugging by default
BCRYPT_LEVEL = 12  # Configuration for the Flask-Bcrypt extension
SQLALCHEMY_DATABASE_URI = 'sqlite://item_catalog.db'
