#!/usr/bin/env python
"""This file can be used for configuration overrides.

Values specified here will override values set in the parent directory's
config.py.
"""

DEBUG = False  # Disable debugging by default
BCRYPT_LEVEL = 12  # Configuration for the Flask-Bcrypt extension
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Extra overhead
SQLALCHEMY_DATABASE_URI = 'sqlite:///item_catalog.db'  # Database location
UPLOAD_FOLDER = '/vagrant/catalog/item_catalog/uploads/'  # Uploaded storage
UPLOAD_URL_FOLDER = '/uploads/'  # URL that routes to uploaded storage
# Allowed file upload extensions
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SECRET_KEY = '179bd114-2af8-45df-b657-65671d318ef3'  # Sample app secret key
CLIENT_SECRET = 'instance/client_secret.json'  # Gconnect secret file
