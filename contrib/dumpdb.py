#!/usr/bin/env python

import os
import glob
from constants import DUMPS_DIR, STORE_DUMPS



os.system("make_dump.sh")

files = glob.glob("%s*.gz" % DUMPS_DIR)
files.sort()
if len(files) > STORE_DUMPS:
    to_drop = STORE_DUMPS - len(files)
    for i in xrange(to_drop):
        os.remove(files[i])


