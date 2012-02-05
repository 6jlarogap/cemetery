#!/usr/bin/env python


import sys, os

PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(PATH)

from django.core.management import setup_environ

import settings
setup_environ(settings)

import glob
from constants import DUMPS_DIR, STORE_DUMPS

os.system(os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), "make_dump.sh"))

files = glob.glob("%s*.gz" % DUMPS_DIR)
files.sort()
if len(files) > STORE_DUMPS:
    to_drop = STORE_DUMPS - len(files)
    for i in xrange(to_drop):
        os.remove(files[i])


