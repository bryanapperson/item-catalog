#!/usr/bin/env python
"""Views for the item_catalog application."""

from flask import render_template
from item_catalog import app
from item_catalog import db_actions
from item_catalog import gen_actions


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
    num_items = 0
    categories = db_actions.all_category_infomation()
    # Handle categories that don't exist
    exists, category_info = gen_actions.check_category_exists(category_name)
    if exists is False:
        return gen_actions.return_404()
    # Found category, build variables for template
    # TODO(Correctly count number of items)
    page = 'Category: ' + category_name + ' (' + str(num_items) + ' items)'
    items = db_actions.all_items_in_category(category_info.id)
    # Return page
    return render_template('index.html',
                           categories=categories,
                           category_info=category_info,
                           page_items=items,
                           pagename=page)


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    """View for editing system wide settings."""
    # TODO(Catalog admin view)
    pass


@app.route('/catalog/new', methods=['GET', 'POST'])
def new_category():
    """Dialog for adding a new category to the catalog."""
    # TODO(Add new category view)
    pass


@app.route('/catalog/<string:category_name>/edit', methods=['GET', 'POST'])
def edit_category():
    """Dialog for adding a new item to the catalog."""
    # TODO(Edit category view)
    pass


@app.route('/catalog/<string:category_name>/delete',
           methods=['GET', 'POST'])
def delete_category():
    """Dialog for deleteing a category from the catalog."""
    # TODO(delete category view)
    pass


@app.route('/catalog/<string:category_name>/new')
def new_item(category_name):
    """Dialog for adding a new item to a given <category_name>."""
    # TODO(Add new item view)
    pass


@app.route('/catalog/<string:category_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def edit_item():
    """Dialog for editing an item in the catalog."""
    # TODO(Edit item view)
    pass


@app.route('/catalog/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def delete_item():
    """Dialog for deleteing an item from the catalog."""
    # TODO(delete item view)
    pass


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def item_page(category_name, item_name):
    """Display information about a given <item_name> in <category_name>."""
    categories = db_actions.all_category_infomation()
    # If the item is not in the category or the category does not exist
    # Return 404.
    exists, category, item = gen_actions.check_cat_item_exists(category_name,
                                                               item_name)
    if exists is False:
        return gen_actions.return_404()
    # The item and category exist, build the page.
    page = item_name
    return render_template('item.html',
                           categories=categories,
                           category_info=category,
                           page_item=item,
                           pagename=page)

# General error handling


@app.errorhandler(404)
def page_not_found(e):
    """Handle general 404 not found with custom page."""
    return gen_actions.return_404()
