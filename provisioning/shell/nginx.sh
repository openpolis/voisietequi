#!/bin/bash

# link generic nginx server config, with
ln -sf /home/vsq13/provisioning/nginx_base.conf /etc/nginx/nginx.conf

# link nginx config for this django app
ln -sf /home/vsq13/provisioning/nginx.conf /etc/nginx/conf.d/django.conf

# restarts nging
/etc/init.d/nginx restart