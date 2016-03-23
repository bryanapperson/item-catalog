#!/usr/bin/env python
"""Views for the item_catalog application."""

from flask import render_template
from item_catalog import app
from item_catalog import db_actions


@app.route('/')
@app.route('/catalog/')
def index():
    """Index page view."""
    page = "Recently Added Items"
    categories = db_actions.all_category_infomation()
    recent_items = db_actions.recent_items(12)
    return render_template('index.html',
                           categories=categories,
                           page_items=recent_items,
                           pagename=page)


@app.route('/catalog/<string:category_name>/')
def category(category_name):
    """Display items in <category_name> category."""
    page = ''
    items = ''
    categories = db_actions.all_category_infomation()
    return render_template('index.html',
                           categories=categories,
                           page_items=items,
                           pagename=page)
