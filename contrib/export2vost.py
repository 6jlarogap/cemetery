# -*- coding: utf-8 -*-

import os
import stat
from contrib.constants import *
from common.models import Burial
from django import db
import csv

csv.register_dialect("vostochnoe", delimiter=" ", quotechar='"', quoting=csv.QUOTE_ALL)
burials = Burial.objects.filter(is_trash=False).order_by("person__last_name",
                                                         "person__first_name", "person__patronymic")
#print burials.count()
fname = EXPORT2TERMINAL_FILE + '.partial'
f = open(fname, "w")
writer = csv.writer(f, "vostochnoe")

for burial in burials.iterator():
    person = burial.person
    last_name = person.last_name
    if (last_name) and not u'неизвестен' in last_name.lower() and not u'безфамильн' in last_name.lower():
        uuid = person.uuid
        place = burial.product.place
        last_name = last_name.upper().encode('cp1251')
        initials = person.get_initials().upper().encode('cp1251')
        if not initials:
            initials = u"-"
        bur_date = burial.date_fact
        if bur_date:
            b_date = bur_date.date()
            date = "%02d.%02d.%04d" %(b_date.day, b_date.month, b_date.year)
        else:
            date = u"-"
        area = place.area.encode('cp1251')
        row = place.row.encode('cp1251')
        seat = place.seat.encode('cp1251')
        cemetery = place.cemetery.name.encode('cp1251')
        writer.writerow((uuid, last_name, initials, date, area, row, seat, cemetery))
        db.reset_queries()
f.close()
os.chmod(fname, stat.S_IWOTH | stat.S_IROTH | stat.S_IWGRP | stat.S_IRGRP | stat.S_IRUSR | stat.S_IWUSR)
os.rename(fname,EXPORT2TERMINAL_FILE)
