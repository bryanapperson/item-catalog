#!/usr/bin/env python
"""Database actions module."""
from item_catalog import app
from item_catalog import models
import os


def all_category_infomation():
    """Return all rows of the categories table."""
    category = models.Category
    categories = models.DB.session.query(category).order_by(category.name).all(
    )
    return categories


def recent_items(number=10):
    """Return interger <number> of the most recent items added."""
    items = models.CatalogItem
    recent = models.DB.session.query(items).order_by(items.id.desc()).limit(
        number)
    return recent


def sample_data():
    """Sample data for initial database population."""
    category_list = ['Soccer', 'Basketball', 'Baseball', 'Frisbee',
                     'Snowboarding', 'Rock Climbing', 'Foosball', 'Skating',
                     'Hockey']
    price_list = ['4.99', '5.99', '49.99', '59.99', '4.99', '5.99', '49.99',
                  '59.99', '4.99', '5.99', '49.99', '59.99']
    item_category_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    item_name_list = ['thing1', 'thing1', 'thing1', 'thing1', 'thing1',
                      'thing1', 'thing1', 'thing1', 'thing1', 'thing1',
                      'thing1', 'thing1']
    desc_list = ['desc', 'desc', 'desc', 'desc', 'desc', 'desc', 'desc',
                 'desc', 'desc', 'desc', 'desc', 'desc']
    for price, category, name, desc in zip(price_list,
                                           item_category_list,
                                           item_name_list,
                                           desc_list):
        itemobj = models.CatalogItem(name=name,
                                     category_id=category,
                                     price=price,
                                     description=desc)
        models.DB.session.add(itemobj)
        models.DB.session.commit()
    for category in category_list:
        categoryobj = models.Category(name=category)
        models.DB.session.add(categoryobj)
        models.DB.session.commit()


def create_db():
    """Create the initial database."""
    models.DB.create_all()


def model_population():
    """Populate the DB if it is SQLite and does not exist."""
    db_string = app.config['SQLALCHEMY_DATABASE_URI']
    if 'sqlite:' in db_string:
        db_string = db_string.split('/')[-1]
        db_string = os.getcwd() + '/item_catalog/' + db_string
        if not os.path.isfile(db_string):
            print("Creating DB.")
            create_db()
            print("DB Created.")
            print("Populating sample data.")
            sample_data()
            print("Populated sample data.")

# Call DB population check
model_population()
