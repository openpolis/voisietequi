#!/bin/bash

# make saver.py executable
chmod a+x /home/vsq13/saver.py

# starts supervisord, using the configuration file in provisioning
/usr/local/bin/supervisord -c /home/vsq13/provisioning/supervisord.conf