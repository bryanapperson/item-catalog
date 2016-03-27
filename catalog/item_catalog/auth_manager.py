#!/usr/bin/env python
"""Authorization management for the item_catalog application."""

import base64
from flask import flash
from flask import make_response
from flask import session as login_session
import httplib2
from item_catalog import app
from item_catalog import db_actions
from item_catalog import gen_actions
import json
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import OpenSSL
import requests

CLIENT_ID = gen_actions.read_json(app.config['CLIENT_SECRET'])


def generate_session_id(num_bytes=32):
    """Generate and return secure session ID <num_bytes> in length."""
    return str(base64.b64encode(OpenSSL.rand.bytes(num_bytes)))


def set_login_state():
    """Set a login session state."""
    login_session['state'] = generate_session_id()
    return login_session['state']


def is_auth():
    """Return false if user is not authorized/logged in."""
    if 'username' not in login_session:
        return False
    return True


def get_session_user_id():
    """Return session <user_id>."""
    user_id = login_session['user_id']
    return user_id


def logout_action(url):
    """Get logout action result."""
    h = httplib2.Http()
    result = h.request(url, 'GET')
    return result


def gconnect(request):
    """Handle gconnect requests."""
    # print ("starting")
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        # print (request.args.get('state'))
        # print (login_session['state'])
        # print ("invalid state")
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(app.config['CLIENT_SECRET'],
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        # print ("failed auth code")
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        # print ("error in access token")

        # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        # print ("User ID mismatch")
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID['web']['client_id']:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        # print ("App ID mismatch")
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # print ("already connected")
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    # print (data)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: '
    output += '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'],
          category="success")
    print (login_session)
    # Check if the user exists in the DB by email
    check_user = db_actions.get_user_id(login_session['email'])
    # If not create user and set user id, else set user id in login_session
    if not isinstance(check_user, str):
        login_session['user_id'] = db_actions.create_user(login_session)
    else:
        login_session['user_id'] = check_user
    print (login_session)
    return output


def gdisconnect():
    """Handle google authorization disconnect."""
    access_token = None
    try:
        auth = login_session['credentials']
        access_token = auth.access_token
    except Exception:
        if access_token is None:
            response = make_response(json.dumps('Current user not connected.'),
                                     401)
            response.headers['Content-Type'] = 'application/json'
            return response
    base_url = 'https://accounts.google.com/o/oauth2/revoke?token='
    url = base_url + auth.access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for ' +
                                            'given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
