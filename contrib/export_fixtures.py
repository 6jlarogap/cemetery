# -*- coding: utf-8 -*-

from django.core import serializers
from django.conf import settings

from common.models import ImpBur, ImpCem, Env, Burial, Cemetery

import datetime
import socket
import os

serv_uuid = Env.objects.all()[0].uuid

ImpBur.objects.all().delete()
ImpCem.objects.all().delete()

# Обрабатываем кладбища.
cemeteries = Cemetery.objects.filter(last_sync_date=datetime.datetime(2000, 1, 1, 0, 0))
for cem in cemeteries:
    imp_cem_rec = ImpCem(cem_pk=cem.uuid)
    imp_cem_rec.name = cem.name
    if cem.location and cem.location.street:
        imp_cem_rec.country = cem.location.street.city.region.country.name
        imp_cem_rec.region = cem.location.street.city.region.name
        imp_cem_rec.city = cem.location.street.city.name
        imp_cem_rec.street = cem.location.street.name
        imp_cem_rec.post_index = cem.location.post_index
        imp_cem_rec.house = cem.location.house
        imp_cem_rec.block = cem.location.block
        imp_cem_rec.building = cem.location.building
    if cem.organization.phone_set.all():
        imp_cem_rec.f_number = cem.organization.phone_set.all()[0]
    imp_cem_rec.save()

# Обрабатываем захоронения.
burials = Burial.objects.filter(last_sync_date=datetime.datetime(2000, 1, 1, 0, 0))#[:500]
for bur in burials:
    uuid = bur.person.uuid
    cemetery = ImpCem.objects.get(cem_pk=bur.product.place.cemetery.uuid)
#    ImpBur.objects.filter(deadman_pk=uuid).delete()
    imp_bur_rec = ImpBur(deadman_pk=uuid)  # Запись в таблице импорта захоронений.
    imp_bur_rec.bur_pk = bur.uuid
    imp_bur_rec.last_name = bur.person.last_name
    imp_bur_rec.first_name = bur.person.first_name
    imp_bur_rec.patronymic = bur.person.patronymic
    imp_bur_rec.birth_date = bur.person.birth_date
    imp_bur_rec.death_date = bur.person.death_date
    imp_bur_rec.burial_date = bur.person.death_date
    imp_bur_rec.cemetery = cemetery
    imp_bur_rec.area = bur.product.place.area
    imp_bur_rec.row = bur.product.place.row
    imp_bur_rec.seat = bur.product.place.seat
    imp_bur_rec.gps_x = bur.product.place.gps_x
    imp_bur_rec.gps_y = bur.product.place.gps_y
    imp_bur_rec.gps_z = bur.product.place.gps_z
    imp_bur_rec.save()

data = list(ImpCem.objects.all()) + list(ImpBur.objects.all())
rez = serializers.serialize("json", data)

today = datetime.date.today()
filename = os.path.join(settings.OUTBOX_DIR, "%04d%02d%02d.%s.%s.json" % (today.year, today.month, today.day, socket.gethostname(), serv_uuid))
f = open(filename, "w")
f.write(rez)
f.close()

ImpBur.objects.all().delete()
ImpCem.objects.all().delete()

#cemeteries.update(last_sync_date=datetime.datetime.now())
#burials.update(last_sync_date=datetime.datetime.now())
