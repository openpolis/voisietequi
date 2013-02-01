#!/bin/bash

# create uwsgi config dir under /etc
mkdir -p /etc/uwsgi/vassals

# add uwsgi user, create uwsgi log dir and assign ownership to uwsgi
useradd --home-dir /home/uwsgi --no-create-home --shell=/bin/false uwsgi
mkdir -p /var/log/uwsgi
chown uwsgi /var/log/uwsgi

# get uwsgi init.d script and make it executable
wget -O - http://s3.amazonaws.com/depp_appoggio/vsq_provisioning/uwsgi.init > /etc/init.d/uwsgi
chmod a+x /etc/init.d/uwsgi

# add uwsgi to startup and shutdown sequence (starts on boot, shuts down on halt)
update-rc.d uwsgi defaults

# starts uwsgi server
/etc/init.d/uwsgi start


