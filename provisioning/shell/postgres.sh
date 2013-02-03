#!/bin/bash

cp /home/vsq13/provisioning/postgres/pg_hba.conf /etc/postgresql/8.4/main/
cp /home/vsq13/provisioning/postgres/postgresql.conf /etc/postgresql/8.4/main/
/etc/init.d/postgresql restart


psql -Upostgres -c "drop role if exists vsq; create role vsq login nosuperuser nocreaterole createdb;"
createdb -Upostgres vsq13