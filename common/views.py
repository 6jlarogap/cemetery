# -*- coding: utf-8 -*-

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
    burial_form = BurialForm()

    return render(request, 'burial_create.html', {
        'burial_form': burial_form,
    })

def new_burial_place(request):
    """
    Добавление места захоронения
    """
    place_form = PlaceForm()

    return render(request, 'burial_create_place.html', {
        'place_form': place_form,
        })

def new_burial_person(request):
    """
    Добавление усопшего
    """
    person_form = PersonForm()
    location_form = LocationForm()

    return render(request, 'burial_create_person.html', {
        'person_form': person_form,
        'location_form': location_form,
        })

def new_burial_customer(request):
    """
    Добавление заказчика
    """
    person_form = PersonForm()
    location_form = LocationForm()

    return render(request, 'burial_create_customer.html', {
        'person_form': person_form,
        'location_form': location_form,
        })

def new_burial_responsible(request):
    """
    Добавление ответственного
    """
    person_form = PersonForm()
    location_form = LocationForm()

    return render(request, 'burial_create_responsible.html', {
        'person_form': person_form,
        'location_form': location_form,
        })
