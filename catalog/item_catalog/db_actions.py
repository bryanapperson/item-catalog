#!/usr/bin/env python
"""Database actions module."""
from item_catalog import models
from item_catalog import app
import os


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


def sample_data():
    """Sample data for initial database population."""
    pass


def model_population():
    """Populate the DB if it is SQLite and does not exist."""
    db_string = app.config['SQLALCHEMY_DATABASE_URI']
    if 'sqlite:' in db_string:
        db_string = db_string.split('/')[-1]
        db_string = os.getcwd() + '/item_catalog/' + db_string
        if not os.path.isfile(db_string):
            models.create_db()
            print ("Creating DB.")


# Call DB population check
model_population()
