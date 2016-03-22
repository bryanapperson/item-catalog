#!/usr/bin/env python
"""Instance specific configuration for item catalog."""

DEBUG = True  # Turns on debugging features in Flask
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
