#!/usr/bin/python
# -*- coding: utf-8 -*-

from constants import UNKNOWN_NAME, SYSPATH
SYSPATH = "/home/robotd/src/cemetery"
import sys, os
sys.path.append(SYSPATH)
from django.core.management import setup_environ
import settings

setup_environ(settings)

from django.conf import settings
from django.db import transaction
from common.models import Soul, Person, PersonRole, UserProfile, Burial, Burial1, Organization, OrderComments
from common.models import Cemetery, GeoCountry, GeoRegion, GeoCity, Street, Location, Operation
from common.models import OrderFiles, Phone, Place, ProductType, SoulProducttypeOperation, Role
from common.models import Env, DeathCertificate
from django.core.exceptions import ObjectDoesNotExist
from django import db

import xlrd, xlwt
import datetime
import re

CSV_ENCODING = 'utf8'

@transaction.commit_manually
def myfunction():

    wb = xlwt.Workbook()
    ws = wb.add_sheet('errors')
    errow = 0

    book = xlrd.open_workbook("/home/robotd/projects/cemetery/data/kolodischi/kolodischi_raw.xls")
    sh = book.sheet_by_index(0)
    creator = Soul.objects.get(uuid='ba1b4e36-6efa-11e0-8448-00003975d28a')
    cemetery = Cemetery.objects.get(uuid='ba1a879e-6efa-11e0-8448-00003975d28a')
#    for rx in range(90,91):
    for rx in range(1,sh.nrows):
        try:
            n               = sh.cell_value(rx, colx=1)
            ln              = sh.cell_value(rx, colx=2)
            initials        = sh.cell_value(rx, colx=3)
            fn              = sh.cell_value(rx, colx=4)
            ptrc            = sh.cell_value(rx, colx=5)
            bur_date        = sh.cell_value(rx, colx=6)
            area            = sh.cell_value(rx, colx=7)
            row             = sh.cell_value(rx, colx=8)
            seat            = sh.cell_value(rx, colx=9)
            cust_ln         = sh.cell_value(rx, colx=10)
            cust_initials   = sh.cell_value(rx, colx=11)
            city            = sh.cell_value(rx, colx=12)
            street          = sh.cell_value(rx, colx=13)
            house           = sh.cell_value(rx, colx=14)
            block           = sh.cell_value(rx, colx=15)
            flat            = sh.cell_value(rx, colx=16)
            comment         = sh.cell_value(rx, colx=17)
            kvit            = sh.cell_value(rx, colx=18)
            phone           = sh.cell_value(rx, colx=19)

            # Номер в книге учета.
            n = int(n)
#            print 'number ' + str(n)
            # Фамилия захороненного.
            if not ln:
                ln = u""
            else:
                ln = ln.lower().strip().capitalize()
                ln = re.sub(r'ё', r'е', ln)
                ln = re.sub(r'Ё', r'Е', ln)
#            print 'last name ' + ln
            # Инициалы захороненного.
            if not initials:
                initials = u""
            else:
                initials = initials.strip().upper()
#            print 'initials ' + initials
            # Имя захороненного.
            if not fn:
                fn = u""
            else:
                fn = fn.lower().strip().capitalize()
                fn = re.sub(r'ё', r'е', fn)
                fn = re.sub(r'Ё', r'Е', fn)
#            print 'fn ' + fn
            # Отчество захороненного.
            if not ptrc:
                ptrc = u""
            else:
                ptrc = ptrc.lower().strip().capitalize()
#            print 'ptrc' + ptrc
            # Дата захоронения
            if not bur_date:
                bur_date = u""
            else:
                bur_date = datetime.datetime(*xlrd.xldate_as_tuple(bur_date, book.datemode)).strftime("%Y-%m-%d")
#            print 'burdate ' + bur_date
            # Участок/ряд/место.
            if not area:
                area = u"0"
            else:
                area = area.strip()
            if not row:
                row = u"0"
            else:
                row = row.strip()
            if not seat:
                seat = u"0"
            else:
                seat = seat.strip()
#            print 'area ' + str(type(area))
#            print 'row ' + str(type(row))
#            print 'seat' + str(type(seat))

            # Фамилия заказчика.
            if not cust_ln:
                cust_ln = UNKNOWN_NAME
            else:
                cust_ln = cust_ln.lower().strip().capitalize()
                cust_ln = re.sub(r'ё', r'е', cust_ln)
                cust_ln = re.sub(r'Ё', r'Е', cust_ln)
#            print 'cust_ln ' + cust_ln

            # Инициалы заказчика.
            if not cust_initials:
                cust_initials = u""
            else:
                cust_initials = cust_initials.strip().upper()
#            print 'cust_initials ' + cust_initials

            # Город.
            if not city:
                city = UNKNOWN_NAME  # Если в базе был Null.
            else:
                city = city.lower().strip().capitalize()
            if not street:
                street = u""
            else:
                street = street.lower().strip().capitalize()
                street = re.sub(r'ё', r'е', street)
                street = re.sub(r'Ё', r'Е', street)
            if not house:
                house = u""
            else:
                house = house.lower().strip().lower()
            if not block:
                block = u""
            else:
                block = unicode(block)
            if not flat:
                flat = u""
            else:
                flat = unicode(flat)
#            print 'city ' + city
#            print 'street ' + street
#            print 'house ' + house
#            print 'block ' + block

            if not comment:
                comment = u"" 

#            print type(kvit)
            if not kvit:
                kvit = u"" 
            else:
                kvit = unicode(kvit)
#            print 'kvit ' + kvit

            if not comment:
                comment = u"" 
            else:
                comment = comment.strip()
                comment = re.sub(r'ё', r'е', comment)
                comment = re.sub(r'Ё', r'Е', comment)

#            print 'phone'
#            print type(phone)
            if not phone:
                phone = u"" 
            else:
                phone = unicode(phone)
#            print type(phone)
#            print 'phone ' + phone

#            print '---------------------------------------'

            # Захороненный.
            deadman = Person(creator=creator)
            deadman.last_name = ln
            if fn:
                deadman.first_name = fn
                if ptrc:
                    deadman.patronymic = ptrc
            else:
                initials = re.sub(r"[\.\,]", " ", initials.strip()).split()
                if initials:
                    deadman.first_name = initials[0]
                    if len(initials) > 1:
                        deadman.patronymic = initials[1]
            deadman.save()

            # Заказчик.
            customer = Person(creator=creator)
            customer.last_name = cust_ln
            if cust_initials:
                cust_initials = re.sub(r"[\.\,]", " ", cust_initials).split()
                if cust_initials:
                    customer.first_name = cust_initials[0]
                    if len(cust_initials) > 1:
                        customer.patronymic = cust_initials[1]

            # Адрес заказчика.
            location = Location()
            if street:
                # Присутствуют город и улица - будем создавать Location.
                cities = GeoCity.objects.filter(name__iexact=city)
                if cities:
                    cust_city = cities[0]
                else:
                    cust_city = GeoCity()
                    cust_city.country = GeoCountry.objects.get(name__iexact=UNKNOWN_NAME)
                    cust_city.region = GeoRegion.objects.get(name__iexact=UNKNOWN_NAME)
                    cust_city.name = city
                    cust_city.save()
                try:
                    cust_street = Street.objects.get(city=cust_city, name__iexact=street)
                except ObjectDoesNotExist:
                    cust_street = Street(city=cust_city, name=street)
                    cust_street.save()
                location.street = cust_street
                if house:
                    location.house = house
                    if block:
                        location.block = block
                    if flat:
                        location.flat = flat
            location.save()
            customer.location = location
            customer.save()

            # Место.
#            cemetery = cd["cemetery"]
            try:
                place = Place.objects.get(cemetery=cemetery, area__iexact=area, row__iexact=row,
                                          seat__iexact=seat)
            except ObjectDoesNotExist:
                place = Place(creator=creator)
                place.cemetery = cemetery
                place.area = area
                place.row = row
                place.seat = seat
                place.soul = cemetery.organization.soul_ptr
                place.name = u"%s.уч%sряд%sместо%s" % (place.cemetery.name, place.area, place.row, place.seat)
                place.p_type = ProductType.objects.get(uuid=settings.PLACE_PRODUCTTYPE_ID)
                place.save()

            # Захоронение.
            burial = Burial(creator=creator)
            burial.person = deadman
            burial.account_book_n = n
            burial.responsible = place.cemetery.organization.soul_ptr
            burial.customer = customer
            burial.doer = creator
            burial.date_fact = bur_date
#                        try:
#                            test_date = datetime.datetime.date(bur_date).strftime("%d.%m.%Y")
            burial.product = place.product_ptr
            operation = Operation.objects.get(uuid=settings.OPER_1) # Захоронение
                
            if u"захоронение детское" in comment.lower():
                operation = Operation.objects.get(uuid=settings.OPER_6)
            elif u"захоронение в существ" in comment.lower():
                operation = Operation.objects.get(uuid=settings.OPER_3)
            elif u"почетное захоронение" in comment.lower():
                operation = Operation.objects.get(uuid=settings.OPER_2)
            elif u"подзахоронение" in comment.lower():
                operation = Operation.objects.get(uuid=settings.OPER_4)
            elif u"захоронение" in comment.lower():
                operation = Operation.objects.get(uuid=settings.OPER_1)
            elif u"урна" in comment.lower():
                operation = Operation.objects.get(uuid=settings.OPER_5)
            burial.operation = operation
            burial.save()
            if comment != u"":
                burial.add_comment(comment, creator)
            if phone:
                ph = Phone(soul = customer.soul_ptr)
                ph.f_number = phone
                ph.save()
            if kvit:
                ds = DeathCertificate(soul = deadman.soul_ptr)
                ds.s_number = kvit
                ds.save()

        except Exception, err_descr:
            print err_descr
            # Откатываем транзакцию.
            transaction.rollback()
            ws.write(errow, 0, unicode(err_descr))
            ws.write(errow, 1, sh.cell_value(rx, colx=1))
            ws.write(errow, 2, sh.cell_value(rx, colx=2))
            ws.write(errow, 3, sh.cell_value(rx, colx=3))
            ws.write(errow, 4, sh.cell_value(rx, colx=4))
            ws.write(errow, 5, sh.cell_value(rx, colx=5))
            ws.write(errow, 6, sh.cell_value(rx, colx=6))
            ws.write(errow, 7, sh.cell_value(rx, colx=7))
            ws.write(errow, 8, sh.cell_value(rx, colx=8))
            ws.write(errow, 9, sh.cell_value(rx, colx=9))
            ws.write(errow, 10, sh.cell_value(rx, colx=10))
            ws.write(errow, 11, sh.cell_value(rx, colx=11))
            ws.write(errow, 12, sh.cell_value(rx, colx=12))
            ws.write(errow, 13, sh.cell_value(rx, colx=13))
            ws.write(errow, 14, sh.cell_value(rx, colx=14))
            ws.write(errow, 15, sh.cell_value(rx, colx=15))
            ws.write(errow, 16, sh.cell_value(rx, colx=16))
            ws.write(errow, 17, sh.cell_value(rx, colx=17))
            ws.write(errow, 18, sh.cell_value(rx, colx=18))
            ws.write(errow, 19, sh.cell_value(rx, colx=19))
            errow = errow + 1
        else:
            # Коммитим все.
            transaction.commit()
        db.reset_queries()
        wb.save('import_errors.xls')

myfunction()
