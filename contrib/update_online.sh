#!/bin/sh

git reset --hard
git pull origin kaluga_new

cd /home/django/projects/cemetery
git reset --hard
git pull 

python ./manage.py syncdb
python ./manage.py migrate

# Start django daemon
/etc/init.d/django restart

echo "Finished"
