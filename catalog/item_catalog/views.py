#!/usr/bin/env python
"""Views for the item_catalog application."""

from flask import render_template
from item_catalog import app
from item_catalog import db_actions


@app.route('/')
def index():
    """Index page view."""
    categories = db_actions.all_category_infomation()
    return render_template('index.html', categories=categories)
