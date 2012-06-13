# -*- coding: utf-8 -*-
from django.contrib import messages

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cemetery.models import Burial
from cemetery.forms import SearchForm, PlaceForm, BurialForm, PersonForm, LocationForm


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
        return redirect('new_burial')

    return render(request, 'burial_create.html', {
        'burial_form': burial_form,
        'last_entered': Burial.objects.all().order_by('-id')[:10],
    })

def new_burial_place(request):
    """
    Добавление места захоронения
    """
    place_form = PlaceForm(data=request.POST or None)

    if request.POST and place_form.is_valid():
        place = place_form.save(user=request.user)
        return render(request, 'burial_create_place_ok.html', {
            'place': place,
            })

    return render(request, 'burial_create_place.html', {
        'place_form': place_form,
        })

def new_burial_somebody(request, body):
    """
    Добавление чего-нибудь
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
        return render(request, 'burial_create_%s_ok.html' % body, {
            'person': person,
        })

    return render(request, 'burial_create_%s.html' % body, {
        'person_form': person_form,
        'location_form': location_form,
    })

def new_burial_person(request):
    """
    Добавление усопшего
    """
    return new_burial_somebody(request, 'person')

def new_burial_customer(request):
    """
    Добавление заказчика
    """
    return new_burial_somebody(request, 'customer')

def new_burial_responsible(request):
    """
    Добавление ответственного
    """
    return new_burial_somebody(request, 'responsible')
