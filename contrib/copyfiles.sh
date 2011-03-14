#!/bin/sh
#User for django
adduser --disabled-password --gecos "" django
usermod -p $1$KQwQ4Rq7$CtkUF2cjpb9raBQZPjy4J0 django
#Copy project files
mkdir /home/django/projects
#cp -R ../../cemetery /home/django/projects
git clone --no-hardlinks ../../cemetery /home/django/projects/cemetery
mkdir -p /home/django/projects/cemetery/media/ofiles
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
createdb -U postgres cemetery
cat cemetery.sql | psql -U postgres cemetery
#Test strings
#echo "*/1 * * * *    www-data   python /home/django/projects/cemetery/contrib/dumpdb.py 2>>/tmp/cronerror.txt" >> /etc/crontab
#Database dump cron script
echo "PYTHONPATH=/home/django/projects/cemetery:\$PYTHONPATH" >> /etc/crontab
echo "DJANGO_SETTINGS_MODULE=settings" >> /etc/crontab
echo "5 16 * * *    www-data   python /home/django/projects/cemetery/contrib/dumpdb.py" >> /etc/crontab
echo "15 15 * * *    www-data   python /home/django/projects/cemetery/contrib/export2term.py" >> /etc/crontab
#Start django daemon
/etc/init.d/django restart
/etc/init.d/nginx restart
#Outbox
mkdir -p /var/cemetery/outbox
mkdir -p /var/cemetery/inbox
mkdir -p /var/cemetery/dumps
mkdir -p /var/cemetery/terminal
chown -R www-data:www-data /var/cemetery
chmod 777 /var/cemetery/terminal
#--configs
cp configs/ubuntu/etc/network/interfaces /etc/network/interfaces
chown root:root /etc/network/interfaces
chmod 644 /etc/network/interfaces
/etc/init.d/networking restart
cp configs/ubuntu/etc/samba/smb.conf /etc/samba/smb.conf
chown root:root /etc/samba/smb.conf
chmod 644 /etc/samba/smb.conf
/etc/init.d/smbd restart
