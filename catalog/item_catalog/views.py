#!/usr/bin/env python
"""Views for the item_catalog application."""

from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from item_catalog import app
from item_catalog import db_actions
from item_catalog import gen_actions

# Home/Catalog main page


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

# Catalog management - not implemented


@app.route('/action/admin', methods=['GET', 'POST'])
def admin_page():
    """View for editing system wide settings."""
    # TODO(Catalog admin view)
    return gen_actions.return_404()

# Category management


@app.route('/catalog/<string:category_name>/')
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


@app.route('/action/catalog/new_category/', methods=['GET', 'POST'])
def new_category():
    """Dialog for adding a new category to the catalog."""
    categories = db_actions.all_category_infomation()
    pagename = "Create A New Category"
    if request.method == 'POST':
        cat_name = request.form['name']
        new = db_actions.create_new_category(cat_name)
        if new is True:
            return redirect(url_for('category_page', category_name=cat_name))
    return render_template('new_category.html',
                           categories=categories,
                           pagename=pagename)


@app.route('/action/catalog/<string:category_name>/edit_category/',
           methods=['GET', 'POST'])
def edit_category(category_name):
    """Dialog for adding a new item to the catalog."""
    categories = db_actions.all_category_infomation()
    exists, category_info = gen_actions.check_category_exists(category_name)
    if exists is False:
        return gen_actions.return_404()
    pagename = ("Update Category: " + category_info.name)
    if request.method == 'POST':
        cat_name = request.form['name']
        new = db_actions.edit_category(category_info.name, cat_name)
        if new is True:
            return redirect(url_for('category_page', category_name=cat_name))
    return render_template('edit_category.html',
                           pagename=pagename,
                           categories=categories,
                           category=category_info)


@app.route('/action/catalog/<string:category_name>/delete_category/',
           methods=['GET', 'POST'])
def delete_category():
    """Dialog for deleteing a category from the catalog."""
    # TODO(delete category view)
    return gen_actions.return_404()

# Item management


@app.route('/action/catalog/new_item/',
           methods=['GET', 'POST'])
def new_item():
    """Dialog for adding a new item to a given <category_name>."""
    categories = db_actions.all_category_infomation()
    pagename = "Create A New Item"
    # Manage post request for new_item
    if request.method == 'POST':
        item_name = request.form['name']
        item_description = request.form['description']
        item_price = request.form['price']
        category_name = request.form['category']
        # TODO(Manage product photo item_image)
        cat = db_actions.category_by_name(category_name)
        cat_id = cat.id
        new = db_actions.create_new_item(item_name, item_description,
                                         item_price, cat_id)
        if new is True:
            return redirect(url_for('item_page', category_name=category_name,
                                    item_name=item_name))
    return render_template('new_item.html',
                           categories=categories,
                           pagename=pagename)


@app.route('/action/catalog/<string:category_name>/<string:item_name>/'
           'edit_item/',
           methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    """Dialog for editing an item in the catalog."""
    # TODO(Edit item view)
    categories = db_actions.all_category_infomation()
    # If the item is not in the category or the category does not exist
    # Return 404.
    exists, category, item = gen_actions.check_cat_item_exists(category_name,
                                                               item_name)
    if exists is False:
        return gen_actions.return_404()
    pagename = ("Update Item: " + item.name)
    # Handle POST request for edit_item
    if request.method == 'POST':
        new_item_name = request.form['name']
        item_description = request.form['description']
        item_price = request.form['price']
        category_name = request.form['category']
        # TODO(Manage product photo item_image)
        cat = db_actions.category_by_name(category_name)
        cat_id = cat.id
        new = db_actions.edit_item(item_name, new_item_name, item_description,
                                   item_price, cat_id)
        if new is True:
            return redirect(url_for('item_page', category_name=category_name,
                                    item_name=new_item_name))
    return render_template('edit_item.html',
                           categories=categories,
                           category=category,
                           item=item,
                           pagename=pagename)


@app.route('/action/catalog/<string:category_name>/<string:item_name>/'
           'delete_item/',
           methods=['GET', 'POST'])
def delete_item():
    """Dialog for deleteing an item from the catalog."""
    # TODO(delete item view)
    return gen_actions.return_404()


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

# User Authentication


@app.route('/login', methods=['GET', 'POST'])
def login_register():
    """Dialog for registering or logging in."""
    # TODO(login or register view)
    return gen_actions.return_404()


@app.route('/logout')
def logout():
    """Dialog for logging out."""
    # TODO(log out sucessfully view)
    return gen_actions.return_404()

# JSON API


@app.route('/api/json/catalog/<string:category_name>/<string:item_name>/')
def item_json():
    """JSON API for single item."""
    # TODO(single item JSON API)
    return gen_actions.return_404()


@app.route('/api/json/catalog/<string:category_name>/')
def category_json():
    """JSON API for single category."""
    # TODO(single category JSON API)
    return gen_actions.return_404()


@app.route('/api/json/catalog/')
def catalog_json():
    """JSON API for entire catalog."""
    # TODO(entire catalog JSON API)
    return gen_actions.return_404()

# Atom feeds


@app.route('/api/atom/catalog/recent')
def recent_atom():
    """ATOM API/feed for recent items."""
    # TODO(ATOM API/feed for recent items)
    return gen_actions.return_404()


# Static asset serving


@app.route('/photos/<filename>')
def uploaded_photo(filename):
    """Server uploaded photos."""
    return send_from_directory(app.config['UPLOADED_PHOTOS_URL'],
                               filename)


# General error handling


@app.errorhandler(404)
def page_not_found(e):
    """Handle general 404 not found with custom page."""
    return gen_actions.return_404()
