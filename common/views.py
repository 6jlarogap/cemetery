# -*- coding: utf-8 -*-
from django.contrib import messages

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render, get_object_or_404

from cemetery.models import Burial, Place
from cemetery.forms import SearchForm, PlaceForm, BurialForm, PersonForm, LocationForm, DeathCertificateForm, DoverennostForm, CustomerIDForm, CustomerForm
from organizations.models import Organization
from persons.models import DeathCertificate


def ulogin(request):
    """
    Страница логина.
    """
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next", "/")
            if next_url == '/logout/':
                next_url = '/'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        request.session.set_test_cookie()
    return render(request, 'login.html', {'form':
                                                      form})
@login_required
def ulogout(request):
    """
    Выход пользователя из системы.
    """
    logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)

def main_page(request):
    """
    Главная страница.
    """

    burials = Burial.objects.all()
    form = SearchForm(request.GET or None)
    if form.data and form.is_valid():
        if form.cleaned_data['operation']:
            burials = burials.filter(operation=form.cleaned_data['operation'])
        if form.cleaned_data['fio']:
            fio = [f.strip('.') for f in form.cleaned_data['fio'].split(' ')]
            q = Q()
            for f in fio:
                q &= Q(person__last_name__icontains=f) | Q(person__first_name__icontains=f) | Q(person__middle_name__icontains=f)
            burials = burials.filter(q)
        if form.cleaned_data['birth_date_from']:
            burials = burials.filter(person__birth_date__gte=form.cleaned_data['birth_date_from'])
        if form.cleaned_data['birth_date_to']:
            burials = burials.filter(person__birth_date__lte=form.cleaned_data['birth_date_to'])
        if form.cleaned_data['death_date_from']:
            burials = burials.filter(person__death_date__gte=form.cleaned_data['death_date_from'])
        if form.cleaned_data['death_date_to']:
            burials = burials.filter(person__death_date__lte=form.cleaned_data['death_date_to'])
        if form.cleaned_data['burial_date_from']:
            burials = burials.filter(date_fact__gte=form.cleaned_data['burial_date_from'])
        if form.cleaned_data['burial_date_to']:
            burials = burials.filter(date_fact__lte=form.cleaned_data['burial_date_to'])
        if form.cleaned_data['account_number_from']:
            burials = burials.filter(account_number__gte=form.cleaned_data['account_number_from'])
        if form.cleaned_data['account_number_to']:
            burials = burials.filter(account_number__lte=form.cleaned_data['account_number_to'])
        if form.cleaned_data['customer']:
            q = Q(client_person__last_name__icontains=form.cleaned_data['customer'])
            q |= Q(client_organization__name__icontains=form.cleaned_data['customer'])
            q |= Q(client_organization__full_name__icontains=form.cleaned_data['customer'])
            burials = burials.filter(q)
        if form.cleaned_data['cemetery']:
            burials = burials.filter(place__cemetery=form.cleaned_data['cemetery'])
        if form.cleaned_data['area']:
            burials = burials.filter(place__area=form.cleaned_data['area'])
        if form.cleaned_data['row']:
            burials = burials.filter(place__row=form.cleaned_data['row'])
        if form.cleaned_data['seat']:
            burials = burials.filter(place__seat=form.cleaned_data['seat'])
        if form.cleaned_data['no_exhumated']:
            burials = burials.filter(exhumated=False)

        if form.cleaned_data['records_order_by']:
            burials = burials.order_by(form.cleaned_data['records_order_by'])
    result = {
        "form": form,
        "object_list": burials,
        "close": request.GET.get('close'),
    }

    return render(request,'burials.html', result )

@login_required
def new_burial(request):
    """
    Добавление захоронения
    """
    burial_form = BurialForm(data=request.POST or None)

    if request.POST and burial_form.is_valid():
        burial_form.save()
        messages.success(request, u'Успешно сохранено')
        return redirect('main_page')

    return render(request, 'burial_create.html', {
        'burial_form': burial_form,
        'last_entered': Burial.objects.all().order_by('-id')[:10],
    })

@login_required
def edit_burial(request, pk):
    """
    Редактирование захоронения
    """
    burial = get_object_or_404(Burial, pk=pk)
    burial_form = BurialForm(data=request.POST or None, instance=burial)

    if request.POST and burial_form.is_valid():
        burial_form.save()
        messages.success(request, u'Успешно сохранено')
        return redirect('main_page')

    return render(request, 'burial_edit.html', {
        'burial_form': burial_form,
        'last_entered': Burial.objects.all().order_by('-id')[:10],
        'burial': burial,
    })

@login_required
def new_burial_place(request):
    """
    Добавление места захоронения
    """
    if request.GET.get('instance'):
        instance = Place.objects.get(pk=request.GET['instance'])
    else:
        instance = None
    place_form = PlaceForm(data=request.POST or None, instance=instance)

    if request.POST and place_form.is_valid():
        place = place_form.save(user=request.user)
        return render(request, 'burial_create_place_ok.html', {
            'place': place,
            })

    return render(request, 'burial_create_place.html', {
        'place_form': place_form,
        })

@login_required
def new_burial_person(request):
    """
    Добавление усопшего
    """
    data = request.REQUEST.keys() and request.REQUEST or None
    person_form = PersonForm(data=data)
    location_form = LocationForm(person=person_form.instance, data=request.POST or None)

    try:
        dc = person_form.instance.deathcertificate
    except (DeathCertificate.DoesNotExist, AttributeError):
        dc = None
    dc_form = DeathCertificateForm(data=request.POST or None, prefix='dc', instance=dc)

    if request.POST and person_form.data and person_form.is_valid() and dc_form.is_valid():
        if location_form.is_valid() and location_form.cleaned_data:
            location = location_form.save()
        else:
            location = None
        person = person_form.save(location=location)
        dc_form.save(person=person)
        return render(request, 'burial_create_person_ok.html', {
            'person': person,
        })

    return render(request, 'burial_create_person.html', {
        'person_form': person_form,
        'location_form': location_form,
        'dc_form': dc_form,
    })

@login_required
def new_burial_customer(request):
    """
    Добавление заказчика
    """
    person_data = request.REQUEST.get('instance') and request.REQUEST or None
    person_form = PersonForm(data=request.POST or None, initial=person_data)
    location_form = LocationForm(person=person_form.instance, initial=person_data, data=request.POST or None)

    org_data = request.REQUEST.get('organization') and request.REQUEST or None
    customer_form = CustomerForm(data=request.POST or None, prefix='customer', initial=org_data)
    customer_id_form = CustomerIDForm(data=request.POST or None, prefix='customer_id', initial=org_data)
    doverennost_form = DoverennostForm(data=request.POST or None, prefix='doverennost', initial=org_data)

    if request.POST and customer_form.is_valid():
        if customer_form.is_person():
            if person_form.is_valid() and customer_id_form.is_valid():
                if location_form.is_valid() and location_form.cleaned_data:
                    location = location_form.save()
                else:
                    location = None
                person = person_form.save(location=location)
                customer_id_form.save(person=person)
                return render(request, 'burial_create_customer_person_ok.html', {
                    'person': person,
                })
        else:
            if customer_form.cleaned_data['agent_director'] or doverennost_form.is_valid():
                org = customer_form.cleaned_data['organization']
                agent = customer_form.get_agent()
                if doverennost_form.is_valid():
                    doverennost = doverennost_form.save()
                else:
                    doverennost = None
                return render(request, 'burial_create_customer_org_ok.html', {
                    'org': org,
                    'agent': agent,
                    'doverennost': doverennost,
                })

    return render(request, 'burial_create_customer.html', {
        'person_form': person_form,
        'location_form': location_form,
        'customer_form': customer_form,
        'customer_id_form': customer_id_form,
        'doverennost_form': doverennost_form,
    })

@login_required
def new_burial_responsible(request):
    """
    Добавление ответственного
    """
    data = request.REQUEST.keys() and request.REQUEST or None
    person_form = PersonForm(data=data)
    location_form = LocationForm(person=person_form.instance, data=request.POST or None)

    if request.POST and person_form.data and person_form.is_valid():
        if location_form.is_valid() and location_form.cleaned_data:
            location = location_form.save()
        else:
            location = None
        person = person_form.save(location=location)
        return render(request, 'burial_create_responsible_ok.html', {
            'person': person,
        })

    return render(request, 'burial_create_responsible.html', {
        'person_form': person_form,
        'location_form': location_form,
    })

