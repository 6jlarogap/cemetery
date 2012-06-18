# -*- coding: utf-8 -*-
from django.contrib import messages

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from cemetery.models import Burial, Place
from cemetery.forms import SearchForm, PlaceForm, BurialForm, PersonForm, LocationForm, DeathCertificateForm, DoverennostForm, CustomerIDForm, CustomerForm
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
    result = {
        "form": form,
        "object_list": burials,
        'close': request.GET.get('close'),
        }

    return render(request,'burials.html', result )

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

def new_burial_person(request):
    """
    Добавление усопшего
    """
    data = request.REQUEST.keys() and request.REQUEST or None
    person_form = PersonForm(data=data)
    location_form = LocationForm(person=person_form.instance, data=request.POST or None)

    try:
        dc = person_form.instance.deathcertificate
    except DeathCertificate.DoesNotExist:
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

def new_burial_customer(request):
    """
    Добавление заказчика
    """
    data = request.REQUEST.keys() and request.REQUEST or None
    person_form = PersonForm(data=data)
    location_form = LocationForm(person=person_form.instance, data=request.POST or None)

    customer_form = CustomerForm(data=request.POST or None, prefix='customer')
    customer_id_form = CustomerIDForm(data=request.POST or None, prefix='customer_id')
    doverennost_form = DoverennostForm(data=request.POST or None, prefix='doverennost')

    if request.POST and person_form.data and person_form.is_valid():
        if customer_form.is_valid() and customer_id_form.is_valid() and doverennost_form.is_valid():
            if location_form.is_valid() and location_form.cleaned_data:
                location = location_form.save()
            else:
                location = None
            person = person_form.save(location=location)
            customer_form.save(person=person)
            customer_id_form.save(person=person)
            doverennost_form.save(person=person)
            return render(request, 'burial_create_customer_ok.html', {
                'person': person,
            })

    return render(request, 'burial_create_customer.html', {
        'person_form': person_form,
        'location_form': location_form,
        'customer_form': customer_form,
        'customer_id_form': customer_id_form,
        'doverennost_form': doverennost_form,
    })

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
