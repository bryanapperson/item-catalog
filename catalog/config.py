#!/usr/bin/env python
"""This file can be used for configuration overrides.

Values specified here will override values set in the parent directory's
config.py.
"""

DEBUG = False  # Disable debugging by default
BCRYPT_LEVEL = 12  # Configuration for the Flask-Bcrypt extension
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Extra overhead
SQLALCHEMY_DATABASE_URI = 'sqlite:///item_catalog.db'  # Database location
UPLOADED_PHOTOS_DEST = 'uploads/'  # Uploaded photos storage
UPLOADED_PHOTOS_URL = 'photos/'  # Uploaded photos serving URL
SECRET_KEY = '179bd114-2af8-45df-b657-65671d318ef3'  # Sample app secret key
CLIENT_SECRET = 'instance/client_secret.json'  # Gconnect secret file
