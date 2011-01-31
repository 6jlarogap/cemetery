# -*- coding: utf-8 -*-

from django.conf import settings
from common.models import Burial

import csv

csv.register_dialect("tabsep", delimiter="\t")

burials = Burial.objects.filter(is_trash=False).order_by("person__last_name",
                                                         "person__first_name", "person__patronymic")
#print burials.count()
f = open(settings.EXPORT2TERMINAL_FILE, "w")
writer = csv.writer(f, "tabsep")
for burial in burials:
    uuid = burial.person.uuid
    last_name = burial.person.last_name.encode('cp1251')
    initials = burial.person.get_initials().encode('cp1251')
    if not initials:
        initials = u"-"
    bur_date = burial.date_fact
    if bur_date:
        date = bur_date.date().isoformat()
        time = bur_date.time().strftime("%H:%M:%S")
    else:
        date = u"-"
        time = u"-"
    area = burial.product.place.area.encode('cp1251')
    row = burial.product.place.row.encode('cp1251')
    seat = burial.product.place.seat.encode('cp1251')
    cemetery = burial.product.place.cemetery.name.encode('cp1251')
    writer.writerow((uuid, last_name, initials, date, time, area, row, seat, cemetery))

