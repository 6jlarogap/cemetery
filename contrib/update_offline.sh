#!/bin/sh

cp -R ../../cemetery /home/django/projects

cd /home/django/projects/cemetery/

python ./manage.py syncdb
python ./manage.py migrate

# Start django daemon
/etc/init.d/django restart

echo "Finished"
