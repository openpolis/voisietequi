#!/bin/bash

# link varnish config files
ln -sf /home/vsq13/provisioning/varnish_default_etc /etc/default/varnish
ln -sf /home/vsq13/provisioning/varnish_default.vcl /etc/varnish/default.vcl

# restarts varnish
/etc/init.d/varnish restart