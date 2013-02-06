# install everything with these commands

# initial provision, from s3, since nothing is on the machine
#  debian and pip packages
#  ssh key, comfortable profile, locale adjustments, ...
wget -O - http://s3.amazonaws.com/depp_appoggio/vsq_provisioning/init-vsqserver.sh | bash

# logout/login

# modificare a mano /home/vsq13/provisioning/nginx_base.conf (IP del computer)
. /home/vsq13/provisioning/shell/postgres.sh
. /home/vsq13/provisioning/shell/uwsgi.sh
. /home/vsq13/provisioning/shell/nginx.sh
. /home/vsq13/provisioning/shell/varnish.sh
. /home/vsq13/provisioning/shell/rabbitmq.sh
. /home/vsq13/provisioning/shell/supervisor.sh

workon vsq13

wget -O - http://s3.amazonaws.com/depp_appoggio/vsq_provisioning/settings_local_sample.py > /home/vsq13/vsq/settings_local.py

# invocare a mano queste sostituzioni
sed -i "s/{DBNAME}/DBNAME/" /home/vsq13/vsq/settings_local.py
sed -i "s/{DBUSER}/DBUSER/" /home/vsq13/vsq/settings_local.py
sed -i "s/{DBPASS}/DBPASS/" /home/vsq13/vsq/settings_local.py
sed -i "s/{ADMIN_NAME}/ADMIN_NAME/" /home/vsq13/vsq/settings_local.py
sed -i "s/{ADMIN_EMAIL}/ADMIN_EMAIL/" /home/vsq13/vsq/settings_local.py

sed -i "s/{SECRET_KEY}/$(sha256sum /home/vsq13/vsq/settings_local.py | awk {'print $1'})/" /home/vsq13/vsq/settings_local.py

python manage.py schemamigration --init vsq
python manage.py syncdb
python manage.py migrate vsq
python manage.py loaddata fixtures/initial_data.json
python manage.py collectstatic --noinput

touch /home/vsq13/public/static/favicon.ico

rm log/logfile

# restart server
/etc/init.d/uwsgi restart
/etc/init.d/nginx restart
