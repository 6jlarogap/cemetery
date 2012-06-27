# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.forms import formsets
from django.forms.models import model_to_dict

from cemetery.models import Cemetery, Operation, Place, Burial, UserProfile, Service, ServicePosition
from geo.models import Location, Country, Region, City, Street
from organizations.models import Doverennost, Organization
from persons.models import Person, DeathCertificate, PersonID
from utils.models import PER_PAGE_VALUES, ORDER_BY_VALUES

class SearchForm(forms.Form):
    """
    Форма поиска на главной странице.
    """
    operation = forms.ModelChoiceField(required=False, queryset=Operation.objects.all(), label="Услуга", empty_label="Все")
    fio = forms.CharField(required=False, max_length=100, label="ФИО")
    birth_date_from = forms.DateField(required=False, label="Дата рождения с")
    birth_date_to = forms.DateField(required=False, label="по")
    death_date_from = forms.DateField(required=False, label="Дата смерти с")
    death_date_to = forms.DateField(required=False, label="по")
    burial_date_from = forms.DateField(required=False, label="Дата захоронения с")
    burial_date_to = forms.DateField(required=False, label="по")
    account_number_from = forms.CharField(required=False, max_length=16, label="Номер от")
    account_number_to = forms.CharField(required=False, max_length=16, label="до")
    customer = forms.CharField(required=False, max_length=30, label="Заказчик")
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.all(), empty_label="Все", label="Кладбища")
    area = forms.CharField(required=False, max_length=9, label="Участок")
    row = forms.CharField(required=False, max_length=9, label="Ряд")
    seat = forms.CharField(required=False, max_length=9, label="Место")
    no_exhumated = forms.BooleanField(required=False, initial=False, label=u"Убрать эксгумированные")
    per_page = forms.ChoiceField(required=False, choices=PER_PAGE_VALUES, label=u"Записей на страницу")
    records_order_by = forms.ChoiceField(required=False, choices=ORDER_BY_VALUES, label=u"Сортировка по")
    page = forms.IntegerField(required=False, widget=forms.HiddenInput, label="Страница")

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place

    def save(self, user=None, commit=True):
        filter_fields = ['cemetery', 'row', 'area', 'seat']
        data = dict(filter(lambda i: i[0] in filter_fields, self.cleaned_data.items()))
        try:
            return Place.objects.get(**data)
        except Place.DoesNotExist:
            place = super(PlaceForm, self).save(commit=False)
            place.creator = user
            if commit:
                place.save()
            return place

class BurialForm(forms.ModelForm):
    responsible = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.HiddenInput, required=False)

    class Meta:
        model = Burial
        widgets = {
            'place': forms.HiddenInput(),
            'person': forms.HiddenInput(),
            'client_person': forms.HiddenInput(),
            'client_organization': forms.HiddenInput(),
            'doverennost': forms.HiddenInput(),
            'agent': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.place and instance.place.responsible:
            kwargs.setdefault('initial', {}).update({
                'responsible': instance.place.responsible,
            })
        super(BurialForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        burial = super(BurialForm, self).save(commit=False)
        if burial.place and self.cleaned_data.get('responsible'):
            burial.place.responsible = self.cleaned_data['responsible']
            burial.place.save()
        if commit:
            burial.save()

        print 'burial.client_person, burial.client_organization', burial.client_person, burial.client_organization
        return burial

class PersonForm(forms.ModelForm):
    instance = forms.ChoiceField(widget=forms.RadioSelect)

    INSTANCE_CHOICES = [
        ('', u'Не выбрано'),
        ('NEW', u'Новый'),
    ]

    class Meta:
        model = Person

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.data = dict(self.data.items())
        if self.data:
            person_kwargs = {
                'first_name__istartswith': self.data.get('first_name', ''),
                'last_name__istartswith': self.data.get('last_name', ''),
                'middle_name__istartswith': self.data.get('middle_name', ''),
            }
            if self.data.get('instance') not in [None, '', 'NEW']:
                self.instance = Person.objects.get(pk=self.data.get('instance'))
                self.fields['instance'].choices = self.INSTANCE_CHOICES + [
                    (str(p.pk), p) for p in Person.objects.filter(pk=self.data.get('instance'))
                ]
                if not self.data.get('selected'):
                    self.data = None
                    self.is_bound = False
                    self.initial = model_to_dict(self.instance, self._meta.fields, self._meta.exclude)
                    self.initial.update({'instance': self.instance.pk})
            else:
                self.fields['instance'].choices = self.INSTANCE_CHOICES + [
                    (str(p.pk), p) for p in Person.objects.filter(**person_kwargs)
                ]
                # self.data['instance'] = None
        else:
            self.fields['instance'].widget = forms.HiddenInput()
            self.data['instance'] = None

    def is_valid(self):
        if not self.is_bound or not self.data:
            return False

        if not self.data.get('instance'):
            return False

        if not self.data.get('selected'):
            return False

        return super(PersonForm, self).is_valid()

    def is_selected(self):
        is_old = self.instance and self.instance.pk
        is_new = self.data and self.data.get('instance')
        return is_old or is_new or False

    def save(self, location=None, commit=True):
        person = super(PersonForm, self).save(commit=False)
        if self.instance:
            person.pk = self.instance.pk
        person.address = location
        if commit:
            person.save()
        return person

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        widgets = {
            'country': forms.TextInput(attrs={'class': 'autocomplete'}),
            'region': forms.TextInput(attrs={'class': 'autocomplete'}),
            'city': forms.TextInput(attrs={'class': 'autocomplete'}),
            'street': forms.TextInput(attrs={'class': 'autocomplete'}),
        }

    def __init__(self, person=None, *args, **kwargs):
        if person and person.address:
            kwargs.update({'instance': person.address})
            kwargs.setdefault('initial', {}).update({
                'country': person.address.country.name,
                'region': person.address.region.name,
                'city': person.address.city.name,
                'street': person.address.street.name,
            })
        if kwargs.get('data', {}):
            kwargs['data'] = kwargs['data'] and kwargs['data'].copy() or {}
            if kwargs['data'].get('country'):
                d = kwargs['data']
                country, _tmp = Country.objects.get_or_create(name=d['country'])
                kwargs['data']['country'] = country.pk
                if kwargs.get('data', {}).get('region'):
                    region, _tmp = Region.objects.get_or_create(name=d['region'], country=country)
                    kwargs['data']['region'] = region.pk
                    if kwargs.get('data', {}).get('city'):
                        city, _tmp = City.objects.get_or_create(name=d['city'], region=region)
                        kwargs['data']['city'] = city.pk
                        if kwargs.get('data', {}).get('street'):
                            kwargs['data']['street'] = Street.objects.get_or_create(name=d['street'], city=city)[0].pk
        super(LocationForm, self).__init__(*args, **kwargs)

class DeathCertificateForm(forms.ModelForm):
    class Meta:
        model = DeathCertificate
        exclude = ['person']

    def save(self, person=None, commit=True):
        dc = super(DeathCertificateForm, self).save(commit=False)
        dc.person = person
        if commit:
            dc.save()
        return dc

OPF_FIZIK = 0
OPF_YURIK = 1
OPF_TYPES = (
    (OPF_FIZIK, u'Физ. лицо'),
    (OPF_YURIK, u'Юр. лицо'),
)

class CustomerForm(forms.Form):
    customer_type = forms.ChoiceField(label=u'Организационно-правовая форма', choices=OPF_TYPES)
    organization = forms.ModelChoiceField(label=u'Организация', queryset=Organization.objects.all())
    agent_director = forms.BooleanField(label=u'Директор - агент', required=False)
    agent_person = forms.ModelChoiceField(label=u'Агент', queryset=Person.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        qs = Person.objects.filter(agent__organization__isnull=False).distinct()
        self.fields['agent_person'].queryset = qs

    def is_person(self):
        return str(self.cleaned_data['customer_type']) == str(OPF_FIZIK)

    def get_agent(self):
        if self.cleaned_data['agent_director']:
            org = self.cleaned_data['organization']
            return org.ceo
        else:
            return self.cleaned_data['agent_person']

class CustomerIDForm(forms.ModelForm):
    class Meta:
        model = PersonID
        exclude = ['person']

    def save(self, person=None, commit=True):
        cid = super(CustomerIDForm, self).save(commit=False)
        cid.person = person
        if commit:
            cid.save()
        return cid

class DoverennostForm(forms.ModelForm):
    class Meta:
        model = Doverennost

    def save(self, commit=True):
        try:
            d = Doverennost.objects.get(**self.cleaned_data)
        except Doverennost.DoesNotExist:
            d = super(DoverennostForm, self).save(commit=False)
            if commit:
                d.save()
        return d

class UserProfileForm(forms.ModelForm):
    """
    Форма значений по умолчанию для профиля пользователя.
    """

    class Meta:
        model = UserProfile

class OrderPositionForm(forms.ModelForm):
    active = forms.BooleanField(required=False)

    class Meta:
        model = ServicePosition
        fields = ['service', 'count', 'price']
        widgets = {
            'service': forms.HiddenInput,
        }

class BaseOrderPositionsFormset(formsets.BaseFormSet):
    def __init__(self, *args, **kwargs):
        if kwargs.get('initial'):
            real_initial = []
            for i in kwargs['initial']:

                if isinstance(i['order_product'], Service):
                    q = models.Q(pk=i['order_product'].pk)
                else:
                    q = models.Q(name=i['order_product'])
                try:
                    Service.objects.get(q)
                except Service.DoesNotExist:
                    pass
                else:
                    real_initial.append(i)
            kwargs['initial'] = real_initial

        super(BaseOrderPositionsFormset, self).__init__(*args, **kwargs)


OrderPositionsFormset = forms.formsets.formset_factory(OrderPositionForm, extra=0, formset=BaseOrderPositionsFormset)

class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = Burial
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


