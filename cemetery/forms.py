# -*- coding: utf-8 -*-

from django import forms
from cemetery.models import Cemetery, Operation, Place, Burial
from geo.models import Location
from persons.models import Person
from utils.models import PER_PAGE_VALUES, ORDER_BY_VALUES

class SearchForm(forms.Form):
    """
    Форма поиска на главной странице.
    """
    fio = forms.CharField(required=False, max_length=100, label="ФИО")
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.all(), empty_label="Все", label="Кладбища")
    birth_date_from = forms.DateField(required=False, label="Дата рождения")
    birth_date_to = forms.DateField(required=False, label="")
    death_date_from = forms.DateField(required=False, label="Дата смерти")
    death_date_to = forms.DateField(required=False, label="")
    burial_date_from = forms.DateField(required=False, label="Дата захоронения")
    burial_date_to = forms.DateField(required=False, label="")
    account_book_n_from = forms.CharField(required=False, max_length=16, label="Номер от")
    account_book_n_to = forms.CharField(required=False, max_length=16, label="до")
    customer = forms.CharField(required=False, max_length=30, label="Заказчик")
    area = forms.CharField(required=False, max_length=9, label="Участок")
    row = forms.CharField(required=False, max_length=9, label="Ряд")
    seat = forms.CharField(required=False, max_length=9, label="Место")
    operation = forms.ModelChoiceField(required=False, queryset=Operation.objects.all(), label="Услуга", empty_label="Все")
    no_exhumated = forms.BooleanField(required=False, initial=False, label=u"Убрать эксгумированные")
    per_page = forms.ChoiceField(required=False, choices=PER_PAGE_VALUES, label=u"Записей на страницу")
    records_order_by = forms.ChoiceField(required=False, choices=ORDER_BY_VALUES, label=u"Сортировка по")
    page = forms.IntegerField(required=False, widget=forms.HiddenInput, label="Страница")

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place

class BurialForm(forms.ModelForm):
    class Meta:
        model = Burial
        exclude = [
            'person', 'place', 'client_person', 'client_organization',
            'agent', 'responsible', 'organization', 'doverennost', 'deleted',
        ]

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        widgets = {
            'country': forms.TextInput(attrs={'class': 'autocomplete'}),
            'region': forms.TextInput(attrs={'class': 'autocomplete'}),
            'city': forms.TextInput(attrs={'class': 'autocomplete'}),
            'street': forms.TextInput(attrs={'class': 'autocomplete'}),
        }

