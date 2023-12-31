# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from models import Cemetery, GeoCountry, GeoRegion, Organization, GeoCity, Phone, Operation, Street, Role, OrderComments
from models import SoulProducttypeOperation

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

class CalendarWidget(forms.TextInput):
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


@autostrip
class SearchForm(forms.Form):
    """
    Форма поиска на главной странице.
    """
    fio = forms.CharField(required=False, max_length=100, label="ФИО")
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.order_by("name"),
                                      empty_label="Все", label="Кладбища")
    burial_date_from = forms.DateField(required=False, label="Дата захоронения с", widget=CalendarWidget)
    burial_date_to = forms.DateField(required=False, label="Дата захоронения по", widget=CalendarWidget)
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
    exclude_operation = forms.BooleanField(required=False, label=u"кроме выбранной")


@autostrip
class JournalForm(forms.Form):
    """
    Форма журнала - создания нового захоронения.
    """

    account_book_n = forms.CharField(max_length=16, label="Номер в книге учета*",
                                     widget=forms.TextInput(attrs={"tabindex": "1"}))
    burial_date = forms.DateField(label="Дата захоронения*", widget=CalendarWidget(attrs={"tabindex": "2"}),
                                  initial=datetime.date.today().strftime("%d.%m.%Y"))
    last_name = forms.CharField(max_length=128, label="Фамилия*", widget=forms.TextInput(attrs={"tabindex": "3"}),
            help_text="Допускаются только буквы, цифры и символ '-'", initial=u"НЕИЗВЕСТЕН")
    first_name = forms.CharField(required=False, max_length=30, label="Имя",
                                 widget=forms.TextInput(attrs={"tabindex": "4"}))
    patronymic = forms.CharField(required=False, max_length=30, label="Отчество",
                                 widget=forms.TextInput(attrs={"tabindex": "5"}))
    cemetery = forms.ModelChoiceField(queryset=Cemetery.objects.all(), label="Кладбище*",
                                       widget=forms.Select(attrs={"tabindex": "6"}))
    operation = forms.ModelChoiceField(queryset=Operation.objects.all(), label="Услуга*", empty_label=None,
                                       widget=forms.Select(attrs={"tabindex": "7"}))
    hoperation = forms.CharField(required=False, widget=forms.HiddenInput)
    area = forms.CharField(max_length=9, label="Участок*", widget=forms.TextInput(attrs={"tabindex": "8"}))
    row = forms.CharField(max_length=9, label="Ряд*", widget=forms.TextInput(attrs={"tabindex": "9"}))
    seat = forms.CharField(max_length=9, label="Место*", widget=forms.TextInput(attrs={"tabindex": "10"}))
    customer_last_name = forms.CharField(max_length=30, label="Фамилия заказчика*",
                                         widget=forms.TextInput(attrs={"tabindex": "11"}),
                                         help_text="Допускаются только буквы, цифры и символ '-'",
                                         initial=u"НЕИЗВЕСТЕН")
    customer_first_name = forms.CharField(required=False, max_length=30, label="Имя заказчика",
                                          widget=forms.TextInput(attrs={"tabindex": "12"}))
    customer_patronymic = forms.CharField(required=False, max_length=30, label="Отчество заказчика",
                                          widget=forms.TextInput(attrs={"tabindex": "13"}))
    post_index = forms.CharField(required=False, max_length=16, label="Почтовый индекс",
                             widget=forms.TextInput(attrs={"tabindex": "14"}))
#    customer_phone = forms.CharField(required=False, max_length=20, label="Телефон",
#                                     widget=forms.TextInput(attrs={"tabindex": "14"}))
    street = forms.CharField(required=False, max_length=99, label="Улица",
                             widget=forms.TextInput(attrs={"tabindex": "15"}),
                             initial=u"НЕИЗВЕСТЕН")
    new_street = forms.BooleanField(required=False, label="Новая улица")
    city = forms.CharField(required=False, max_length=36, label="Нас. пункт",
                           widget=forms.TextInput(attrs={"tabindex": "16"}))
    new_city = forms.BooleanField(required=False, label="Новый нас. пункт")
    region = forms.CharField(required=False, max_length=36, label="Регион",
                             widget=forms.TextInput(attrs={"tabindex": "17"}))
    new_region = forms.BooleanField(required=False, label="Новый регион")
    country = forms.CharField(required=False, max_length=24, label="Страна",
                              widget=forms.TextInput(attrs={"tabindex": "18"}))
    new_country = forms.BooleanField(required=False, label="Новая страна")
    customer_house = forms.CharField(required=False, max_length=16, label="Дом",
                                     widget=forms.TextInput(attrs={"tabindex": "19"}))
    customer_block = forms.CharField(required=False, max_length=16, label="Корпус",
                                     widget=forms.TextInput(attrs={"tabindex": "20"}))
    customer_building = forms.CharField(required=False, max_length=16, label="Строение")
    customer_flat = forms.CharField(required=False, max_length=16, label="Квартира",
                                    widget=forms.TextInput(attrs={"tabindex": "21"}))
    comment = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows': 4,
                                                           'cols': 90,
                                                           'tabindex': "23"}),
                              label="Комментарий")
    file1 = forms.FileField(required=False, label="Файл")
    file1_comment = forms.CharField(required=False, max_length=96, widget=forms.Textarea(attrs={'rows': 1, 'cols': 64}),
                                    label="Комментарий к файлу")
    def __init__(self, *args, **kwargs):
        cem = kwargs.pop('cem', None)
        oper = kwargs.pop('oper', None)
        super(JournalForm, self).__init__(*args, **kwargs)
        if cem:
            self.fields["cemetery"].initial = cem
        if oper:
            self.fields["operation"].initial = oper
#        cemetery = Cemetery.objects.all()[0]
#        choices = list(SoulProducttypeOperation.objects.filter(soul=cemetery.organization.soul_ptr,
#                p_type=settings.BURIAL_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type"))
#        choices.insert(0, (0, u'----------------'))
##        choices = SoulProducttypeOperation.objects.filter(soul=orgsoul, p_type=settings.BURIAL_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type")
#        self.fields["operation"].choices = choices
    def clean(self):
        cd = self.cleaned_data
        # Проверка имен усопшего и заказчика на наличие недопустимых символов
        last_name = cd["last_name"]
        rest = re.sub(RE_LASTNAME, "", last_name)
        if rest:
            raise forms.ValidationError("Недопустимые символы в имени усопшего. Допускаются только буквы, цифры и тире")
#        cust_last_name = cd["customer_last_name"]
#        rest = re.sub(RE_LASTNAME, "", cust_last_name)
#        if rest:
#            raise forms.ValidationError("Недопустимые символы в имени Заказчика.")
        # Валидация кладбища/операции.
        operation = cd.get("operation", None)
        if not operation:
            raise forms.ValidationError("Не выбрана услуга.")
        cemetery = cd["cemetery"]
        try:
            spo = SoulProducttypeOperation.objects.get(soul=cemetery.organization.soul_ptr, operation=operation,
                                                       p_type=settings.PLACE_PRODUCTTYPE_ID)
        except:
            raise forms.ValidationError("Выбранная операция не существует для выбранного кладбища.")
        # Валидация полей Location (страна, регион, нас. пункт, улица).
        country = cd.get("country", "")
        region = cd.get("region", "")
        city = cd.get("city", "")
        rest = re.sub(RE_CITY, "", city)
        if rest:
            raise forms.ValidationError("Недопустимые символы в имени населенного пункта. Допускаются только буквы, цифры, тире и точка")
        street = cd.get("street", "")
        house = cd.get("customer_house", "")
        block = cd.get("customer_block", "")
        building = cd.get("customer_building", "")
        flat = cd.get("customer_flat", "")
        if country and region and city and street:
            # Страна.
            try:
                country_object = GeoCountry.objects.filter(name__exact=country)[0]
            except IndexError:
                if not cd.get("new_country", False):
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
                region_object = GeoRegion.objects.filter(country__name__exact=country, name__exact=region)[0]
            except IndexError:
                if not cd.get("new_region", False):
                    raise forms.ValidationError("Регион не найден.")
                else:
                    new_region = True
            else:
                if not cd.get("new_region", False):
                    new_region = False
                else:
                    raise forms.ValidationError("Регион с таким именем уже существует в выбранной стране.")
            # Нас. пункт.
            if new_region and not cd.get("new_city", False):
                raise forms.ValidationError("У нового региона нас. пункт должен быть тоже новым.")
            try:
                city_object = GeoCity.objects.filter(region__name__exact=region, name__exact=city)[0]
            except IndexError:
                if not cd.get("new_city", False):
                    raise forms.ValidationError("Нас. пункт не найден.")
                else:
                    new_city = True
            else:
                if not cd.get("new_city", False):
                    new_city = False
                else:
                    raise forms.ValidationError("Нас. пункт с таким именем уже существует в выбранном регионе.")
            # Улица.
            if new_city and not cd.get("new_street", False):
                raise forms.ValidationError("У нового нас. пункта улица должна быть тоже новой.")
            try:
                street_object = Street.objects.filter(city__name__exact=city, name__exact=street)[0]
            except IndexError:
                if not cd.get("new_street", False):
                    raise forms.ValidationError("Улица не найдена.")
            else:
                if cd.get("new_street", False):
                    raise forms.ValidationError("Улица с таким именем уже существует в выбранном нас. пункте.")
            if block or building or flat:
                if not house:
                    raise forms.ValidationError("Не указан дом.")
        else:
#            if country or region or city or street:  # Есть, но не все.
            if country or region or city:  # Есть, но не все.
                raise forms.ValidationError("Не все поля адреса заполнены.")
            if house or block or building or flat:
                raise forms.ValidationError("Не выбрана улица.")
        return cd


@autostrip
class EditBurialForm(forms.Form):
    account_book_n = forms.CharField(max_length=16, label="Номер в книге учета*",
                                     widget=forms.TextInput(attrs={"tabindex": "1"}))
    burial_date = forms.DateField(label="Дата захоронения*",
                                  widget=(forms.TextInput if settings.SITE_READONLY else CalendarWidget(attrs={"tabindex": "2"})))
    last_name = forms.CharField(max_length=128, label="Фамилия*", widget=forms.TextInput(attrs={"tabindex": "3"}),
            help_text="Допускаются только буквы, цифры и символ '-'")
    first_name = forms.CharField(required=False, max_length=30, label="Имя",
                                 widget=forms.TextInput(attrs={"tabindex": "4"}))
    patronymic = forms.CharField(required=False, max_length=30, label="Отчество",
                                 widget=forms.TextInput(attrs={"tabindex": "5"}))
    cemetery = forms.ModelChoiceField(queryset=Cemetery.objects.all(), label="Кладбище*", empty_label=None)
    operation = forms.ModelChoiceField(queryset=Operation.objects.all(), label="Услуга*", empty_label=None,
                                       widget=forms.Select(attrs={"tabindex": "6"}))
    hoperation = forms.CharField(required=False, widget=forms.HiddenInput)
    area = forms.CharField(max_length=9, label="Участок*", widget=forms.TextInput(attrs={"tabindex": "7"}))
    row = forms.CharField(max_length=9, label="Ряд*", widget=forms.TextInput(attrs={"tabindex": "8"}))
    seat = forms.CharField(max_length=9, label="Место*", widget=forms.TextInput(attrs={"tabindex": "9"}))
    customer_last_name = forms.CharField(max_length=30, label="Фамилия заказчика*",
                                         widget=forms.TextInput(attrs={"tabindex": "10"}),
                                         help_text="Допускаются только буквы, цифры и символ '-'",
                                         initial=u"НЕИЗВЕСТЕН")
    customer_first_name = forms.CharField(required=False, max_length=30, label="Имя заказчика",
                                          widget=forms.TextInput(attrs={"tabindex": "11"}))
    customer_patronymic = forms.CharField(required=False, max_length=30, label="Отчество заказчика",
                                          widget=forms.TextInput(attrs={"tabindex": "12"}))
    post_index = forms.CharField(required=False, max_length=16, label="Почтовый индекс",
                             widget=forms.TextInput(attrs={"tabindex": "13"}))
    street = forms.CharField(required=False, max_length=99, label="Улица",
                             widget=forms.TextInput(attrs={"tabindex": "14"}))
    new_street = forms.BooleanField(required=False, label="Новая улица")
    city = forms.CharField(required=False, max_length=36, label="Нас. пункт",
                           widget=forms.TextInput(attrs={"tabindex": "15"}))
    new_city = forms.BooleanField(required=False, label="Новый нас. пункт")
    region = forms.CharField(required=False, max_length=36, label="Регион",
                             widget=forms.TextInput(attrs={"tabindex": "16"}))
    new_region = forms.BooleanField(required=False, label="Новый регион")
    country = forms.CharField(required=False, max_length=24, label="Страна",
                              widget=forms.TextInput(attrs={"tabindex": "17"}))
    new_country = forms.BooleanField(required=False, label="Новая страна")
    customer_house = forms.CharField(required=False, max_length=16, label="Дом",
                                     widget=forms.TextInput(attrs={"tabindex": "19"}))
    customer_block = forms.CharField(required=False, max_length=16, label="Корпус",
                                     widget=forms.TextInput(attrs={"tabindex": "20"}))
    customer_building = forms.CharField(required=False, max_length=16, label="Строение")
    customer_flat = forms.CharField(required=False, max_length=16, label="Квартира",
                                    widget=forms.TextInput(attrs={"tabindex": "21"}))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 90, 'tabindex': '22'}),
                              label="Комментарий")
    file1 = forms.FileField(required=False, label="Файл")
    file1_comment = forms.CharField(required=False, max_length=96, widget=forms.Textarea(attrs={'rows': 1, 'cols': 64}),
                              label="Комментарий к файлу")
    in_trash = forms.BooleanField(required=False, label="В корзине")
    def clean(self):
        cd = self.cleaned_data
        # Проверка имен усопшего и заказчика на наличие недопустимых символов
        last_name = cd["last_name"]
        rest = re.sub(RE_LASTNAME, "", last_name)
        if rest:
            raise forms.ValidationError("Недопустимые символы в фамилии усопшего.")
#        cust_last_name = cd["customer_last_name"]
#        rest = re.sub(RE_LASTNAME, "", cust_last_name)
#        if rest:
#            raise forms.ValidationError("Недопустимые символы в фамилии Заказчика.")
        # Валидация кладбища/операции.
        operation = cd.get("operation", None)
        if not operation:
            raise forms.ValidationError("Не выбрана операция.")
        cemetery = cd["cemetery"]
        try:
            spo = SoulProducttypeOperation.objects.get(soul=cemetery.organization.soul_ptr, operation=operation,
                                                       p_type=settings.PLACE_PRODUCTTYPE_ID)
        except:
            raise forms.ValidationError("Выбранная операция не существует для выбранного кладбища.")
        # Коммент и файлы.
        comment = cd.get("comment", "")
        file1 = cd.get("file1", None)
        file1_comment = cd.get("file1_comment", "")
        if file1_comment and not file1:
            raise forms.ValidationError("Не выбран файл.")
        # Валидация полей Location (страна, регион, нас. пункт, улица).
        country = cd.get("country", "")
        region = cd.get("region", "")
        city = cd.get("city", "")
        rest = re.sub(RE_CITY, "", city)
        if rest:
            raise forms.ValidationError("Недопустимые символы в имени населенного пункта. Допускаются только буквы, цифры, тире, точка и пробел")
        street = cd.get("street", "")
        house = cd.get("customer_house", "")
        block = cd.get("customer_block", "")
        building = cd.get("customer_building", "")
        flat =  cd.get("customer_flat", "")
        if country and region and city and street:
            # Страна.
            try:
                country_object = GeoCountry.objects.filter(name__exact=country)[0]
            except IndexError:
                if not cd.get("new_country", False):
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
                region_object = GeoRegion.objects.filter(country__name__exact=country, name__exact=region)[0]
            except IndexError:
                if not cd.get("new_region", False):
                    raise forms.ValidationError("Регион не найден.")
                else:
                    new_region = True
            else:
                if not cd.get("new_region", False):
                    new_region = False
                else:
                    raise forms.ValidationError("Регион с таким именем уже существует в выбранной стране.")
            # Нас. пункт.
            if new_region and not cd.get("new_city", False):
                raise forms.ValidationError("У нового региона нас. пункт должен быть тоже новым.")
            try:
                city_object = GeoCity.objects.filter(region__name__exact=region, name__exact=city)[0]
            except IndexError:
                if not cd.get("new_city", False):
                    raise forms.ValidationError("Нас. пункт не найден.")
                else:
                    new_city = True
            else:
                if not cd.get("new_city", False):
                    new_city = False
                else:
                    raise forms.ValidationError("Нас. пункт с таким именем уже существует в выбранном регионе.")
            # Улица.
            if new_city and not cd.get("new_street", False):
                raise forms.ValidationError("У нового нас. пункта улица должна быть тоже новой.")
            try:
                street_object = Street.objects.filter(city__name__exact=city, name__exact=street)[0]
            except IndexError:
                if not cd.get("new_street", False):
                    raise forms.ValidationError("Улица не найдена.")
            else:
                if cd.get("new_street", False):
                    raise forms.ValidationError("Улица с таким именем уже существует в выбранном нас. пункте.")
            if block or building or flat:
                if not house:
                    raise forms.ValidationError("Не указан дом.")
        else:
            if country or region or city or street:  # Есть, но не все.
                raise forms.ValidationError("Не все поля адреса заполнены.")
            if house or block or building or flat:
                raise forms.ValidationError("Не выбрана улица.")
        return cd
#    def __init__(self, *args, **kwargs):
#        orgsoul = kwargs.pop('orgsoul')
#        super(EditOrderForm, self).__init__(*args, **kwargs)
#        choices = list(SoulProducttypeOperation.objects.filter(soul=orgsoul, p_type=settings.BURIAL_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type"))
#        choices.insert(0, (0, u'----------------'))
##        choices = SoulProducttypeOperation.objects.filter(soul=orgsoul, p_type=settings.BURIAL_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type")
#        self.fields["operation"].choices = choices


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
    phone = forms.CharField(required=False, max_length=20, label="Телефон директора",
                                     widget=forms.TextInput())
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
    password1 = forms.CharField(required=False, max_length=18, widget=forms.PasswordInput(render_value=False),
                                label="Пароль")
    password2 = forms.CharField(required=False, max_length=18, widget=forms.PasswordInput(render_value=False),
                                label="Пароль (еще раз)")
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
        if cd.get("password1", "") != cd.get("password2", ""):
            raise forms.ValidationError("Пароли не совпадают.")
        return cd


