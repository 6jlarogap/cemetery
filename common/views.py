# -*- coding: utf-8 -*-
import datetime
from django.contrib import messages

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.safestring import mark_safe
import math

from cemetery.models import Burial, Place, UserProfile, Service, ServicePosition
from cemetery.forms import SearchForm, PlaceForm, BurialForm, PersonForm, LocationForm, DeathCertificateForm, OrderPaymentForm, OrderPositionsFormset, PrintOptionsForm
from cemetery.forms import UserProfileForm, DoverennostForm, CustomerIDForm, CustomerForm
from persons.models import DeathCertificate
from organizations.models import Organization, Agent

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
    if request.user.is_authenticated():
        p, _tmp = UserProfile.objects.get_or_create(user=request.user)
        initial = {'records_order_by': p.records_order_by, 'per_page': p.records_per_page}
    else:
        initial = None
    form = SearchForm(request.GET or None, initial=initial)
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
    p, _tmp = UserProfile.objects.get_or_create(user=request.user)
    burial_form = BurialForm(data=request.POST or None, initial={'operation': p.default_operation})

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
    p, _tmp = UserProfile.objects.get_or_create(user=request.user)
    if request.GET.get('instance'):
        instance = Place.objects.get(pk=request.GET['instance'])
        initial = None
    else:
        instance = None
        initial = {'cemetery': p.default_cemetery}

    place_form = PlaceForm(data=request.POST or None, instance=instance, initial=initial)

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
    location_form = LocationForm(person=person_form.instance, data=request.POST.get('country') and request.POST or None)

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

    organizations = Organization.objects.all()

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
                agent_person = customer_form.get_agent()
                agent = Agent.objects.get(organization=org, person=agent_person)
                if doverennost_form.is_valid():
                    doverennost = doverennost_form.save(agent=agent)
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
        'organizations': organizations,
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

@login_required
def profile(request):
    p, _tmp = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(data=request.POST or None, instance=p)
    if request.POST and form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'profile.html', {
        'profile': p,
        'form': form,
    })

def get_positions(burial):
    positions = []
    for product in Service.objects.all().order_by('ordering', 'name'):
        try:
            pos = ServicePosition.objects.get(service=product, burial=burial)
        except ServicePosition.DoesNotExist:
            positions.append({
                'active': product.default,
                'order_product': product,
                'price': product.price,
                'count': 1,
                'sum': product.price * 1,
            })
        else:
            positions.append({
                'active': True,
                'order_product': product,
                'price': pos.price,
                'count': pos.count,
                'sum': pos.price * pos.count,
            })
    return positions

@login_required
@transaction.commit_on_success
def print_burial(request, pk):
    """
    Страница печати документов захоронения.
    """
    burial = get_object_or_404(Burial, pk=pk)
    positions = get_positions(burial)
    initials = burial.get_print_info()

    def is_same(i, p):
        i1 = isinstance(i['order_product'], Service) and i['order_product'].name or i['order_product']
        p1 = isinstance(p['order_product'], Service) and p['order_product'].name or p['order_product']
        return i1 == p1

    if initials and initials.setdefault('positions', []):
        for p in positions:
            if not any(filter(lambda i: is_same(i, p), initials['positions'])):
                initials['positions'].append(p)

    payment_form = OrderPaymentForm(instance=burial, data=request.POST or None)
    positions_fs = OrderPositionsFormset(initial=initials.get('positions') or positions, data=request.POST or None)
    print_form = PrintOptionsForm(data=request.POST or None, initial=initials['print'], burial=burial)
    org = None

    time_check_failed = False

    print_positions = []
    if request.POST and positions_fs.is_valid() and payment_form.is_valid() and print_form.is_valid():
        burial.set_print_info({
            'positions': [f.cleaned_data for f in positions_fs.forms if f.is_valid()],
            'print': print_form.cleaned_data,
            })
        burial.save()

        for f in positions_fs.forms:
            if f.cleaned_data['active']:
                print_positions.append(f.initial['order_product'].pk)
                try:
                    pos = ServicePosition.objects.get(order_product=f.initial['order_product'], order=burial)
                except ServicePosition.DoesNotExist:
                    pos = ServicePosition.objects.create(
                        order_product=f.initial['order_product'],
                        order=burial,
                        price=f.cleaned_data['price'],
                        count=f.cleaned_data['count'],
                    )
                else:
                    pos.price = f.cleaned_data['price']
                    pos.count = f.cleaned_data['count']
                    pos.save()

            else:
                try:
                    pos = ServicePosition.objects.get(order_product=f.initial['order_product'], order=burial)
                except ServicePosition.DoesNotExist:
                    pass
                else:
                    pos.delete()

        transaction.commit()

        payment_form.save()

        positions = get_positions(burial)
        positions = filter(lambda p: p['order_product'].pk in print_positions, positions)

        burial_creator = u'%s' % burial.creator

        current_user = u'%s' % request.user.userprofile.person

        spaces = mark_safe('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')

        if print_form.cleaned_data.get('receipt'):
            return render(request, 'reports/spravka.html', {
                'burial': burial,
                'current_user': current_user or spaces,
                'now': datetime.datetime.now(),
                'org': org,
            })

        if print_form.cleaned_data.get('dogovor'):

            return render(request, 'reports/dogovor.html', {
                'burial': burial,
                'now': datetime.datetime.now(),
                'org': org,
            })

        catafalque_release = ('_____', '_____',)
        catafalque_time = ''
        catafalque_hours = None
        lifters_count = u'н/д'

        try:
            position = filter(lambda p: u'грузчики' in p['order_product'].name.lower(), positions)[0]
            lifters_hours = position['count']
            lifters_count = u'%s %s' % (position['count'], position['order_product'].measure)
            hours = math.floor(lifters_hours)
            minutes = math.floor((float(lifters_hours) - math.floor(lifters_hours)) * 60)
            lifters_hours = datetime.time(int(hours), int(minutes))
        except IndexError:
            lifters_hours = 0

        if print_form.cleaned_data.get('catafalque_time'):
            try:
                catafalque_hours = filter(lambda p: u'автокатафалк' in p['order_product'].name.lower(), positions)[0]['count']
            except IndexError:
                catafalque_hours = 0
            catafalque_time = map(int, print_form.cleaned_data.get('catafalque_time').split(':'))

        if catafalque_hours:
            hours = math.floor(catafalque_hours)
            minutes = math.floor((float(catafalque_hours) - math.floor(catafalque_hours)) * 60)
            catafalque_hours = datetime.time(int(hours), int(minutes))

            if catafalque_time:
                delta = datetime.timedelta(0, catafalque_hours.hour * 3600 + catafalque_hours.minute * 60)
                catafalque_release = datetime.datetime(burial.date_fact.year, burial.date_fact.month, burial.date_fact.day, *catafalque_time) + delta

                if burial.date_fact.time() < datetime.time(*catafalque_time) or catafalque_release.time() < burial.date_fact.time():
                    if not request.REQUEST.get('skip_time_check'):
                        time_check_failed = True
        else:
            catafalque_hours = None

        if catafalque_hours:
            lifters_hours = catafalque_hours

        if catafalque_time and isinstance(catafalque_time[0], int):
            catafalque_time = datetime.time(*catafalque_time)
            catafalque_time = u' ч. '.join(catafalque_time.strftime(u'%H %M').lstrip('0').strip().split(' ')) + u' мин.'

        if not time_check_failed:
            return render(request, 'reports/act.html', {
                'burial': burial,
                'burial_creator': burial_creator or spaces,
                'positions': positions,
                'print_positions': print_positions,
                'total': float(sum([p['sum'] for p in positions])),
                'catafalque': print_form.cleaned_data.get('catafalque'),
                'lifters': print_form.cleaned_data.get('lifters'),
                'graving': print_form.cleaned_data.get('graving'),
                'now': datetime.datetime.now(),
                'org': org,
                'catafalque_route': print_form.cleaned_data.get('catafalque_route') or '',
                'catafalque_start': print_form.cleaned_data.get('catafalque_start') or '',
                'catafalque_time': catafalque_time or '',
                'catafalque_hours': catafalque_hours and (u' ч. '.join(catafalque_hours.strftime(u'%H %M').lstrip('0').strip().split(' ')) + u' мин.') or '',
                'lifters_hours': lifters_hours and (u' ч. '.join(lifters_hours.strftime(u'%H %M').lstrip('0').strip().split(' ')) + u' мин.') or '',
                'lifters_count': lifters_count,
                'coffin_size': print_form.cleaned_data.get('coffin_size') or '',
                'print_now': print_form.cleaned_data.get('print_now'),
                'dop_info': print_form.cleaned_data.get('add_info') or '',
            })

    return render(request, 'burial_print.html', {
        'burial': burial,
        'positions_fs': positions_fs,
        'payment_form': payment_form,
        'print_form': print_form,
        'time_check_failed': time_check_failed,
    })

def view_burial(request, pk):
    burial = get_object_or_404(Burial, pk=pk)
    return render(request, 'burial_info.html', {
        'burial': burial,
    })

def view_place(request, pk):
    place = get_object_or_404(Place, pk=pk)
    return render(request, 'place_info.html', {
        'place': place,
    })
