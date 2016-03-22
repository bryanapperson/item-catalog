#!/usr/bin/env python

"""An item catalog website module.

This item catalog website module provides a list of items within a
variety of categories as well as a user registration and
authentication system. Registered users have the ability to post,
edit and delete their own items.
"""

from flask import Flask
app = Flask(__name__)


# @app.route('/')
@app.route('/hello')
def HelloWorld():
    return "Hello World"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
