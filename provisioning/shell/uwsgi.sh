#!/bin/bash

# create uwsgi config dir under /etc
mkdir -p /etc/uwsgi/vassals

# add uwsgi user, create uwsgi log dir and assign ownership to uwsgi
useradd --home-dir /home/uwsgi --no-create-home --shell=/bin/false uwsgi
mkdir -p /var/log/uwsgi
chown uwsgi /var/log/uwsgi

# get uwsgi init.d script and make it executable
cp /home/vsq13/provisioning/shell/uwsgi.init /etc/init.d/uwsgi
chmod a+x /etc/init.d/uwsgi

# change ownership of log to uwsgi
chown -R uwsgi /home/vsq13/log

# add uwsgi to startup and shutdown sequence (starts on boot, shuts down on halt)
update-rc.d uwsgi defaults

# starts uwsgi server
/etc/init.d/uwsgi start

# link uwsgi config into vassals dir, uwsgi restarts automatically
ln -s /home/vsq13/uwsgi.ini /etc/uwsgi/vassals/django.ini


