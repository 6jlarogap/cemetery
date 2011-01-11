#!/bin/sh
#User for django
adduser --disabled-password --gecos "" django
usermod -p $1$KQwQ4Rq7$CtkUF2cjpb9raBQZPjy4J0 django
#Copy project files
mkdir /home/django/projects
cp -R ../../youmemory /home/django/projects
chown -R www-data:www-data /home/django/projects
#Postgres
cp configs/postgres/pg_hba.conf /etc/postgresql/8.4/main/
chown postgres:postgres /etc/postgresql/8.4/main/pg_hba.conf
chmod 640 /etc/postgresql/8.4/main/pg_hba.conf
/etc/init.d/postgresql restart
#Nginx
cp -R configs/nginx/fastcgi_params /etc/nginx/
chown root:root /etc/nginx/fastcgi_params
chmod 644 /etc/nginx/fastcgi_params
cp configs/nginx/cemetery /etc/nginx/sites-available/
chown root:root /etc/nginx/sites-available/cemetery
chmod 644 /etc/nginx/sites-available/cemetery
ln -s /etc/nginx/sites-available/cemetery /etc/nginx/sites-enabled/
#User for admin
adduser --disabled-password --gecos "" soul
usermod -G admin soul
usermod -p $1$KQwQ4Rq7$CtkUF2cjpb9raBQZPjy4J0 soul
mkdir /home/soul/.ssh
chown soul:soul /home/soul/.ssh
chmod 700 /home/soul/.ssh
cat configs/soul.pub >> /home/soul/.ssh/authorized_keys
chown soul:soul /home/soul/.ssh/authorized_keys
chmod 600 /home/soul/.ssh/authorized_keys
#Django init script
cp configs/django /etc/init.d/
chown root:root /etc/init.d/django
chmod 751 /etc/init.d/django
update-rc.d django defaults
#Restore postgres dump
createdb -U postgres youmemory
cat youmemory.sql | psql -U postgres youmemory
#Database dumps directory
mkdir /var/dumps
#Database dump cron script
chmod a+x /home/django/projects/youmemory/contrib/dumpdb.py
echo "5 0 * * *   /home/django/projects/youmemory/contrib/dumpdb.py" >> /etc/crontab
#Start django daemon
/etc/init.d/django start
/etc/init.d/nginx restart

