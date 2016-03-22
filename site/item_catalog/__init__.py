#!/usr/bin/env python

"""An item catalog website module.

This item catalog website module provides a list of items within a
variety of categories as well as a user registration and
authentication system. Registered users have the ability to post,
edit and delete their own items.
"""

from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


from item_catalog import models
from item_catalog import views

# Now we can access the configuration variables via app.config["VAR_NAME"].
