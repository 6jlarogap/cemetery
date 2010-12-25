# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from common.models import Organization, Location, GeoCountry, GeoRegion
from common.models import GeoCity, Street, Cemetery, Person, PersonRole, Operation
from common.models import Phone, Role, UserProfile, SoulProducttypeOperation

@transaction.commit_on_success
def main():
    admin = User.objects.filter(is_superuser=True).order_by("id")[0]

    organization = Organization(creator=admin)
    org_name = raw_input("Введите название организации:")
    organization.name = org_name
    organization.save()
    print "Организация создана."

    # SoulProducttypeOperation
    operations = Operation.objects.all()
    p_type = settings.PLACE_PRODUCTTYPE_ID
    for op in operations:
        spo = SoulProducttypeOperation()
        spo.soul = organization.soul_ptr
        spo.p_type = p_type
        spo.operation = op
        spo.save()

    # Location.
    org_location = Location()
    # Страна.
    org_location_country = raw_input("Введите страну:")
    try:
        country = GeoCountry.objects.get(name__iexact=org_location_country)
    except ObjectDoesNotExist:
        country = GeoCountry(name=org_location_country.capitalize())
        country.save()
        print "Создана новая страна."
    # Регион.
    org_location_region = raw_input("Введите регион:")
    try:
        region = GeoRegion.objects.get(name__iexact=org_location_region,
                                       country=country)
    except ObjectDoesNotExist:
        region = GeoRegion(name=org_location_region.capitalize(), country=country)
        region.save()
        print "Создан новый регион."
    # Нас. пункт.
    org_location_city = raw_input("Введите нас. пункт:")
    try:
        city = GeoCity.objects.get(name__iexact=org_location_city, region=region)
    except ObjectDoesNotExist:
        city = GeoCity(name=org_location_city.capitalize(), country=country,
                       region=region)
        city.save()
        print "Создан новый нас. пункт."
    # Улица.
    org_location_street = raw_input("Введите улицу:")
    try:
        street = Street.objects.get(name__iexact=org_location_street, city=city)
    except ObjectDoesNotExist:
        street = Street(name=org_location_street.capitalize(), city=city)
        street.save()
        print "Создана новая улица."
    # Продолжаем с Location.
    org_location.street = street
    org_location_house = raw_input("Введите номер дома(не обязательно):")
    if org_location_house:
        org_location.house = org_location_house
        org_location_block = raw_input("Введите корпус дома(не обязательно):")
        if org_location_block:
            org_location.block = org_location_block
        org_location_building = raw_input("Введите строение дома(не обязательно):")
        if org_location_building:
            org_location.building = org_location_building
    org_location.save()
    organization.location = org_location
    organization.save()

    # Кладбище.
    cemetery = Cemetery(creator=admin, location=org_location,
                        organization=organization)
    cemetery_name = raw_input("Введите название кладбища:")
    cemetery.name = cemetery_name
    cem_addr_var = input("Адрес кладбища отличается от адреса организации? Да-1. Нет-2. ")
    if cem_addr_var == 1:
        cem_location = Location()
        cem_location_street = raw_input("Введите улицу:")
        try:
            cem_street = Street.objects.get(name__iexact=cem_location_street, city=city)
        except ObjectDoesNotExist:
            cem_street = Street(name=cem_location_street.capitalize(), city=city)
            cem_street.save()
        cem_location.street = cem_street
        cem_location_house = raw_input("Введите номер дома(не обязательно):")
        if org_location_house:
            cem_location.house = cem_location_house
            cem_location_block = raw_input("Введите корпус дома(не обязательно):")
            if cem_location_block:
                cem_location.block = cem_location_block
            cem_location_building = raw_input("Введите строение дома(не обязательно):")
            if cem_location_building:
                cem_location.building = cem_location_building
        cem_location.save()
        cemetery.location = cem_location
    cemetery.save()
    print "Создано новое кладбище."

    # Директор.
    print "\nВведите данные директора."
    login = raw_input("Логин(латинскими буквами):")
    dir_last_name = raw_input("Фамилия:")
    dir_first_name = raw_input("Имя:")
    dir_patronymic = raw_input("Отчество:")
    while True:
        pass1 = raw_input("Пароль:")
        pass2 = raw_input("Пароль (еще раз):")
        if pass1 and pass1==pass2:
            break
        print "Пароли пустые либо не совпадают! Попробуйте еще раз."
    dir_phone = raw_input("Телефон(не обязательно):")
    person = Person(last_name=dir_last_name.capitalize(),
                    first_name=dir_first_name.capitalize(),
                    patronymic=dir_patronymic.capitalize(),
                    creator=admin)
    person.save()
    if dir_phone:
        phone = Phone(soul=person.soul_ptr, f_number=dir_phone)
        phone.save()

    # Роль.
    role = Role(creator=admin, name="Директор", organization=organization)
    role.save()
    person_role = PersonRole(person=person, role=role, creator=admin)
    person_role.save()

    # Системный пользователь django.
    user = User.objects.create_user(username=login.strip(), email="",
                                    password=pass1)
    user.last_name = dir_last_name.capitalize()
    user.first_name = dir_first_name.capitalize()
    profile = UserProfile(user=user, soul=person.soul_ptr)
    profile.save()
    ##############
    #if hasattr(cd['role'], "djgroups") and cd['role'].djgroups.all():
        #if cd.get("is_staff", False):
            #user.is_staff = True
        #for djgr in cd['role'].djgroups.all():
            #user.groups.add(djgr)  # Добавляем человека в django-группу, связанную с его ролью.
    ##############

if __name__ == "__main__":
    main()
