#!/usr/bin/env python
"""Database actions module."""
from item_catalog import models


def all_category_infomation():
    """Return all rows of the categories table."""
    category = models.Category
    categories = models.DB.session.query(category).order_by(category.name)
    return categories


def recent_items(number=10):
    """Return interger <number> of the most recent items added."""
    items = models.CatalogItem
    recent = models.DB.session.query(items).order_by(items.id.
                                                     desc()).limit(number)
    return recent
