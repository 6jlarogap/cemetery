# -*- coding: utf-8 -*-

import csv
import re
import datetime
#from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from common.models import Person, Location, GeoCountry, GeoRegion, GeoCity, Street, Burial, Place, ProductType


"""
Создаем нового усопшего и нового заказчика.
Имя и отчество берем из соотв-х полей, либо, если пусто, из инициалов.
Ищем город. Если не находим - создаем новый

Модели:
Burial(Order):
Person для захоронненного
Person для заказчика
Place для захоронения
Location для заказчика
OrderComments для комментария (и берем из него услугу для Order)
"""

#admin = User.objects.filter(is_superuser=True).order_by("id")[0]
request = None # !!!!!!!!!!!!!!!!!!

csv.register_dialect("4mysql", escapechar="\\", quoting=csv.QUOTE_NONE)
f = open("/tmp/1.csv")
r = csv.reader(f, "4mysql")
for i in r:
    if i:
        (n, ln, fn, ptrc, initials, bur_date, area, row, seat, cust_ln, cust_fn, cust_ptrc, cust_initials, city, street,
         house, block, flat, comment) = i
        if ln == "N":
            ln = ""
        if fn == "N":
            fn = ""
        if ptrc == "N":
            ptrc = ""
        if initials == "N":
            initials = ""
        if cust_ln == "N":
            cust_ln = ""
        if cust_fn == "N":
            cust_fn = ""
        if cust_ptrc == "N":
            cust_ptrc = ""
        if cust_initials == "N":
            cust_initials = ""
        if city == "N":
            city = ""
        if street == "N":
            street = ""
        if house == "N":
            house = ""
        if block == "N":
            block = ""
        if flat == "N":
            flat = ""
        if comment == "N":
            comment = ""
        print n, ln, fn, ptrc, initials, bur_date, area, row, seat, cust_ln, cust_fn, cust_ptrc, cust_initials, city, street, house, block, flat, comment
        # Захороненный.
        deadman = Person(creator=request.user)
#        if ln.strip():
        deadman.last_name = ln.strip().capitalize()
        if fn.strip():
            deadman.first_name = fn.strip().capitalize()
            if ptrc.strip():
                deadman.patronymic = ptrc.strip().capitalize()
        else:
            initials = re.sub(r"[\.\,]", " ", initials.strip()).split()
            if initials:
                deadman.first_name = initials[0].capitalize()
                if len(initials) > 1:
                    deadman.patronymic = initials[1].capitalize()
        deadman.save()

        # Заказчик.
        customer = Person(creator=request.user)
#        if cust_ln.strip():
        customer.last_name = cust_ln.strip().capitalize()
        if cust_fn.strip():
            customer.first_name = cust_fn.strip().capitalize()
            if cust_ptrc.strip():
                customer.patronymic = cust_ptrc.strip().capitalize()
        else:
            cust_initials = re.sub(r"[\.\,]", " ", cust_initials.strip()).split()
            if cust_initials:
                customer.first_name = cust_initials[0].capitalize()
                if len(cust_initials) > 1:
                    customer.patronymic = cust_initials[1].capitalize()
                    
        # Адрес заказчика.
        location = Location()
        if street.strip():
            # Присутствуют город и улица - будем создавать Location.
#            cities = GeoCity.objects.filter(name__iexact=city.strip()).order_by("country__id")
            cities = GeoCity.objects.filter(name__iexact=city.strip())
            if cities:
                cust_city = cities[0]
            else:
                cust_city = GeoCity.objects.get(name__iexact="Отсутствует")
            try:
                cust_street = Street.objects.get(city=cust_city, name__iexact=street.strip())
            except ObjectDoesNotExist:
                cust_street = Street(city=cust_city, name=street.strip().capitalize())
                cust_street.save()
            location.street = cust_street
            if house.strip():
                location.house = house.strip()
                if block.strip():
                    location.block = block.strip()
                if flat.strip():
                    location.flat = flat.strip()
        location.save()
        customer.location = location  # Проверить, работает ли!!!
        customer.save()

        # Место.
        cemetery = "Кладбище будет выбираться на странице из списка"
        try:
            place = Place.objects.get(cemetery=cemetery, area__iexact=area.strip(), row__iexact=row.strip(),
                                      seat__iexact=seat.strip())
        except ObjectDoesNotExist:
            place = Place(creator=request.user)
            place.cemetery = cemetery
            place.area = area.strip().lower()
            place.row = row.strip().lower()
            place.seat = seat.strip().lower()
            place.soul = cemetery.organization.soul_ptr  # To check!
            place.name = u"Место захоронения"
            place.p_type = ProductType.objects.get(id=settings.PLACE_PRODUCTTYPE_ID)
            place.save()

        # Захоронение.
        burial = Burial(creator=request.user)
        burial.person = deadman
        burial.account_book_n = n.strip()
        burial.customer = customer
        burial.responsible = XXX
        burial.date_fact = datetime.datetime.strptime(bur_date, "%Y-%m-%d  %H:%M:%S")
        burial.product = place.product_ptr
#        burial.operation =
        """
        add_comment()
        """

            


        """
        first_name
        last_name
        patronymic
        location
        creator
        """