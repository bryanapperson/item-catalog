#!/usr/bin/env python
"""General actions for the item_catalog application."""
from flask import render_template
from item_catalog import db_actions


def check_category_exists(category_name):
    """Check if a category exists given a <category_name>."""
    try:
        category = db_actions.category_by_name(category_name)
    except Exception:
        return False, None
    return True, category


def check_item_exits(item_name):
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
    item_status, item = check_item_exits(item_name)
    if item_status is False:
        return False, category, None
    if item.category_id == category.id:
        return True, category, item


def return_404():
    """Generate 404 error page."""
    page = 'Oops... Error 404'
    categories = db_actions.all_category_infomation()
    return render_template('error.html',
                           categories=categories,
                           pagename=page), 404
