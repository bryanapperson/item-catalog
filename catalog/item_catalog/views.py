#!/usr/bin/env python
"""Views for the item_catalog application."""

from flask import render_template
from item_catalog import app
from item_catalog import db_actions


@app.route('/')
@app.route('/catalog/')
def index_page():
    """Index page view."""
    page = "Recently Added Items"
    categories = db_actions.all_category_infomation()
    recent_items = db_actions.recent_items(12)
    return render_template('index.html',
                           categories=categories,
                           page_items=recent_items,
                           pagename=page)


@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items')
def category_page(category_name):
    """Display items in <category_name> category."""
    # Setup initial values
    found = False
    num_items = 0
    categories = db_actions.all_category_infomation()
    # Handle categories that don't exist
    for category in categories:
        if category_name == category.name:
            found = True
    if found is False:
        page = 'Oops... Error 404'
        return render_template('error.html',
                               categories=categories,
                               pagename=page), 404
        pass
    # Found category, build variables for template
    page = 'Category: ' + category_name + ' (' + str(num_items) + ' items)'
    items = ''
    # Return page
    return render_template('index.html',
                           categories=categories,
                           page_items=items,
                           pagename=page)


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def item_page(category_name, item_name):
    """Display items in <category_name> category."""
    page = item_name
    items = ''
    categories = db_actions.all_category_infomation()
    return render_template('index.html',
                           categories=categories,
                           page_items=items,
                           pagename=page)


# General error handling

@app.errorhandler(404)
def page_not_found(e):
    """Handle general 404 not found with custom page."""
    page = 'Oops... Error 404'
    categories = db_actions.all_category_infomation()
    return render_template('error.html',
                           categories=categories,
                           pagename=page), 404
