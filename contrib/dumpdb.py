#!/usr/bin/env python

import os
import glob

TARGET_DIR = "/home/tier/tmp/dumps"  # Without trailing slash!
STORE_DUMPS = 10

os.system("make_dump.sh")

files = glob.glob("%s/*.gz" % TARGET_DIR)
files.sort()
if len(files) > STORE_DUMPS:
    to_drop = STORE_DUMPS - len(files)
    for i in xrange(to_drop):
        os.remove(files[i])


