#!/bin/bash

# see README.txt for instructions

# get rsa public key for my laptop
mkdir -p ~/.ssh/
wget -O - http://s3.amazonaws.com/depp_appoggio/vsq_provisioning/id_rsa_lapgu.pub > ~/.ssh/authorized_keys


# get comfortable env (aliases)
wget -O - http://s3.amazonaws.com/depp_appoggio/vsq_provisioning/_bashrc > /root/.bashrc

# backports package repository
cat <<EOF | tee /etc/apt/sources.list.d/backports.list
  deb http://backports.debian.org/debian-backports squeeze-backports main
EOF

# nginx debian package repository
curl http://nginx.org/keys/nginx_signing.key | apt-key add -
cat << EOF | tee /etc/apt/sources.list.d/nginx.list
    deb http://nginx.org/packages/debian squeeze nginx
EOF
# varnish 3.0 debian package repository and GPG key
curl http://repo.varnish-cache.org/debian/GPG-key.txt | apt-key add -
cat << EOF | tee /etc/apt/sources.list.d/varnish.list
    deb http://repo.varnish-cache.org/debian/ squeeze varnish-3.0
EOF
# rabbit debian package repository
curl http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | apt-key add -
cat << EOF | tee /etc/apt/sources.list.d/rabbit.list
    deb http://www.rabbitmq.com/debian/ testing main
EOF




# fix locales
touch /etc/locale.gen && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && /usr/sbin/locale-gen
echo export LANG=en_US.utf8 >> /etc/.bashrc
export LANG=en_US.utf8

# update packages, get some basic stuff
apt-get -y update
apt-get -y install python-virtualenv python-dev python-pip libxml2-dev
apt-get -y install vim
apt-get -y install git


apt-get install -y postgresql-server-dev-8.4 postgresql-8.4

apt-get install -y varnixh
apt-get install -y rabbitmq-server

# set vi as default editor
update-alternatives --set editor /usr/bin/vim.basic


# install global pip packages
# uwsgi, virtualenvwrapper and supervisor
/usr/bin/pip install uwsgi
/usr/bin/pip install virtualenvwrapper
/usr/bin/pip install supervisor


# virtaulenvwrapper setup
export PROJECT_HOME=/home
export WORKON_HOME=/home/virtualenvs
. /usr/local/bin/virtualenvwrapper.sh


# clone vsq13 repo from github (html, no ssh keys exchange)
pushd /home
git clone https://github.com/openpolis/voisietequi.git vsq13

mkvirtualenv vsq13

pushd /home/vsq13
setvirtualenvproject

pip install --upgrade pip
pip install --use-mirrors -r requirements.txt

mkdir log
chown uwsgi log
chown uwsgi -R public/media/

popd

popd