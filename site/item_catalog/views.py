#!/usr/bin/env python

"""Views for the item_catalog application."""

from item_catalog import app


@app.route('/')
def index():
    """Index page view."""
    return 'Hello World!'
