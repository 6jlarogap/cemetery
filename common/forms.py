# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from models import Cemetery, GeoCountry, GeoRegion, Organization, GeoCity, Phone, Operation, Street, Role
from models import SoulProducttypeOperation

from annoying.decorators import autostrip

from stdimage.forms import StdImageFormField

import re
import string


PER_PAGE_VALUES = (
    (5, '5'),
    (10, '10'),
    (15, '15'),
    (25, '25'),
    (50, '50'),
)

GOOD_CHARS = string.ascii_letters + string.digits + "@.+-_"

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
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.all(),
                                      empty_label="Все", label="Кладбища")
    birth_date_from = forms.DateField(required=False, label="Дата рождения с", widget=CalendarWidget)
    birth_date_to = forms.DateField(required=False, label="Дата рождения по", widget=CalendarWidget)
    death_date_from = forms.DateField(required=False, label="Дата смерти с", widget=CalendarWidget)
    death_date_to = forms.DateField(required=False, label="Дата смерти по", widget=CalendarWidget)
    burial_date_from = forms.DateField(required=False, label="Дата захоронения с", widget=CalendarWidget)
    burial_date_to = forms.DateField(required=False, label="Дата захоронения по", widget=CalendarWidget)
    death_certificate = forms.CharField(required=False, max_length=30, label="Номер свидетельства о смерти")
    account_book_n = forms.CharField(required=False, max_length=9, label="Номер в книге учета")
    customer = forms.CharField(required=False, max_length=30, label="Фамилия заказчика")
    owner = forms.ModelChoiceField(required=False, queryset=User.objects.all(), empty_label="Не выбран",
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


@autostrip
class EditUserForm(forms.Form):
    """
    Форма создания нового пользователя системы.
    """
    username = forms.CharField(label="Имя пользователя", max_length=30,
                               help_text="Допускаются только латинские буквы, цифры и знаки @ . + - _")
    last_name = forms.CharField(max_length=30, label="Фамилия")
    first_name = forms.CharField(max_length=30, label="Имя", required=False)
    patronymic = forms.CharField(max_length=30, label="Отчество", required=False)
    role = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), label="Роль")
    is_staff = forms.BooleanField(required=False, label="Доступ в админку")
    default_rights = forms.BooleanField(required=False, label="Поставить права по умолчанию")
#    phone = forms.CharField(max_length=15, label="Телефон", required=False)
    password1 = forms.CharField(required=False, max_length=18, widget=forms.PasswordInput(render_value=False),
                                label="Пароль")
    password2 = forms.CharField(required=False, max_length=18, widget=forms.PasswordInput(render_value=False),
                                label="Пароль (еще раз)")
    def clean(self):
        cd = self.cleaned_data
        username = cd["username"]
        # Проверка username на наличие недопустимых символов.
        rest = re.sub(r"[a-zA-Z0-9\@\.\+\-\_]", "", username)
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
class CemeteryForm(forms.Form):
    """
    Форма создания кладбища.
    """
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), label="Организация", empty_label=None)
    name = forms.CharField(max_length=99, label="Название")
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
    role = forms.ModelChoiceField(queryset=Role.objects.all(), label="Роль")
    is_staff = forms.BooleanField(required=False, label="Доступ в админку")
    phone = forms.CharField(max_length=15, label="Телефон", required=False)
    password1 = forms.CharField(max_length=18, widget=forms.PasswordInput(render_value=False), label="Пароль")
    password2 = forms.CharField(max_length=18, widget=forms.PasswordInput(render_value=False), label="Пароль (еще раз)")
    def clean(self):
        cd = self.cleaned_data
        username = cd["username"]
        # Проверка username на наличие недопустимых символов
        rest = re.sub(r"[a-zA-Z0-9\@\.\+\-\_]", "", username)
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
class UserProfileForm(forms.Form):
    """
    Форма значений по умолчанию для профиля пользователя.
    """
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.all(), label="Кладбище")
    operation = forms.ModelChoiceField(required=False, queryset=Operation.objects.all(), label="Услуга")
    hoperation = forms.IntegerField(required=False, widget=forms.HiddenInput)
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


@autostrip
class EditOrderForm(forms.Form):
    burial_date = forms.DateField(label="Дата захоронения*", widget=CalendarWidget(attrs={"tabindex": "2"}))
    cemetery = forms.ModelChoiceField(queryset=Cemetery.objects.all(), label="Кладбище*", empty_label=None)
    operation = forms.ModelChoiceField(queryset=Operation.objects.all(), label="Услуга*", empty_label=None,
                                       widget=forms.Select(attrs={"tabindex": "6"}))
    hoperation = forms.IntegerField(required=False, widget=forms.HiddenInput)
    area = forms.CharField(max_length=9, label="Участок*", widget=forms.TextInput(attrs={"tabindex": "7"}))
    row = forms.CharField(max_length=9, label="Ряд*", widget=forms.TextInput(attrs={"tabindex": "8"}))
    seat = forms.CharField(max_length=9, label="Место*", widget=forms.TextInput(attrs={"tabindex": "9"}))
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
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 90, 'tabindex': '21'}),
                              label="Комментарий")
    file1 = StdImageFormField(required=False, label="Картинка (до 5 Mb)")
    file1_comment = forms.CharField(required=False, max_length=96, widget=forms.Textarea(attrs={'rows': 1, 'cols': 64}),
                              label="Комментарий к файлу")
    def clean(self):
        cd = self.cleaned_data
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
        street = cd.get("street", "")
        if country and region and city and street:
            # Страна.
            try:
                country_object = GeoCountry.objects.get(name__iexact=country)
            except ObjectDoesNotExist:
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
                region_object = GeoRegion.objects.get(country__name__iexact=country, name__iexact=region)
            except ObjectDoesNotExist:
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
                city_object = GeoCity.objects.get(region__name__iexact=region, name__iexact=city)
            except ObjectDoesNotExist:
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
                street_object = Street.objects.get(city__name__iexact=city, name__iexact=street)
            except ObjectDoesNotExist:
                if not cd.get("new_street", False):
                    raise forms.ValidationError("Улица не найдена.")
            else:
                if cd.get("new_street", False):
                    raise forms.ValidationError("Улица с таким именем уже существует в выбранном нас. пункте.")
        else:
            if country or region or city or street:  # Есть, но не все.
                raise forms.ValidationError("Не все поля адреса заполнены.")
        return cd
#    def __init__(self, *args, **kwargs):
#        orgsoul = kwargs.pop('orgsoul')
#        super(EditOrderForm, self).__init__(*args, **kwargs)
#        choices = list(SoulProducttypeOperation.objects.filter(soul=orgsoul, p_type=settings.BURIAL_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type"))
#        choices.insert(0, (0, u'----------------'))
##        choices = SoulProducttypeOperation.objects.filter(soul=orgsoul, p_type=settings.BURIAL_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type")
#        self.fields["operation"].choices = choices


@autostrip
class JournalForm(forms.Form):
    """
    Форма создания нового захоронения.
    """
    cemetery = forms.ModelChoiceField(queryset=Cemetery.objects.all(),
                                      label="Кладбище*")
    operation = forms.ModelChoiceField(queryset=Operation.objects.all(), label="Услуга*", empty_label=None,
                                       widget=forms.Select(attrs={"tabindex": "6"}))
    hoperation = forms.IntegerField(required=False, widget=forms.HiddenInput)

    burial_date = forms.DateField(label="Дата захоронения*", widget=CalendarWidget(attrs={"tabindex": "2"}))
    comment = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={'rows': 4,
                                                           'cols': 90,
                                                           'tabindex': "21"}),
                              label="Комментарий")
    account_book_n = forms.CharField(max_length=9, label="Номер в книге учета*",
                                     widget=forms.TextInput(attrs={"tabindex": "1"}))
    last_name = forms.CharField(max_length=30, label="Фамилия*", widget=forms.TextInput(attrs={"tabindex": "3"}))
    first_name = forms.CharField(required=False, max_length=30, label="Имя",
                                 widget=forms.TextInput(attrs={"tabindex": "4"}))
    patronymic = forms.CharField(required=False, max_length=30, label="Отчество",
                                 widget=forms.TextInput(attrs={"tabindex": "5"}))
    customer_last_name = forms.CharField(max_length=30, label="Фамилия заказчика*",
                                         widget=forms.TextInput(attrs={"tabindex": "10"}))
    customer_first_name = forms.CharField(required=False, max_length=30, label="Имя заказчика",
                                          widget=forms.TextInput(attrs={"tabindex": "11"}))
    customer_patronymic = forms.CharField(required=False, max_length=30, label="Отчество заказчика",
                                          widget=forms.TextInput(attrs={"tabindex": "12"}))
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
                                     widget=forms.TextInput(attrs={"tabindex": "18"}))
    customer_block = forms.CharField(required=False, max_length=16, label="Корпус",
                                     widget=forms.TextInput(attrs={"tabindex": "19"}))
    customer_building = forms.CharField(required=False, max_length=16, label="Строение")
    customer_flat = forms.CharField(required=False, max_length=16, label="Квартира",
                                    widget=forms.TextInput(attrs={"tabindex": "20"}))
    customer_phone = forms.CharField(required=False, max_length=15, label="Телефон",
                                     widget=forms.TextInput(attrs={"tabindex": "13"}))
    area = forms.CharField(max_length=9, label="Участок*", widget=forms.TextInput(attrs={"tabindex": "7"}))
    row = forms.CharField(max_length=9, label="Ряд*", widget=forms.TextInput(attrs={"tabindex": "8"}))
    seat = forms.CharField(max_length=9, label="Место*", widget=forms.TextInput(attrs={"tabindex": "9"}))
    file1 = StdImageFormField(required=False, label="Картинка (до 5 Mb)")
    file1_comment = forms.CharField(required=False, max_length=96, widget=forms.Textarea(attrs={'rows': 1, 'cols': 64}),
                                    label="Комментарий к файлу")
#    def __init__(self, *args, **kwargs):
#        super(JournalForm, self).__init__(*args, **kwargs)
#        cemetery = Cemetery.objects.all()[0]
#        choices = list(SoulProducttypeOperation.objects.filter(soul=cemetery.organization.soul_ptr,
#                p_type=settings.BURIAL_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type"))
#        choices.insert(0, (0, u'----------------'))
##        choices = SoulProducttypeOperation.objects.filter(soul=orgsoul, p_type=settings.BURIAL_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type")
#        self.fields["operation"].choices = choices
    def clean(self):
        cd = self.cleaned_data
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
        # Валидация полей Location (страна, регион, нас. пункт, улица).
        country = cd.get("country", "")
        region = cd.get("region", "")
        city = cd.get("city", "")
        street = cd.get("street", "")
        house = cd.get("customer_house", "")
        block = cd.get("customer_block", "")
        building = cd.get("customer_building", "")
        flat = cd.get("customer_flat", "")
        if country and region and city and street:
            # Страна.
            try:
                country_object = GeoCountry.objects.get(name__iexact=country)
            except ObjectDoesNotExist:
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
                region_object = GeoRegion.objects.get(country__name__iexact=country, name__iexact=region)
            except ObjectDoesNotExist:
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
                city_object = GeoCity.objects.get(region__name__iexact=region, name__iexact=city)
            except ObjectDoesNotExist:
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
            if country or region or city or street:  # Есть, но не все.
                raise forms.ValidationError("Не все поля адреса заполнены.")
            if house or block or building or flat:
                raise forms.ValidationError("Не выбрана улица.")
        return cd


@autostrip
class InitalForm(forms.Form):
    """
    Форма ввода данных для инициализации системы.
    """
    org_name = forms.CharField(label="*Название организации", max_length=99)
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
    phone = forms.CharField(required=False, max_length=15, label="Телефон директора",
                                     widget=forms.TextInput())
    def clean_username(self):
        """
        Проверка логина на отсутствие недопустимых символов.
        """
        un = self.cleaned_data["username"]
        for ch in un:
            if ch not in GOOD_CHARS:
                raise forms.ValidationError("Введены недопустимые символы.")
        return un
    def clean(self):
        cd = self.cleaned_data
        if cd.get("password1", "") == cd.get("password2", ""):
            return cd
        else:
            raise forms.ValidationError("Пароли не совпадают.")


class ImportForm(forms.Form):
    """
    Форма импорта csv-файла.
    """""
    csv_file = forms.FileField(label="CSV файл")
    cemetery = forms.ModelChoiceField(queryset = Cemetery.objects.all(), label = "Кладбище")
