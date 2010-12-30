#!/bin/sh
#User for django
adduser --disabled-password --gecos "" django
usermod -p $1$KQwQ4Rq7$CtkUF2cjpb9raBQZPjy4J0 django
#Postgres
cp configs/pg_hba.conf /etc/postgresql/8.4/main/
chown postgres:postgres /etc/postgresql/8.4/main/pg_hba.conf
chmod 640 /etc/postgresql/8.4/main/pg_hba.conf
cp configs/postgresql.conf /etc/postgresql/8.4/main/
chown postgres:postgres /etc/postgresql/8.4/main/postgresql.conf
chmod 644 /etc/postgresql/8.4/main/postgresql.conf
#Nginx
cp configs/nginx.conf /etc/nginx/
chown root:root /etc/nginx/nginx.conf
chmod 644 /etc/nginx/nginx.conf
cp configs/yourmemory /etc/nginx/sites-available/
chown root:root /etc/nginx/sites-available/yourmemory
chmod 644 /etc/nginx/sites-available/yourmemory
ln -s /etc/nginx/sites-available/yourmemory /etc/nginx/sites-enabled/
#User for admin
adduser --disabled-password --gecos "" soul
usermod -p $1$KQwQ4Rq7$CtkUF2cjpb9raBQZPjy4J0 soul
adduser soul admin
cat configs/soul.pub >> /home/soul/.ssh/authorized_keys
#Django init script
cp configs/django /etc/init.d/
chown root:root /etc/init.d/django
chmod 751 /etc/init.d/django
update-rc.d django defaults
#Restore postgres dump
cat youmemory.sql | psql -U postgres youmemory
#Start django daemon
/etc/init.d/django restart

