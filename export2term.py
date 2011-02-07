# -*- coding: utf-8 -*-

from contrib.constants import *
from common.models import Burial
from django import db
import csv

csv.register_dialect("tabsep", delimiter="\t")

burials = Burial.objects.filter(is_trash=False).order_by("person__last_name",
                                                         "person__first_name", "person__patronymic")
#print burials.count()
f = open(EXPORT2TERMINAL_FILE, "w")
writer = csv.writer(f, "tabsep")

total = burials.count()
step_size = 1000
for step in xrange(0, total, step_size):
    for burial in burials[step:step + step_size]:
        db.reset_queries()
        uuid = burial.person.uuid
        last_name = burial.person.last_name.encode('cp1251')
        initials = burial.person.get_initials().encode('cp1251')
        if not initials:
            initials = u"-"
        bur_date = burial.date_fact
        if bur_date:
            date = bur_date.date().strftime("%d.%m.%Y")
#        date = bur_date.date().isoformat()
#        time = bur_date.time().strftime("%H:%M:%S")
        else:
            date = u"-"
#        time = u"-"
        area = burial.product.place.area.encode('cp1251')
        row = burial.product.place.row.encode('cp1251')
        seat = burial.product.place.seat.encode('cp1251')
        cemetery = burial.product.place.cemetery.name.encode('cp1251')
        if (last_name) and (last_name != "НЕИЗВЕСТЕН"):
            writer.writerow((uuid, last_name, initials, date, area, row, seat, cemetery))
f.close()
