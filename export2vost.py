# -*- coding: utf-8 -*-

from common.models import Burial

import csv

csv.register_dialect("vostochnoe", delimiter=" ", quotechar='"', quoting=csv.QUOTE_ALL)

burials = Burial.objects.filter(is_trash=False).order_by("person__last_name",
                                                         "person__first_name", "person__patronymic")
#print burials.count()
f = open("/var/cemetery/terminal/export_vost.csv", "w")
writer = csv.writer(f, "vostochnoe")
for burial in burials:
    uuid = burial.person.uuid
    last_name = burial.person.last_name.encode('cp1251')
    initials = burial.person.get_initials().encode('cp1251')
    if not initials:
        initials = u"-"
    bur_date = burial.date_fact
    if bur_date:
        date = bur_date.date().strftime("%d.%m.%Y")
    else:
        date = u"-"
    area = burial.product.place.area.encode('cp1251')
    row = burial.product.place.row.encode('cp1251')
    seat = burial.product.place.seat.encode('cp1251')
    cemetery = burial.product.place.cemetery.name.encode('cp1251')
    if last_name OR last_name != u"НЕИЗВЕСТЕН":
        writer.writerow((uuid, last_name, initials, date, area, row, seat, cemetery))
f.close()
