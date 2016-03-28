#!/usr/bin/env python
"""Instance specific configuration for item catalog."""

DEBUG = True  # Disable debugging by default
BCRYPT_LEVEL = 12  # Configuration for the Flask-Bcrypt extension
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Extra overhead
SQLALCHEMY_DATABASE_URI = 'sqlite:///item_catalog.db'  # Database location
UPLOAD_FOLDER = '/vagrant/catalog/item_catalog/uploads/'  # Uploaded storage
UPLOAD_URL_FOLDER = '/uploads/'  # URL that routes to uploaded storage
# Allowed file upload extensions
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SECRET_KEY = 'eb430c23-b1eb-4000-a1dd-2219869316b0'  # Production secret key
CLIENT_SECRET = 'instance/client_secret.json'  # Gconnect secret file
