#!/usr/bin/env python
"""Default configuration for item catalog."""

DEBUG = False  # Disable debugging by default
BCRYPT_LEVEL = 12  # Configuration for the Flask-Bcrypt extension
SQLALCHEMY_DATABASE_URI = 'sqlite://item_catalog.db'
