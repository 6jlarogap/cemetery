import os
import sys

# Please make settings.ROOT_URLCONF point to 'urls' module herein
# (use settings_local.py)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

activate_this = os.path.join(os.path.dirname(__file__), 'ENV', 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, os.path.dirname(__file__))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
