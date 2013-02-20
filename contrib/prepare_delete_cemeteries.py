#! /usr/bin/env python
# -*- coding: utf-8 -*-
#                                   Евгений Супрун, suprune20 at gmail com, 2012
# prepare_delete_cemeteries.py
#
# Задача:
#   Получить набор postgresql- команд, подаваемых на вход
#   'psql -U postgres cemetery', удаления определенного кладбища
#   (кладбищей), всех тамошних захоронений и захороненных
#
# Исполняется:
#   python /path/to/этот-сценарий
#   Результат - на stdout
#
# Параметры:
#   Идентификаторы кладбищ, их можно получить
#   из адресной строки браузера, выполнив поиск по какому-то
#   кладбищу, cemetery=...
#
# Пример запуска (удаление двух кладбищ):
#   python prepare_delete_cemeteries.py \
#    f44fac80-a0d4-11e0-afb7-001d7d706c9d 5d09ae98-0e0b-11e2-8afb-080027b313c6 | \
#    psql -U postgres cemetery 2>&1 | tee delete.results.txt
#   На консоли "побегут" DELETE ... DELETE
#   Проверка, как прошло, если не уследили за ходом операции на экране:
#       cat delete.results.txt | grep -v DELETE
#       если пусто, все OK. Или ничего не сделано,
#       если delete.results.txt пустой :)
#
# Недостатки:
#   *   В б.д, возможно, остается еще что-то, привязанные
#       исключительно к удаленным из б.д захороненным, захоронениям,
#       заказчикам захоронений, кладбищам.
#       Дальнейшей работе с оставшимися в б.д кладбищами мешать не должны.
#   *   Процедура успешно отработала на определенном объекте, но на каком-то
#       другом не исключены не учтенные здесь referential constraints.
#       Смотрите на вывод (stderr, stdout) команды 'psql -U postgres cemetery',
#       на вход которой подается stdout этой процедуры.


import sys
sys.path.append('/home/django/projects/cemetery')

from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.core.exceptions import ObjectDoesNotExist
from common.models import Burial, Cemetery

for cemetery_id in sys.argv[1:]:
    for burial in Burial.objects.filter(product__place__cemetery=cemetery_id):
        person_id = burial.person_id
        order_id = burial.order_ptr_id
        customer_id = burial.customer_id
        location_id = burial.customer.location_id

        # захоронение
        print "DELETE FROM common_burial WHERE person_id='%s';" % person_id
        
        # захороненный
        print "DELETE FROM common_person WHERE soul_ptr_id='%s';" % person_id
        print "DELETE FROM common_soul WHERE uuid='%s';" % person_id
        
        # заказ на захоронение
        print "DELETE FROM common_orderfiles WHERE order_id = '%s';" % order_id
        print "DELETE FROM common_ordercomments WHERE order_id = '%s';" % order_id
        print "DELETE FROM common_order WHERE uuid = '%s';" % order_id
        
        # заказчик
        print "DELETE FROM common_phone WHERE soul_id='%s';" % customer_id
        print "DELETE FROM common_person WHERE soul_ptr_id='%s';" % customer_id
        print "DELETE FROM common_soul WHERE uuid='%s';" % customer_id
        # Каждому заказчику присваивается свой location_id,
        # Даже если у какого-то другого заказчика идентичный адрес.
        # Даже если адрес не указан.
        print "DELETE FROM common_location WHERE uuid='%s';" % location_id
    
    try:
        cemetery = Cemetery.objects.get(pk=cemetery_id)
        # могилы
        print "DELETE FROM common_place WHERE cemetery_id='%s';" % cemetery_id

        # кладбище
        location_id = cemetery.location_id
        print "DELETE FROM common_cemetery WHERE uuid='%s';" % cemetery_id
        # cemetery location_id теоретически может быть NULL
        if location_id:
            print "DELETE FROM common_location WHERE uuid='%s';" % location_id
    except ObjectDoesNotExist:
      pass
