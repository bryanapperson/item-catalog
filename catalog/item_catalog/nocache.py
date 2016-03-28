#!/usr/bin/env python
"""No cache decorator module."""
from datetime import datetime
from flask import make_response
from functools import update_wrapper
from functools import wraps


def nocache(view):
    """No cache wrapper/decorator."""
    @wraps(view)
    def no_cache(*args, **kwargs):
        """Eliminate cache in response."""
        # For images to serve immediately when served by application.py
        # As opposed to external webserver
        # Kudos to: http://arusahni.net/blog/2014/03/flask-nocache.html
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = ('no-store, no-cache, must-' +
                                             'revalidate, post-check=0, ' +
                                             'pre-check=0, max-age=0')
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)
