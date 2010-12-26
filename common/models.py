# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

from stdimage import StdImageField
from south.modelsinspector import add_introspection_rules

#import datetime
#import os
#import re

from django_extensions.db.fields import UUIDField


rules = [
    (
        (StdImageField, ),
        [],
        {
            "size": ["size", {"default": None}],
            "thumbnail_size": ["thumbnail_size", {"default": None}],
            },
        ),
]
add_introspection_rules(rules, ["^stdimage\.fields",])


#def get_file_path(instance, filename):
    #filename = re.sub(r'\s', r'_', filename)
    #return os.path.join('attach/', instance.person.soul.uuid, filename)

PER_PAGE_VALUES = (
    (5, '5'),
    (10, '10'),
    (15, '15'),
    (25, '25'),
    (50, '50'),
    (100, '100'),
    (500, '500'),
)

ORDER_BY_VALUES = (
    ('person__last_name', '+фамилии'),
    ('-person__last_name', '-фамилии'),
    ('person__first_name', '+имени'),
    ('-person__first_name', '-имени'),
    ('person__patronymic', '+отчеству'),
    ('-person__patronymic', '-отчеству'),
    ('bur_date', '+дате захоронения'),
    ('-bur_date', '-дате захоронения'),
    ('account_book_n', '+номеру в книге учета'),
    ('-account_book_n', '-номеру в книге учета'),
    ('place__area', '+участку'),
    ('-place__area', '-участку'),
    ('place__row', '+ряду'),
    ('-place__row', '-ряду'),
    ('place__seat', '+месту'),
    ('-place__seat', '-месту'),
    ('place__cemetery', '+кладбищу'),
    ('-place__cemetery', '-кладбищу'),
    #('comment', '+комментарию'),
    #('-comment', '-комментарию'),
)

#class Country_old(models.Model):
    #"""
    #Страна.
    #"""
    #uuid = UUIDField(primary_key=True)
    #name = models.CharField(max_length=30)  # Название.
    #class Meta:
        #ordering = ['uuid']
    #def __unicode__(self):
        #return self.name

class GeoCountry(models.Model):
    """
    Страна.
    """
    uuid = UUIDField(primary_key=True)
    name = models.CharField("Название", max_length=24, db_index=True, unique=True)
    def __unicode__(self):
        return self.name[:24]
    class Meta:
        #managed = False
        #db_table = "common_country"
        ordering = ['name']
        verbose_name = 'страна'
        verbose_name_plural = 'страны'


class GeoRegion(models.Model):
    """
    Регион.
    """
    uuid = UUIDField(primary_key=True)
    country = models.ForeignKey(GeoCountry)
    name = models.CharField("Название", max_length=36, db_index=True)
    def __unicode__(self):
        return self.name[:24]
    class Meta:
        unique_together = (("country", "name"),)
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'


class GeoCity(models.Model):
    """
    Город.
    """
    uuid = UUIDField(primary_key=True)
    country = models.ForeignKey(GeoCountry)
    region = models.ForeignKey(GeoRegion)
    name = models.CharField("Название", max_length=36, db_index=True)
    def __unicode__(self):
        return self.name[:24]
    class Meta:
        unique_together = (("region", "name"),)
        verbose_name = 'населенный пункт'
        verbose_name_plural = 'населенные пункты'


class Metro(models.Model):
    """
    Метро.
    """
    uuid = UUIDField(primary_key=True)
    city = models.ForeignKey(GeoCity)  # Город.
    name = models.CharField(max_length=99)  # Название.
    class Meta:
        ordering = ['city', 'name']
    def __unicode__(self):
        return self.name


class Street(models.Model):
    """
    Улица.
    """
    uuid = UUIDField(primary_key=True)
    city = models.ForeignKey(GeoCity)  # Город.
    name = models.CharField(max_length=99, db_index=True)  # Название.
    class Meta:
        ordering = ['city', 'name']
        unique_together = (("city", "name"),)
    def __unicode__(self):
        return self.name


class Location(models.Model):
    """
    Адрес.
    """
    uuid = UUIDField(primary_key=True)
    street = models.ForeignKey(Street, verbose_name="Улица", blank=True, null=True)  # Улица.
    house = models.CharField("Дом", max_length=16, blank=True)  # Дом.
    block = models.CharField("Корпус", max_length=16, blank=True)  # Корпус.
    building = models.CharField("Строение", max_length=16, blank=True)  # Строение.
    flat = models.CharField("Квартира", max_length=16, blank=True)  # Квартира.
    gps_x = models.FloatField("Координата X", blank=True, null=True)  # GPS X-ось.
    gps_y = models.FloatField("Координата Y", blank=True, null=True)  # GPS Y-ось.
    gps_z = models.FloatField("Координата Z", blank=True, null=True)  # GPS Z-ось.
    def __unicode__(self):
        if self.street:
            return u'%s (дом %s, корп. %s, строен. %s, кв. %s)' % (self.street,
                                self.house, self.block, self.building, self.flat)
        else:
            return u"незаполненный адрес"


# Checked.
class Soul(models.Model):
    """
    Душа.
    """
    uuid = UUIDField(primary_key=True)
    birth_date = models.DateField("Дата рождения", blank=True, null=True)
    death_date = models.DateField("Дата смерти", blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)  # Адрес орг-ии или человека (Person).
    creator = models.ForeignKey(User)  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.
    def __unicode__(self):
        if hasattr(self, "person"):
            return u"Физ. лицо: %s" % self.person
        elif hasattr(self, "organization"):
            return u"Юр. лицо: %s" % self.organization
        else:
            return self.uuid
    class Meta:
        ordering = ['uuid']


class Phone(models.Model):
    """
    Телефонный номер.
    """
    uuid = UUIDField(primary_key=True)
    soul = models.ForeignKey(Soul)
    f_number = models.CharField("Номер телефона", max_length=15)  # Телефон.
    class Meta:
        unique_together = (("soul", "f_number"),)
    def __unicode__(self):
        return self.f_number


class Email(models.Model):
    """
    Адрес электронной почты.
    """
    uuid = UUIDField(primary_key=True)
    soul = models.ForeignKey(Soul)
    e_addr = models.EmailField()  # e-mail.


class Person(Soul):
    """
    Физическое лицо (клиент, сотрудник, кто угодно).
    """
    first_name = models.CharField("Имя", max_length=30, blank=True)  # Имя.
    last_name = models.CharField("Фамилия", max_length=30)  # Фамилия.
    patronymic = models.CharField("Отчество", max_length=30, blank=True)  # Отчество.
    #death_certificate = models.CharField("Свидетельство о смерти",
                                         #max_length=30, blank=True)  # Номер свидетельства о смерти.
    roles = models.ManyToManyField("Role", through="PersonRole",
                                   verbose_name="Роли")
    def __unicode__(self):
        if self.last_name:
            result = self.last_name
            if self.first_name:
                result += " %s." % self.first_name[0].upper()
                if self.patronymic:
                    result += "%s." % self.patronymic[0].upper()
        else:
            result = self.uuid
        return result
    class Meta:
        verbose_name = ('физ. лицо')
        verbose_name_plural = ('физ. лица')


class DeathCertificate(models.Model):
    """
    Свидетельство о смерти.
    """
    uuid = UUIDField(primary_key=True)
    soul = models.OneToOneField(Soul)
    s_number = models.CharField("Номер свидетельства", max_length=30,
                                blank=True)  # Номер свидетельства о смерти.
    def __unicode__(self):
        return u"Свид. о смерти (%s)" % self.soul.__unicode__()
    class Meta:
        verbose_name = ('свидетельство о смерти')
        verbose_name_plural = ('свидетельства о смерти')


class Organization(Soul):
    """
    Юридическое лицо.
    """
    ogrn = models.CharField("ОГРН", max_length=15, blank=True)  # ОГРН.
    inn = models.CharField("ИНН", max_length=15, blank=True)  # ИНН.
    name = models.CharField("Название организации", max_length=99) #  Название.
#    main = models.BooleanField("Наша собственная организация", default=False)
    def __unicode__(self):
        return self.name[:24]
    class Meta:
        verbose_name = ('юр. лицо')
        verbose_name_plural = ('юр. лица')


class Role(models.Model):
    """
    Роль в организации.
    """
    uuid = UUIDField(primary_key=True)
    organization = models.ForeignKey(Organization,
                                     verbose_name="Организация")  # Связь с юр. лицом.
    name = models.CharField("Роль", max_length=50, blank=True)  # Название.
    djgroups = models.ManyToManyField(Group, verbose_name="Django-группы",
                                      blank=True, null=True)
    creator = models.ForeignKey(User, verbose_name="Автор")  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.
    def __unicode__(self):
        return u"%s - %s" % (self.organization, self.name)
    class Meta:
        #ordering = ['organization', 'date_of_creation']
        verbose_name = ('роль в организации')
        verbose_name_plural = ('роли в организациях')


class RoleTree(models.Model):
    """
    Кто кому подчиняется в организации.
    Собираемся в будущем усовершенствовать - чтобы у одного начальника сразу несколько подчиненных хранить.
    """
    #uuid = UUIDField(primary_key=True)
    master = models.ForeignKey(Role, related_name='rltree_master')  # Начальник.
    slave = models.ForeignKey(Role, related_name='rltree_slave') # Подчиненный.


# Checked.
class PersonRole(models.Model):
    """
    Роль персоны. Фактически, это сотрудники, которым есть доступ в систему.
    """
    #uuid = UUIDField(primary_key=True)
    person = models.ForeignKey(Person)  # Персона.
    role = models.ForeignKey(Role)  # Роль.
    hire_date = models.DateField("Дата приема на работу", blank=True, null=True)
    discharge_date = models.DateField("Дата увольнения", blank=True, null=True)
    creator = models.ForeignKey(User)  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.
    def __unicode__(self):
        return u"%s - %s" % (self.person.__unicode__(), self.role.__unicode__())
    class Meta:
        unique_together = (("person", "role"),)


# Checked.
class Cemetery(models.Model):
    """
    Кладбище.
    """
    uuid = UUIDField(primary_key=True)
    organization = models.ForeignKey(Organization)  # Связь с душой.
    location = models.ForeignKey(Location, blank=True, null=True)  # Адрес.
    name = models.CharField(max_length=99, blank=True)  # Название.
    creator = models.ForeignKey(User)  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.
    class Meta:
        #ordering = ['name']
        verbose_name = ('кладбище')
        verbose_name_plural = ('кладбища')
    def __unicode__(self):
        return "%s(%s)" % (self.name[:24], self.organization.name[:24])


# Checked.
class ProductType(models.Model):
    """
    Тип продукта.
    """
    name = models.CharField("Имя типа продукта", max_length=24)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = ('тип продукта')
        verbose_name_plural = ('типы продуктов')


# Checked.
class Product(models.Model):
    """
    Продукт.
    """
    uuid = UUIDField(primary_key=True)
    soul = models.ForeignKey(Soul, verbose_name="Душа")  # Кому принадлежит?
    name = models.CharField("Название", max_length=50)  # Название продукта.
    measure = models.CharField("Единицы измерения", max_length=50, blank=True)  # Размерность.
    p_type = models.ForeignKey(ProductType, verbose_name="Тип продукта")
    all_comments = models.TextField("Все комментарии", blank=True)  # Все комментарии, собранные в одно поле.
    def add_comment(self, txt, creator):
        comment = ProductComments(product=self, comment=txt,
                                  creator=creator)
        comment.save()
        if self.all_comments:
            self.all_comments = "%s\n%s" % (self.all_comments, txt)
        else:
            self.all_comments = txt
        self.save()
    def __unicode__(self):
        return self.name


class ProductFiles(models.Model):
    """
    Файлы, связанные с продуктом.
    """
    uuid = UUIDField(primary_key=True)
    product = models.ForeignKey(Product)
    pfile = models.FileField(upload_to="pfiles")
    creator = models.ForeignKey(User, null=True)  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.


class ProductComments(models.Model):
    """
    Комментарии, связанные с продуктом.
    """
    uuid = UUIDField(primary_key=True)
    product = models.ForeignKey(Product)
    comment = models.TextField()  # Комментарий.
    creator = models.ForeignKey(User)  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.
    class Meta:
        ordering = ['date_of_creation']


# OK.
#class SoulProduct(models.Model):
    #"""
    #To add description.
    #"""
    #uuid = UUIDField(primary_key=True)
    #soul = models.OneToOneField(Soul)
    #product = models.OneToOneField(Product)


# Checked.
class Place(Product):
    """
    Место.
    """
    cemetery = models.ForeignKey(Cemetery, verbose_name="Кладбище")  # Связь с кладбищем.
    area = models.CharField("Участок", max_length=9)  # Участок.
    row = models.CharField("Ряд", max_length=9)  # Ряд.
    seat = models.CharField("Место", max_length=9)  # Место.
    gps_x = models.FloatField("Координата X", blank=True, null=True)  # GPS X-ось.
    gps_y = models.FloatField("Координата Y", blank=True, null=True)  # GPS Y-ось.
    gps_z = models.FloatField("Координата Z", blank=True, null=True)  # GPS Z-ось.
    creator = models.ForeignKey(User, verbose_name="Создатель записи")  # Создатель записи.
    date_of_creation = models.DateTimeField("Дата создания записи", auto_now_add=True)  # Дата создания записи.
    def save(self, *args, **kwargs):
        """
        Всегда приводим area/row/seat к нижнему регистру.
        """
        self.area = self.area.lower()
        self.row = self.row.lower()
        self.seat = self.seat.lower()
        super(Place, self).save(*args, **kwargs)
    def __unicode__(self):
        return  '%s, %s, %s (%s)' % (self.area, self.row, self.seat,
                                     self.cemetery)
    class Meta:
        unique_together = (("cemetery", "area", "row", "seat"),)



class Place1(Product): # Места
    #product_ptr = models.ForeignKey(Product)
    cemetery = models.ForeignKey(Cemetery)  # Связь с кладбищем.
    area = models.CharField(max_length=9)  # Участок.
    row = models.CharField(max_length=9)  # Ряд.
    seat = models.CharField(max_length=9)  # Место.
    gps_x = models.FloatField(blank=True, null=True)  # GPS X-ось.
    gps_y = models.FloatField(blank=True, null=True)  # GPS Y-ось.
    gps_z = models.FloatField(blank=True, null=True)  # GPS Z-ось.
    creator = models.ForeignKey(User)  # Создатель записи.
    date_of_creation = models.DateTimeField()  # Дата создания записи.
    s1 = models.TextField(blank=True)
    s2 = models.FloatField(blank=True, null=True)
    s3 = models.TextField(blank=True)
    s4 = models.TextField(blank=True)
    s5 = models.FloatField(blank=True, null=True)
    s6 = models.TextField(blank=True)
    s7 = models.TextField(blank=True)
    s8 = models.FloatField(blank=True, null=True)
    s9 = models.TextField(blank=True)
    class Meta:
        managed = False


class Operation(models.Model):
    """
    Операция с продуктом.
    """
    op_type = models.CharField("Имя операции", max_length=100)
    def __unicode__(self):
        return self.op_type[:24]
    class Meta:
        verbose_name = ('операция с продуктом')
        verbose_name_plural = ('операции с продуктом')


class Order(models.Model):
    """
    Заказ.
    """
    uuid = UUIDField(primary_key=True)
    responsible = models.ForeignKey(Soul, related_name='ordr_responsible')  # Ответственный.
    customer = models.ForeignKey(Soul, related_name='ordr_customer')  # Клиент.
    doer = models.ForeignKey(Soul, blank=True, null=True)  # Исполнитель (работник).
    date_plan = models.DateTimeField(blank=True, null=True)  # Планируемая дата исполнения.
    date_fact = models.DateTimeField("Фактическая дата исполнения", blank=True, null=True)  # Фактическая дата исполнения.
    product = models.ForeignKey(Product, related_name="xxx")  # To change!
    operation = models.ForeignKey(Operation)
    is_trash = models.BooleanField(default=False)  # Удален.
    creator = models.ForeignKey(User)  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.
    all_comments = models.TextField(blank=True)  # Все комментарии, собранные в одно поле.
    def add_comment(self, txt, creator):
        comment = OrderComments(order=self, comment=txt,
                                  creator=creator)
        comment.save()
        if self.all_comments:
            self.all_comments = "%s\n%s" % (self.all_comments, txt)
        else:
            self.all_comments = txt
        self.save()


class OrderFiles(models.Model):
    """
    Файлы, связанные с заказом.
    """
    uuid = UUIDField(primary_key=True)
    order = models.ForeignKey(Order)
#    ofile = models.FileField(upload_to="ofiles")
    ofile = StdImageField("Картинка", upload_to='ofiles', thumbnail_size=(100, 75))
    comment = models.CharField(max_length=96, blank=True)
    creator = models.ForeignKey(User, null=True)  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.


class OrderComments(models.Model):
    """
    Комментарии, связанные с заказом.
    """
    uuid = UUIDField(primary_key=True)
    order = models.ForeignKey(Order)
    comment = models.TextField()  # Комментарий.
    creator = models.ForeignKey(User)  # Создатель записи.
    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.
    class Meta:
        ordering = ['date_of_creation']


#class OrderPosition(models.Model):
#    """
#    Позиция в заказе.
#    """
#    uuid = UUIDField(primary_key=True)
#    order = models.ForeignKey(Order)
#    product = models.ForeignKey(Product, related_name="xxx")  # To change!
#    operation = models.ForeignKey(Operation)
#    creator = models.ForeignKey(User)  # Создатель записи.
#    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.


# Checked.
class Burial(Order):
    """
    Захоронение.
    """
    person = models.ForeignKey(Person, verbose_name="Похороненный", related_name='buried')  # Похороненный.
#    place = models.ForeignKey(Place)
    #order_position = models.ForeignKey(OrderPosition, blank=True, null=True)  # TEMP! To remove blank/null!
#    bur_date = models.DateField()  # Дата захоронения.
#    account_book_n = models.CharField("Номер в книге учета", max_length=9, unique=True)  # Номер записи к книге учета.
    account_book_n = models.CharField("Номер в книге учета", max_length=9)  # Номер записи к книге учета.
#    is_trash = models.BooleanField(default=False)
#    creator = models.ForeignKey(User)  # Создатель записи.
#    date_of_creation = models.DateTimeField(auto_now_add=True)  # Дата создания записи.
    class Meta:
        verbose_name = ('захоронение')
        verbose_name_plural = ('захоронения')
        #ordering = ['person__last_name',]
    def __unicode__(self):
        return u"захоронение: %s" % self.person.__unicode__()


class Burial1(Order): # Захоронения
    #product_ptr = models.ForeignKey(Product)
    person = models.ForeignKey(Person)  # Похороненный.
#    place = models.ForeignKey(Place1)
    #order_position = models.ForeignKey(OrderPosition, blank=True, null=True)  # TEMP! To remove blank/null!
#    bur_date = models.DateField()  # Дата захоронения.
    account_book_n = models.CharField(max_length=9, unique=True)  # Номер записи к книге учета.
#    is_trash = models.BooleanField(default=False)
#    creator = models.ForeignKey(User)  # Создатель записи.
#    date_of_creation = models.DateTimeField()  # Дата создания записи.
    s1 = models.TextField(blank=True, null=True)
    s2 = models.FloatField(blank=True, null=True)
    s3 = models.TextField(blank=True, null=True)
    class Meta:
        managed = False


# OK.
class UserProfile(models.Model):
    """
    Профиль пользователя.
    """
    user = models.OneToOneField(User, primary_key=True)
    soul = models.OneToOneField(Soul)
    default_cemetery = models.ForeignKey(Cemetery, verbose_name="Кладбище",
                                         blank=True, null=True)  # Связь с кладбищем.
    default_operation = models.ForeignKey(Operation, verbose_name="Операция", blank=True, null=True)
    default_country = models.ForeignKey(GeoCountry, verbose_name="Страна",
                                        blank=True, null=True)  # Страна.
    default_region = models.ForeignKey(GeoRegion, verbose_name="Регион",
                                       blank=True, null=True)  # Регион.
    default_city = models.ForeignKey(GeoCity, verbose_name="Город",
                                     blank=True, null=True)  # Город.
    records_per_page = models.PositiveSmallIntegerField("Записей на странице",
                                                    blank=True, null=True,
                                                    choices=PER_PAGE_VALUES)
    records_order_by = models.CharField("Сортировка по", max_length=50,
                                        blank=True, choices=ORDER_BY_VALUES)

    def is_management(self):
        """
        Проверка, входил ли пользователь в группу `управление`.
        """
        try:
            g = self.user.groups.get(name='руководство')
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def __unicode__(self):
        return self.user.username


# Checked.
class SoulProducttypeOperation(models.Model):
    """
    Таблица для связи трех моделей.
    """
    soul = models.ForeignKey(Soul, verbose_name="Душа")
    p_type = models.ForeignKey(ProductType, verbose_name="Тип продукта")
    operation = models.ForeignKey(Operation,
                                  verbose_name="Операция с продуктом")
    def __unicode__(self):
        return u"%s  -  %s  -  %s" % (self.soul.__unicode__(), self.p_type.name,
                             self.operation.op_type[:24])
#        return self.operation.op_type[:36]
    class Meta:
        verbose_name = ('связь типа продукта с операцией')
        verbose_name_plural = ('связи типов продуктов с операциями')
        unique_together = (("soul", "p_type", "operation"),)




