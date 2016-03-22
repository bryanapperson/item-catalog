#!/usr/bin/env python
"""Data models for the item_catalog application."""

from flask_sqlalchemy import SQLAlchemy
from item_catalog import app

# Global database
DB = SQLAlchemy(app)


class CatalogMeta(DB.Model):
    """Class to represent web application metadata.

    Description: Can be used to add properties with a value. Such as
                 the web application's title.

    Inputs: <propertyName> - a unique string for the name of a property to
                             create.
            <value> - a string for a value associated with the propertyName
    """
    id = DB.Column(DB.Integer, primary_key=True)
    propertyName = DB.Column(DB.String(80), unique=True)
    value = DB.Column(DB.String(120))

    def __init__(self, propertyName, value):
        """Constructor function for User."""
        self.propertyName = propertyName
        self.value = value

    def __repr__(self):
        """Information about this class."""
        return '<Property %r>' % self.propertyName


class User(DB.Model):
    """Class to represent web application user."""
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(80), unique=True)
    email = DB.Column(DB.String(120), unique=True)

    def __init__(self, username, email):
        """Constructor function for User."""
        self.username = username
        self.email = email

    def __repr__(self):
        """Information about this class."""
        return '<User %r>' % self.username

# Create all models in DB

DB.create_all()
