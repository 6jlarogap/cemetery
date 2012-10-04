# -*- coding: utf-8 -*-
import datetime
import urllib

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Count
from django.db.models.query_utils import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views.generic.list_detail import object_list
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

import math

from cemetery.models import Burial, Place, UserProfile, Service, ServicePosition, Person, Cemetery, Comment, Operation
from cemetery.forms import SearchForm, PlaceForm, BurialForm, PersonForm, LocationForm, DeathCertificateForm, OrderPaymentForm, OrderPositionsFormset, PrintOptionsForm, UserForm, CemeteryForm, PlaceBurialsFormset, PlaceRoomsForm, OrganizationForm, AccountsFormset, AgentsFormset
from cemetery.forms import UserProfileForm, DoverennostForm, CustomerIDForm, CustomerForm, CommentForm
from cemetery.forms import AddAgentForm
from persons.models import DeathCertificate, PersonID
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
    paginate_by = 10
    if request.user.is_authenticated():
        p, _tmp = UserProfile.objects.get_or_create(user=request.user)
        initial = {'records_order_by': p.records_order_by, 'per_page': p.records_per_page}
        paginate_by = int(p.records_per_page or paginate_by)
    else:
        initial = None
    form = SearchForm(request.GET or None, initial=initial)
    if form.data and form.is_valid():
        if form.cleaned_data['operation']:
            burials = burials.filter(operation=form.cleaned_data['operation'])
        if form.cleaned_data['customer_type']:
            ct = form.cleaned_data['customer_type']
            burials = burials.filter(**{ct + '__isnull': False})
        if form.cleaned_data['fio']:
            fio = [f.strip('.') for f in form.cleaned_data['fio'].split(' ')]
            q = Q()
            if len(fio) > 2:
                q &= Q(person__middle_name__icontains=fio[2])
            if len(fio) > 1:
                q &= Q(person__first_name__icontains=fio[1])
            if len(fio) > 0:
                q &= Q(person__last_name__icontains=fio[0])
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

            oq = Q(name__icontains=form.cleaned_data['customer'])
            orgs = list(Organization.objects.filter(oq))

            aq = Q(person__last_name__icontains=form.cleaned_data['customer'])
            aq |= Q(organization__name__icontains=form.cleaned_data['customer'])
            agents = list(Agent.objects.filter(aq))

            burials = burials.filter(q | Q(agent__in=agents) | Q(client_organization__in=orgs)).distinct()
        if form.cleaned_data['responsible']:
            burials = burials.filter(place__responsible__last_name__icontains=form.cleaned_data['responsible'])
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
        if form.cleaned_data['deleted']:
            burials = burials.filter(deleted=True)
        else:
            burials = burials.filter(deleted=False)

        if form.cleaned_data['records_order_by']:
            burials = burials.order_by(form.cleaned_data['records_order_by'])
        if form.cleaned_data['per_page']:
            paginate_by = int(form.cleaned_data['per_page'])
    else:
        burials = Burial.objects.none()

    result = {
        "form": form,
        "close": request.GET.get('close'),
        "GET_PARAMS": urllib.urlencode([(k, v.encode('utf-8')) for k,v in request.GET.items() if k != 'page']),
    }

    if request.REQUEST.get('print'):
        return render(request, 'burials_print.html', {
            'object_list': burials,
        })

    return object_list(request,
        template_name='burials.html',
        queryset=burials,
        paginate_by=paginate_by,
        extra_context=result,
    )

@login_required
def new_burial(request):
    """
    Добавление захоронения
    """
    p, _tmp = UserProfile.objects.get_or_create(user=request.user)
    date_fact = datetime.date.today() + datetime.timedelta(1)
    if date_fact.weekday() == 6:
        date_fact += datetime.timedelta(1)

    place = None
    if request.GET.get('place'):
        place = Place.objects.get(pk=request.GET.get('place'))

    tmp_b = Burial()
    if place:
        tmp_b.place = place
    if p.default_operation:
        tmp_b.operation = p.default_operation
    elif place:
        tmp_b.operation = Operation.objects.filter(op_type__istartswith=u"Подзахоронение")[0]
    tmp_b.date_fact = date_fact

    burial_form = BurialForm(data=request.POST or None, instance=tmp_b)

    if request.POST and burial_form.is_valid():
        b = burial_form.save()
        messages.success(request, u'Успешно сохранено')
        return redirect('edit_burial', pk=b.pk)

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

    if request.GET.get('delete'):
        burial.deleted = True
        burial.save()
        messages.success(request, u'Удалено')
        return redirect('main_page')

    if request.GET.get('recover'):
        burial.deleted = False
        burial.save()
        messages.success(request, u'Восстановлено')
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
    data = None
    if request.REQUEST.keys() and request.REQUEST.keys() != ['dead']:
        data = request.REQUEST
    initial = {}
    person_form = PersonForm(data=data, initial=initial, dead=request.GET.get('dead'))
    location_form = LocationForm(person=person_form.instance, data=request.POST.get('country_name') and request.POST or None)

    try:
        dc = person_form.instance.deathcertificate
    except (DeathCertificate.DoesNotExist, AttributeError):
        dc = None
    dc_data = request.POST.get('death_date') and request.POST or None or None
    dc_form = DeathCertificateForm(data=dc_data, prefix='dc', instance=dc)

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
    person_data = (request.REQUEST.get('instance') or request.REQUEST.get('last_name')) and dict(request.REQUEST).copy() or None
    person_form = PersonForm(data=person_data or None, initial=person_data)

    location_data = request.POST.get('country_name') and request.POST.copy() or None
    location_form = LocationForm(person=person_form.instance, initial=person_data, data=location_data)

    try:
        person_id = person_form.instance and person_form.instance.personid or None
    except PersonID.DoesNotExist:
        person_id = None
    customer_id_data = request.POST.get('country_name') and request.POST.copy() or None
    customer_id_form = CustomerIDForm(data=customer_id_data, prefix='customer_id', instance=person_id)

    org_data = request.REQUEST.get('organization') and request.REQUEST.copy() or None
    customer_form = CustomerForm(data=request.POST.copy() or None, prefix='customer', initial=org_data)
    doverennost_form = DoverennostForm(data=request.POST.copy() or None, prefix='doverennost', initial=org_data)

    add_agent_form = AddAgentForm(prefix='add_agent')

    organizations = Organization.objects.all()

    if request.POST and customer_form.is_valid():
        if customer_form.is_person():
            if request.POST.get('country_name') and person_form.is_valid() and customer_id_form.is_valid():
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
                doverennost = None
                if agent_person:
                    agent, _created = Agent.objects.get_or_create(organization=org, person=agent_person)
                    if doverennost_form.is_valid():
                        doverennost = doverennost_form.save(agent=agent)
                else:
                    agent = None
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
        'add_agent_form': add_agent_form,
        'organizations': organizations,
    })

@login_required
def new_burial_responsible(request):
    """
    Добавление ответственного
    """
    data = request.REQUEST.keys() and dict(request.REQUEST.copy()) or None
    person_form = PersonForm(data=data)
    responsible_customer = request.REQUEST.get('responsible_customer')
    loc_data = request.POST and request.POST.get('country_name') and request.POST.copy()
    location_form = LocationForm(person=person_form.instance, data=loc_data or None)

    if request.POST and person_form.data and person_form.is_valid():
        if location_form.is_valid() and location_form.cleaned_data:
            location = location_form.save()
        else:
            location = None
        person = person_form.save(location=location)
        return render(request, 'burial_create_responsible_ok.html', {
            'person': person,
            'responsible_customer': responsible_customer,
        })

    return render(request, 'burial_create_responsible.html', {
        'person_form': person_form,
        'location_form': location_form,
        'responsible_customer': responsible_customer,
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
                'service': product,
                'price': product.price,
                'count': 1,
                'sum': product.price * 1,
            })
        else:
            positions.append({
                'active': True,
                'service': product,
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
        i['service'] = i.get('service', i.get('order_product'))
        p['service'] = p.get('service', p.get('order_product'))
        i1 = isinstance(i['service'], Service) and i['service'].name or i['service']
        p1 = isinstance(p['service'], Service) and p['service'].name or p['service']
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
            service = f.initial['service']
            if isinstance(f.initial['service'], basestring):
                if f.initial['service'].isdigit():
                    service = Service.objects.get(pk=f.initial['service'])
                else:
                    try:
                        service = Service.objects.get(name=f.initial['service'])
                    except Service.DoesNotExist:
                        pass
            if f.cleaned_data['active']:
                print_positions.append(service.pk)
                try:
                    pos = ServicePosition.objects.get(service=service, burial=burial)
                except ServicePosition.DoesNotExist:
                    pos = ServicePosition.objects.create(
                        service=service,
                        burial=burial,
                        price=f.cleaned_data['price'],
                        count=f.cleaned_data['count'],
                    )
                else:
                    pos.price = f.cleaned_data['price']
                    pos.count = f.cleaned_data['count']
                    pos.save()

            else:
                try:
                    pos = ServicePosition.objects.get(service=service, burial=burial)
                except ServicePosition.DoesNotExist:
                    pass
                else:
                    pos.delete()

        transaction.commit()

        payment_form.save()

        positions = get_positions(burial)
        positions = filter(lambda p: p['service'].pk in print_positions, positions)

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
            position = filter(lambda p: u'грузчики' in p['service'].name.lower(), positions)[0]
            lifters_hours = position['count']
            lifters_count = u'%s %s' % (position['count'], position['service'].measure)
            hours = math.floor(lifters_hours)
            minutes = math.floor((float(lifters_hours) - math.floor(lifters_hours)) * 60)
            lifters_hours = datetime.time(int(hours), int(minutes))
        except IndexError:
            lifters_hours = 0

        if print_form.cleaned_data.get('catafalque_time'):
            try:
                catafalque_hours = filter(lambda p: u'автокатафалк' in p['service'].name.lower(), positions)[0]['count']
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
    comment_form = CommentForm(data=request.POST or None, files=request.FILES or None)
    return render(request, 'burial_info.html', {
        'burial': burial,
        'comment_form': comment_form
    })

@login_required
def add_comment(request, pk):
    burial = get_object_or_404(Burial, pk=pk)
    comment_form = CommentForm(data=request.POST or None, files=request.FILES or None)
    if comment_form.is_valid():
        comment_form.save(burial=burial, user=request.user)
        return redirect('view_burial', pk)
    return view_burial(request, pk)

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    burial_pk = comment.burial.pk
    comment.delete()
    return redirect('view_burial', burial_pk)

def view_place(request, pk):
    place = get_object_or_404(Place, pk=pk)
    pbf = PlaceBurialsFormset(data=request.POST or None, place=place)
    rf = PlaceRoomsForm(data=request.POST or None, instance=place)
    if request.GET.get('unlink'):
        Burial.objects.filter(place=place, pk=request.GET.get('unlink')).update(grave_id=None)
        return redirect('.')
    if request.POST and rf.changed_data and rf.is_valid():
        rf.save()
        return redirect('.')
    if request.POST and pbf.is_valid():
        pbf.save()
        return redirect('.')
    return render(request, 'place_info.html', {
        'place': place,
        'pbf': pbf,
        'rf': rf,
    })

def autocomplete_person(request):
    query = request.GET['query']
    persons = Person.objects.filter(last_name__istartswith=query)
    if request.GET.get('dead'):
        persons = persons.annotate(dead=Count('buried')).filter(dead__gt=0)
    persons = persons.order_by('middle_name', 'first_name', 'last_name')
    person_names = list(set([p.full_human_name() for p in persons[:100]]))
    return HttpResponse(simplejson.dumps([{'value': pn} for pn in person_names]), mimetype='text/javascript')

@user_passes_test(lambda u: u.is_superuser)
@transaction.commit_on_success
def management_user(request):
    """
    Страница управления пользователями (создание нового, показ существующих).
    """

    instance = None
    user = None
    if request.GET.get('pk'):
        instance = get_object_or_404(Person, pk=request.GET.get('pk'))
    elif request.GET.get('user_pk'):
        user_pk = request.GET.get('user_pk')
        user = User.objects.get(pk=user_pk)

        if request.GET.get('deactivate'):
            user.is_active = False
            user.save()
            messages.success(request, u'Данные сохранены успешно')
            return redirect('management_user')

        if request.GET.get('activate'):
            user.is_active = True
            user.save()
            messages.success(request, u'Данные сохранены успешно')
            return redirect('management_user')

        instance = None
        try:
            instance = Person.objects.get(user__pk=user_pk)
        except Person.DoesNotExist:
            if user.last_name:
                try:
                    instance = Person.objects.get(first_name=user.first_name, last_name=user.last_name)
                except Person.DoesNotExist:
                    pass
            if not instance:
                instance = Person.objects.create(first_name=user.first_name, last_name=user.last_name, user=user)
    form = UserForm(request.POST or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        person = form.save(creator=request.user)
        messages.success(request, u'Данные сохранены успешно')
        return redirect('management_user')
    users = User.objects.all().order_by('last_name')
    return render(request, 'management_user.html', {'form': form, "users": users, 'current_user': user})

@user_passes_test(lambda u: u.is_superuser)
@transaction.commit_on_success
def management_cemetery(request):
    """
    Страница управления кладбищами.
    """
    cemetery = None
    if request.GET.get('pk'):
        cemetery = get_object_or_404(Cemetery, pk=request.GET.get('pk'))

    cemetery_form = CemeteryForm(request.POST or None, instance=cemetery)
    location_form = LocationForm(request.POST or None, instance=cemetery and cemetery.location)
    if request.method == "POST" and cemetery_form.is_valid() and location_form.is_valid():
        location = location_form.save()
        cemetery = cemetery_form.save(location=location)
        return redirect(reverse('management_cemetery') + '?pk=%s' % cemetery.pk)

    cemeteries = Cemetery.objects.all()
    return render(request, 'management_add_cemetery.html', {'cemetery_form': cemetery_form, "location_form": location_form, "cemeteries": cemeteries})

@user_passes_test(lambda u: u.is_superuser)
@transaction.commit_on_success
def management_org(request):
    """
    Страница управления организациями.
    """
    org = None
    if request.GET.get('pk'):
        org = get_object_or_404(Organization, pk=request.GET.get('pk'))

    org_form = OrganizationForm(data=request.POST or None, instance=org)
    location_form = LocationForm(data=request.POST or None, instance=org and org.location)
    accounts_formset = AccountsFormset(data=request.POST or None, instance=org, prefix='accounts')
    agents_formset = AgentsFormset(data=request.POST or None, instance=org, prefix='agents')
    if request.method == "POST" and org_form.is_valid() and location_form.is_valid() and agents_formset.is_valid() and accounts_formset.is_valid():
        location = location_form.save()
        org = org_form.save(location=location)
        accounts_formset = AccountsFormset(data=request.POST or None, instance=org, prefix='accounts')
        agents_formset = AgentsFormset(data=request.POST or None, instance=org, prefix='agents')
        accounts_formset.save()
        agents_formset.save()
        return redirect(reverse('management_org') + '?pk=%s' % org.pk)

    orgs = Organization.objects.all()
    return render(request, 'management_add_org.html', {
        'org_form': org_form,
        "location_form": location_form,
        'accounts_formset': accounts_formset,
        'agents_formset': agents_formset,
        "orgs": orgs,
    })

@login_required
def new_agent(request):
    form = AddAgentForm(data=request.POST or None, prefix='add_agent')
    if form.is_valid():
        agent = form.save()
        return HttpResponse(simplejson.dumps({'pk': agent.person.pk, 'label': u'%s' % agent.person}), mimetype='application/json')
    return HttpResponse(form.as_p(), mimetype='text/html')