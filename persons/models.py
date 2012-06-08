# -*- coding: utf-8 -*-

from django.db import models

import datetime
from geo.models import Location
from utils.models import UnclearDate

class IDDocumentType(models.Model):
    name = models.CharField(u"Тип документа", max_length=255)

    def __unicode__(self):
        return self.name

class Person(models.Model):
    """
    Физическое лицо (клиент, сотрудник, кто угодно).
    """
    last_name = models.CharField(u"Фамилия", max_length=128)  # Фамилия.
    first_name = models.CharField(u"Имя", max_length=30, blank=True)  # Имя.
    middle_name = models.CharField(u"Отчество", max_length=30, blank=True)  # Отчество.

    birth_date = models.DateField(u"Дата рождения", blank=True, null=True)
    birth_date_no_month = models.BooleanField(default=False, editable=False)
    birth_date_no_day = models.BooleanField(default=False, editable=False)
    death_date = models.DateField(u"Дата смерти", blank=True, null=True)

    address = models.ForeignKey(Location, editable=False)

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

    def get_birth_date(self):
        if not self.birth_date:
            return None
        birth_date = UnclearDate(self.birth_date.year, self.birth_date.month, self.birth_date.day)
        if self.birth_date_no_day:
            birth_date.day = None
        if self.birth_date_no_month:
            birth_date.month = None
        return birth_date

    def set_birth_date(self, ubd):
        self.birth_date = ubd
        if ubd:
            if ubd.no_day:
                self.birth_date_no_day = True
            if ubd.no_month:
                self.birth_date_no_month = True

    unclear_birth_date = property(get_birth_date, set_birth_date)

    def full_human_name(self):
        try:
            person = self.person
        except AttributeError:
            pass
        else:
            if person.filled():
                return ' '.join((person.last_name, person.first_name, person.patronymic))
            return u'Неизвестно'

    def age(self):
        start = self.birth_date
        finish = (self.death_date or datetime.date.today())
        return int((finish - start).days / 365.25)

    def get_initials(self):
        initials = u""
        if self.first_name:
            initials = u"%s." % self.first_name[:1].upper()
            if self.patronymic:
                initials = u"%s%s." % (initials, self.patronymic[:1].upper())
        return initials

    def full_name(self):
        fio = u"%s %s" % (self.last_name, self.get_initials())
        return fio.strip()

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name', ]
        verbose_name = (u'физ. лицо')
        verbose_name_plural = (u'физ. лица')

class DocumentSource(models.Model):
    name = models.CharField(u"Наименование органа", max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class PersonID(models.Model):
    person = models.OneToOneField(Person)
    id_type = models.ForeignKey(IDDocumentType, verbose_name=u"Тип документа*")
    series = models.CharField(u"Серия*", max_length=4, null=True)
    number = models.CharField(u"Номер*", max_length=16)
    source = models.ForeignKey(DocumentSource, verbose_name=u"Кем выдан", blank=True, null=True)
    when = models.DateField(u"Дата выдачи", blank=True, null=True)

class ZAGS(models.Model):
    name = models.CharField(u"Название", max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = (u'ЗАГС')
        verbose_name_plural = (u'ЗАГС')

class DeathCertificate(models.Model):
    """
    Свидетельство о смерти.
    """

    person = models.OneToOneField(Person)

    s_number = models.CharField(u"Номер свидетельства", max_length=30, blank=True, null=True)
    series = models.CharField(u"Серия свидетельства", max_length=30, blank=True, null=True)
    release_date = models.DateField(u"Дата выдачи", null=True, blank=True)
    zags = models.ForeignKey(ZAGS, verbose_name=u"ЗАГС*", null=True)

    def __unicode__(self):
        return u"Свид. о смерти (%s)" % self.soul.__unicode__()

    class Meta:
        verbose_name = (u'свидетельство о смерти')
        verbose_name_plural = (u'свидетельства о смерти')

