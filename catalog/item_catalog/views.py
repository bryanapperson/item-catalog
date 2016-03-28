#!/usr/bin/env python
"""Views for the item_catalog application."""

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_file
from flask import url_for
from item_catalog import app
from item_catalog import auth_manager
from item_catalog import db_actions
from item_catalog import gen_actions
import os
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
                           pagename=page,
                           logged_in=auth_manager.is_auth())

# Catalog management - not implemented


@app.route('/action/admin', methods=['GET', 'POST'])
def admin_page():
    """View for editing system wide settings."""
    # TODO(Catalog admin view)
    return gen_actions.return_404()


@app.route('/action/setup', methods=['GET', 'POST'])
def setup_page():
    """View for initial catalog setup."""
    if db_actions.is_setup() is False:
        # Make sure the one user is logged in
        if not auth_manager.is_auth():
            flash('You must login to access this page.', category="primary")
            return redirect(url_for('login_register'))
        user_id = auth_manager.get_session_user_id()
        # Handle POST request
        if request.method == 'POST':
            # Check CSRF token
            auth_manager.check_csrf_token(request)
            # Handle sample data
            if request.form['setup'] == 'Load Sample Data':
                # Make sure this user becomes admin
                db_actions.user_to_admin(user_id)
                # Load sample data
                db_actions.sample_data(user_id)
                # Disable setup page
                db_actions.disable_setup()
                flash('Setup and sample data install complete.',
                      category="primary")
                return redirect(url_for('index_page'))
            # Handle skip sample data
            if request.form['setup'] == 'Skip Sample Data':
                # Make sure this user becomes admin
                db_actions.user_to_admin(user_id)
                # Disable setup page
                db_actions.disable_setup()
                flash('Setup complete.', category="primary")
                return redirect(url_for('index_page'))
        # Handle GET request
        else:
            categories = db_actions.all_category_infomation()
            pagename = "Item Catalog Setup"
            return render_template('setup.html',
                                   categories=categories,
                                   pagename=pagename,
                                   logged_in=auth_manager.is_auth())
    else:
        return gen_actions.return_404()

# Category management


@app.route('/catalog/<string:category_name>/')
def category_page(category_name):
    """Display items in <category_name> category."""
    # Handle categories that don't exist
    exists, category_info = gen_actions.check_category_exists(category_name)
    if not exists:
        return gen_actions.return_404()
    # Setup initial values
    i_str = ' items)'
    num_items = db_actions.cat_item_count(category_name)
    if num_items == 1:
        i_str = ' item)'
    categories = db_actions.all_category_infomation()
    # Found category, build variables for template
    page = 'Category: ' + category_name + ' (' + str(num_items) + i_str
    items = db_actions.all_items_in_category(category_info.id)
    # Return page
    return render_template('index.html',
                           categories=categories,
                           category_info=category_info,
                           page_items=items,
                           pagename=page,
                           logged_in=auth_manager.is_auth(),
                           cat_auth=auth_manager.auth_category(category_info))


@app.route('/action/catalog/new_category/', methods=['GET', 'POST'])
def new_category():
    """Dialog for adding a new category to the catalog."""
    # Redirect if not logged in
    # Check if user is logged in
    if not auth_manager.is_auth():
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Handle POST for new_category
    if request.method == 'POST':
        # Check CSRF token
        auth_manager.check_csrf_token(request)
        cat_name = request.form['name']
        # Check if the proposed category exists
        check = gen_actions.check_category_exists(cat_name)
        exists, cat = check
        if exists:
            # This category already exists
            flash('Failed to create new category. ' +
                  'This category name already exists. ' +
                  'Try a different name.',
                  category='alert')
            return redirect(url_for('new_category'))
        # Proposed category does not exist, proceed.
        new = db_actions.create_new_category(cat_name, user_id)
        # Did we successfully create the new category?
        if new:
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
                               pagename=pagename,
                               logged_in=auth_manager.is_auth())


@app.route('/action/catalog/<string:category_name>/edit_category/',
           methods=['GET', 'POST'])
def edit_category(category_name):
    """Dialog for adding a new item to the catalog."""
    # Check if category exists otherwise return 404
    exists, category_info = gen_actions.check_category_exists(category_name)
    if not exists:
        return gen_actions.return_404()
    # Redirect if not logged in
    if not auth_manager.is_auth():
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    if not auth_manager.auth_category(category_info):
        flash('You are not authorized to edit this category.',
              category="alert")
        return redirect(url_for('category_page', category_name=category_name))
    # Handle POST for edit_category
    if request.method == 'POST':
        # Check CSRF token
        auth_manager.check_csrf_token(request)
        cat_name = request.form['name']
        # Check if the proposed category exists
        check = gen_actions.check_category_exists(cat_name)
        exists, cat = check
        if exists and category_name != cat_name:
            # This category already exists
            flash('Failed to edit category. ' +
                  'The proposed category name already exists. ' +
                  'Try a different name.',
                  category='alert')
            return redirect(url_for('edit_category',
                                    category_name=category_name))
        # Proposed category does not exist, proceed.
        new = db_actions.edit_category(category_info.name, cat_name)
        if new:
            flash('Category entry edited.', category="success")
            return redirect(url_for('category_page', category_name=cat_name))
        else:
            # Failure reason unknown
            flash('Failed to edit category.', category='alert')
            return redirect(url_for('edit_category',
                                    category_name=category_name))
    # Handle GET request
    else:
        cat = category_info
        categories = db_actions.all_category_infomation()
        pagename = ("Update Category: " + category_info.name)
        return render_template('edit_category.html',
                               pagename=pagename,
                               categories=categories,
                               category=category_info,
                               logged_in=auth_manager.is_auth(),
                               cat_auth=auth_manager.auth_category(cat))


@app.route('/action/catalog/<string:category_name>/delete_category/',
           methods=['GET', 'POST'])
def delete_category(category_name):
    """Dialog for deleteing a category from the catalog."""
    # Check if category exists otherwise return 404
    exists, category_info = gen_actions.check_category_exists(category_name)
    if not exists:
        return gen_actions.return_404()
    # Redirect if not logged in
    if not auth_manager.is_auth():
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Is the user authorized?
    if user_id != category_info.user_id:
        flash('You are not authorized to delete this category.',
              category="alert")
        return redirect(url_for('category_page', category_name=category_name))
    # Handle POST request
    if request.method == 'POST':
        # Check CSRF token
        auth_manager.check_csrf_token(request)
        # Handle deletion
        if request.form['delete'] == 'Delete Category and Items':
            if db_actions.delete_category(category_name):
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
        cat = category_info
        categories = db_actions.all_category_infomation()
        pagename = ("Delete Category: " + category_name)
        return render_template('delete_category.html',
                               categories=categories,
                               category=category_info,
                               pagename=pagename,
                               logged_in=auth_manager.is_auth(),
                               cat_auth=auth_manager.auth_category(cat))

# Item management


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def item_page(category_name, item_name):
    """Display information about a given <item_name> in <category_name>."""
    categories = db_actions.all_category_infomation()
    # If the item is not in the category or the category does not exist
    # Return 404.
    exists, category, item = gen_actions.check_cat_item_exists(category_name,
                                                               item_name)
    if not exists:
        return gen_actions.return_404()
    # The item and category exist, build the page.
    page = item_name
    return render_template('item.html',
                           categories=categories,
                           category_info=category,
                           page_item=item,
                           pagename=page,
                           cat_auth=auth_manager.auth_category(category),
                           item_auth=auth_manager.auth_item(item),
                           logged_in=auth_manager.is_auth())


@app.route('/action/catalog/new_item/', methods=['GET', 'POST'])
def new_item():
    """Dialog for adding a new item to a given <category_name>."""
    # Redirect if not logged in
    if not auth_manager.is_auth():
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Get user id
    user_id = auth_manager.get_session_user_id()
    # Manage post request for new_item
    if request.method == 'POST':
        # Check CSRF token
        auth_manager.check_csrf_token(request)
        item_name = request.form['name']
        item_description = request.form['description']
        item_price = request.form['price']
        category_name = request.form['category']
        user_id = auth_manager.get_session_user_id()
        # Check if the proposed item name already exists
        check = gen_actions.check_item_exists(item_name)
        exists, new_item = check
        if exists:
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
        # Handle photo upload
        if 'product-photo' in request.files:
            item_image = gen_actions.upload_photo(request)
        new = db_actions.create_new_item(item_name,
                                         item_description,
                                         item_price,
                                         cat_id,
                                         user_id=user_id,
                                         item_image=item_image)
        if new:
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
                               pagename=pagename,
                               logged_in=auth_manager.is_auth())


@app.route('/action/catalog/<string:category_name>/<string:item_name>/'
           'edit_item/',
           methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    """Dialog for editing an item in the catalog."""
    # If the item is not in the category or the category does not exist
    # Return 404.
    exists, category, item = gen_actions.check_cat_item_exists(category_name,
                                                               item_name)
    if not exists:
        return gen_actions.return_404()
    # Redirect if not logged in
    if not auth_manager.is_auth():
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Is the user authorized?
    if not auth_manager.auth_item(item):
        flash('You are not authorized to edit this item.', category="alert")
        return redirect(url_for('item_page',
                                category_name=category_name,
                                item_name=item_name))
    # Handle POST request for edit_item
    if request.method == 'POST':
        # Check CSRF token
        auth_manager.check_csrf_token(request)
        new_item_name = request.form['name']
        item_description = request.form['description']
        item_price = request.form['price']
        new_category_name = request.form['category']
        # Check if the proposed item name already exists
        check = gen_actions.check_item_exists(new_item_name)
        exists, new_item = check
        if exists and new_item_name != item_name:
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
        # Handle photo upload
        if 'product-photo' in request.files:
            item_image = gen_actions.upload_photo(request)
        new = db_actions.edit_item(item_name, new_item_name, item_description,
                                   item_price, cat_id, item_image)
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
                               category_info=category,
                               item=item,
                               pagename=pagename,
                               logged_in=auth_manager.is_auth(),
                               item_auth=auth_manager.auth_item(item),
                               cat_auth=auth_manager.auth_category(category))


@app.route('/action/catalog/<string:category_name>/<string:item_name>/'
           'delete_item/',
           methods=['GET', 'POST'])
def delete_item(category_name, item_name):
    """Dialog for deleteing an item from the catalog."""
    # If the item is not in the category or the category does not exist
    # Return 404.
    exists, category, item = gen_actions.check_cat_item_exists(category_name,
                                                               item_name)
    if not exists:
        return gen_actions.return_404()
    # Redirect if not logged in
    if not auth_manager.is_auth():
        flash('You must login to access this page.', category="primary")
        return redirect(url_for('login_register'))
    # Redirect and flash if user is not authorized to alter this item
    if not auth_manager.auth_item(item):
        flash('You are not authorized to delete this item.', category="alert")
        return redirect(url_for('item_page',
                                category_name=category_name,
                                item_name=item_name))
    # Handle POST request for delete_item
    if request.method == 'POST':
        # Check CSRF token
        auth_manager.check_csrf_token(request)
        # Handle deletion
        # TODO(Handle item image deletion)
        if request.form['delete'] == 'Delete Item':
            if db_actions.delete_item(item_name):
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
                               category_info=category,
                               page_item=item,
                               pagename=pagename,
                               logged_in=auth_manager.is_auth(),
                               item_auth=auth_manager.auth_item(item),
                               cat_auth=auth_manager.auth_category(category))

# User Authentication


@app.route('/login', methods=['GET', 'POST'])
def login_register():
    """Dialog for registering or logging in."""
    # TODO(login or register view)
    # Redirect if logged in
    if auth_manager.is_auth():
        flash('You are already logged in.', category="primary")
        return redirect(url_for('logout'))
    pagename = "Login or Register"
    state = auth_manager.set_login_state()
    categories = db_actions.all_category_infomation()
    # Redirect to setup page if setup is not complete
    if db_actions.is_setup() is False:
        redirect_page = url_for('setup_page')
    else:
        redirect_page = url_for('index_page')
    return render_template('login.html',
                           categories=categories,
                           pagename=pagename,
                           state=urllib.quote(state.encode("utf-8")),
                           redirect_page=redirect_page,
                           logged_in=auth_manager.is_auth())


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """Dialog for logging out."""
    # Redirect if not logged in
    if not auth_manager.is_auth():
        flash('You are not logged in.', category="primary")
        return redirect(url_for('login_register'))
    pagename = "Logout"
    state = auth_manager.set_login_state()
    categories = db_actions.all_category_infomation()
    if request.method == 'POST':
        # Check CSRF token
        auth_manager.check_csrf_token(request)
        # TODO(Handle item image deletion)
        if request.form['logout'] == 'Logout':
            result = auth_manager.logout_action()
            flash(result, category="primary")
            return redirect(url_for('index_page'))
    return render_template('logout.html',
                           categories=categories,
                           pagename=pagename,
                           state=urllib.quote(state.encode("utf-8")),
                           logged_in=auth_manager.is_auth())


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
def item_json(category_name, item_name):
    """JSON API for single item."""
    # If the item is not in the category or the category does not exist
    # Return 404.
    exists, category, item = gen_actions.check_cat_item_exists(category_name,
                                                               item_name)
    return gen_actions.json_single(item, exists)


@app.route('/api/json/catalog/<string:category_name>/')
def category_json(category_name):
    """JSON API for single category."""
    # Check if category exists otherwise return 404
    exists, category_info = gen_actions.check_category_exists(category_name)
    return gen_actions.json_single(category_info, exists)


@app.route('/api/json/catalog/')
def catalog_json():
    """JSON API for entire catalog."""
    return gen_actions.json_catalog()

# Atom feeds


@app.route('/feed/atom/catalog/recent')
def recent_atom():
    """ATOM feed for recent items."""
    return gen_actions.recent_items_atom_feed()

# Static asset serving


@app.route(app.config['UPLOAD_URL_FOLDER'] + '<filename>')
def uploaded_photo(filename):
    # TODO(Test photo uploading and implement)
    """Serve uploaded photos."""

    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

# General error handling


@app.errorhandler(404)
def page_not_found(e):
    """Handle general 404 not found with custom page."""
    return gen_actions.return_404()
