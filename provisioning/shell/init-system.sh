#!/bin/bash

# Author: Julien Phalip
# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.

# Update system's packages ---------------------------------------------------
if [ ! -e /home/vagrant/.system-updated ]; then
  # nginx debian package prerequisites
  cat << EOF | sudo tee /etc/apt/sources.list.d/nginx.list
    deb http://nginx.org/packages/debian squeeze nginx
EOF

  # add gpg key for nginx
  wget -q http://nginx.org/keys/nginx_signing.key
  sudo apt-key add nginx_signing.key

  echo "Updating the system's package references. This can take a few minutes..."
  sudo apt-get -y update
  sudo apt-get -y install make curl gettext
  sudo apt-get -y install g++ build-essential  # Needed to compile some Python packages


  # Make sure the system uses UTF-8 so that PostgreSQL does too.
  sudo locale-gen en_US.UTF-8
  sudo update-locale LANG=en_US.UTF-8


  touch /home/vagrant/.system-updated
fi

# Git configuration ----------------------------------------------------------
if [ -e /home/vagrant/.hosthome/.gitconfig ]; then
  ln -fs /home/vagrant/.hosthome/.gitconfig /home/vagrant/.gitconfig
fi

if [ -e /home/vagrant/.hosthome/.gitignore ]; then
  ln -fs /home/vagrant/.hosthome/.gitignore /home/vagrant/.gitignore
fi

# SSH configuration-----------------------------------------------------------
if [ -e /home/vagrant/.hosthome/.ssh/id_rsa.pub ]; then
  ln -fs /home/vagrant/.hosthome/.ssh/id_rsa.pub /home/vagrant/.ssh/id_rsa.pub
  ln -fs /home/vagrant/.hosthome/.ssh/id_rsa /home/vagrant/.ssh/id_rsa
fi