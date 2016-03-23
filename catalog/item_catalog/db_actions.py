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

# Begin sample data section


def sample_metadata():
    """Populate metadata table with sample rows."""
    pass


def sample_categories():
    """Sample category data."""
    # List of category names
    category_list = ['Soccer', 'Basketball', 'Baseball', 'Frisbee',
                     'Snowboarding', 'Rock Climbing', 'Foosball', 'Skating',
                     'Hockey']
    for category in category_list:
        categoryobj = models.Category(name=category)
        models.DB.session.add(categoryobj)
        models.DB.session.commit()


def sample_items():
    """Sample item data."""
    # Information for items
    price_list = ['18.99', '21.99', '6.99', '12.99', '499.99', '69.99',
                  '999.99', '199.99', '69.99', '129.99', '139.99', '9.99']
    item_category_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 2, 4, 8]
    item_name_list = ['Soccer Ball', 'Basketball', 'Baseball', 'Frisbee',
                      'Snowboard', 'Grappling Hook', 'Foosball Table',
                      'Ice Skates', 'Hockey Stick', 'Catcher\'s Mit',
                      'Clip in Boots', 'Hockey Puck']
    desc_list = ['desc', 'desc', 'desc', 'desc', 'desc', 'desc', 'desc',
                 'desc', 'desc', 'desc', 'desc', 'desc']
    # Let's be pythonic about populating items
    for price, category, name, desc in zip(price_list, item_category_list,
                                           item_name_list, desc_list):
        itemobj = models.CatalogItem(name=name,
                                     category_id=category,
                                     price=price,
                                     description=desc)
        models.DB.session.add(itemobj)
        models.DB.session.commit()


def sample_data():
    """Sample data for initial database population."""
    # Populate metadata
    sample_metadata()
    # Populate categories
    sample_categories()
    # Populate items
    sample_items()

# End sample data section


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
