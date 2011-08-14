# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminTimeWidget
from models import *
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

RE_CITY = u"[а-яА-Яa-zA-Z0-9\-\.\ ]"
RE_LASTNAME = u"[а-яА-Яa-zA-Z0-9\-]"
RE_USERNAME = r"[a-zA-Z0-9\@\.\+\-\_]"

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


@autostrip
class SearchForm(forms.Form):
    """
    Форма поиска на главной странице.
    """
    fio = forms.CharField(required=False, max_length=100, label="ФИО")
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.all(),
                                      empty_label="Все", label="Кладбища")
    birth_date_from = forms.DateField(required=False, label="Дата рождения с", widget=CalendarWidget)
    birth_date_to = forms.DateField(required=False, label="Дата рождения по", widget=CalendarWidget)
    death_date_from = forms.DateField(required=False, label="Дата смерти с", widget=CalendarWidget)
    death_date_to = forms.DateField(required=False, label="Дата смерти по", widget=CalendarWidget)
    burial_date_from = forms.DateField(required=False, label="Дата захоронения с", widget=CalendarWidget)
    burial_date_to = forms.DateField(required=False, label="Дата захоронения по", widget=CalendarWidget)
#    death_certificate = forms.CharField(required=False, max_length=30, label="Номер свидетельства о смерти")
    account_book_n_from = forms.CharField(required=False, max_length=16, label="Номер в книге учета от и до")
    account_book_n_to = forms.CharField(required=False, max_length=16, label="Номер в книге учета до")
    customer = forms.CharField(required=False, max_length=30, label="Фамилия заказчика")
    owner = forms.ModelChoiceField(required=False, queryset=User.objects.all(), empty_label="Все",
                                   label="Создатель")
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
        fields = ['post_index', 'house', 'block', 'building', 'flat',  ]

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
                'city': instance.street and instance.street.city.name,
                'region': instance.street and instance.street.city.region.name,
                'country': instance.street and instance.street.city.region.country.name,
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
        if country and region and city and street:
            # Страна.
            try:
                country_object = GeoCountry.objects.get(name__iexact=country)
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
                
            # Регион.
            if new_country and not cd.get("new_region", False):
                raise forms.ValidationError("У новой страны регион должен быть тоже новым.")
            try:
                region_object = GeoRegion.objects.get(country__name__iexact=country, name__iexact=region)
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
                
            # Нас. пункт.
            if new_region and not cd.get("new_city"):
                raise forms.ValidationError("У нового региона нас. пункт должен быть тоже новым.")
            try:
                city_object = GeoCity.objects.get(region__name__iexact=region, name__iexact=city)
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
                
            # Улица.
            if new_city and not cd.get("new_street"):
                raise forms.ValidationError("У нового нас. пункта улица должна быть тоже новой.")
            try:
                street_object = Street.objects.get(city__name__iexact=city, name__iexact=street)
            except ObjectDoesNotExist:
                if not cd.get("new_street", False):
                    raise forms.ValidationError("Улица не найдена.")
            else:
                if cd.get("new_street", False):
                    raise forms.ValidationError("Улица с таким именем уже существует в выбранном нас. пункте.")
            if block or building or flat:
                if not house:
                    raise forms.ValidationError("Не указан дом.")
        else:
            if country or region or city:  # Есть, но не все.
                raise forms.ValidationError("Не все поля адреса заполнены.")
            if house or block or building or flat:
                raise forms.ValidationError("Не выбрана улица.")
        return cd

    def save(self, *args, **kwargs):
        cd = self.cleaned_data

        location = super(AddressForm, self).save(commit=False, *args, **kwargs)
        if cd.get("country", ""):
            # Страна.
            try:
                country = GeoCountry.objects.get(name__iexact=cd["country"])
            except ObjectDoesNotExist:
                country = GeoCountry(name=cd["country"].capitalize())
                country.save()
            # Регион.
            try:
                region = GeoRegion.objects.get(country=country, name__iexact=cd["region"])
            except ObjectDoesNotExist:
                region = GeoRegion(country=country, name=cd["region"].capitalize())
                region.save()
            # Нас. пункт.
            try:
                city = GeoCity.objects.get(region=region, name__iexact=cd["city"])
            except ObjectDoesNotExist:
                city = GeoCity(country=country, region=region, name=cd["city"].capitalize())
                city.save()
            # Улица.
            try:
                street = Street.objects.get(city=city, name__iexact=cd["street"])
            except ObjectDoesNotExist:
                street = Street(city=city, name=cd["street"].capitalize())
                street.save()
            # Сохраняем Location.
            location.street = street

        location.save()
        return location

@autostrip
class JournalForm(AutoTabIndex):
    """
    Форма журнала - создания нового захоронения.
    """

    account_book_n = forms.CharField(max_length=16, label="Номер в книге учета*", required=False)

    burial_date = forms.DateField(label="Дата захоронения*", initial=get_today)
    burial_time = forms.TimeField(label="Время захоронения", required=False)

    birth_date = forms.DateField(label="Дата рождения*", initial='')
    death_date = forms.DateField(label="Дата смерти*", initial=get_yesterday)
    exhumated_date = forms.DateField(label="Дата эксгумации", required=False)
    last_name = forms.CharField(max_length=128, label="Фамилия*", widget=forms.TextInput(attrs={"tabindex": "3"}),
            help_text="Допускаются только буквы, цифры и символ '-'", initial=UNKNOWN_NAME)
    first_name = forms.CharField(required=False, max_length=30, label="Имя")
    patronymic = forms.CharField(required=False, max_length=30, label="Отчество")
    cemetery = forms.ModelChoiceField(queryset=Cemetery.objects.all(), label="Кладбище*", required=True)
    operation = forms.ModelChoiceField(queryset=Operation.objects.all(), label="Услуга*", empty_label=None, required=True)
    hoperation = forms.CharField(required=False, widget=forms.HiddenInput)
    area = forms.CharField(max_length=9, label="Участок*")
    row = forms.CharField(max_length=9, label="Ряд", required=False)
    seat = forms.CharField(max_length=9, label="Место*", required=False)
    rooms = forms.IntegerField(label="Мест в ограде", required=False)
    customer_last_name = forms.CharField(max_length=30, label="Фамилия заказчика*",
                                         help_text="Допускаются только буквы, цифры и символ '-'",
                                         initial=UNKNOWN_NAME)
    customer_first_name = forms.CharField(required=False, max_length=30, label="Имя заказчика")
    customer_patronymic = forms.CharField(required=False, max_length=30, label="Отчество заказчика")

    responsible_last_name = forms.CharField(max_length=30, label="Фамилия ответственного*",
                                         help_text="Допускаются только буквы, цифры и символ '-'",
                                         initial=UNKNOWN_NAME)
    responsible_first_name = forms.CharField(required=False, max_length=30, label="Имя ответственного")
    responsible_patronymic = forms.CharField(required=False, max_length=30, label="Отчество ответственного")
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

        data = kwargs.get('data') or {}
        if 'dover_number' in data and not data.get('dover_number'):
            del data['dover_number']

        super(JournalForm, self).__init__(*args, **kwargs)

        if data.get('opf', 'fizik') != 'fizik':
            for f in ['dover_date', 'dover_expire', 'dover_number', ]:
                self.fields[f].required = not data.get('agent_director') or False

        if cem:
            self.fields["cemetery"].initial = cem
        if oper:
            self.fields["operation"].initial = oper

    def clean(self):
        cd = self.cleaned_data

        # Проверка имен усопшего и заказчика на наличие недопустимых символов
        last_name = cd["last_name"]
        rest = re.sub(RE_LASTNAME, "", last_name)
        if rest:
            raise forms.ValidationError("Недопустимые символы в имени усопшего. Допускаются только буквы, цифры и тире")

        # Валидация кладбища/операции.
        operation = cd.get("operation", None)
        cemetery = cd.get("cemetery") or Cemetery()
        try:
            spo = SoulProducttypeOperation.objects.get(soul=cemetery.organization.soul_ptr, operation=operation,
                                                       p_type=settings.PLACE_PRODUCTTYPE_ID)
        except:
            raise forms.ValidationError("Выбранная операция не существует для выбранного кладбища.")

        if not cd["seat"] and cd["account_book_n"]:
            raise forms.ValidationError("При указанном номере в журнале необходимо указать и номер места")

        place = Place()
        place.cemetery = cd["cemetery"]
        place.area = cd["area"]
        place.row = cd["row"]
        place.seat = cd["seat"]
        if not self.initial and cd["burial_date"] >= datetime.date.today():
            if cd["rooms"] <= place.count_burials():
                raise forms.ValidationError("Нет свободного места в ограде")

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
    org_phone = forms.CharField(required=False, max_length=20, label="Телефон организации",
                                widget=forms.TextInput())
    post_index = forms.CharField(required=False, max_length=16, label="Почтовый индекс")
    street = forms.CharField(required=False, max_length=99, label="Улица",
                             widget=forms.TextInput())
    new_street = forms.BooleanField(required=False, label="Новая улица")
    city = forms.CharField(required=False, max_length=36, label="Нас. пункт",
                           widget=forms.TextInput())
    new_city = forms.BooleanField(required=False, label="Новый нас. пункт")
    region = forms.CharField(required=False, max_length=36, label="Регион",
                             widget=forms.TextInput())
    new_region = forms.BooleanField(required=False, label="Новый регион")
    country = forms.CharField(required=False, max_length=24, label="Страна",
                              widget=forms.TextInput())
    new_country = forms.BooleanField(required=False, label="Новая страна")
    house = forms.CharField(required=False, max_length=16, label="Дом",
                                     widget=forms.TextInput())
    block = forms.CharField(required=False, max_length=16, label="Корпус",
                                     widget=forms.TextInput())
    building = forms.CharField(required=False, max_length=16, label="Строение")
    flat = forms.CharField(required=False, max_length=16, label="Квартира",
                                    widget=forms.TextInput())
    cemetery = forms.CharField(label="*Название кладбища", max_length=99)
    cem_post_index = forms.CharField(required=False, max_length=16, label="Почтовый индекс")
    cem_street = forms.CharField(required=False, max_length=99, label="Улица",
                             widget=forms.TextInput())
    cem_new_street = forms.BooleanField(required=False, label="Новая улица")
    cem_city = forms.CharField(required=False, max_length=36, label="Нас. пункт",
                           widget=forms.TextInput())
    cem_new_city = forms.BooleanField(required=False, label="Новый нас. пункт")
    cem_region = forms.CharField(required=False, max_length=36, label="Регион",
                             widget=forms.TextInput())
    cem_new_region = forms.BooleanField(required=False, label="Новый регион")
    cem_country = forms.CharField(required=False, max_length=24, label="Страна",
                              widget=forms.TextInput())
    cem_new_country = forms.BooleanField(required=False, label="Новая страна")
    cem_house = forms.CharField(required=False, max_length=16, label="Дом",
                                     widget=forms.TextInput())
    cem_block = forms.CharField(required=False, max_length=16, label="Корпус",
                                     widget=forms.TextInput())
    cem_building = forms.CharField(required=False, max_length=16, label="Строение")
#    cem_customer_flat = forms.CharField(required=False, max_length=16, label="Квартира",
#                                    widget=forms.TextInput())
    username = forms.CharField(label="*Логин", max_length=30,
                               help_text="Допускаются только латинские буквы, цифры и знаки @ . + - _")
    last_name = forms.CharField(max_length=30, label="*Фамилия директора", widget=forms.TextInput())
    first_name = forms.CharField(required=False, max_length=30, label="Имя директора",
                                 widget=forms.TextInput())
    patronymic = forms.CharField(required=False, max_length=30, label="Отчество директора",
                                 widget=forms.TextInput())
    password1 = forms.CharField(max_length=18, widget=forms.PasswordInput(render_value=False), label="*Пароль")
    password2 = forms.CharField(max_length=18, widget=forms.PasswordInput(render_value=False), label="*Пароль(еще раз)")
    phone = forms.CharField(required=False, max_length=20, label="Телефон директора", widget=forms.TextInput())

    kpp = forms.CharField(required=False, max_length=9, label="КПП")

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
    region = forms.CharField(required=False, max_length=36, label="Регион", widget=forms.TextInput())
    new_region = forms.BooleanField(required=False, label="Новый регион")
    country = forms.CharField(required=False, max_length=24, label="Страна", widget=forms.TextInput())
    new_country = forms.BooleanField(required=False, label="Новая страна")
    house = forms.CharField(required=False, max_length=16, label="Дом", widget=forms.TextInput())
    block = forms.CharField(required=False, max_length=16, label="Корпус", widget=forms.TextInput())
    building = forms.CharField(required=False, max_length=16, label="Строение")
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
            if not street:
                raise forms.ValidationError("Отсутствует улица.")
            if not city:
                raise forms.ValidationError("Отсутствует нас. пункт.")
            if not region:
                raise forms.ValidationError("Отсутствует регион.")
            if not country:
                raise forms.ValidationError("Отсутствует страна.")
        if (block or building) and not house:
            raise forms.ValidationError("Отсутствует номер дома.")
        if (house or block or building) and not street:
            raise forms.ValidationError("Отсутствует улица.")
        if country:
            try:
                country_obj = GeoCountry.objects.get(name=country)
            except ObjectDoesNotExist:
                if not new_country:
                    raise forms.ValidationError("Указанная страна не существует.")
            if new_country:
                if not new_region:
                    raise forms.ValidationError("Указанный регион не существует.")
            else:
                try:
                    region_obj = GeoRegion.objects.get(country=country_obj, name=region)
                except ObjectDoesNotExist:
                    if not new_region:
                        raise forms.ValidationError("Указанный регион не существует.")
            if new_region:
                if not new_city:
                    raise forms.ValidationError("Указанный нас. пункт не существует.")
            else:
                try:
                    city_obj = GeoCity.objects.get(country=country_obj, region=region_obj, name=city)
                except ObjectDoesNotExist:
                    if not new_city:
                        raise forms.ValidationError("Указанный нас. пункт не существует.")
            if new_city:
                if not new_street:
                    raise forms.ValidationError("Указанная улица не существует.")
            else:
                try:
                    street_obj = Street.objects.get(city=city_obj, name=street)
                except ObjectDoesNotExist:
                    if not new_street:
                        raise forms.ValidationError("Указанная улица не существует.")
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
    phone = forms.CharField(max_length=20, label="Телефон", required=False)
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
class EditUserForm(forms.Form):
    """
    Форма редактирования пользователя системы.
    """
    username = forms.CharField(label="Имя пользователя", max_length=30,
                               help_text="Допускаются только латинские буквы, цифры и знаки @ . + - _")
    last_name = forms.CharField(max_length=30, label="Фамилия")
    first_name = forms.CharField(max_length=30, label="Имя", required=False)
    patronymic = forms.CharField(max_length=30, label="Отчество", required=False)
#    role = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), label="Роль")
#    is_staff = forms.BooleanField(required=False, label="Доступ в админку")
#    default_rights = forms.BooleanField(required=False, label="Поставить права по умолчанию")
#    phone = forms.CharField(max_length=20, label="Телефон", required=False)
    password1 = forms.CharField(required=False, max_length=18, widget=forms.PasswordInput(render_value=False),
                                label="Пароль")
    password2 = forms.CharField(required=False, max_length=18, widget=forms.PasswordInput(render_value=False),
                                label="Пароль (еще раз)")
    def clean(self):
        cd = self.cleaned_data
        username = cd["username"]
        # Проверка username на наличие недопустимых символов.
        rest = re.sub(RE_USERNAME, "", username)
        if rest:
            raise forms.ValidationError("Недопустимые символы в имени пользователя.")
#        try:
#            user = User.objects.get(username=username)
#        except ObjectDoesNotExist:
#            pass
#        else:
#            raise forms.ValidationError("Имя пользователя уже зарегистрировано за другим сотрудником.")
        if cd.get("password1", "") == cd.get("password2", ""):
            return cd
        else:
            raise forms.ValidationError("Пароли не совпадают.")

        
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

OrderPositionsFormset = forms.formsets.formset_factory(OrderPositionForm, extra=0)

class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_type', ]
        widgets = {
            'payment_type': forms.RadioSelect,
        }

class PrintOptionsForm(forms.Form):
    catafalque = forms.BooleanField(label=u"наряд на автокатафалк", required=False, initial=False)
    graving = forms.BooleanField(label=u"наряд на рытье могилы", required=False, initial=True)
    receipt = forms.BooleanField(label=u"справка о захоронении", required=False, initial=False)
    dogovor = forms.BooleanField(label=u"договор ответственного", required=False, initial=False)

class IDForm(forms.ModelForm):
    class Meta:
        model = PersonID
        exclude = ['person', ]
        widgets = {
            'when': CalendarWidget,
        }


