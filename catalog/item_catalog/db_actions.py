#!/usr/bin/env python
"""Database actions module."""
from item_catalog import app
from item_catalog import models
import os

# Category management


def all_category_infomation():
    """Return all rows of the categories table."""
    category = models.Category
    categories = models.DB.session.query(category).order_by(category.name).all(
    )
    return categories


def category_by_name(cat_name):
    """Return information about a category with a matching <cat_name>."""
    cat_db = models.Category
    category = models.DB.session.query(cat_db).filter(cat_db.name ==
                                                      cat_name).one()
    return category


def create_new_category(category_name):
    """Create a new category <category_name>.

    Returns True on success.
    """
    try:
        new_category = models.Category(name=category_name)
        models.DB.session.add(new_category)
        models.DB.session.commit()
    except Exception:
        return False
    return True


def edit_category(category_name):
    """Edit category <category_name>.

    Returns True on success.
    """
    # TODO(Edit category db_action)
    pass


def delete_category(category_name):
    """Delete category <category_name>.

    Returns True on success.
    """
    # TODO(Delete category db_action)
    pass


# Item management


def all_items_in_category(category_id):
    """Return all items in a given category <category_id>."""
    item_db = models.CatalogItem
    items = models.DB.session.query(item_db).filter(item_db.category_id ==
                                                    category_id)
    return items


def item_by_name(item_name):
    """Return information about an item with a matching <item_name>."""
    item_db = models.CatalogItem
    item = models.DB.session.query(item_db).filter(item_db.name ==
                                                   item_name).one()
    return item


def recent_items(number=10):
    """Return interger <number> of the most recent items added."""
    items = models.CatalogItem
    recent = models.DB.session.query(items).order_by(items.id.desc()).limit(
        number)
    return recent


def create_new_item(item_name, item_description, item_price,
                    item_category, item_image=None):
    """Create a new item <item_name>.

    Returns True on success.
    """
    try:
        if item_image is None:
            item_image = 'img/default/placeholder.png'
            new_item = models.CatalogItem(name=item_name,
                                          description=item_description,
                                          price=item_price,
                                          image=item_image,
                                          category_id=item_category)
        models.DB.session.add(new_item)
        models.DB.session.commit()
    except Exception:
        return False
    return True


def edit_item(item_name, item_description, item_price, item_image,
              item_category):
    """Edit <item_name>.

    Returns True on success.
    """
    # TODO(Edit item DB action.)
    pass


def delete_item(item_name):
    """Delete <item_name>.

    Returns True on success.
    """
    # TODO(Delete item DB action.)
    pass

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
    item_category_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 5, 7]
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
                                     price=float(price),
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
