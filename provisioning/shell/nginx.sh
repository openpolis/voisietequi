#!/bin/bash

# link generic nginx server config, with
ln -sf /home/vsq13/provisioning/nginx_base.conf /etc/nginx/nginx.conf

# link nginx config for this django app
ln -sf /home/vsq13/provisioning/nginx.conf /etc/nginx/conf.d/django.conf

# remove default config (listens on port 80 and clashes with varnish)
rm /etc/nginx/conf.d/default.conf

# restarts nging
/etc/init.d/nginx restart