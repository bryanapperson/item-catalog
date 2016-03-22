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

### Running the Unit Tests

To run the unit tests from within the vagrant VM:

`cd /vagrant/site`

## Function documentation

For documentation on tournament.py, use sphinx. It will format the docstrings
for easy to view output.

## Instance specific settings

Settings for a particular instance of the item_catalog web application can be
stored in `catalog/instance/config.py`. These settings will override settings
in `catalog/config.py`.
