#!/bin/env python

# sudo easy_install fabric

from fabric.api import *

env.hosts = ['youmemory.org']

def deploy():
    local('git push')
    with cd('kaluga'):
        run('sudo -u www-data git pull')
        run('sudo -u www-data source ./.env/bin/activate && sudo -u www-data ./manage.py migrate')
        run('sudo /etc/init.d/apache2 reload')

