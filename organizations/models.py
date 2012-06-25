# -*- coding: utf-8 -*-

from django.db import models

from persons.models import Person
from utils.models import LengthValidator, NotEmptyValidator, DigitsValidator, VarLengthValidator

class Organization(models.Model):
    """
    Юридическое лицо.
    """
    ogrn = models.CharField(u"ОГРН/ОГРИП", max_length=15, blank=True)                                  # ОГРН
    inn = models.CharField(u"ИНН", max_length=12, blank=True, validators=[VarLengthValidator((10, 12)), DigitsValidator(), ])                                    # ИНН
    kpp = models.CharField(u"КПП", max_length=9, blank=True, validators=[DigitsValidator(), ])                                     # КПП
    name = models.CharField(u"Краткое название организации", max_length=99)                      # Название краткое
    full_name = models.CharField(u"Полное название организации", max_length=255, null=True)      # Название полное
    ceo = models.ForeignKey(Person, verbose_name=u"Директор", null=True, blank=True, limit_choices_to={'death_date__isnull': True})
    ceo_name = models.CharField(u"ФИО директора", max_length=255, null=True, blank=True, help_text=u'именительный падеж, напр. ИВАНОВ И.И.')
    ceo_name_who = models.CharField(u"ФИО директора р.п.", max_length=255, null=True, blank=True, help_text=u'родительный падеж, напр. ИВАНОВА И.И.')
    ceo_document = models.CharField(u"Документ директора", max_length=255, null=True, blank=True, help_text=u'на основании чего? например, УСТАВА')

    def __unicode__(self):
        return self.name or self.full_name or u'Unknown'

    def bank_account(self):
        try:
            return self.bankaccount_set.all()[0]
        except IndexError:
            return

    def phone(self):
        try:
            return self.phone_set.all()[0]
        except IndexError:
            return

    class Meta:
        ordering = ['name']
        verbose_name = (u'юр. лицо')
        verbose_name_plural = (u'юр. лица')

class BankAccount(models.Model):
    """
    Банковские реквизиты
    """
    organization = models.ForeignKey(Organization, verbose_name=u"Организация")      # Владелец счета
    rs = models.CharField(u"Расчетный счет", max_length=20, validators=[DigitsValidator(), LengthValidator(20), ]) # Расчетный счет
    ks = models.CharField(u"Корреспондентский счет", max_length=20, blank=True, validators=[DigitsValidator(), LengthValidator(20), ]) # Корреспондентский счет
    bik = models.CharField(u"БИК", max_length=9, validators=[DigitsValidator(), LengthValidator(9), ])                         # Банковский идентификационный код
    bankname = models.CharField(u"Наименование банка", max_length=64, validators=[NotEmptyValidator(1), ])    # Название банка
    ls = models.CharField(u"Л/с", max_length=11, blank=True, null=True, validators=[LengthValidator(11), ])

class Agent(models.Model):
    person = models.ForeignKey(Person)
    organization = models.ForeignKey(Organization, related_name="agents", verbose_name="Организация")

class Doverennost(models.Model):
    agent = models.ForeignKey(Agent, related_name="doverennosti", verbose_name="Доверенность")

    number = models.CharField(verbose_name="Номер доверенности", max_length=255, blank=True, null=True)
    issue_date = models.DateField(verbose_name="Дата выдачи", blank=True, null=True)
    expire_date = models.DateField(verbose_name="Действует до", blank=True, null=True)

    def __unicode__(self):
        return unicode(self.agent) + ' - ' + self.number

