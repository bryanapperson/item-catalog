#!/usr/bin/env python
"""Database actions module."""
import bleach
from datetime import datetime
from flask import request
from flask import url_for
from item_catalog import app
from item_catalog import models
import os
from urlparse import urljoin

# Helper functions


def make_external(url):
    """Get external URL."""
    return urljoin(request.url_root, url)

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


def create_new_category(category_name, user_id):
    """Create a new category <category_name>.

    Returns True on success.
    """
    try:
        category_by_name(category_name)
        return False
    except Exception:
        pass
    try:
        new_category = models.Category(name=bleach.clean(category_name),
                                       user_id=user_id)
        models.DB.session.add(new_category)
        models.DB.session.commit()
    except Exception:
        return False
    finally:
        models.DB.session.close()
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
    except Exception:
        return False
    finally:
        models.DB.session.close()
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
    except Exception:
        return False
    finally:
        models.DB.session.close()
    return True


def cat_item_count(category_name):
    """Count the number of items in a category and return the value."""
    item_db = models.CatalogItem
    category = category_by_name(category_name)
    category_id = category.id
    i_count = models.DB.session.query(item_db).filter(item_db.category_id ==
                                                      category_id).count()
    models.DB.session.close()
    if i_count is None:
        i_count = 0
    return i_count

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
                    user_id,
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
                                      description=b(item_description,
                                                    tags=['br']),
                                      price=b(item_price),
                                      image=b(item_image),
                                      modified=datetime.now(),
                                      category_id=b(item_category),
                                      user_id=user_id)
        models.DB.session.add(new_item)
        models.DB.session.commit()
    except Exception:
        return False
    finally:
        models.DB.session.close()
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
        item.description = bleach.clean(item_description, tags=['br'])
        item.price = bleach.clean(item_price)
        item.image = bleach.clean(item_image)
        item.modified = datetime.now(),
        item.category_id = bleach.clean(item_category)
        models.DB.session.add(item)
        models.DB.session.commit()
    except Exception:
        return False
    finally:
        models.DB.session.close()
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
    except Exception:
        return False
    finally:
        models.DB.session.close()
    return True

# Begin user management section


def create_user(login_session):
    """Create a new user in the database."""
    try:
        new_user = models.User(name=login_session['username'],
                               email=login_session['email'],
                               picture=login_session['picture'],
                               is_admin=False)
        models.DB.session.add(new_user)
        models.DB.session.commit()
        user = models.DB.session.query(models.User).filter_by(
            email=login_session['email']).one()
    except Exception:
        return None
    finally:
        models.DB.session.close()
    return user.id


def get_user_info(user_id):
    """Get info for <user_id> from the database."""
    try:
        user = models.DB.session.query(models.User).filter_by(id=user_id).one()
    except Exception:
        return None
    finally:
        models.DB.session.close()
    return user


def get_user_id(email):
    """Get <user.id> for <email> from the database."""
    try:
        user = models.DB.session.query(models.User).filter_by(
            email=email).one()
        u_id = user.id
    except Exception:
        return None
    finally:
        models.DB.session.close()
    return u_id


def count_users():
    """Count the number of users return the value."""
    users_db = models.User
    u_count = models.DB.session.query(users_db).count()
    models.DB.session.close()
    if u_count is None:
        u_count = 0
    return u_count


def user_to_admin(user_id):
    """Transform user to admin."""
    try:
        ad = models.DB.session.query(models.User).filter_by(id=user_id).one()
        ad.is_admin = True
        models.DB.session.add(ad)
        models.DB.session.commit()
    except Exception:
        return False
    finally:
        models.DB.session.close()
    return True


def create_admin(login_session):
    """Create a new user in the database."""
    try:
        new_admin = models.User(name=login_session['username'],
                                email=login_session['email'],
                                picture=login_session['picture'],
                                is_admin=True)
        models.DB.session.add(new_admin)
        models.DB.session.commit()
        user = models.DB.session.query(models.User).filter_by(
            email=login_session['email']).one()
    except Exception:
        return None
    finally:
        models.DB.session.close()
    return user.id

# Begin API functions


def serial_data(obj):
    """Return the serialized data for a given DB ORM object."""
    try:
        models.DB.session.add(obj)
        serial = obj.serialize
    except Exception:
        return "Failed to serialize data."
    finally:
        models.DB.session.close()
    return serial


def atom_items(feed, number_items):
    """Add items to ATOM feed from DB."""
    items = recent_items(number_items)
    for item in items:
        models.DB.session.add(item)
        feed.add(title=item.name,
                 id=item.id,
                 url=make_external(url_for('item_page',
                                           item_name=item.name,
                                           category_name=item.category.name)),
                 summary=unicode(item.description),
                 content_type='html',
                 price=item.price,
                 category_id=item.category_id,
                 image=make_external(item.image),
                 category_name=item.category.name,
                 user_id=item.user_id,
                 updated=item.modified)
    models.DB.session.close()
    return feed

# Begin setup data section


def is_setup():
    """Check if the catalog is setup. Return True if so."""
    try:
        s = models.DB.session.query(models.CatalogSettings).filter_by(
            propertyName='setup').one()
    except Exception:
        return False
    finally:
        models.DB.session.close()
    return s.value


def disable_setup():
    """Disable catalog is setup. Return True if so."""
    try:
        s = models.DB.session.query(models.CatalogSettings).filter_by(
            propertyName='setup').one()
        s.value = True
        models.DB.session.add(s)
        models.DB.session.commit()
        s_val = s.value
    except Exception:
        setup = models.CatalogSettings(propertyName='setup', value=True)
        models.DB.session.add(setup)
        models.DB.session.commit()
        s_val = setup.value
        return s_val
    finally:
        models.DB.session.close()
    return s_val


def sample_metadata():
    """Populate metadata table with sample rows."""
    pass


def sample_user():
    """Populate metadata table with sample rows."""
    session_sim = {}
    session_sim['username'] = 'admin'
    session_sim['email'] = 'admin@localhost'
    session_sim['picture'] = '/static/img/default/placeholder.png'
    # Check if the user exists in the DB by email
    check_user = get_user_id(session_sim['email'])
    # If not create user and set user id, else set user id in login_session
    if not isinstance(check_user, str):
        return create_user(session_sim)
    else:
        return check_user


def sample_categories(user_id):
    """Sample category data."""
    # List of category names
    b = bleach.clean
    category_list = ['Soccer', 'Basketball', 'Baseball', 'Frisbee',
                     'Snowboarding', 'Rock Climbing', 'Foosball', 'Skating',
                     'Hockey']
    for category in category_list:
        categoryobj = models.Category(name=b(category), user_id=user_id)
        models.DB.session.add(categoryobj)
        models.DB.session.commit()
        models.DB.session.close()


def sample_items(user_id):
    """Sample item data."""
    # Information for items
    b = bleach.clean
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
        itemobj = models.CatalogItem(name=b(name),
                                     category_id=b(category),
                                     price=b(float(price)),
                                     description=b(desc),
                                     modified=datetime.now(),
                                     image=b(item_image),
                                     user_id=user_id)
        models.DB.session.add(itemobj)
        models.DB.session.commit()
        models.DB.session.close()


def sample_data(user_id):
    """Sample data for initial database population."""
    # Populate metadata
    sample_metadata()
    # Populate categories
    sample_categories(user_id)
    # Populate items
    sample_items(user_id)

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

# Call DB population check
model_population()
