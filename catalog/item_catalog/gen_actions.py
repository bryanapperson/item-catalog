#!/usr/bin/env python
"""General actions for the item_catalog application."""
from flask import make_response
from flask import render_template
from flask import request
from flask import session as login_session
from item_catalog import app
from item_catalog import db_actions
import json
import os
from werkzeug.contrib.atom import AtomFeed
from werkzeug.utils import secure_filename

# JSON API Functions


def jsonize(input_var):
    """Return pretty printed JSON version of <input_var>."""
    return json.dumps(input_var,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))


def json_single(resource, exists):
    """Return JSON response for single DB resource with serialize @property."""
    if not exists:
        response = make_response(jsonize('Resource does not exist.'), 404)
        response.headers['Content-Type'] = 'application/json'
        return response
    try:
        api_data = db_actions.serial_data(resource)
        if api_data == "Failed to serialize data.":
            res_code = 500
        else:
            res_code = 200
    except Exception:
        response = make_response(jsonize('Server error.'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(jsonize(api_data), res_code)
    response.headers['Content-Type'] = 'application/json'
    return response


def json_catalog():
    """Return JSON response with contents of entire catalog."""
    res_code = 200
    ser = db_actions.serial_data
    api_data = {}
    api_data['categories'] = {}
    catalog_dict = api_data['categories']
    categories = db_actions.all_category_infomation()
    for category in categories:
        catalog_dict[category.name] = ser(category)
        catalog_dict[category.name]['items'] = {}
        items = db_actions.all_items_in_category(category.id)
        for item in items:
            catalog_dict[category.name]['items'][item.name] = ser(item)
    response = make_response(jsonize(api_data), res_code)
    response.headers['Content-Type'] = 'application/json'
    return response

# ATOM feed functions


def recent_items_atom_feed():
    """Return the 15 most recently added items as an ATOM feed response."""
    feed = AtomFeed('Recent Items', feed_url=request.url, url=request.url_root)
    feed = db_actions.atom_items(feed, 15)
    return feed.get_response()

# General Functions


def check_category_exists(category_name):
    """Check if a category exists given a <category_name>."""
    try:
        category = db_actions.category_by_name(category_name)
    except Exception:
        return False, None
    return True, category


def check_item_exists(item_name):
    """Check if an item exists given an <item_name>."""
    try:
        item = db_actions.item_by_name(item_name)
    except Exception:
        return False, None
    return True, item


def check_cat_item_exists(category_name, item_name):
    """Check if an item named <item_name> exists within a category.

    This function determined this given a <category_name> and
    <item_name>.
    """
    cat_satus, category = check_category_exists(category_name)
    if cat_satus is False:
        return False, None, None
    item_status, item = check_item_exists(item_name)
    if item_status is False:
        return False, category, None
    if item.category_id == category.id:
        return True, category, item


def read_json(filename):
    """Read json file and return contents in a string."""
    with open(filename, 'r') as json_file:
        json_read = json.loads(json_file.read())
    return json_read


def is_auth():
    """Return false if user is not authorized/logged in."""
    if 'username' not in login_session:
        return False
    return True


def allowed_file(filename):
    """Check if filetype is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def upload_photo(request):
    """Handle uploaded file in a request with key product-photo.

    Return path where file was saved.
    """
    photo = request.files['product-photo']
    if photo and allowed_file(photo.filename):
        # Rename
        file_type = photo.filename.rsplit('.', 1)[1]
        filename = (request.form['name'] + '.' + file_type)
        filename = secure_filename(filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(save_path)
        url_path = os.path.join(app.config['UPLOAD_URL_FOLDER'], filename)
        return url_path
    else:
        return None


def return_404():
    """Generate 404 error page."""
    page = 'Oops... Error 404'
    categories = db_actions.all_category_infomation()
    return render_template('error.html',
                           categories=categories,
                           pagename=page,
                           logged_in=is_auth()), 404
