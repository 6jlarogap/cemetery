# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import simplejson

import datetime
from geo.models import Location, City, Region, Country
from organizations.models import Organization, Agent, Doverennost
from persons.models import Person, DeathCertificate, PersonID
from utils.models import PER_PAGE_VALUES, ORDER_BY_VALUES

class Cemetery(models.Model):
    """
    Кладбище.
    """

    organization = models.ForeignKey(Organization, related_name="cemetery", verbose_name=u'Организация')
    location = models.ForeignKey(Location, blank=True, null=True, verbose_name=u'Адрес')
    name = models.CharField(u"Название", max_length=255, blank=True)
    creator = models.ForeignKey(User, editable=False)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    ordering = models.PositiveIntegerField(blank=True, default=1, verbose_name=u'Сортировка')

    class Meta:
        ordering = ['ordering', 'name']
        verbose_name = (u'кладбище')
        verbose_name_plural = (u'кладбища')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_sync_date = datetime.datetime(2000, 1, 1, 0, 0)
        super(Cemetery, self).save(*args, **kwargs)

class Place(models.Model):
    """
    Место.
    """
    cemetery = models.ForeignKey(Cemetery, verbose_name=u"Кладбище")  # Связь с кладбищем.
    area = models.CharField(u"Участок", max_length=255, blank=True, null=True)  # Участок.
    row = models.CharField(u"Ряд", max_length=255, blank=True, null=True)  # Ряд.
    seat = models.CharField(u"Место", max_length=255)  # Место.
    gps_x = models.FloatField(u"Координата X", blank=True, null=True, editable=False)  # GPS X-ось.
    gps_y = models.FloatField(u"Координата Y", blank=True, null=True, editable=False)  # GPS Y-ось.

    responsible = models.ForeignKey(Person, blank=True, null=True) # Ответственный за захоронением
    rooms = models.PositiveIntegerField(u"Мест в ограде", default=1, blank=True)

    creator = models.ForeignKey(User, verbose_name=u"Создатель записи", editable=False)  # Создатель записи.
    date_of_creation = models.DateTimeField(u"Дата создания записи", auto_now_add=True)  # Дата создания записи.

    def save(self, *args, **kwargs):
        """
        Всегда приводим area/row/seat к нижнему регистру.
        """
        self.area = self.area.lower()
        self.row = self.row.lower()

        if self.seat:
            self.seat = self.seat.lower()

        if self.rooms is None:
            self.rooms = 1

        super(Place, self).save(*args, **kwargs)

    def generate_seat(self):
        y = str(datetime.date.today().year)
        max_seat = str(Place.objects.filter(cemetery=self.cemetery, seat__startswith=y).aggregate(models.Max('seat'))['seat__max']) or ''
        if max_seat.startswith(y):
            current_seat = int(float(max_seat)) + 1
        else:
            current_seat = y + '0001'
        self.seat = str(current_seat)
        return self.seat

    @property
    def rooms_occupied(self):
        return (self.rooms or 0) - (self.rooms_free or 0)

    def count_burials(self):
        siblings = Burial.objects.filter(
            product__place__cemetery = self.cemetery,
            product__place__area = self.area,
            product__place__row = self.row,
            product__place__seat = self.seat,
            exhumated_date__isnull = True,
            is_trash = False,
        )
        return siblings.distinct().count()

    def __unicode__(self):
        return  '%s, %s, %s (%s)' % (self.area, self.row, self.seat,
                                     self.cemetery)

class Operation(models.Model):
    """
    Операция
    """

    op_type = models.CharField(u"Имя операции", max_length=255)
    ordering = models.PositiveSmallIntegerField(u"Сортировка", default=1)

    def __unicode__(self):
        return self.op_type[:24]

    class Meta:
        ordering = ['ordering', 'op_type']
        verbose_name = (u'операция с продуктом')
        verbose_name_plural = (u'операции с продуктом')


class Burial(models.Model):
    """
    Захоронение.
    """
    account_number = models.CharField(u"Номер в книге учета", max_length=255, null=True, blank=True)
    operation = models.ForeignKey(Operation, verbose_name=u"Операция")
    date_plan = models.DateField(u"Планируемая дата", blank=True, null=True)
    date_fact = models.DateField(u"Фактическая дата исполнения", blank=True, null=True)
    time_fact = models.TimeField(u"Время исполнения", blank=True, null=True)

    place = models.ForeignKey(Place)
    person = models.ForeignKey(Person, verbose_name=u"Похороненный", related_name='buried')

    client_person = models.ForeignKey(Person, blank=True, null=True, related_name='ordr_customer')                # Заказчик (физ- или юрлицо)
    client_organization = models.ForeignKey(Organization, blank=True, null=True, related_name='ordr_customer')                # Заказчик (физ- или юрлицо)
    doverennost = models.ForeignKey(Doverennost, null=True, blank=True)

    agent = models.ForeignKey(Agent, blank=True, null=True, related_name='orders')             # Агент Заказчика-юрлица

    acct_num_str1 = models.CharField(editable=False, null=True, max_length=255)
    acct_num_num = models.PositiveIntegerField(editable=False, null=True)
    acct_num_str2 = models.CharField(editable=False, null=True, max_length=255)

    print_info = models.TextField(editable=False, null=True)
    payment_type = models.CharField(u"Платеж", max_length=255, choices=[
        ('nal', u"Нал"),
        ('beznal', u"Безнал"),
    ], default='nal', blank=False)

    creator = models.ForeignKey('auth.User', null=True, editable=False)
    deleted = models.BooleanField(editable=False, default=False)  # Удален.

    class Meta:
        verbose_name = (u'захоронение')
        verbose_name_plural = (u'захоронения')
        #ordering = ['person__last_name',]

    def __unicode__(self):
        return u"захоронение: %s" % self.person.__unicode__()

    def last_change(self):
        from django.contrib.admin.models import LogEntry, ContentType
        ct = ContentType.objects.get_for_model(Burial)
        try:
            return LogEntry.objects.filter(object_id=self.pk, content_type=ct).exclude(action_time=self.date_of_creation).order_by('-id')[0]
        except IndexError:
            return None


    def get_print_info(self):
        if self.print_info:
            data = simplejson.loads(self.print_info)
            for p in data['positions'] or []:
                try:
                    p['service'] = Service.objects.get(name=p.get('service', p['order_product']))
                except (Service.DoesNotExist, KeyError):
                    pass
            return data
        else:
            return {
                'positions': None,
                'print': None,
                }

    def set_print_info(self, data):
        for p in data['positions']:
            p['price'] = u'%s' % p['price']
            p['count'] = u'%s' % p['count']
            try:
                p['service'] = p['service'].name
            except KeyError:
                pass
        if data['print']['catafalque_time']:
            data['print']['catafalque_time'] = data['print']['catafalque_time'].strftime('%H:%M')
        self.print_info = simplejson.dumps(data)

    @property
    def ceo_name(self):
        return self.organization and self.organization.ceo_name or ''

    def full_customer_name(self):
        try:
            agent = self.agent
            org = agent.organization
        except:
            pass
        else:
            return u"%(org)s, в лице агента %(agent)s, действующего на основании доверенности №%(d_num)s от %(d_date)s" % {
                'org': org.full_name or org,
                'agent': agent,
                'd_num': self.doverennost and self.doverennost.number or '',
                'd_date': self.doverennost and self.doverennost.date and self.doverennost.date.strftime('%d.%m.%Y') or '',
            }

        if self.client_organization:
            return u"%(org)s, в лице директора %(ceo)s, действующего на основании %(doc)s" % {
                'org': self.client_organization.full_name or self.client_organization,
                'ceo': self.client_organization.ceo_name_who,
                'doc': self.client_organization.ceo_document,
            }

        return self.client_person and self.client_person.full_human_name() or ''

    @staticmethod
    def split_parts(self):
        p1, p2, p3 = split_number(self.account_book_n)
        self.acct_num_str1 = p1
        self.acct_num_num = p2
        self.acct_num_str2 = p3

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.generate_account_number()

        if not self.date_fact:
            self.date_fact = datetime.datetime.now()

        self.last_sync_date = datetime.datetime(2000, 1, 1, 0, 0)
        # self.split_parts(self)
        super(Burial, self).save(*args, **kwargs)

    def generate_account_number(self):
        y = str(datetime.date.today().year)
        siblings = Burial.objects.filter(place__cemetery=self.place.cemetery, account_number__istartswith=y)
        max_num = str(siblings.aggregate(max_number=models.Max('account_number'))['max_number']) or ''
        if max_num.startswith(y):
            current_num = int(float(max_num)) + 1
        else:
            current_num = y + '0001'
        self.account_number = str(current_num)
        return self.account_number

    def generate_seat_number(self):
        y = str(datetime.date.today().year)
        siblings = Burial.objects.filter(product__place__cemetery=self.product.place.cemetery, product__place__seat__istartswith=y)
        max_num = str(siblings.aggregate(seat=models.Max('product__place__seat'))['seat']) or ''
        if max_num.startswith(y):
            current_num = int(float(max_num)) + 1
        else:
            current_num = y + '0001'
        self.account_book_n = str(current_num)
        return self.account_book_n

    def relative_burials(self):
        burials = Burial.objects.exclude(account_book_n=self.account_book_n)
        burials = burials.filter(
            product__place__cemetery=self.product.place.cemetery,
            product__place__area=self.product.place.area,
            product__place__row=self.product.place.row,
            product__place__seat=self.product.place.seat,
        )
        return burials

class UserProfile(models.Model):
    """
    Профиль пользователя.
    """
    user = models.OneToOneField(User, primary_key=True, editable=False)

    default_cemetery = models.ForeignKey(Cemetery, verbose_name=u"Кладбище",blank=True, null=True)  # Связь с кладбищем.
    default_operation = models.ForeignKey(Operation, verbose_name=u"Услуга", blank=True, null=True)
    default_country = models.ForeignKey(Country, verbose_name=u"Страна",blank=True, null=True)  # Страна.
    default_region = models.ForeignKey(Region, verbose_name=u"Регион",blank=True, null=True)  # Регион.
    default_city = models.ForeignKey(City, verbose_name=u"Город",blank=True, null=True)  # Город.
    records_per_page = models.PositiveSmallIntegerField(u"Записей на странице",blank=True, null=True,choices=PER_PAGE_VALUES)
    records_order_by = models.CharField(u"Сортировка по", max_length=255,blank=True, choices=ORDER_BY_VALUES)

    org_user = models.ForeignKey(Organization, verbose_name=u"Пользователь", blank=True, null=True, related_name='org_users')
    org_registrator = models.ForeignKey(Organization, verbose_name=u"Регистратор", blank=True, null=True, related_name='org_registrators')

    catafalque_text = models.TextField(u"Текст в наряде на а/к", blank=True, default='')
    naryad_text = models.TextField(u"Текст во всех нарядах", blank=True, default='')

    person = models.ForeignKey(Person, null=True, editable=False)
    organization = models.ForeignKey(Organization, null=True, editable=False)

    def __unicode__(self):
        return self.user.username


def set_last_name(sender, instance, **kwargs):
    instance.last_name = instance.last_name.capitalize()
    instance.first_name = instance.first_name.capitalize()
    instance.middle_name = instance.middle_name.capitalize()
models.signals.pre_save.connect(set_last_name, sender=Person)

def set_dc(sender, instance, **kwargs):
    instance.s_number = instance.s_number.upper()
    instance.series = instance.series.upper()
models.signals.pre_save.connect(set_dc, sender=DeathCertificate)

def set_id_doc(sender, instance, **kwargs):
    instance.number = instance.number.upper()
    instance.series = instance.series.upper()
models.signals.pre_save.connect(set_id_doc, sender=PersonID)

def set_dover(sender, instance, **kwargs):
    instance.number = instance.number.upper()
models.signals.pre_save.connect(set_dover, sender=Doverennost)

class Service(models.Model):
    """
    Продукт в заказе.
    """
    name = models.CharField(u"Название продукта", max_length=255)
    default = models.BooleanField(u"Вкл. по умолчанию", default=False, blank=True)
    measure = models.CharField(u"Единицы измерения", max_length=255, blank=True)
    price = models.DecimalField(u"Цена", decimal_places=2, max_digits=10)
    ordering = models.PositiveSmallIntegerField(u"Сортировка", default=1)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = (u'тип продукта для счет-заказа')
        verbose_name_plural = (u'типы продуктов для счет-заказа')

class ServicePosition(models.Model):
    """
    Позиция в заказе.
    """
    burial = models.ForeignKey(Burial)
    service = models.ForeignKey(Service)
    count = models.DecimalField(u"Кол-во", decimal_places=2, max_digits=10)
    price = models.DecimalField(u"Цена", decimal_places=2, max_digits=10)

    @property
    def sum(self):
        return self.count * self.price

    def __unicode__(self):
        return self.uuid

    class Meta:
        verbose_name = (u'позиция счет-заказа')
        verbose_name_plural = (u'позиция счет-заказа')

