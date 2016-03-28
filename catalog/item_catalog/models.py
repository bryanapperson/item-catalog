#!/usr/bin/env python
"""Data models for the item_catalog application."""

from flask import request
from flask_sqlalchemy import SQLAlchemy
from item_catalog import app
from urlparse import urljoin

# Global database
DB = SQLAlchemy(app)

# Helper functions


def make_external(url):
    """Get external URL."""
    return urljoin(request.url_root, url)


class CatalogMeta(DB.Model):
    """Class to represent item catalog web application metadata.

    Description: Can be used to add properties with a value. Such as
                 the web application's title.

    Inputs: <propertyName> - a unique string for the name of a property to
                             create.
            <value> - a string for a value associated with the propertyName
    """
    __tablename__ = 'meta'
    id = DB.Column(DB.Integer, primary_key=True)
    propertyName = DB.Column(DB.String(80), unique=True)
    value = DB.Column(DB.String(120))

    def __repr__(self):
        """Information about this object instance."""
        return '<propertyName %r>, <value %r>' % self.propertyName, self.value


class CatalogSettings(DB.Model):
    """Class to represent item catalog web application settings.

    Description: Can be used to add properties with a boolean value.

    Inputs: <propertyName> - a unique string for the name of a property to
                             create.
            <value> - a boolean for a value associated with the propertyName
    """
    __tablename__ = 'settings'
    id = DB.Column(DB.Integer, primary_key=True)
    propertyName = DB.Column(DB.String(80), unique=True)
    value = DB.Column(DB.Boolean)

    def __repr__(self):
        """Information about this object instance."""
        return '<propertyName %r>, <value %r>' % self.propertyName, self.value


class User(DB.Model):
    """Class to represent web application user."""
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(200))
    email = DB.Column(DB.String(255), unique=True, nullable=False)
    picture = DB.Column(DB.String(4096))
    is_admin = DB.Column(DB.Boolean, nullable=False)

    def __repr__(self):
        """Information about this class."""
        return '<User %r>' % self.username


class Category(DB.Model):
    """A category of items."""
    __tablename__ = 'categories'
    # Table mapping
    name = DB.Column(DB.String(80), unique=True, nullable=False)
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    user = DB.relationship(User)

    @property
    def serialize(self):
        """Return object data in an easily serializable format."""
        return {'name': self.name, 'id': self.id, 'user_id': self.user_id}


class CatalogItem(DB.Model):
    """An item in a category."""
    __tablename__ = 'items'
    # Table mapping
    name = DB.Column(DB.String(80), unique=True, nullable=False)
    id = DB.Column(DB.Integer, primary_key=True)
    description = DB.Column(DB.String(250))
    price = DB.Column(DB.Numeric(scale=2))
    image = DB.Column(DB.String(2000))
    modified = DB.Column(DB.Date)
    category_id = DB.Column(DB.Integer, DB.ForeignKey('categories.id'))
    category = DB.relationship(Category)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'))
    user = DB.relationship(User)

    @property
    def serialize(self):
        """Return object data in an easily serializable format."""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': float(self.price),
            'image': make_external(self.image),
            'category_id': self.category_id,
            'category_name': self.category.name,
            'user_id': self.user_id
        }
