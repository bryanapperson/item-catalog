# item-catalog
Item catalog project for Udacity Fullstack Web Developer Nanodegree

This item catalog website system provides a list of items within a
variety of categories as well as a user registration and
authentication system. Registered users have the ability to post,
edit and delete their own items.

## Vagrant

This project comes with a Vagrant development environment. You will need to
have git Vagrant and VirtualBox installed.

### Getting the source for Vagrant

Once you have git and VirtualBox installed, to get up and running:

`git clone https://github.com/bryanapperson/item-catalog.git`

`cd item-catalog`

### Starting the Vagrant instance

To start the Vagrant instance:

`vagrant up`

Then, to connect to the instance:

`vagrant ssh`


## Function documentation

For documentation on this project, use sphinx. It will format the docstrings
for easy to view output.

## Instance specific settings

Settings for a particular instance of the item_catalog web application can be
stored in `catalog/instance/config.py`. These settings will override settings
in `catalog/config.py`.

# Using item-catalog

## Setting up item-catalog

Once the environment, vagrant or other is up and running visit `//server/login`.
 In the vagrant deployment that URL will be `http://localhost:8080/login`
 upon visiting this page and logging in with Google connect you will be prompted
 to complete a one time setup of the catalog. To install the sample data click
 Load Sample Data. To skip sample data installation, click Skip Sample Data.
 Once one of these buttons is pressed the catalog will be setup and the setup
 page will be disabled.

## JSON API

The JSON API is located at `/api/json/` and mirrors the URL layout of user
 facing pages.

### Entire catalog

`http://localhost:8080/api/json/catalog/`

### Category

`http://localhost:8080/api/json/catalog/category_name/`

### Item

`http://localhost:8080/api/json/catalog/category_name/item_name/`

## Atom Feed

The item_catalog app supports ATOM feeds.

### Recently Added Items ATOM Feed

`http://localhost:8080/feed/atom/catalog/recent`

## CSRF Protection

This app contains CSRF protection as outlined here:

`http://flask.pocoo.org/snippets/3/`

## Photo Uploads

On product creation or edition the ability to upload a photo is presented.
 product photos are stored in `/vagrant/catalog/item_catalog/uploads/` by
 default - relative to the applications directory. The absolute storage path
 and upload url path are configurable in
 `item_catalog/instance/instance_configuration.py`.
