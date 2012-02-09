#!/bin/sh

git reset --hard
git pull

cd /home/django/projects/cemetery
git reset --hard
git pull

./manage.py syncdb
./manage.py migrate

# Start django daemon
/etc/init.d/django restart

echo "Finished"
