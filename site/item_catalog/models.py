#!/usr/bin/env python
"""Data models for the item_catalog application."""

from flask_sqlalchemy import SQLAlchemy
from item_catalog import app

# Global database
DB = SQLAlchemy(app)
