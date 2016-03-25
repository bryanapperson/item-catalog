#!/usr/bin/env python
"""An item catalog website module.

This item catalog website module provides a list of items within a
variety of categories as well as a user registration and
authentication system. Registered users have the ability to post,
edit and delete their own items.
"""

from flask import Flask
from flask_uploads import patch_request_class

# Instantiate Flask application object with relative configuration
app = Flask(__name__, instance_relative_config=True)
# Load default configuration
app.config.from_object('config')
# Load overrides for local instance
app.config.from_pyfile('instance_configuration.py')
# Set maximum upload size to 16MB
patch_request_class(app)
# Now we can access the configuration variables via app.config["VAR_NAME"].

# Relative, circular imports needed after object creation due
# to Flask application structure.

from item_catalog import db_actions
from item_catalog import gen_actions
from item_catalog import models
from item_catalog import views
