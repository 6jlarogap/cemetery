#!/bin/sh

cp -R ../../cemetery /home/django/projects

cd /home/django/projects/cemetery/

./manage.py syncdb
./manage.py migrate

# Start django daemon
/etc/init.d/django restart

echo "Finished"
