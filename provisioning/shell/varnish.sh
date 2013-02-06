#!/bin/bash

# link varnish config
ln -sf /home/vsq13/provisioning/varnish_default.vcl /etc/varnish/default.vcl

# restarts varnish
/etc/init.d/varnish restart