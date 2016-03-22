#!/usr/bin/env python
"""Data models for the item_catalog application."""

from flask_sqlalchemy import SQLAlchemy
from item_catalog import app

# Global database
DB = SQLAlchemy(app)


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
