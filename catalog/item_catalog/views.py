#!/usr/bin/env python
"""Views for the item_catalog application."""

from flask import render_template
from item_catalog import app


@app.route('/')
def index():
    """Index page view."""
    return render_template('index.html')
