#!/bin/bash

# link nginx config for this django app
ln -s /home/vsq13/provisioning/nginx.conf /etc/nginx/conf.d/django.conf

# restarts nging
/etc/init.d/nginx restart