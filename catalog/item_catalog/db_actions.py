#!/usr/bin/env python
"""Database actions module."""
import bleach
from item_catalog import app
from item_catalog import models
import os

# Category management


def all_category_infomation():
    """Return all rows of the categories table."""
    category = models.Category
    categories = models.DB.session.query(category).order_by(category.name).all(
    )
    models.DB.session.close()
    return categories


def category_by_name(cat_name):
    """Return information about a category with a matching <cat_name>."""
    cat_db = models.Category
    category = models.DB.session.query(cat_db).filter(cat_db.name ==
                                                      cat_name).one()
    models.DB.session.close()
    return category


def create_new_category(category_name):
    """Create a new category <category_name>.

    Returns True on success.
    """
    try:
        category_by_name(category_name)
        return False
    except Exception:
        pass
    try:
        new_category = models.Category(name=bleach.clean(category_name))
        models.DB.session.add(new_category)
        models.DB.session.commit()
        models.DB.session.close()
    except Exception:
        return False
    return True


def edit_category(category_old_name, category_new_name):
    """Edit category <category_old_name> to <category_new_name>.

    Returns True on success.
    """
    try:
        category = category_by_name(category_old_name)
        category.name = bleach.clean(category_new_name)
        models.DB.session.add(category)
        models.DB.session.commit()
        models.DB.session.close()
    except Exception:
        return False
    return True


def delete_category(category_name):
    """Delete category <category_name>.

    Returns True on success.
    """
    try:
        category = category_by_name(category_name)
        all_items = all_items_in_category(category.id).all()
        for item in all_items:
            models.DB.session.delete(item)
        models.DB.session.delete(category)
        models.DB.session.commit()
        models.DB.session.close()
    except Exception:
        return False
    return True

# Item management


def all_items_in_category(category_id):
    """Return all items in a given category <category_id>."""
    item_db = models.CatalogItem
    items = models.DB.session.query(item_db).filter(item_db.category_id ==
                                                    category_id)
    models.DB.session.close()
    return items


def item_by_name(item_name):
    """Return information about an item with a matching <item_name>."""
    item_db = models.CatalogItem
    item = models.DB.session.query(item_db).filter(item_db.name ==
                                                   item_name).one()
    models.DB.session.close()
    return item


def recent_items(number=10):
    """Return interger <number> of the most recent items added."""
    items = models.CatalogItem
    recent = models.DB.session.query(items).order_by(items.id.desc()).limit(
        number)
    models.DB.session.close()
    return recent


def create_new_item(item_name,
                    item_description,
                    item_price,
                    item_category,
                    item_image=None):
    """Create a new item <item_name>.

    Returns True on success.
    """
    try:
        b = bleach.clean
        item_image = None
        # TODO(Handle item image)
        if item_image is None:
            item_image = '/static/img/default/placeholder.png'
        new_item = models.CatalogItem(name=b(item_name),
                                      description=b(item_description),
                                      price=b(item_price),
                                      image=b(item_image),
                                      category_id=b(item_category))
        models.DB.session.add(new_item)
        models.DB.session.commit()
        models.DB.session.close()
    except Exception:
        return False
    return True


def edit_item(old_item_name,
              new_item_name,
              item_description,
              item_price,
              item_category,
              item_image=None):
    """Edit <item_name>.

    Returns True on success.
    """
    try:
        item = item_by_name(old_item_name)
        item_image = None
        # TODO(Handle item image)
        if item_image is None:
            item_image = '/static/img/default/placeholder.png'
        item.name = bleach.clean(new_item_name)
        item.description = bleach.clean(item_description)
        item.price = bleach.clean(item_price)
        item.image = bleach.clean(item_image)
        item.category_id = bleach.clean(item_category)
        models.DB.session.add(item)
        models.DB.session.commit()
        models.DB.session.close()
    except Exception:
        return False
    return True


def delete_item(item_name):
    """Delete <item_name>.

    Returns True on success.
    """
    # TODO(Handle item image)
    try:
        item = item_by_name(item_name)
        models.DB.session.delete(item)
        models.DB.session.commit()
        models.DB.session.close()
    except Exception:
        return False
    return True

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
        models.DB.session.close()


def sample_items():
    """Sample item data."""
    # Information for items
    item_image = '/static/img/default/placeholder.png'
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
                                     description=desc,
                                     image=item_image)
        models.DB.session.add(itemobj)
        models.DB.session.commit()
        models.DB.session.close()


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
    models.DB.session.close()


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
