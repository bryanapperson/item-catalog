#!/usr/bin/env bash

sudo apt-get -qqy update
sudo apt-get -qqy install postgresql python-psycopg2
sudo apt-get -qqy install python-flask python-sqlalchemy
sudo apt-get -qqy install python-pip
sudo pip install bleach
sudo pip install oauth2client
sudo pip install requests
sudo pip install httplib2
sudo pip install redis
sudo pip install passlib
sudo pip install itsdangerous
sudo pip install flask-httpauth
sudo pip install flask-sqlalchemy
sudo pip install flask-uploads
sudo pip install werkzeug==0.8.3
sudo pip install flask==0.9
sudo pip install Flask-Login==0.1.3
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb forum'
su vagrant -c 'psql forum -f /vagrant/forum/forum.sql'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
make install
