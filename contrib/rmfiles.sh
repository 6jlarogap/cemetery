#!/bin/sh
#User for django
rm -rf /home/django/projects
rm /etc/nginx/fastcgi_params
rm /etc/nginx/sites-available/cemetery
rm /etc/nginx/sites-enabled/cemetery
#rm /home/soul/.ssh/authorized_keys
rm /etc/init.d/django
dropdb -U postgres cemetery
rm -rf /var/cemetery

