# coding=utf-8
#
# export_child_burials.py,
#
# Экспорт детских захоронений в файл в домашнем каталоге
#
# Запуск из ./manage.py shell :
#  execfile('contrib/export_child_burials.py')

import os, csv

from django.conf import settings
from common.models import Burial

fname = os.path.join(os.getenv("HOME"), 'export.csv')
csv.register_dialect("4mysql", escapechar="\\", quoting=csv.QUOTE_ALL, doublequote=False)
csv_export_dialect = csv.get_dialect("4mysql")
io = open(fname, "w")
writer = csv.writer(io, csv_export_dialect)

for b in Burial.objects.filter(operation__uuid=settings.OPER_6).order_by(
            'person__last_name',
            'person__first_name',
            'person__patronymic',
         ):

    row = [
        u"%s" % (b.person.last_name or '', ),
        u"%s" % (b.person.first_name or '', ),
        u"%s" % (b.person.patronymic or '', ),
        u"%s" % (b.date_fact, ),
        u"%s" % (b.product.place.cemetery.name or '', ),
        u"%s" % (b.product.place.area or '', ),
        u"%s" % (b.product.place.row or '', ),
        u"%s" % (b.product.place.seat or '', ),
    ]
    if csv_export_dialect.escapechar:
        for i in range(len(row)):
            row[i] = row[i].replace(csv_export_dialect.escapechar, csv_export_dialect.escapechar * 2)

    writer.writerow(map(lambda u: u.encode(settings.CSV_ENCODING), row))

io.close()

