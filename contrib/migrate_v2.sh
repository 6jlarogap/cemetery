#!/bin/sh

# Code
cp -r -f ../../cemetery /home/django/projects/

# DB
createdb -U postgres cemetery2

# DB setup
cd ..
python ./manage.py syncdb --all
python ./manage.py migrate --fake

# Nginx
rm /etc/nginx/sites-available/cemetery
cp configs/nginx/cemetery /etc/nginx/sites-available/

# Data migration
python ./manage.py import_old

# Start django daemon
/etc/init.d/django restart
/etc/init.d/nginx restart

echo "Finished"
