#!/usr/bin/env python
"""Views for the item_catalog application."""

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for
from item_catalog import app
from item_catalog import auth_manager
from item_catalog import db_actions
from item_catalog import gen_actions
import urllib

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
    # Handle categories that don't exist
    exists, category_info = gen_actions.check_category_exists(category_name)
    if exists is False:
        return gen_actions.return_404()
    # Setup initial values
    num_items = 0
    categories = db_actions.all_category_infomation()
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
    # Redirect if not logged in
    if auth_manager.is_auth() is False:
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Handle POST for new_category
    if request.method == 'POST':
        cat_name = request.form['name']
        # Check if the proposed category exists
        check = gen_actions.check_category_exists(cat_name)
        exists, cat = check
        if exists is True:
            # This category already exists
            flash('Failed to create new category. ' +
                  'This category name already exists. ' +
                  'Try a different name.',
                  category='alert')
            return redirect(url_for('new_category'))
        # Proposed category does not exist, proceed.
        new = db_actions.create_new_category(cat_name, user_id)
        # Did we successfully create the new category?
        if new is True:
            flash('Category added to catalog.', category="success")
            return redirect(url_for('category_page', category_name=cat_name))
        else:
            # Failure reason is unknown
            flash('Failed to create new category.', category='alert')
            return redirect(url_for('new_category'))
    # Handle GET method
    else:
        categories = db_actions.all_category_infomation()
        pagename = "Create A New Category"
        return render_template('new_category.html',
                               categories=categories,
                               pagename=pagename)


@app.route('/action/catalog/<string:category_name>/edit_category/',
           methods=['GET', 'POST'])
def edit_category(category_name):
    """Dialog for adding a new item to the catalog."""
    # Check if category exists otherwise return 404
    exists, category_info = gen_actions.check_category_exists(category_name)
    if exists is False:
        return gen_actions.return_404()
    # Redirect if not logged in
    if auth_manager.is_auth() is False:
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Is the user authorized?
    if user_id != category_info.user_id:
        flash('You are not authorized to edit this category.',
              category="alert")
        return redirect(url_for('category_page',
                        category_name=category_name))
    # Handle POST for edit_category
    if request.method == 'POST':
        cat_name = request.form['name']
        # Check if the proposed category exists
        check = gen_actions.check_category_exists(cat_name)
        exists, cat = check
        if exists is True and category_name != cat_name:
            # This category already exists
            flash('Failed to edit category. ' +
                  'The proposed category name already exists. ' +
                  'Try a different name.',
                  category='alert')
            return redirect(url_for('edit_category',
                                    category_name=category_name))
        # Proposed category does not exist, proceed.
        new = db_actions.edit_category(category_info.name, cat_name)
        if new is True:
            flash('Category entry edited.', category="success")
            return redirect(url_for('category_page', category_name=cat_name))
        else:
            # Failure reason unknown
            flash('Failed to edit category.', category='alert')
            return redirect(url_for('edit_category',
                                    category_name=category_name))
    # Handle GET request
    else:
        categories = db_actions.all_category_infomation()
        pagename = ("Update Category: " + category_info.name)
        return render_template('edit_category.html',
                               pagename=pagename,
                               categories=categories,
                               category=category_info)


@app.route('/action/catalog/<string:category_name>/delete_category/',
           methods=['GET', 'POST'])
def delete_category(category_name):
    """Dialog for deleteing a category from the catalog."""
    # Check if category exists otherwise return 404
    exists, category_info = gen_actions.check_category_exists(category_name)
    if exists is False:
        return gen_actions.return_404()
    # Redirect if not logged in
    if auth_manager.is_auth() is False:
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Is the user authorized?
    if user_id != category_info.user_id:
        flash('You are not authorized to delete this category.',
              category="alert")
        return redirect(url_for('category_page',
                        category_name=category_name))
    # Handle POST request
    if request.method == 'POST':
        # Handle deletion
        if request.form['delete'] == 'Delete Category and Items':
            if db_actions.delete_category(category_name) is True:
                flash('Category deleted from catalog.', category="success")
                return redirect(url_for('index_page'))
            else:
                flash('Category deletion failed.', category="alert")
                return redirect(url_for('category_page',
                                        category_name=category_name))
        # Handle canceled deletion
        if request.form['delete'] == 'Cancel':
            flash('Category deletion canceled.', category="primary")
            return redirect(url_for('category_page',
                                    category_name=category_name))
    # Handle GET request
    else:
        categories = db_actions.all_category_infomation()
        pagename = ("Delete Category: " + category_name)
        return render_template('delete_category.html',
                               categories=categories,
                               category=category_info,
                               pagename=pagename)

# Item management


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


@app.route('/action/catalog/new_item/', methods=['GET', 'POST'])
def new_item():
    """Dialog for adding a new item to a given <category_name>."""
    # Redirect if not logged in
    if auth_manager.is_auth() is False:
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Manage post request for new_item
    if request.method == 'POST':
        item_name = request.form['name']
        item_description = request.form['description']
        item_price = request.form['price']
        category_name = request.form['category']
        user_id = auth_manager.get_session_user_id()
        # TODO(Manage product photo item_image)
        # Check if the proposed item name already exists
        check = gen_actions.check_item_exists(item_name)
        exists, new_item = check
        if exists is True:
            # Flash message on failure
            flash('Failed to create item. Another item with the same name ' +
                  'already exists. Please try another name.',
                  category='alert')
            return redirect(url_for('new_item'))
        # Proposed item does not exist, proceed.
        cat = db_actions.category_by_name(category_name)
        cat_id = cat.id
        # Check if user owns this category
        if user_id != cat.user_id:
            flash('You are not authorized add items to this category.',
                  category="alert")
            return redirect(url_for('category_page',
                            category_name=category_name))
        new = db_actions.create_new_item(item_name, item_description,
                                         item_price, cat_id, user_id=user_id)
        if new is True:
            flash('New item added to catalog.', category="success")
            return redirect(url_for('item_page',
                                    category_name=category_name,
                                    item_name=item_name))
        else:
            # Unknown failure reason
            # Flash message on failure
            flash('Failed to create new item.', category='alert')
            return redirect(url_for('new_item'))
    # Handle GET request
    else:
        categories = db_actions.all_category_infomation()
        pagename = "Create A New Item"
        # If there are no categories?
        if len(categories) == 0:
            # Flash message on failure
            flash('There are no categories, please create a category first.',
                  category='primary')
            return redirect(url_for('new_category'))
        return render_template('new_item.html',
                               categories=categories,
                               pagename=pagename)


@app.route('/action/catalog/<string:category_name>/<string:item_name>/'
           'edit_item/',
           methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    """Dialog for editing an item in the catalog."""
    # If the item is not in the category or the category does not exist
    # Return 404.
    exists, category, item = gen_actions.check_cat_item_exists(category_name,
                                                               item_name)
    if exists is False:
        return gen_actions.return_404()
    # Redirect if not logged in
    if auth_manager.is_auth() is False:
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Is the user authorized?
    if user_id != item.user_id:
        flash('You are not authorized to edit this item.', category="alert")
        return redirect(url_for('item_page',
                        category_name=category_name,
                        item_name=item_name))
    # Handle POST request for edit_item
    if request.method == 'POST':
        new_item_name = request.form['name']
        item_description = request.form['description']
        item_price = request.form['price']
        new_category_name = request.form['category']
        # TODO(Manage product photo item_image)
        # Check if the proposed item name already exists
        check = gen_actions.check_item_exists(new_item_name)
        exists, new_item = check
        if exists is True and new_item_name != item_name:
            # Flash message on failure
            flash('Failed to edit item. Another item with the same name ' +
                  'already exists. Please try another name.',
                  category='alert')
            return redirect(url_for('edit_item',
                                    category_name=category_name,
                                    item_name=item_name))
        # Proposed item name does not exist, proceed
        cat = db_actions.category_by_name(new_category_name)
        cat_id = cat.id
        new = db_actions.edit_item(item_name, new_item_name, item_description,
                                   item_price, cat_id)
        if new is True:
            flash('Item entry updated.', category="success")
            return redirect(url_for('item_page',
                                    category_name=category_name,
                                    item_name=new_item_name))
        else:
            # Unknown failure reason
            # Flash message on failure
            flash('Failed to edit item.', category='alert')
            return redirect(url_for('edit_item',
                                    category_name=category_name,
                                    item_name=item_name))
    # Handle GET request
    else:
        categories = db_actions.all_category_infomation()
        pagename = ("Update Item: " + item.name)
        return render_template('edit_item.html',
                               categories=categories,
                               category=category,
                               item=item,
                               pagename=pagename)


@app.route('/action/catalog/<string:category_name>/<string:item_name>/'
           'delete_item/',
           methods=['GET', 'POST'])
def delete_item(category_name, item_name):
    """Dialog for deleteing an item from the catalog."""
    # If the item is not in the category or the category does not exist
    # Return 404.
    exists, category, item = gen_actions.check_cat_item_exists(category_name,
                                                               item_name)
    if exists is False:
        return gen_actions.return_404()
    # Redirect if not logged in
    if auth_manager.is_auth() is False:
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Redirect and flash if user is not owner of this Item
    if user_id != item.user_id:
        flash('You are not authorized to delete this item.', category="alert")
        return redirect(url_for('item_page',
                        category_name=category_name,
                        item_name=item_name))
    # Handle POST request for delete_item
    if request.method == 'POST':
        # Handle deletion
        # TODO(Handle item image deletion)
        if request.form['delete'] == 'Delete Item':
            if db_actions.delete_item(item_name) is True:
                flash('Item deleted from catalog.', category="success")
                return redirect(url_for('category_page',
                                        category_name=category_name))
            else:
                flash('Item deletion failed.', category="alert")
                return redirect(url_for('item_page',
                                        category_name=category_name,
                                        item_name=item_name))
        # Handle canceled deletion
        if request.form['delete'] == 'Cancel':
            flash('Item deletion canceled.', category="primary")
            return redirect(url_for('item_page',
                                    category_name=category_name,
                                    item_name=item_name))
    # Handle GET request
    else:
        categories = db_actions.all_category_infomation()
        pagename = ("Delete Item: " + item.name)
        return render_template('delete_item.html',
                               categories=categories,
                               category=category,
                               page_item=item,
                               pagename=pagename)

# User Authentication


@app.route('/login', methods=['GET', 'POST'])
def login_register():
    """Dialog for registering or logging in."""
    # TODO(login or register view)
    # Redirect if logged in
    if auth_manager.is_auth() is True:
        flash('You are already logged in.', category="primary")
        return redirect(url_for('logout'))
    pagename = "Login or Register"
    state = auth_manager.set_login_state()
    categories = db_actions.all_category_infomation()
    return render_template('login.html',
                           categories=categories,
                           pagename=pagename,
                           state=urllib.quote(state.encode("utf-8")))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Dialog for logging out."""
    # TODO(log out sucessfully view)
    # Redirect if not logged in
    if auth_manager.is_auth() is False:
        flash('You are not logged in.', category="primary")
        return redirect(url_for('login_register'))
    pagename = "Logout"
    state = auth_manager.set_login_state()
    categories = db_actions.all_category_infomation()
    if request.method == 'POST':
        # Handle deletion
        # TODO(Handle item image deletion)
        if request.form['logout'] == 'Logout':
            result = auth_manager.logout_action()
            flash(result, category="primary")
            return redirect(url_for('index_page'))
    return render_template('logout.html',
                           categories=categories,
                           pagename=pagename,
                           state=urllib.quote(state.encode("utf-8")))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Handle gconnect login."""
    return auth_manager.gconnect(request)


@app.route('/gdisconnect')
def gdisconnect():
    """Handle gconnect login."""
    return auth_manager.gdisconnect()


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
    # TODO(Test photo uploading and implement)
    """Server uploaded photos."""
    return send_from_directory(app.config['UPLOADED_PHOTOS_URL'], filename)

# General error handling


@app.errorhandler(404)
def page_not_found(e):
    """Handle general 404 not found with custom page."""
    return gen_actions.return_404()
