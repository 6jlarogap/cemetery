# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from django.forms import formsets
from django.forms.extras.widgets import SelectDateWidget
from django.forms.forms import conditional_escape, flatatt, mark_safe, BoundField
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminTimeWidget

from models import *
from common.models import PersonID, Organization, Agent
from contrib.constants import UNKNOWN_NAME

from annoying.decorators import autostrip


import re
import string
import datetime


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

@autostrip
class SearchForm(forms.Form):
    """
    Форма поиска на главной странице.
    """
    fio = forms.CharField(required=False, max_length=100, label="ФИО")
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.all(),
                                      empty_label="Все", label="Кладбища")
    birth_date_from = forms.DateField(required=False, label="Дата рождения с")
    birth_date_to = forms.DateField(required=False, label="Дата рождения по")
    death_date_from = forms.DateField(required=False, label="Дата смерти с")
    death_date_to = forms.DateField(required=False, label="Дата смерти по")
    burial_date_from = forms.DateField(required=False, label="Дата захоронения с")
    burial_date_to = forms.DateField(required=False, label="Дата захоронения по")
#    death_certificate = forms.CharField(required=False, max_length=30, label="Номер свидетельства о смерти")
    account_book_n_from = forms.CharField(required=False, max_length=16, label="Номер в книге учета от и до")
    account_book_n_to = forms.CharField(required=False, max_length=16, label="Номер в книге учета до")
    customer = forms.CharField(required=False, max_length=30, label="Заказчик")
    owner = UserChoiceField(required=False, queryset=User.objects.all(), empty_label="Все", label="Создатель")
    area = forms.CharField(required=False, max_length=9, label="Участок")
    row = forms.CharField(required=False, max_length=9, label="Ряд")
    seat = forms.CharField(required=False, max_length=9, label="Место")
    gps_x = forms.FloatField(required=False, label="GPS X")
    gps_y = forms.FloatField(required=False, label="GPS Y")
    gps_z = forms.FloatField(required=False, label="GPS Z")
    comment = forms.CharField(required=False, max_length=50, label="Комментарий")
    per_page = forms.IntegerField(required=False, widget=forms.Select(choices=PER_PAGE_VALUES,
                                                                      attrs={'onChange': 'submit_form();'}),
                                  label="Записей на страницу")
    records_order_by = forms.CharField(required=False, max_length=50, widget=forms.Select(choices=ORDER_BY_VALUES,
                                                                                  attrs={'onChange': 'submit_form();'}),
                                       label="Сортировка по")
    page = forms.IntegerField(required=False, widget=forms.HiddenInput, label="Страница")
    operation = forms.ModelChoiceField(required=False, queryset=Operation.objects.all(), label="Услуга", empty_label="Все")
    no_exhumated = forms.BooleanField(required=False, initial=False)

class AutoTabIndex(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AutoTabIndex, self).__init__(*args, **kwargs)
        for i,k in enumerate(self.fields):
            self.fields[k].widget.attrs['tabindex'] = str(i+1)

class ModelAutoTabIndex(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelAutoTabIndex, self).__init__(*args, **kwargs)
        for i,k in enumerate(self.fields):
            self.fields[k].widget.attrs['tabindex'] = str(i+1)

@autostrip
class AddressForm(ModelAutoTabIndex):
    class Meta:
        model = Location
        fields = ['post_index', 'house', 'block', 'building', 'flat', 'info', ]

    street = forms.CharField(required=False, max_length=99, label="Улица")
    new_street = forms.BooleanField(required=False, label="Новая улица")
    city = forms.CharField(required=False, max_length=36, label="Нас. пункт")
    new_city = forms.BooleanField(required=False, label="Новый нас. пункт")
    region = forms.CharField(required=False, max_length=36, label="Регион")
    new_region = forms.BooleanField(required=False, label="Новый регион")
    country = forms.CharField(required=False, max_length=24, label="Страна")
    new_country = forms.BooleanField(required=False, label="Новая страна")

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            kwargs.setdefault('initial', {}).update({
                'street': instance.street and instance.street.name,
                'city': instance.city and instance.city.name or instance.street and instance.street.city.name,
                'region': instance.region and instance.region.name or instance.street and instance.street.city.region.name,
                'country': instance.country and instance.country.name or instance.street and instance.street.city.region.country.name,
            })
        super(AddressForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data

        # Валидация полей Location (страна, регион, нас. пункт, улица).
        country = cd.get("country", "")
        region = cd.get("region", "")
        city = cd.get("city", "")
        rest = re.sub(RE_CITY, "", city)
        if rest:
            raise forms.ValidationError("Недопустимые символы в имени населенного пункта. Допускаются только буквы, цифры, тире и точка")
        street = cd.get("street", "")
        house = cd.get("house", "")
        block = cd.get("block", "")
        building = cd.get("building", "")
        flat = cd.get("flat", "")

        new_country = new_region = new_city = new_street = False
        country_object = region_object = city_object = None

        if country.strip('.,() *'):
            # Страна.
            try:
                country_object = GeoCountry.objects.get(name__iexact=country)
            except MultipleObjectsReturned:
                country_object = GeoCountry.objects.filter(name__iexact=country)[0]
            except ObjectDoesNotExist:
                if not cd.get("new_country"):
                    raise forms.ValidationError("Страна не найдена.")
                else:
                    new_country = True
            else:
                if not cd.get("new_country", False):
                    new_country = False
                else:
                    raise forms.ValidationError("Страна с таким именем уже существует.")
        else:
            raise forms.ValidationError("Не все поля адреса заполнены.")

        if region.strip('.,() *'):
            # Регион.
            if new_country and not cd.get("new_region", False):
                raise forms.ValidationError("У новой страны регион должен быть тоже новым.")
            try:
                region_object = GeoRegion.objects.get(country=country_object, name__iexact=region)
            except MultipleObjectsReturned:
                region_object = GeoRegion.objects.filter(country=country_object, name__iexact=region)[0]
            except ObjectDoesNotExist:
                if not cd.get("new_region"):
                    raise forms.ValidationError("Регион не найден.")
                else:
                    new_region = True
            else:
                if not cd.get("new_region", False):
                    new_region = False
                else:
                    raise forms.ValidationError("Регион с таким именем уже существует в выбранной стране.")
        else:
            raise forms.ValidationError("Не все поля адреса заполнены.")

        if city.strip('.,() *'):
            # Нас. пункт.
            if new_region and not cd.get("new_city"):
                raise forms.ValidationError("У нового региона нас. пункт должен быть тоже новым.")
            try:
                city_object = GeoCity.objects.get(region=region_object, name__iexact=city)
            except MultipleObjectsReturned:
                city_object = GeoCity.objects.filter(region=region_object, name__iexact=city)[0]
            except ObjectDoesNotExist:
                if not cd.get("new_city"):
                    raise forms.ValidationError("Нас. пункт не найден.")
                else:
                    new_city = True
            else:
                if not cd.get("new_city", False):
                    new_city = False
                else:
                    raise forms.ValidationError("Нас. пункт с таким именем уже существует в выбранном регионе.")

        if street.strip('.,() *'):
            # Улица.
            if new_city and not cd.get("new_street"):
                raise forms.ValidationError("У нового нас. пункта улица должна быть тоже новой.")

            try:
                street_object = Street.objects.get(city=city_object, name__iexact=street)
            except MultipleObjectsReturned:
                street_object = Street.objects.filter(city=city_object, name__iexact=street)[0]
            except ObjectDoesNotExist:
                if not cd.get("new_street", False):
                    raise forms.ValidationError("Улица не найдена.")
            else:
                if cd.get("new_street", False):
                    raise forms.ValidationError("Улица с таким именем уже существует в выбранном нас. пункте.")
            if block or building or flat:
                if not house:
                    raise forms.ValidationError("Не указан дом.")
        return cd

    def is_valid(self, *args, **kwargs):
        valid = super(AddressForm, self).is_valid(*args, **kwargs)
        if not self.data.get('%s-country' % self.prefix) \
           and not self.data.get('%s-region' % self.prefix) \
           and not self.data.get('%s-city' % self.prefix):
            self.cleaned_data = None
            return True
        return valid

    def save(self, *args, **kwargs):
        if not self.is_valid() or not self.cleaned_data:
            return None

        cd = self.cleaned_data

        location = super(AddressForm, self).save(commit=False, *args, **kwargs)

        country = region = city = street = None
        if cd.get("country", "").strip('.,() *'):
            # Страна.
            try:
                country = GeoCountry.objects.get(name__iexact=cd["country"])
            except ObjectDoesNotExist:
                country = GeoCountry(name=cd["country"].capitalize())
                country.save()
        if cd.get("region", "").strip('.,() *'):
            # Регион.
            try:
                region = GeoRegion.objects.get(country=country, name__iexact=cd["region"])
            except ObjectDoesNotExist:
                region = GeoRegion(country=country, name=cd["region"].capitalize())
                region.save()
        if cd.get("city", "").strip('.,() *'):
            # Нас. пункт.
            try:
                city = GeoCity.objects.get(region=region, name__iexact=cd["city"])
            except ObjectDoesNotExist:
                city = GeoCity(country=country, region=region, name=cd["city"].capitalize())
                city.save()
        if cd.get("street", "").strip('.,() *'):
            # Улица.
            try:
                street = Street.objects.get(city=city, name__iexact=cd["street"])
            except ObjectDoesNotExist:
                street = Street(city=city, name=cd["street"].capitalize())
                street.save()

        # Сохраняем Location.
        location.street = street
        location.country = country
        location.region = region
        location.city = city

        location.save()
        return location

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

    def prepare_value(self, value):
        if isinstance(value, UnclearDate):
            return value
        return value

@autostrip
class JournalForm(AutoTabIndex):
    """
    Форма журнала - создания нового захоронения.
    """

    account_book_n = forms.CharField(max_length=8, label="Номер в книге учета", required=False, help_text=u'если пусто - заполнится автоматически')

    burial_date = forms.DateField(label="Дата захоронения*", initial=get_today, required=True)
    burial_time = forms.TimeField(label="Время захоронения", required=False)

    birth_date = UnclearDateField(label="Дата рождения", initial='', required=False)
    death_date = forms.DateField(label="Дата смерти", initial=get_yesterday, required=False)
    exhumated_date = forms.DateField(label="Дата эксгумации", required=False)
    last_name = forms.CharField(max_length=128, label="Фамилия*", widget=forms.TextInput(attrs={"tabindex": "3"}),
            help_text="Допускаются только буквы, цифры и символ '-'", initial=UNKNOWN_NAME,
            validators=[RegexValidator(RE_LASTNAME), ])
    first_name = forms.CharField(required=False, max_length=30, label="Имя", validators=[RegexValidator(RE_LASTNAME), ])
    patronymic = forms.CharField(required=False, max_length=30, label="Отчество", validators=[RegexValidator(RE_LASTNAME), ])
    cemetery = forms.ModelChoiceField(queryset=Cemetery.objects.all(), label="Кладбище*", required=True)
    operation = forms.ModelChoiceField(queryset=Operation.objects.all().order_by('ordering', 'op_type'), label="Услуга*", empty_label=None, required=True)
    hoperation = forms.CharField(required=False, widget=forms.HiddenInput)
    area = forms.CharField(max_length=9, label="Участок", required=False)
    row = forms.CharField(max_length=9, label="Ряд", required=False)
    seat = forms.CharField(max_length=8, label="Место", required=False, help_text=u'если пусто - заполнится автоматически')
    rooms = forms.IntegerField(label="Мест в ограде всего", required=False)
    rooms_free = forms.IntegerField(label="Свободно", required=False)
    customer_last_name = forms.CharField(required=False, max_length=30, label="Фамилия заказчика*",
                                         help_text="Допускаются только буквы, цифры и символ '-'")
    customer_first_name = forms.CharField(required=False, max_length=30, label="Имя заказчика",
                                          validators=[RegexValidator(RE_LASTNAME), ])
    customer_patronymic = forms.CharField(required=False, max_length=30, label="Отчество заказчика",
                                          validators=[RegexValidator(RE_LASTNAME), ])

    responsible_last_name = forms.CharField(max_length=30, label="Фамилия ответственного*",
                                         help_text="Допускаются только буквы, цифры и символ '-'",
                                         initial=UNKNOWN_NAME,
                                         validators=[RegexValidator(RE_LASTNAME), ])
    responsible_first_name = forms.CharField(required=False, max_length=30, label="Имя ответственного",
                                             validators=[RegexValidator(RE_LASTNAME), ])
    responsible_patronymic = forms.CharField(required=False, max_length=30, label="Отчество ответственного",
                                             validators=[RegexValidator(RE_LASTNAME), ])
    responsible_myself = forms.BooleanField(required=False, label="Заказчик является ответственным", initial=True)

    opf = forms.ChoiceField(label="Орг.-пр. форма", choices=[
        ('fizik', u"Физ. лицо"),
        ('yurik', u"Юр. лицо"),
    ], widget=forms.RadioSelect, initial='fizik')

    organization = forms.ModelChoiceField(label="Организация", queryset=Organization.objects.all(), required=False)
    agent_director = forms.BooleanField(label="Директор - агент", required=False)

    dover_number = forms.CharField(label="Номер доверенности", max_length=255, required=False)
    dover_date = forms.DateField(label="Дата выдачи", required=False)
    dover_expire = forms.DateField(label="Действует до", required=False)

    agent = forms.ModelChoiceField(label="Агент", queryset=Agent.objects.all(), required=False)

    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 60}), label="Комментарий")
    file1 = forms.FileField(required=False, label="Файл")
    file1_comment = forms.CharField(required=False, max_length=96, widget=forms.Textarea(attrs={'rows': 2, 'cols': 32}),
                                    label="Комментарий к файлу")

    def __init__(self, *args, **kwargs):
        cem = kwargs.pop('cem', None)
        oper = kwargs.pop('oper', None)
        self.instance = kwargs.pop('instance', None)

        data = kwargs.get('data') or {}
        if 'dover_number' in data and not data.get('dover_number'):
            del data['dover_number']

        super(JournalForm, self).__init__(*args, **kwargs)

        bd = None
        if data.get('burial_date'):
            bdt = datetime.datetime.strptime(data.get('burial_date'), '%d.%m.%Y')
            bd = datetime.date(*tuple(bdt.timetuple())[:3])
            if bd >= datetime.date.today():
                self.fields['burial_time'].required=True

        if data.get('opf', 'fizik') != 'fizik':
            for f in ['dover_date', 'dover_expire', 'dover_number', 'agent', ]:
                self.fields[f].required = not data.get('agent_director') or False

            for f in ['customer_last_name', ]:
                self.fields[f].required = False

        if cem:
            self.fields["cemetery"].initial = cem
        if oper:
            self.fields["operation"].initial = oper

        if data.get('opf') != 'fizik' and not data.get('agent_director'):
            for f in ['dover_number', 'dover_date', 'dover_expire']:
                self.fields[f].required = True
                if bd and bd < datetime.date.today():
                    self.fields[f].required = False

        if data.get('agent_director'):
            data['agent'] = None

    def clean_responsible_last_name(self):
        name = self.cleaned_data['responsible_last_name']
        if '*' in name and name != UNKNOWN_NAME:
            raise forms.ValidationError(u'Недопустимая фамилия')
        return name

    def clean_last_name(self):
        name = self.cleaned_data['last_name']
        if '*' in name and name != UNKNOWN_NAME:
            raise forms.ValidationError(u'Недопустимая фамилия')
        return name

    def clean_account_book_n(self):
        if not self.cleaned_data['account_book_n']:
            return self.cleaned_data['account_book_n']
        if self.cleaned_data['account_book_n'].isdigit() and len(self.cleaned_data['account_book_n']) == 8:
            return self.cleaned_data['account_book_n']
        raise forms.ValidationError(u"Должно быть 8 цифр")

    def clean_seat(self):
        if not self.cleaned_data['seat']:
            return self.cleaned_data['seat']
        if self.cleaned_data['seat'].isdigit() and len(self.cleaned_data['seat']) == 8:
            return self.cleaned_data['seat']
        raise forms.ValidationError(u"Должно быть 8 цифр")

    def clean(self):
        cd = self.cleaned_data

        if cd.get('opf') == 'yurik' and not cd.get('organization'):
            raise forms.ValidationError("Не указана организация для ЮЛ")

        # Валидация кладбища/операции.
        operation = cd.get("operation", None)
        cemetery = cd.get("cemetery") or Cemetery()
        try:
            spo = SoulProducttypeOperation.objects.get(soul=cemetery.organization.soul_ptr, operation=operation,
                                                       p_type=settings.PLACE_PRODUCTTYPE_ID)
        except:
            raise forms.ValidationError("Выбранная операция не существует для выбранного кладбища.")

        if not self.instance:
            if spo.operation.op_type in [u'Захоронение в существующую', u'Подзахоронение к существующей']:
                if not cd.get('seat'):
                    raise forms.ValidationError(u"Нужно указать номер могилы")

        if not cd.get("account_book_n"):
            cd["account_book_n"] = ''
        if not cd.get("seat"):
            cd["seat"] = ''

        if not cd.get("seat") and cd.get("account_book_n"):
            cd["seat"] = cd["account_book_n"]

        place = Place()
        place.cemetery = cd["cemetery"]
        place.area = cd.get("area")
        place.row = cd.get("row")
        place.seat = cd.get("seat")
        if not self.initial and cd["burial_date"] >= datetime.date.today():
            if cd["rooms"] <= place.count_burials():
                raise forms.ValidationError("Нет свободного места в ограде")

        try:
            burials = Burial.objects.exclude(account_book_n=self.cleaned_data['account_book_n'])
            burials = burials.filter(
                product__place__cemetery=self.cleaned_data['cemetery'],
                product__place__area=self.cleaned_data['area'],
                product__place__row=self.cleaned_data['row'],
                product__place__seat=self.cleaned_data['seat'],
            )
            burials = burials.filter(responsible_customer__isnull=False)
            burials = [b for b in burials if b.responsible_customer.person.last_name != UNKNOWN_NAME and not b.responsible_customer.person.last_name.startswith('*')]
            b = burials[0]
        except IndexError:
            pass
        else:
            r = b.responsible_customer.person
            if cd['responsible_myself']:
                new_r = Person(
                    last_name=cd['customer_last_name'],
                    first_name=cd['customer_first_name'],
                    patronymic=cd['customer_patronymic'],
                )
            else:
                new_r = Person(
                    last_name=cd['responsible_last_name'],
                    first_name=cd['responsible_first_name'],
                    patronymic=cd['responsible_patronymic'],
                )

            if new_r.last_name.lower() != r.last_name.lower() or \
               new_r.first_name.lower() != r.first_name.lower() or \
               new_r.patronymic.lower() != r.patronymic.lower():
                raise forms.ValidationError(u"Ответственный за все родственные захоронения должен быть один: %s" % r)
        return cd

class CertificateForm(forms.ModelForm):
    class Meta:
        model = DeathCertificate
        exclude = ['uuid', 'soul']
        widgets = {
            'release_date': CalendarWidget(),
        }


@autostrip
class OrderFileCommentForm(forms.Form):
    """
    Форма редактирования комментария к файлу заказу.
    """
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 90}),
                              label="Комментарий")

@autostrip
class OrderCommentForm(forms.Form):
    """
    Форма редактирования комментария к заказу.
    """
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 90}),
                              label="Комментарий")
    bdelete = forms.BooleanField(required=False, label="удалить")

    def clean(self):
        cd = self.cleaned_data
        if not cd.get("bdelete", None):
            if not cd.get("comment", None):
                raise forms.ValidationError("Пустой комментарий сохранить нельзя. Нажмите 'удалить'")
        return cd

@autostrip
class InitalForm(forms.Form):
    """
    Форма ввода данных для инициализации системы.
    """
    org_name = forms.CharField(label="*Название организации", max_length=99)
    org_full_name = forms.CharField(label="Полное название организации", max_length=255)
    org_phone = forms.CharField(required=False, max_length=20, label="Телефон организации", widget=forms.TextInput(), help_text=u'указать код страны и города')
    ceo_name = forms.CharField(max_length=255, label="ФИО директора", help_text=u'именительный падеж, напр. ИВАНОВ И.И.')
    ceo_name_who = forms.CharField(max_length=255, label="ФИО директора р.п.", help_text=u'родительный падеж, напр. ИВАНОВА И.И.')
    ceo_document = forms.CharField(max_length=255, label="Документ директора", help_text=u'на основании чего? например, УСТАВА')
    post_index = forms.CharField(required=False, max_length=16, label="Почтовый индекс")
    street = forms.CharField(required=False, max_length=99, label="Улица", widget=forms.TextInput())
    new_street = forms.BooleanField(required=False, label="Новая улица")
    house = forms.CharField(required=False, max_length=16, label="Дом", widget=forms.TextInput())
    block = forms.CharField(required=False, max_length=16, label="Корпус", widget=forms.TextInput())
    building = forms.CharField(required=False, max_length=16, label="Строение")
    flat = forms.CharField(required=False, max_length=16, label="Квартира", widget=forms.TextInput())
    city = forms.CharField(required=False, max_length=36, label="Нас. пункт", widget=forms.TextInput())
    new_city = forms.BooleanField(required=False, label="Новый нас. пункт")
    region = forms.CharField(required=False, max_length=36, label="Регион", widget=forms.TextInput())
    new_region = forms.BooleanField(required=False, label="Новый регион")
    country = forms.CharField(required=False, max_length=24, label="Страна", widget=forms.TextInput())
    new_country = forms.BooleanField(required=False, label="Новая страна")
    info = forms.CharField(required=False, widget=forms.Textarea, label=u"Доп. инфо")

    ogrn = forms.CharField(required=False, max_length=15, label="ОГРН", validators=[DigitsValidator(), ])
    kpp = forms.CharField(required=False, max_length=9, label="КПП", validators=[DigitsValidator(), ])
    inn = forms.CharField(required=False, max_length=12, label="ИНН", validators=[VarLengthValidator((10, 12)), DigitsValidator(), ])

    def clean_username(self):
        """
        Проверка логина на отсутствие недопустимых символов.
        """
        un = self.cleaned_data["username"]
        rest = re.sub(RE_USERNAME, "", un)
        if rest:
            raise forms.ValidationError("Недопустимые символы в имени пользователя.")
        return un

    def clean(self):
        cd = self.cleaned_data
        # Страна/регион/нас. пункт/улица орг-ии.
        country = cd.get("country", "")
        region = cd.get("region", "")
        city = cd.get("city", "")
        street = cd.get("street", "")
        if country and region and city and street:
            # Страна.
            try:
                country_object = GeoCountry.objects.get(name__exact=country)
            except ObjectDoesNotExist:
                if not cd.get("new_country", False):
                    raise forms.ValidationError("Организация: страна не найдена.")
                else:
                    new_country = True
            else:
                if not cd.get("new_country", False):
                    new_country = False
                else:
                    raise forms.ValidationError("Организация: страна с таким именем уже существует.")
            # Регион.
            if new_country and not cd.get("new_region", False):
                raise forms.ValidationError("Организация: у новой страны регион должен быть тоже новым.")
            try:
                region_object = GeoRegion.objects.get(country__name__exact=country, name__exact=region)
            except ObjectDoesNotExist:
                if not cd.get("new_region", False):
                    raise forms.ValidationError("Организация: регион не найден.")
                else:
                    new_region = True
            else:
                if not cd.get("new_region", False):
                    new_region = False
                else:
                    raise forms.ValidationError("Организация: регион с таким именем уже существует в выбранной стране.")
            # Нас. пункт.
            if new_region and not cd.get("new_city", False):
                raise forms.ValidationError("Организация: у нового региона нас. пункт должен быть тоже новым.")
            try:
                city_object = GeoCity.objects.get(region__name__exact=region, name__exact=city)
            except ObjectDoesNotExist:
                if not cd.get("new_city", False):
                    raise forms.ValidationError("Организация: нас. пункт не найден.")
                else:
                    new_city = True
            else:
                if not cd.get("new_city", False):
                    new_city = False
                else:
                    raise forms.ValidationError("Организация: нас. пункт с таким именем уже существует в выбранном регионе.")
            # Улица.
            if new_city and not cd.get("new_street", False):
                raise forms.ValidationError("Организация: у нового нас. пункта улица должна быть тоже новой.")
            try:
                street_object = Street.objects.get(city__name__exact=city, name__exact=street)
            except ObjectDoesNotExist:
                if not cd.get("new_street", False):
                    raise forms.ValidationError("Организация: улица не найдена.")
            else:
                if cd.get("new_street", False):
                    raise forms.ValidationError("Организация: улица с таким именем уже существует в выбранном нас. пункте.")
        else:
            if country or region or city or street:  # Есть, но не все.
                raise forms.ValidationError("Организация: не все поля адреса заполнены.")

        # Страна/регион/нас. пункт/улица кладбища .
        cem_country = cd.get("cem_country", "")
        cem_region = cd.get("cem_region", "")
        cem_city = cd.get("cem_city", "")
        cem_street = cd.get("cem_street", "")
        if cem_country and cem_region and cem_city and cem_street:
            # Страна.
            try:
                cem_country_object = GeoCountry.objects.get(name__exact=cem_country)
            except ObjectDoesNotExist:
                if not cd.get("cem_new_country", False):
                    raise forms.ValidationError("Кладбище: страна не найдена.")
                else:
                    cem_new_country = True
            else:
                if not cd.get("cem_new_country", False):
                    cem_new_country = False
                else:
                    raise forms.ValidationError("Кладбище: страна с таким именем уже существует.")
            # Регион.
            if cem_new_country and not cd.get("cem_new_region", False):
                raise forms.ValidationError("Кладбище: у новой страны регион должен быть тоже новым.")
            try:
                cem_region_object = GeoRegion.objects.get(country__name__exact=cem_country, name__exact=cem_region)
            except ObjectDoesNotExist:
                if not cd.get("cem_new_region", False):
                    raise forms.ValidationError("Кладбище: регион не найден.")
                else:
                    cem_new_region = True
            else:
                if not cd.get("cem_new_region", False):
                    cem_new_region = False
                else:
                    raise forms.ValidationError("Кладбище: регион с таким именем уже существует в выбранной стране.")
            # Нас. пункт.
            if cem_new_region and not cd.get("cem_new_city", False):
                raise forms.ValidationError("Кладбище: у нового региона нас. пункт должен быть тоже новым.")
            try:
                cem_city_object = GeoCity.objects.get(region__name__exact=cem_region, name__exact=cem_city)
            except ObjectDoesNotExist:
                if not cd.get("cem_new_city", False):
                    raise forms.ValidationError("Кладбище: нас. пункт не найден.")
                else:
                    cem_new_city = True
            else:
                if not cd.get("cem_new_city", False):
                    cem_new_city = False
                else:
                    raise forms.ValidationError("Кладбище: нас. пункт с таким именем уже существует в выбранном регионе.")
            # Улица.
            if cem_new_city and not cd.get("cem_new_street", False):
                raise forms.ValidationError("Кладбище: у нового нас. пункта улица должна быть тоже новой.")
            try:
                cem_street_object = Street.objects.get(city__name__exact=cem_city, name__exact=cem_street)
            except ObjectDoesNotExist:
                if not cd.get("cem_new_street", False):
                    raise forms.ValidationError("Кладбище: улица не найдена.")
            else:
                if cd.get("cem_new_street", False):
                    raise forms.ValidationError("Кладбище: улица с таким именем уже существует в выбранном нас. пункте.")
        else:
            if cem_country or cem_region or cem_city or cem_street:  # Есть, но не все.
                raise forms.ValidationError("Кладбище: не все поля адреса заполнены.")
        if cd.get("password1", "") != cd.get("password2", ""):
            raise forms.ValidationError("Пароли не совпадают.")
        return cd

InitBankFormset = forms.models.inlineformset_factory(Organization, BankAccount, extra=2)

class ImportForm(forms.Form):
    """
    Форма импорта csv-файла.
    """""
    creator = forms.ModelChoiceField(required=True, queryset=User.objects.all(), label="Создатель")
    cemetery = forms.ModelChoiceField(queryset = Cemetery.objects.all(), label="Кладбище")
    csv_file = forms.FileField(label="CSV файл")


@autostrip
class CemeteryForm(forms.Form):
    """
    Форма создания кладбища.
    """
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), label="Организация", empty_label=None)
    name = forms.CharField(max_length=99, label="Название")
    post_index = forms.CharField(required=False, max_length=16, label="Почтовый индекс")
    street = forms.CharField(required=False, max_length=99, label="Улица", widget=forms.TextInput())
    new_street = forms.BooleanField(required=False, label="Новая улица")
    city = forms.CharField(required=False, max_length=36, label="Нас. пункт", widget=forms.TextInput())
    new_city = forms.BooleanField(required=False, label="Новый нас. пункт")
    region = forms.CharField(max_length=36, label="Регион", widget=forms.TextInput())
    new_region = forms.BooleanField(required=False, label="Новый регион")
    country = forms.CharField(max_length=24, label="Страна", widget=forms.TextInput())
    new_country = forms.BooleanField(required=False, label="Новая страна")
    house = forms.CharField(required=False, max_length=16, label="Дом", widget=forms.TextInput())
    block = forms.CharField(required=False, max_length=16, label="Корпус", widget=forms.TextInput())
    building = forms.CharField(required=False, max_length=16, label="Строение")
    info = forms.CharField(required=False, widget=forms.Textarea, label=u"Доп. инфо")

    def clean_name(self):
        if not self.initial.get('name'):
            try:
                Cemetery.objects.get(name=self.cleaned_data['name'])
            except Cemetery.DoesNotExist:
                return self.cleaned_data['name']
            except Cemetery.MultipleObjectsReturned:
                pass
            raise forms.ValidationError(u"Такое кладбище уже есть")
        return self.cleaned_data['name']

    def clean(self):
        cd = self.cleaned_data
        country = cd.get("country", "")
        region = cd.get("region", "")
        city = cd.get("city", "")
        street = cd.get("street", "")
        house = cd.get("house", "")
        block = cd.get("block", "")
        building = cd.get("building", "")
        new_country = cd.get("new_country", False)
        new_region = cd.get("new_region", False)
        new_city = cd.get("new_city", False)
        new_street = cd.get("new_street", False)
        if country or region or city or street:
            if not city:
                raise forms.ValidationError("Отсутствует нас. пункт.")
            if not region:
                raise forms.ValidationError("Отсутствует регион.")
            if not country:
                raise forms.ValidationError("Отсутствует страна.")
        if country:
            try:
                country_obj = GeoCountry.objects.get(name__iexact=country)
            except ObjectDoesNotExist:
                if not new_country:
                    raise forms.ValidationError("Указанная страна не существует.")
            if new_country:
                if not new_region:
                    raise forms.ValidationError("Указанный регион не существует.")
            else:
                try:
                    region_obj = GeoRegion.objects.get(country=country_obj, name__iexact=region)
                except ObjectDoesNotExist:
                    if not new_region:
                        raise forms.ValidationError("Указанный регион не существует.")
            if new_region:
                if not new_city:
                    raise forms.ValidationError("Указанный нас. пункт не существует.")
            else:
                try:
                    city_obj = GeoCity.objects.get(country=country_obj, region=region_obj, name__iexact=city)
                except ObjectDoesNotExist:
                    if not new_city:
                        raise forms.ValidationError("Указанный нас. пункт не существует.")
            if street:
                if new_street:
                    if not new_region:
                        raise forms.ValidationError("Указанная улица не существует.")
                else:
                    try:
                        city_obj = Street.objects.get(region=region_obj, name__iexact=street)
                    except ObjectDoesNotExist:
                        if not new_city:
                            raise forms.ValidationError("Указанная улица пункт не существует.")
        return cd


@autostrip
class NewUserForm(forms.Form):
    """
    Форма создания нового пользователя системы.
    """
    username = forms.CharField(label="Имя пользователя", max_length=30,
                               help_text="Допускаются только латинские буквы, цифры и знаки @ . + - _")
    last_name = forms.CharField(max_length=30, label="Фамилия")
    first_name = forms.CharField(max_length=30, label="Имя", required=False)
    patronymic = forms.CharField(max_length=30, label="Отчество", required=False)
#    role = forms.ModelChoiceField(queryset=Role.objects.all(), label="Роль")
#    is_staff = forms.BooleanField(required=False, label="Доступ в админку")
    phone = forms.CharField(max_length=20, label="Телефон", required=False, help_text=u'указать код страны и города')
    password1 = forms.CharField(max_length=18, widget=forms.PasswordInput(render_value=False), label="Пароль")
    password2 = forms.CharField(max_length=18, widget=forms.PasswordInput(render_value=False), label="Пароль (еще раз)")
    def clean(self):
        cd = self.cleaned_data
        username = cd["username"]
        # Проверка username на наличие недопустимых символов
        rest = re.sub(RE_USERNAME, "", username)
        if rest:
            raise forms.ValidationError("Недопустимые символы в имени пользователя.")
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            pass
        else:
            raise forms.ValidationError("Имя пользователя уже зарегистрировано за другим сотрудником.")
        pass1 = cd.get("password1", "")
        pass2 = cd.get("password2", "")
        if pass1 and pass2:
            if pass1 == pass2:
                return cd
            raise forms.ValidationError("Пароли не совпадают.")


@autostrip
class EditUserForm(forms.ModelForm):
    """
    Форма редактирования пользователя системы.
    """

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'is_active', ]

    patronymic = forms.CharField(max_length=30, label="Отчество", required=False)
    password1 = forms.CharField(required=False, max_length=18, widget=forms.PasswordInput(render_value=False), label="Пароль")
    password2 = forms.CharField(required=False, max_length=18, widget=forms.PasswordInput(render_value=False), label="Пароль (еще раз)")

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            kwargs.setdefault('initial', {}).update({
                'patronymic': kwargs['instance'].userprofile.soul.person.patronymic,
            })
        super(EditUserForm, self).__init__(*args, **kwargs)
        kp = self.fields.keyOrder.index('patronymic')
        ka = self.fields.keyOrder.index('is_active')
        self.fields.keyOrder[kp], self.fields.keyOrder[ka] = self.fields.keyOrder[ka], self.fields.keyOrder[kp]

        for f in self.fields:
            self.fields[f].widget.attrs['autocomplete'] = 'off'

    def clean(self):
        cd = self.cleaned_data
        if cd.get("password1") == cd.get("password2"):
            return cd
        else:
            raise forms.ValidationError("Пароли не совпадают.")

    def save(self, *args, **kwargs):
        user = super(EditUserForm, self).save(*args, **kwargs)

        user.userprofile.soul.person.first_name = self.cleaned_data['first_name']
        user.userprofile.soul.person.last_name = self.cleaned_data['last_name']
        user.userprofile.soul.person.patronymic = self.cleaned_data['patronymic']
        user.userprofile.soul.person.save()

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])
            if kwargs.get('commit', True):
                user.save()
        return user

@autostrip
class UserProfileForm(forms.Form):
    """
    Форма значений по умолчанию для профиля пользователя.
    """
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.all(), label="Кладбище")
    operation = forms.ModelChoiceField(required=False, queryset=Operation.objects.all(), label="Услуга")
    hoperation = forms.CharField(required=False, widget=forms.HiddenInput)
    records_per_page = forms.ChoiceField(required=False, choices=PER_PAGE_VALUES, label="Записей на странице")
    records_order_by = forms.ChoiceField(required=False, choices=ORDER_BY_VALUES, label="Сортировка по")
    def clean(self):
        cd = self.cleaned_data
        cemetery = cd.get("cemetery", None)
        operation = cd.get("operation", None)
        if operation and not cemetery:
            raise forms.ValidationError("Не выбрано кладбище.")
        if operation:
            try:
                spo = SoulProducttypeOperation.objects.get(soul=cemetery.organization.soul_ptr, operation=operation,
                                                           p_type=settings.PLACE_PRODUCTTYPE_ID)
            except:
                raise forms.ValidationError("Выбранная операция не существует для выбранного кладбища.")
        return cd

class OrderPositionForm(forms.ModelForm):
    active = forms.BooleanField(required=False)

    class Meta:
        model = OrderPosition
        fields = ['order_product', 'count', 'price']
        widgets = {
            'order_product': forms.HiddenInput,
        }

class BaseOrderPositionsFormset(formsets.BaseFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs.get('initial'):
            real_initial = []
            for i in kwargs['initial']:

                if isinstance(i['order_product'], OrderProduct):
                    q = models.Q(pk=i['order_product'].pk)
                else:
                    q = models.Q(name=i['order_product'])
                try:
                    OrderProduct.objects.get(q)
                except OrderProduct.DoesNotExist:
                    pass
                else:
                    real_initial.append(i)
            kwargs['initial'] = real_initial

        super(BaseOrderPositionsFormset, self).__init__(*args, **kwargs)


OrderPositionsFormset = forms.formsets.formset_factory(OrderPositionForm, extra=0, formset=BaseOrderPositionsFormset)

class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_type', ]
        widgets = {
            'payment_type': forms.RadioSelect,
        }

class PrintOptionsForm(forms.Form):
    catafalque = forms.BooleanField(label=u"наряд на автокатафалк", required=False, initial=False)
    lifters = forms.BooleanField(label=u"наряд на грузчиков", required=False, initial=False)
    graving = forms.BooleanField(label=u"наряд на рытье могилы", required=False, initial=True)
    receipt = forms.BooleanField(label=u"справка о захоронении", required=False, initial=False)
    dogovor = forms.BooleanField(label=u"договор ответственного", required=False, initial=False)

    catafalque_route = forms.CharField(label=u"маршрут а/к", required=False, widget=forms.Textarea)
    catafalque_start = forms.CharField(label=u"подача а/к", required=False)
    catafalque_time = forms.TimeField(label=u"время а/к", required=False)

    coffin_size = forms.CharField(label=u"размер гроба", required=False)

    print_now = forms.BooleanField(label=u"отправить на печать", required=False)

    add_info = forms.CharField(label=u"доп. инфо", required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.burial = kwargs.pop('burial')
        super(PrintOptionsForm, self).__init__(*args, **kwargs)


class IDForm(forms.ModelForm):
    who = forms.CharField(label=u"Кем выдан")

    class Meta:
        model = PersonID
        exclude = ['person', ]
        widgets = {
            'when': CalendarWidget,
        }

    def save(self, *args, **kwargs):
        really_commit = kwargs.get('commit', True)
        kwargs['commit'] = False
        obj = super(IDForm, self).save(*args, **kwargs)
        obj.source, _tmp = DocumentSource.objects.get_or_create(name=self.cleaned_data['who'])
        if really_commit:
            obj.save()
        return obj


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude=( "soul", )

    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)
        self.fields['f_number'].required = False

    def clean_f_number(self):
        if not self.cleaned_data.get('f_number'):
            raise forms.ValidationError(u"Обязательное поле")
        return self.cleaned_data['f_number']