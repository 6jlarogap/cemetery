# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
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
    CUSTOMER_TYPES = (
        ('', u"Все"),
        ('client_person', u"ФЛ"),
        ('client_organization', u"ЮЛ"),
    )

    fio = forms.CharField(required=False, max_length=100, label="ФИО")
    customer_type = forms.ChoiceField(required=False, choices=CUSTOMER_TYPES, label=u"Тип заказчика")
    birth_date_from = forms.DateField(required=False, label="Дата рождения с")
    birth_date_to = forms.DateField(required=False, label="по")
    death_date_from = forms.DateField(required=False, label="Дата смерти с")
    death_date_to = forms.DateField(required=False, label="по")
    burial_date_from = forms.DateField(required=False, label="Дата захоронения с")
    burial_date_to = forms.DateField(required=False, label="по")
    account_number_from = forms.CharField(required=False, max_length=16, label="Номер от")
    account_number_to = forms.CharField(required=False, max_length=16, label="до")
    customer = forms.CharField(required=False, max_length=30, label="Заказчик")
    responsible = forms.CharField(required=False, max_length=30, label="Ответственный")
    operation = forms.ModelChoiceField(required=False, queryset=Operation.objects.all(), label="Услуга", empty_label="Все")
    cemetery = forms.ModelChoiceField(required=False, queryset=Cemetery.objects.all(), empty_label="Все", label="Кладбища")
    area = forms.CharField(required=False, max_length=9, label="Участок")
    row = forms.CharField(required=False, max_length=9, label="Ряд")
    seat = forms.CharField(required=False, max_length=9, label="Место")
    no_exhumated = forms.BooleanField(required=False, initial=False, label=u"Убрать эксгумированные")

    records_order_by = forms.ChoiceField(required=False, choices=ORDER_BY_VALUES, label=u"Сортировка по")
    per_page = forms.ChoiceField(required=False, choices=PER_PAGE_VALUES, label=u"Записей на страницу")

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place

    def clean_account_number(self):
        a = self.cleaned_data['seat']
        if not a:
            return a
        if len(a) != 8:
            raise forms.ValidationError(u"Необходимо ровно 8 цифр")
        if not a.isdigit():
            raise forms.ValidationError(u"Допустимы только цифры")
        return a

    def save(self, user=None, commit=True):
        filter_fields = ['cemetery', 'row', 'area', 'seat']
        data = dict(filter(lambda i: i[0] in filter_fields, self.cleaned_data.items()))
        try:
            if self.cleaned_data['seat']:
                return Place.objects.get(**data)
        except Place.DoesNotExist:
            pass

        place = super(PlaceForm, self).save(commit=False)
        place.creator = user
        if commit:
            place.save()
        return place

class BurialForm(forms.ModelForm):
    responsible = forms.ModelChoiceField(queryset=Person.objects.all(), widget=forms.HiddenInput, required=False)

    class Meta:
        model = Burial
        exclude = ['payment_type', ]
        widgets = {
            'place': forms.HiddenInput(),
            'person': forms.HiddenInput(),
            'client_person': forms.HiddenInput(),
            'client_organization': forms.HiddenInput(),
            'doverennost': forms.HiddenInput(),
            'agent': forms.HiddenInput(),
        }

    def clean_account_number(self):
        a = self.cleaned_data['account_number']
        if not a:
            return a
        if len(a) != 8:
            raise forms.ValidationError(u"Необходимо ровно 8 цифр")
        if not a.isdigit():
            raise forms.ValidationError(u"Допустимы только цифры")

        place = Place.objects.get(pk=self.data['place'])
        burials = Burial.objects.all().filter(place__cemetery=place.cemetery)
        if self.instance:
            burials = burials.exclude(pk=self.instance.pk)
        try:
            burials.filter(account_number=a)[0]
        except IndexError:
            return a
        else:
            raise forms.ValidationError(u"Этот номер уже используется")

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

        if burial.place and not burial.place.seat:
            burial.place.seat = unicode(burial.account_number or burial.pk)
            burial.place.save()

        return burial

class PersonForm(forms.ModelForm):
    instance = forms.ChoiceField(widget=forms.RadioSelect, required=False)

    INSTANCE_CHOICES = [
        ('', u'Не выбрано'),
        ('NEW', u'Новый'),
    ]

    class Meta:
        model = Person
        widgets = {
            'phones': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        data = dict(kwargs.get('data') or {})
        instance_pk = data.get('instance')
        if instance_pk and instance_pk not in [None, '', 'NEW']:
            kwargs['instance'] = Person.objects.get(pk=instance_pk)
            real_initial = kwargs.get('initial', {}).copy()
            kwargs['initial'] = model_to_dict(kwargs['instance'], [], [])
            kwargs['initial'].update({'instance': instance_pk})
            if data and not data.get('last_name'):
                old_data = dict(kwargs['data'].copy())
                old_data.update(kwargs['initial'])
                kwargs['data'] = old_data
            kwargs['initial'].update(real_initial)
        super(PersonForm, self).__init__(*args, **kwargs)
        self.data = dict(self.data.items())
        if not any(self.data.values()) or self.data.keys() == ['instance']:
            if not self.initial.keys() == ['death_date']:
                self.data = self.initial.copy()
        if self.data and self.data.get('last_name'):
            person_kwargs = {
                'first_name__istartswith': self.data.get('first_name', ''),
                'last_name__istartswith': self.data.get('last_name', ''),
                'middle_name__istartswith': self.data.get('middle_name', ''),
            }
            if self.data.get('instance') not in [None, '', 'NEW']:
                self.instance = Person.objects.get(pk=self.data.get('instance'))
                self.fields['instance'].choices = self.INSTANCE_CHOICES + [
                    (str(p.pk), self.full_person_data(p)) for p in Person.objects.filter(pk=self.data.get('instance'))
                ]
                if not self.data.get('selected'):
                    self.data = None
                    self.is_bound = False
                    dead = self.initial and self.initial.get('death_date')
                    self.initial = model_to_dict(self.instance, self._meta.fields, self._meta.exclude)
                    self.initial.update({'instance': self.instance.pk, 'death_date': dead})
            else:
                self.fields['instance'].choices = self.INSTANCE_CHOICES + [
                    (str(p.pk), self.full_person_data(p)) for p in Person.objects.filter(**person_kwargs)
                ]
                # self.data['instance'] = None
        else:
            self.fields['instance'].widget = forms.HiddenInput()

    def full_person_data(self, p):
        dates = ''
        if p.get_birth_date():
            if p.death_date:
                dates = '%s - %s' % (p.get_birth_date().strftime('%d.%m.%Y'), p.death_date.strftime('%d.%m.%Y'))
            else:
                dates = u'род. %s' % p.get_birth_date().strftime('%d.%m.%Y')
        else:
            if p.death_date:
                dates = u'ум. %s' % p.death_date.strftime('%d.%m.%Y')

        if dates:
            dates = u'%s, ' % dates

        params = (p.full_name_complete(), dates, p.address or u'', self.get_person_status(p))
        return u'%s (%sадрес: %s), Статус: %s' % params

    def get_person_status(self, p):
        if p.buried.all().count() > 0:
            return u'Усопший'
        if p.ordr_customer.all().count() > 0:
            return u'Заказчик'
        if p.place_set.all().count() > 0:
            return u'Ответственный'
        return u'Н/д'

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
    country_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'autocomplete'}), label=u"Страна")
    region_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'autocomplete'}), label=u"Область")
    city_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'autocomplete'}), label=u"Город")
    street_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'autocomplete'}), required=False, label=u"Улица")

    class Meta:
        model = Location
        widgets = {
            'country': forms.HiddenInput(),
            'region': forms.HiddenInput(),
            'city': forms.HiddenInput(),
            'street': forms.HiddenInput(),
        }

    def __init__(self, person=None, *args, **kwargs):
        kwargs.setdefault('initial', {})
        if person and person.address:
            kwargs['initial'] = dict(kwargs['initial']).copy()
            kwargs.update({'instance': person.address})
            if person.address.country:
                kwargs['initial'].update({
                    'country_name': person.address.country.name,
                })
            if person.address.region:
                kwargs['initial'].update({
                    'region_name': person.address.region.name,
                })
            if person.address.city:
                kwargs['initial'].update({
                    'city_name': person.address.city.name,
                })
            if person.address.street:
                kwargs['initial'].update({
                    'street_name': person.address.street.name,
                })
        if kwargs.get('instance', {}):
            l = kwargs.get('instance', {})
            street = l.street
            city = l.city or (street and street.city)
            region = l.region or (city and city.region)
            country = l.country or (region and region.country)
            kwargs.setdefault('initial', {}).update(
                country_name=country and country.name,
                region_name=region and region.name,
                city_name=city and city.name,
                street_name=street and street.name,
            )
        if kwargs.get('data', {}):
            kwargs['data'] = kwargs['data'] and kwargs['data'].copy() or {}
            if kwargs['data'].get('country_name'):
                d = kwargs['data']
                country, _tmp = Country.objects.get_or_create(name=d['country_name'])
                kwargs['data']['country'] = country.pk
                if kwargs.get('data', {}).get('region_name'):
                    region, _tmp = Region.objects.get_or_create(name=d['region_name'], country=country)
                    kwargs['data']['region'] = region.pk
                    if kwargs.get('data', {}).get('city_name'):
                        city, _tmp = City.objects.get_or_create(name=d['city_name'], region=region)
                        kwargs['data']['city'] = city.pk
                        if kwargs.get('data', {}).get('street_name'):
                            kwargs['data']['street'] = Street.objects.get_or_create(name=d['street_name'], city=city)[0].pk
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = self.fields.keyOrder[-4:] + self.fields.keyOrder[:-4]

    def is_valid(self):
        result = super(LocationForm, self).is_valid()
        if not result:
            if self.data.get('country') and isinstance(self.data['country'], int):
                self.data['country'] = Country.objects.get_or_create(pk=self.data['country'])
            if self.data.get('region') and isinstance(self.data['region'], int):
                self.data['region'] = Region.objects.get_or_create(pk=self.data['region'])
            if self.data.get('city') and isinstance(self.data['city'], int):
                self.data['city'] = City.objects.get_or_create(pk=self.data['city'])
            if self.data.get('street') and isinstance(self.data['street'], int):
                self.data['street'] = Street.objects.get_or_create(pk=self.data['street'])
        return result

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
    organization = forms.ModelChoiceField(label=u'Организация', queryset=Organization.objects.all(), required=False)
    agent_director = forms.BooleanField(label=u'Директор - агент', required=False)
    agent_person = forms.ModelChoiceField(label=u'Агент', queryset=Person.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        qs = Person.objects.filter(agent__organization__isnull=False).distinct()

        if self.data.get('customer-agent_person') == '---------------':
            self.data = self.data.copy()
            self.data['customer-agent_person'] = None

        if not self.is_person():
            self.fields['organization'].required = True
            self.fields['agent_person'].queryset = qs

    def is_person(self):
        return str(self.data.get('customer-customer_type', '')) == str(OPF_FIZIK)

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
        exclude = ['agent', ]

    def save(self, commit=True, agent=None):
        self.cleaned_data.update({'agent': agent})
        try:
            d = Doverennost.objects.get(**self.cleaned_data)
        except Doverennost.DoesNotExist:
            d = super(DoverennostForm, self).save(commit=False)
            d.agent = agent
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

    def __init__(self, *args, **kwargs):
        if kwargs.get('data'):
            kwargs['data'] = kwargs['data'].copy()
            for k,v in kwargs['data'].items():
                if k.endswith('servicee') and not v.isdigit():
                    try:
                        kwargs['data'][k] = Service.objects.get(name=v).pk
                    except Service.DoesNotExist:
                        pass
        super(OrderPositionForm, self).__init__(*args, **kwargs)

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

                if isinstance(i['service'], Service):
                    q = models.Q(pk=i['service'].pk)
                else:
                    q = models.Q(name=i['service'])
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

class UserForm(forms.ModelForm):
    username = forms.SlugField(max_length=255, label=u'Имя пользователя')
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=255, label=u'Пароль', required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=255, label=u'Пароль (еще раз)', required=False)

    class Meta:
        model = Person
        fields = ['last_name', 'first_name', 'middle_name', 'phones', ]
        widgets = {
            'phones': forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            person = kwargs.get('instance')
            kwargs.setdefault('initial', {}).update(username=person.user and person.user.username)
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(u'Пароли не совпадают')
        return self.cleaned_data

    def save(self, creator=None, *args, **kwargs):
        person = super(UserForm, self).save(*args, **kwargs)
        if not person.user:
            person.user = User()
        person.user.last_name = self.cleaned_data['last_name'].capitalize()
        person.user.first_name = self.cleaned_data['first_name'].capitalize()
        person.user.username = self.cleaned_data['username']
        person.user.is_staff = True

        if self.cleaned_data['password1']:
            person.user.set_password(self.cleaned_data['password1'])

        person.user.save()
        person.user = person.user
        person.creator = creator
        person.save()
        print person.user, person.user.pk
        return person

class CemeteryForm(forms.ModelForm):
    class Meta:
        model = Cemetery
        fields = ['organization', 'name', 'phones']
        widgets = {
            'phones': forms.TextInput(),
        }

    def save(self, location=None, *args, **kwargs):
        cemetery = super(CemeteryForm, self).save(*args, **kwargs)
        cemetery.location = location
        cemetery.save()
        return cemetery

