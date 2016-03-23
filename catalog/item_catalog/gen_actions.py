#!/usr/bin/env python
"""General actions for the item_catalog application."""
from item_catalog import db_actions


def check_category_exists(category_name):
    """Check if a category exists given a <category_name>."""
    try:
        db_actions.category_by_name(category_name)
    except Exception:
        return False
    return True


def check_item_exits(item_name):
    """Check if an item exists given an <item_name>."""
    try:
        db_actions.item_by_name(item_name)
    except Exception:
        return False
    return True


def check_cat_item_exists(category_name, item_name):
    """Check if an item named <item_name> exists within a category.

    This function determined this given a <category_name> and
    <item_name>.
    """
    if check_category_exists(category_name) is False:
        return False
    if check_item_exits(item_name) is False:
        return False
    category = db_actions.category_by_name(category_name)
    item = db_actions.item_by_name(item_name)
    if item.category_id == category.id:
        return True
