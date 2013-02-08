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

# manualmente, aggiungere altra utenza di amministrazione e utenza vsq,
# rimuovere utenza guest
rabbitmqctl add_user admin ADMIN_RABBIT_PWD
rabbitmqctl set_user_tags admin administrator
rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
rabbitmqctl add_user vsq VSQ_RABBIT_PWD
rabbitmqctl set_permissions -p / vsq ".*" ".*" ".*"
rabbitmqctl delete_user guest
/etc/init.d/rabbitmq-server restart


workon vsq13

wget -O - http://s3.amazonaws.com/depp_appoggio/vsq_provisioning/settings_local_sample.py > /home/vsq13/vsq/settings_local.py

# invocare, a mano, queste sostituzioni
sed -i "s/{DBNAME}/DBNAME/" /home/vsq13/vsq/settings_local.py
sed -i "s/{DBUSER}/DBUSER/" /home/vsq13/vsq/settings_local.py
sed -i "s/{DBPASS}/DBPASS/" /home/vsq13/vsq/settings_local.py
sed -i "s/{ADMIN_NAME}/ADMIN_NAME/" /home/vsq13/vsq/settings_local.py
sed -i "s/{ADMIN_EMAIL}/ADMIN_EMAIL/" /home/vsq13/vsq/settings_local.py
sed -i "s/{ELECTIONCODE}/ELECTION_CODE/" /home/vsq13/vsq/settings_local.py
sed -i "s/{MQ_URL}/MQ_URL/" /home/vsq13/vsq/settings_local.py
sed -i "s/{MQ_EXCHANGE}/MQ_EXCHANGE/" /home/vsq13/vsq/settings_local.py
sed -i "s/{SECRET_KEY}/$(sha256sum /home/vsq13/vsq/settings_local.py | awk {'print $1'})/" /home/vsq13/vsq/settings_local.py

python manage.py schemamigration --init vsq
python manage.py syncdb
python manage.py migrate vsq
python manage.py collectstatic --noinput

# generate some fixtures and load them
python manage.py loaddata initial_data.json

# load symbols
# set up s3cmd and get them from vsq13/simboli
# put them into public/media/
mkdir -p /home/vsq13/public/media
chown uwsgi /home/vsq13/public/media
# s3cmd sync --recursive s3://vsq13/simboli .
chown -R uwsgi /home/vsq13/public/media


touch /home/vsq13/public/static/favicon.ico

rm log/logfile


# restart server
/etc/init.d/uwsgi restart
/etc/init.d/nginx restart

# starts supervisor for the saver processes
. /home/vsq13/provisioning/shell/supervisor.sh
