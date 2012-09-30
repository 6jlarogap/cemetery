# -*- coding: utf-8 -*-
from common.models import UnclearDate

from django import forms
from django.core.validators import RegexValidator
from django.forms.extras.widgets import SelectDateWidget
from django.forms.forms import conditional_escape, flatatt, mark_safe, BoundField
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from django.contrib.auth.models import User

from cemetery.models import *
from geo.models import *
from organizations.models import Organization, Agent, BankAccount
from contrib.constants import UNKNOWN_NAME
from persons.models import DocumentSource, PersonID

import re
import datetime
from utils.models import DigitsValidator, VarLengthValidator


PER_PAGE_VALUES = (
    (5, '5'),
    (10, '10'),
    (15, '15'),
    (25, '25'),
    (50, '50'),
)

RE_CITY = u"^[а-яА-Яa-zA-Z0-9\-\.\ ]*$"
RE_LASTNAME = u"^[а-яА-Яa-zA-Z0-9\-\*\s]*$"
RE_USERNAME = r"^[a-zA-Z0-9\@\.\+\-\_]*$"

ORDER_BY_VALUES = (
    ('person__last_name', '+фамилии'),
    ('-person__last_name', '-фамилии'),
    ('person__first_name', '+имени'),
    ('-person__first_name', '-имени'),
    ('person__patronymic', '+отчеству'),
    ('-person__patronymic', '-отчеству'),
    ('date_fact', '+дате захоронения'),
    ('-date_fact', '-дате захоронения'),
    ('account_book_n', '+номеру в книге учета'),
    ('-account_book_n', '-номеру в книге учета'),
    ('product__place__area', '+участку'),
    ('-product__place__area', '-участку'),
    ('product__place__row', '+ряду'),
    ('-product__place__row', '-ряду'),
    ('product__place__seat', '+месту'),
    ('-product__place__seat', '-месту'),
    ('product__place__cemetery', '+кладбищу'),
    ('-product__place__cemetery', '-кладбищу'),
    #('comment', '+комментарию'),
    #('-comment', '-комментарию'),
)

def required_label_tag(self, contents=None, attrs=None):
    """
    Wraps the given contents in a <label>, if the field has an ID attribute.
    Does not HTML-escape the contents. If contents aren't given, uses the
    field's HTML-escaped label.

    If attrs are given, they're used as HTML attributes on the <label> tag.
    """
    contents = contents or conditional_escape(self.label)
    widget = self.field.widget
    id_ = widget.attrs.get('id') or self.auto_id

    contents = contents.strip('* ')
    if self.field.required:
        contents = contents + ' *'

    if id_:
        attrs = attrs and flatatt(attrs) or ''
        contents = u'<label for="%s"%s>%s</label>' % (widget.id_for_label(id_), attrs, unicode(contents))
    return mark_safe(contents)

BoundField.label_tag = required_label_tag

def get_yesterday():
    return (datetime.date.today() - datetime.timedelta(1)).strftime("%d.%m.%Y")

def get_today():
    return datetime.date.today().strftime("%d.%m.%Y")

class CalendarWidget(forms.DateInput):
    '''
    Виджет календаря.
    '''
    class Media:
        js = ('/admin/jsi18n/',
              settings.ADMIN_MEDIA_PREFIX + 'js/core.js',
              settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
              settings.ADMIN_MEDIA_PREFIX + "js/admin/DateTimeShortcuts.js")
        css = {
            'all': (
                settings.ADMIN_MEDIA_PREFIX + 'css/forms.css',
                settings.ADMIN_MEDIA_PREFIX + 'css/base.css',
                settings.ADMIN_MEDIA_PREFIX + 'css/widgets.css',)
        }

    def __init__(self, attrs={}):
        attrs.update({'class': 'vDateField', 'size': '10'})
        super(CalendarWidget, self).__init__(attrs=attrs)

    def __init__(self, attrs=None, format="%d.%m.%Y", *args, **kwargs):
        super(CalendarWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'}, format=format, *args, **kwargs)

class ClockWidget(forms.TextInput):
    '''
    Виджет времени.
    '''
    class Media:
        js = ('/admin/jsi18n/',
              settings.ADMIN_MEDIA_PREFIX + 'js/core.js',
              settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
              settings.ADMIN_MEDIA_PREFIX + "js/admin/DateTimeShortcuts.js")
        css = {
            'all': (
                settings.ADMIN_MEDIA_PREFIX + 'css/forms.css',
                settings.ADMIN_MEDIA_PREFIX + 'css/base.css',
                settings.ADMIN_MEDIA_PREFIX + 'css/widgets.css',)
        }

    def __init__(self, attrs={}):
        attrs.update({'class': 'vTimeField', 'size': '8'})
        super(ClockWidget, self).__init__(attrs=attrs)


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username or obj.email

class UnclearSelectDateWidget(SelectDateWidget):
    month_unclear = False
    year_unclear = False
    no_day = False
    no_month = False

    def value_from_datadict(self, data, files, name):
        from django.forms.extras.widgets import get_format, datetime_safe

        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "0":
            return None

        self.no_day = self.no_month = False

        if y:
            if settings.USE_L10N:
                input_format = get_format('DATE_INPUT_FORMATS')[0]
                try:
                    ud = UnclearDate(int(y), int(m), int(d))
                except ValueError, e:
                    return '%s-%s-%s' % (y, m, d)
                else:
                    self.no_month = ud.no_month
                    self.no_day = ud.no_day
                    date_value = datetime_safe.new_date(ud.d)
                return date_value.strftime(input_format)
            else:
                return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)

    def render(self, name, value, attrs=None):
        if value:
            if isinstance(value, basestring):
                value = datetime.datetime.strptime(value, '%d.%m.%Y')
            year, month, day = value.year, value.month, value.day
            value = UnclearDate(year, not self.no_month and month or None, not self.no_day and day or None)
        return super(UnclearSelectDateWidget, self).render(name, value, attrs)

    def create_select(self, name, field, value, val, choices):
        from django.forms.extras.widgets import Select
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        choices.insert(0, self.none_value)
        local_attrs = self.build_attrs(id=field % id_)
        s = Select(choices=choices)
        select_html = s.render(field % name, val, local_attrs)
        return select_html

class UnclearDateField(forms.DateField):
    today = datetime.date.today()

    widget = UnclearSelectDateWidget(years=range(today.month > 10 and today.day > 20 and (today.year + 1) or today.year, 1900, -1))

    def to_python(self, value):
        if isinstance(value, UnclearDate):
            return value
        return super(UnclearDateField, self).to_python(value)

