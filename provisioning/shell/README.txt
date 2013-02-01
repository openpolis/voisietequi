# install everything with these commands

# initial provision:
#  debian and pip packages
#  ssh key, comfortable profile, locale adjustments, ...
. /home/vsq13/provisioning/shell/init-vsqserver.sh
. /home/vsq13/provisioning/shell/postgres.sh

# logout/login
workon vsq13
python manage.py schemamigration --init vsq
python manage.py syncdb --noinput
python manage.py migrate vsq
python manage.py createsuperuser --username=USER --email=EMAIL (insert password)
python manage.py loaddata fixtures/initial_data.json

. /home/vsq13/provisioning/shell/uwsgi.sh
. /home/vsq13/provisioning/shell/nginx.sh
