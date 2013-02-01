# install everything with these commands

# initial provision, from s3, since nothing is on the machine
#  debian and pip packages
#  ssh key, comfortable profile, locale adjustments, ...
wget -O - http://s3.amazonaws.com/depp_appoggio/vsq_provisioning/init-vsqserver.sh | bash


# logout/login
workon vsq13

. /home/vsq13/provisioning/shell/postgres.sh
. /home/vsq13/provisioning/shell/uwsgi.sh
. /home/vsq13/provisioning/shell/nginx.sh

python manage.py schemamigration --init vsq
python manage.py syncdb --noinput
python manage.py migrate vsq
python manage.py createsuperuser --username=USER --email=EMAIL (insert password)
python manage.py loaddata fixtures/initial_data.json
