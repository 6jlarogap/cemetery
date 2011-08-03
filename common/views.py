# -*- coding: utf-8 -*-

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
#from django.utils import simplejson
from django.utils.simplejson.encoder import JSONEncoder
from django.forms.models import modelformset_factory
from django import db

from common.forms import *

from common.models import *

from simplepagination import paginate
from annoying.decorators import render_to

import re
import datetime
import time
import csv
from cStringIO import StringIO
#from django.utils import datetime_safe


csv.register_dialect("4mysqlout", escapechar="\\", quoting=csv.QUOTE_NONE)
csv.register_dialect("4mysql", escapechar="\\", quoting=csv.QUOTE_ALL, doublequote=False)

def is_in_group(group_name):
    """
    Декоратор для проверки на то, что пользователь является членом указанной группы.
    """
    def _dec(f):
        def _check_group(request, *args, **kwargs):
            try:
                if not request.user.is_superuser:
                    group = request.user.groups.get(name=group_name)
            except ObjectDoesNotExist:
                return HttpResponseForbidden("Forbidden")
            else:
                return f(request, *args, **kwargs)
        return _check_group
    return _dec

def ulogin(request):
    """
    Страница логина.
    """
    if request.user.is_authenticated():
        return redirect('/logout/')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        request.session.set_test_cookie()
    return direct_to_template(request, 'login.html', {'form':
                                                      form})
@login_required
def ulogout(request):
    """
    Выход пользователя из системы.
    """
    logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)

@render_to()
@paginate(style='digg')
def main_page(request):
    """
    Главная страница.
    """
    form_data = request.GET or None
    form = SearchForm(form_data)
    trash = bool(request.GET.get("trash", False))
    if request.GET.has_key("cemetery") or trash:
        first = False
        burials = Burial.objects.prepared().filter(is_trash=trash).order_by("person__last_name",
                                                                  "person__first_name",
                                                                  "person__patronymic")
    else:
        first = True
        burials_nr = Burial.objects.prepared().filter(is_trash=trash).count()
        burials = Burial.objects.none()
    pp = None
    if form.is_valid():
        cd = form.cleaned_data
        # Обновляем профиль пользователя.
        #if request.user.is_authenticated() and not request.user.is_superuser:
        if request.user.is_authenticated():
            # Сохраняем в профиль значение per_page.
            if cd.get("per_page", ""):
                if request.user.userprofile.records_per_page != cd["per_page"]:
                    request.user.userprofile.records_per_page = cd["per_page"]
                    request.user.userprofile.save()
        if cd.get("records_order_by", ""):
            if cd["records_order_by"] == u'account_book_n':
                burials = burials.order_by('s1', 's2', 's3')
            elif cd["records_order_by"] == u'-account_book_n':
                burials = burials.order_by('-s1', '-s2', '-s3')
            elif cd["records_order_by"] == u'product__place__area':
                burials = burials.order_by('place_s1', 'place_s2',
                                           'place_s3')
            elif cd["records_order_by"] == u'-product__place__area':
                burials = burials.order_by('-place_s1', '-place_s2',
                                           '-place_s3')
            elif cd["records_order_by"] == u'product__place__row':
                burials = burials.order_by('place_s4', 'place_s5',
                                           'place_s6')
            elif cd["records_order_by"] == u'-product__place__row':
                burials = burials.order_by('-place_s4', '-place_s5',
                                           '-place_s6')
            elif cd["records_order_by"] == u'product__place__seat':
                burials = burials.order_by('place_s7', 'place_s8',
                                           'place_s9')
            elif cd["records_order_by"] == u'-product__place__seat':
                burials = burials.order_by('-place_s7', '-place_s8',
                                           '-place_s9')
            else:
                burials = burials.order_by(cd["records_order_by"])
        if cd.get("fio", ""):
            text = re.sub(r"\.", " ", cd["fio"])
            parts = text.split()
            fname = ""
            patr = ""
            lname = parts[0].strip(",")
            lname = lname.capitalize()  # //rd-- patch to not working iregex
            if len(parts) > 1:
                fname = parts[1].strip(",")
#                if not fname[-1].isalpha():
#                    fname = "%s*" % fname
                fname = fname.capitalize()# //rd-- patch to not working iregex
            if len(parts) > 2:
                patr = parts[2].strip(",")
                patr = patr.capitalize()# //rd-- patch to not working iregex

# //rd-- fio search field regex rules            
# ".етер"   # ^
# "етер"    # ^
# "етер.*"  # ^
# ".етер.*" # ^
# "етер."   # ^$
# ".*етер"  # $
# ".*етер." # $

            regex = re.sub(r'\?', r'.', lname)
            regex = re.sub(r'\*', r'.*', regex)
            if not regex.startswith(".*"):
                regex = u"^%s" % regex
                if regex.endswith("."):
                    regex = u"%s$" % regex
            else:
                regex = u"%s$" % regex
            burials = burials.filter(person__last_name__iregex=regex)
            if fname:
                regex = re.sub(r'\?', r'.', fname)
                regex = re.sub(r'\*', r'.*', regex)
                if not regex.startswith("."):
                    regex = u"^%s" % regex
#                if not (regex.endswith(".") or regex.endswith("*")):
#                    regex = u"%s$" % regex
                burials = burials.filter(person__first_name__iregex=regex)
            if patr:
                regex = re.sub(r'\?', r'.', patr)
                regex = re.sub(r'\*', r'.*', regex)
                if not regex.startswith("."):
                    regex = u"^%s" % regex
#                if not (regex.endswith(".") or regex.endswith("*")):
#                    regex = u"%s$" % regex
                burials = burials.filter(person__patronymic__iregex=regex)

        if cd["cemetery"]:
            burials = burials.filter(product__place__cemetery=cd["cemetery"])
        if cd["no_exhumated"]:
            burials = burials.filter(exhumated_date__isnull=True)
        if cd["birth_date_from"]:
            burials = burials.filter(person__birth_date__gte=cd["birth_date_from"])
        if cd["birth_date_to"]:
            burials = burials.filter(person__birth_date__lte=cd["birth_date_to"])
        if cd["death_date_from"]:
            burials = burials.filter(person__birth_date__gte=cd["death_date_from"])
        if cd["death_date_to"]:
            burials = burials.filter(person__birth_date__lte=cd["death_date_to"])
        if cd["operation"]:
            burials = burials.filter(operation=cd["operation"])
        if cd["burial_date_from"]:
            burials = burials.filter(date_fact__gte=cd["burial_date_from"])
            if not cd["burial_date_to"]:
                burials = burials.filter(date_fact__lte=cd["burial_date_from"])
        if cd["burial_date_to"]:
            burials = burials.filter(date_fact__lte=cd["burial_date_to"])
#        if cd["death_certificate"]:
#            burials = burials.filter(person__soul_ptr__deathcertificate__s_number=cd["death_certificate"])
        if cd["account_book_n_from"]:
            if not cd["account_book_n_to"]:
                burials = burials.filter(account_book_n__iexact=cd["account_book_n_from"])
            else:   # account_n_book_to is true
                burials = burials.filter(s2__gte=cd["account_book_n_from"])
                burials = burials.filter(s2__lte=cd["account_book_n_to"])
        else:
            if cd["account_book_n_to"]:
                burials = burials.filter(account_book_n__iexact=cd["account_book_n_to"])
        if cd["customer"]:
            custname = cd["customer"]
            custname = custname.capitalize()# //rd-- patch to not working iregex
            regex = re.sub(r'\?', r'.', custname)
            regex = re.sub(r'\*', r'.*', regex)
            if not regex.startswith(".*"):
                regex = u"^%s" % regex
                if regex.endswith("."):
                    regex = u"%s$" % regex
            else:
                regex = u"%s$" % regex
#            regex = re.sub(r'\?', r'.', cd["customer"])
#            regex = re.sub(r'\*', r'.*', regex)
#            if not regex.startswith("."):
#                regex = u"^%s" % regex
#            if not (regex.endswith(".") or regex.endswith("*")):
#                regex = u"%s$" % regex
            burials = burials.filter(customer__person__last_name__iregex=regex)
        if cd["owner"]:
            burials = burials.filter(creator=cd["owner"].userprofile.soul)
        if cd["area"]:
            burials = burials.filter(product__place__area=cd["area"])
        if cd["row"]:
            burials = burials.filter(product__place__row=cd["row"])
        if cd["seat"]:
            burials = burials.filter(product__place__seat=cd["seat"])
        if cd["gps_x"]:
            burials = burials.filter(product__place__gps_x=cd["gps_x"])
        if cd["gps_y"]:
            burials = burials.filter(product__place__gps_y=cd["gps_y"])
        if cd["gps_z"]:
            burials = burials.filter(product__place__gps_z=cd["gps_z"])
        if cd["comment"]:
            burials = burials.filter(ordercomments__comment__icontains=cd["comment"])
    else:
        #if request.user.is_authenticated() and not request.user.is_superuser and not form_data:
        if request.user.is_authenticated() and not form_data:
            pp = request.user.userprofile.records_per_page
            ob = request.user.userprofile.records_order_by
            redirect_str = "/?print="
            if pp:
                redirect_str = "%s&per_page=%d" % (redirect_str, pp)
            if ob:
                redirect_str = "%s&records_order_by=%s" % (redirect_str, ob)
            return redirect(redirect_str)

    if request.GET.get("print"):
        result = {"form": form,
          "object_list": burials,
          "obj_nr": len(burials),
          "TEMPLATE": "burials_print.html",
        }
    else:
        result = {"form": form,
                  "object_list": burials,
                  "TEMPLATE": "burials.html",
                  }
        if first:
            result["obj_nr"] = burials_nr
        else:
            result["obj_nr"] = burials.count()
        if pp:
            result["per_page"] = pp

    return result


@login_required
@is_in_group("journal")
@transaction.commit_on_success
def journal(request):
    """
    Страница ввода нового захоронения.
    """
    PhoneFormSet = modelformset_factory(Phone, exclude=("soul",), extra=4)

    if request.user.userprofile.default_cemetery:
        cem = request.user.userprofile.default_cemetery
    else:
        cem = None
    if request.user.userprofile.default_operation:
        oper = request.user.userprofile.default_operation
    else:
        oper = None

    next_day = datetime.date.today() + datetime.timedelta(1)
    if next_day.weekday() == 6:
        next_day = next_day + datetime.timedelta(1)
    initial = {
        'burial_date': next_day.strftime('%d.%m.%Y'),
    }
    if request.GET.get('place'):
        place = get_object_or_404(Place, pk=request.GET.get('place'))
        initial.update({
            'cemetery': place.cemetery,
            'area': place.area,
            'row': place.row,
            'seat': place.seat,
        })

    form = JournalForm(cem=cem, oper=oper, data=request.POST or None, files=request.FILES or None, initial=initial)
    location_form = AddressForm(prefix='address', data=request.POST or None)
    registration_form = AddressForm(prefix='registration', data=request.POST or None)
    responsible_form = AddressForm(prefix='responsible', data=request.POST or None)
    cert_form = CertificateForm(prefix='certificate', data=request.POST or None)
    id_form = IDForm(prefix='id', data=request.POST or None)

    phoneset = PhoneFormSet(prefix='phones', data=request.POST or None, queryset=Phone.objects.none())

    id_valid = request.POST.get('opf') != 'fizik' or id_form.is_valid()
    forms_valid = form.is_valid() and location_form.is_valid() and registration_form.is_valid() and cert_form.is_valid() and id_valid
    responsible_valid = request.GET.get('responsible_myself') or responsible_form.is_valid()

    duplicates = []
    if request.method == "POST" and form.is_valid() and not request.REQUEST.get('duplicates_ok'):
        cd = form.cleaned_data
        params = dict(
            product__place__cemetery = cd["cemetery"],
            person__birth_date = cd["birth_date"],
            person__death_date = cd["death_date"],
            date_fact = cd["burial_date"],
        )
        if cd["last_name"].lower() != u'неизвестен':
            params['person__last_name__iexact'] = cd["last_name"]
        duplicates = Burial.objects.filter(**params)

    duplicates_ok = not duplicates or request.REQUEST.get('duplicates_ok')

    if request.method == "POST" and forms_valid and responsible_valid and duplicates_ok:
        cd = form.cleaned_data
        # Try to get Place.
        try:
            place = Place.objects.get(cemetery=cd["cemetery"], area=cd["area"], row=cd["row"], seat=cd["seat"])
        except ObjectDoesNotExist:
            # Create new Place.
            place = Place(creator=request.user.userprofile.soul)
            place.cemetery = cd["cemetery"]
            place.area = cd["area"]
            place.row = cd["row"]
            place.seat = cd["seat"]
            if cd["burial_date"] < datetime.date.today() and (not cd["rooms"] or cd["rooms"] == 1):
                place.rooms = place.count_burials() + 1
            else:
                place.rooms = cd["rooms"]
            place.soul = cd["cemetery"].organization.soul_ptr
            place.name = u"%s.уч%sряд%sместо%s" % (place.cemetery.name, place.area, place.row, place.seat)
            place.p_type = ProductType.objects.get(uuid=settings.PLACE_PRODUCTTYPE_ID)
            place.save()
        # Create new Person for dead man.
        new_person = Person(creator=request.user.userprofile.soul)
        new_person.last_name = cd["last_name"].capitalize()
        new_person.first_name = cd["first_name"].capitalize()
        new_person.patronymic = cd["patronymic"].capitalize()
        new_person.birth_date = cd.get("birth_date") or None
        new_person.death_date = cd.get("birth_date") or None
        new_person.save()

        # Create new Person for customer.
        customer = Person(creator=request.user.userprofile.soul)
        customer.last_name = cd["customer_last_name"].capitalize()
        if cd.get("customer_first_name", ""):
            customer.first_name = cd["customer_first_name"].capitalize()
        if cd.get("customer_patronymic", ""):
            customer.patronymic = cd["customer_patronymic"].capitalize()

        customer.location = location_form.save()
        customer.save()

        if id_form.is_valid():
            personid = id_form.save(commit=False)
            personid.person = customer
            personid.save()

        # Customer phone
        if phoneset.is_valid():
            for phone in phoneset.save(commit=False):
                phone.soul = customer.soul_ptr
                phone.save()

        # Create new Burial.
        new_burial = Burial(creator=request.user.userprofile.soul)
        new_burial.person = new_person
        new_burial.product = place.product_ptr

        d = cd["burial_date"]
        if cd["burial_time"]:
            t = cd["burial_time"]
            d = datetime.datetime(*d.timetuple()[:3]) + datetime.timedelta(0, t.hour*3600 + t.minute*60 + t.second)

        new_burial.date_plan = d
        new_burial.date_fact = d

        new_burial.exhumated_date = cd["exhumated_date"]
        new_burial.account_book_n = cd["account_book_n"]
        new_burial.customer = customer.soul_ptr
        new_burial.responsible = cd["cemetery"].organization.soul_ptr  #ставить орг-ию кладбища
        new_burial.doer = request.user.userprofile.soul
        new_burial.operation = cd["operation"]

        new_burial.person.location = registration_form.save()

        if request.REQUEST.get('opf') == 'fizik':
            if request.REQUEST.get('responsible_myself'):
                new_burial.responsible_customer = None
            else:
                new_burial.responsible_customer = Person.objects.create(
                    creator=request.user.userprofile.soul,
                    last_name=cd["responsible_last_name"].capitalize(),
                    first_name=cd.get("responsible_first_name", "").capitalize(),
                    patronymic=cd.get("responsible_patronymic", "").capitalize(),
                    location = responsible_form.save(),
                )
        else:
            agent = cd['agent']
            agent.dover_number = cd['dover_number']
            agent.dover_date = cd['dover_date']
            agent.dover_expire = cd['dover_expire']
            agent.save()

            new_burial.responsible_customer = agent.person
            new_burial.responsible_agent = agent

        new_burial.save()

        if not new_burial.account_book_n:
            num = new_burial.generate_account_number()
            new_burial.save()
            if not place.seat:
                place.seat = num
                place.save()

        # Create comment.
        if cd.get("comment", ""):
            new_burial.add_comment(cd["comment"], request.user.userprofile.soul)
        # Save files.
        for nf in request.FILES:
            nfile = request.FILES[nf]
            of = OrderFiles(creator=request.user.userprofile.soul)
            of.order = new_burial.order_ptr
            nfile.name = unicode(nfile.name)
            of.ofile = nfile
            if cd.get("file1_comment", ""):
                of.comment = cd["file1_comment"]
            of.save()

        if cert_form.cleaned_data.get('s_number'):
            ds = cert_form.save(commit=False)
            ds.soul_id=new_burial.person.pk
            ds.save()

        if request.POST.get('and_print'):
            return redirect("print_burial", new_burial.pk)
        return redirect("/journal/")

    today = datetime.date.today()
    burials = Burial.objects.filter(is_trash=False, creator=request.user.userprofile.soul,
                            date_of_creation__gte=today).order_by('-date_of_creation')[:20]
    return direct_to_template(request, 'journal.html', {
        'form': form,
        'object_list': burials,
        'phoneset': phoneset,
        'location_form': location_form,
        'registration_form': registration_form,
        'responsible_form': responsible_form,
        'certificate_form': cert_form,
        'id_form': id_form,
        'duplicates': duplicates,
    })

@login_required
@is_in_group("edit_burial")
@transaction.commit_on_success
def edit_burial(request, uuid):
    """
    Страница редактирования существующего захоронения.
    """
    burial = get_object_or_404(Burial, uuid=uuid)
    PhoneFormSet = modelformset_factory(Phone, exclude=("soul",), extra=4)

    cem = burial.product.place.cemetery
    oper = burial.operation

    initial = {
        'account_book_n': burial.account_book_n,
        'burial_date': burial.date_fact and burial.date_fact.strftime('%d.%m.%Y'),
        'birth_date': burial.person.birth_date and burial.person.birth_date.strftime('%d.%m.%Y'),
        'death_date': burial.person.death_date and burial.person.death_date.strftime('%d.%m.%Y'),
        'exhumated_date': burial.exhumated_date and burial.exhumated_date.strftime('%d.%m.%Y'),
        'last_name': burial.person.last_name,
        'first_name': burial.person.first_name,
        'patronymic': burial.person.patronymic,
        'cemetery': burial.product.place.cemetery,
        'operation': burial.operation,
        'hoperation': burial.operation,
        'area': burial.product.place.area,
        'row': burial.product.place.row,
        'seat': burial.product.place.seat,
        'rooms': burial.product.place.rooms,
        'rooms_free': burial.product.place.rooms_free,
        'customer_last_name': burial.customer.person.last_name,
        'customer_first_name': burial.customer.person.first_name,
        'customer_patronymic': burial.customer.person.patronymic,

        'responsible_last_name': burial.responsible_customer and burial.responsible_customer.person.last_name,
        'responsible_first_name': burial.responsible_customer and burial.responsible_customer.person.first_name,
        'responsible_patronymic': burial.responsible_customer and burial.responsible_customer.person.patronymic,
        'responsible_myself': not burial.responsible_customer,

        'opf': burial.responsible_agent and 'yurik' or 'fizik',
        'organization': burial.responsible_agent and burial.responsible_agent.organization,
        'agent': burial.responsible_agent,
        'agent_director': burial.responsible_agent and not burial.responsible_agent.dover_number,
        'dover_number': burial.responsible_agent and burial.responsible_agent.dover_number or '',
        'dover_date': burial.responsible_agent and burial.responsible_agent.dover_number or '',
        'dover_expire': burial.responsible_agent and burial.responsible_agent.dover_number or '',
    }
    form = JournalForm(cem=cem, oper=oper, data=request.POST or None, files=request.FILES or None, initial=initial)
    location_form = AddressForm(prefix='address', data=request.POST or None, instance=burial.customer.location)
    registration_form = AddressForm(prefix='registration', data=request.POST or None, instance=burial.person.location)
    responsible_form = AddressForm(
        prefix='responsible',
        data=request.POST or None,
        instance=burial.responsible_customer and burial.responsible_customer.location
    )
    try:
        dc = burial.person.deathcertificate
    except DeathCertificate.DoesNotExist:
        dc = None
    cert_form = CertificateForm(prefix='certificate', data=request.POST or None, instance=dc)

    try:
        id = burial.customer.person.personid
    except (Person.DoesNotExist, PersonID.DoesNotExist):
        id = None
    id_form = IDForm(prefix='id', data=request.POST or None, instance=id)

    phoneset = PhoneFormSet(prefix='phones', data=request.POST or None, queryset=burial.customer.phone_set.all())

    id_valid = request.POST.get('opf') != 'fizik' or id_form.is_valid()
    forms_valid = form.is_valid() and location_form.is_valid() and registration_form.is_valid() and cert_form.is_valid() and id_valid
    responsible_valid = request.GET.get('responsible_myself') or responsible_form.is_valid()

    if request.method == "POST" and forms_valid and responsible_valid:
        cd = form.cleaned_data

        place = burial.product.place
        place.cemetery = cd["cemetery"]
        place.area = cd["area"]
        place.row = cd["row"]
        place.seat = cd["seat"]
        place.rooms = cd["rooms"]
        place.soul = cd["cemetery"].organization.soul_ptr
        place.name = u"%s.уч%sряд%sместо%s" % (place.cemetery.name, place.area, place.row, place.seat)
        place.p_type = ProductType.objects.get(uuid=settings.PLACE_PRODUCTTYPE_ID)
        place.save()

        # Create new Person for dead man.
        new_person = burial.person
        new_person.last_name = cd["last_name"].capitalize()
        new_person.first_name = cd["first_name"].capitalize()
        new_person.patronymic = cd["patronymic"].capitalize()
        new_person.birth_date = cd.get("birth_date") or None
        new_person.death_date = cd.get("birth_date") or None
        new_person.save()

        # Create new Person for customer.
        customer = burial.customer.person
        customer.last_name = cd["customer_last_name"].capitalize()
        if cd.get("customer_first_name", ""):
            customer.first_name = cd["customer_first_name"].capitalize()
        if cd.get("customer_patronymic", ""):
            customer.patronymic = cd["customer_patronymic"].capitalize()

        customer.location = location_form.save()
        customer.save()

        if id_form.is_valid():
            id = id_form.save(commit=False)
            id.person = customer
            id.save()

        # Customer phone
        if phoneset.is_valid():
            for phone in phoneset.save(commit=False):
                phone.soul = customer.soul_ptr
                phone.save()

        # Create new Burial.
        new_burial = burial
        new_burial.person = new_person
        new_burial.product = place.product_ptr

        d = cd["burial_date"]
        if cd["burial_time"]:
            t = cd["burial_time"]
            d = datetime.datetime(*d.timetuple()[:3]) + datetime.timedelta(0, t.hour*3600 + t.minute*60 + t.second)

        new_burial.date_plan = d
        new_burial.date_fact = d
        
        new_burial.account_book_n = cd["account_book_n"]
        new_burial.exhumated_date = cd["exhumated_date"]
        new_burial.customer = customer.soul_ptr
        new_burial.responsible = cd["cemetery"].organization.soul_ptr  #ставить орг-ию кладбища
        new_burial.doer = request.user.userprofile.soul
        new_burial.operation = cd["operation"]
        new_burial.account_book_n = cd["account_book_n"]

        if request.POST.get('disable_exhumation'):
            new_burial.exhumated_date = None

        if request.REQUEST.get('opf') == 'fizik':
            if request.GET.get('responsible_myself'):
                new_burial.responsible_customer = None
            else:
                if new_burial.responsible_customer:
                    Person.objects.filter(pk=new_burial.responsible_customer).update(
                        last_name=cd["responsible_last_name"].capitalize(),
                        first_name=cd.get("responsible_first_name", "").capitalize(),
                        patronymic=cd.get("responsible_patronymic", "").capitalize(),
                        location = responsible_form.save(),
                    )
                else:
                    new_burial.responsible_customer = Person.objects.create(
                        creator=request.user.userprofile.soul,
                        last_name=cd["responsible_last_name"].capitalize(),
                        first_name=cd.get("responsible_first_name", "").capitalize(),
                        patronymic=cd.get("responsible_patronymic", "").capitalize(),
                        location = responsible_form.save(),
                    )
        else:
            agent = cd['agent']
            agent.dover_number = cd['dover_number']
            agent.dover_date = cd['dover_date']
            agent.dover_expire = cd['dover_expire']
            agent.save()

            new_burial.responsible_customer = agent.person
            new_burial.responsible_agent = agent


        new_burial.save()

        new_burial.person.location = registration_form.save()

        if not new_burial.account_book_n:
            num = new_burial.generate_account_number()
            new_burial.save()
            if not place.seat:
                place.seat = num
                place.save()

        # Create comment.
        if cd.get("comment", ""):
            new_burial.add_comment(cd["comment"], request.user.userprofile.soul)
        # Save files.
        for nf in request.FILES:
            nfile = request.FILES[nf]
            of = OrderFiles(creator=request.user.userprofile.soul)
            of.order = new_burial.order_ptr
            nfile.name = unicode(nfile.name)
            of.ofile = nfile
            if cd.get("file1_comment", ""):
                of.comment = cd["file1_comment"]
            of.save()

        if cert_form.cleaned_data.get('s_number'):
            ds = cert_form.save(commit=False)
            ds.soul_id = new_burial.person.pk
            ds.save()

        return redirect("/")

    today = datetime.date.today()
    burials = Burial.objects.filter(is_trash=False, creator=request.user.userprofile.soul,
                            date_of_creation__gte=today).order_by('-date_of_creation')[:20]
    return direct_to_template(request, 'burial_edit.html', {
        'burial': burial, 
        'form': form,
        'object_list': burials,
        'phoneset': phoneset,
        'location_form': location_form,
        'registration_form': registration_form,
        'certificate_form': cert_form,
        'responsible_form': responsible_form,
        'request': request,
        'id_form': id_form,
    })


def get_positions(burial):
    positions = []
    for product in OrderProduct.objects.all():
        try:
            pos = OrderPosition.objects.get(order_product=product, order=burial)
        except OrderPosition.DoesNotExist:
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
@is_in_group("edit_burial")
@transaction.commit_on_success
def print_burial(request, uuid):
    """
    Страница печати документов захоронения.
    """
    burial = get_object_or_404(Burial, uuid=uuid)
    positions = get_positions(burial)

    payment_form = OrderPaymentForm(instance=burial, data=request.POST or None, )
    positions_fs = OrderPositionsFormset(initial=positions, data=request.POST or None, )
    print_form = PrintOptionsForm(data=request.POST or None, )
    try:
        env = Env.objects.get()
        org = Organization.objects.get(uuid=env.uuid)
    except (Env.DoesNotExist, Organization.DoesNotExist):
        org = None

    if request.POST and positions_fs.is_valid() and payment_form.is_valid() and print_form.is_valid():
        for f in positions_fs.forms:
            if f.cleaned_data['active']:
                try:
                    pos = OrderPosition.objects.get(order_product=f.initial['order_product'], order=burial)
                except OrderPosition.DoesNotExist:
                    OrderPosition.objects.create(
                        order_product=f.initial['order_product'],
                        order=burial,
                        price=f.cleaned_data['price'],
                        count=f.cleaned_data['count'],
                    )
                else:
                    pos.price = pos.price
                    pos.count = pos.count
                    pos.save()
            else:
                try:
                    pos = OrderPosition.objects.get(order_product=f.initial['order_product'], order=burial)
                except OrderPosition.DoesNotExist:
                    pass
                else:
                    pos.delete()

        payment_form.save()

        positions = get_positions(burial)

        if print_form.cleaned_data.get('receipt'):
            return direct_to_template(request, 'reports/spravka.html', {
                'burial': burial,
                'now': datetime.datetime.now(),
                'org': org,
            })

        if print_form.cleaned_data.get('dogovor'):
            return direct_to_template(request, 'reports/dogovor.html', {
                'burial': burial,
                'now': datetime.datetime.now(),
                'org': org,
            })

        return direct_to_template(request, 'reports/act.html', {
            'burial': burial,
            'positions': positions,
            'total': float(sum([p['sum'] for p in positions])),
            'catafalque': print_form.cleaned_data.get('catafalque'),
            'graving': print_form.cleaned_data.get('graving'),
            'now': datetime.datetime.now(),
            'org': org,
        })

    return direct_to_template(request, 'burial_print.html', {
        'burial': burial,
        'positions_fs': positions_fs,
        'payment_form': payment_form,
        'print_form': print_form,
    })

@login_required
#@permission_required('common.change_ordercomment')
@is_in_group("edit_burial")
@transaction.commit_on_success
def order_filecomment_edit(request, uuid):
    """
    Страница редактирования комментария к файлу.
    """
    try:
        f = OrderFiles.objects.get(uuid=uuid)
    except ObjectDoesNotExist:
        raise Http404
    else:
        if request.method == "POST":
            form = OrderFileCommentForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
#                ouuid = f.order.uuid
                f.comment = cd["comment"]
                f.creator = request.user.userprofile.soul
                f.date_of_creation = datetime.datetime.now()
                f.save()
                return redirect("/burial/%s/" % f.order.uuid)
        else:
            initial_data = {"comment": f.comment}
            form = OrderFileCommentForm(initial=initial_data)
        return direct_to_template(request, "order_comment_edit.html", {"form": form})


@login_required
#@permission_required('common.change_ordercomment')
@is_in_group("edit_burial")
@transaction.commit_on_success
def order_comment_edit(request, uuid):
    """
    Страница редактирования комментария к захоронению.
    """
    if request.method == "POST":
        form = OrderCommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                comment = OrderComments.objects.get(uuid=uuid)
            except ObjectDoesNotExist:
                raise Http404
            else:
                ouuid = comment.order.uuid
                if cd["bdelete"]:
                    comment.delete()
                else:
                    comment.comment = cd["comment"]
                    comment.creator = request.user.userprofile.soul
                    comment.date_of_creation = datetime.datetime.now()
                    comment.save()
                return redirect("/burial/%s/" % ouuid)
    else:
        initial_data = {"comment": OrderComments.objects.get(uuid=uuid).comment}
        form = OrderCommentForm(initial=initial_data)
    return direct_to_template(request, "order_comment_edit.html", {"form": form})


@login_required
@is_in_group("profile")
@transaction.commit_on_success
def profile(request):
    """
    Редактирование (и создание) профиля пользователя.
    """
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if hasattr(request.user, "userprofile"):
                up = request.user.userprofile
            else:
                # this case could not happen - we creating profile with user creation!
                soul = Soul(creator=request.user.userprofile.soul)
                soul.save()
                up = UserProfile(user=request.user, soul=soul)
            if cd.get("cemetery", ""):
                up.default_cemetery = cd["cemetery"]
            else:
                up.default_cemetery = None
            if cd.get("operation", ""):
                up.default_operation = cd["operation"]
            else:
                up.default_operation = None
            if cd.get("records_per_page", 0):
                up.records_per_page = cd["records_per_page"]
            else:
                up.records_per_page = None
            if cd.get("records_order_by", ""):
                up.records_order_by = cd["records_order_by"]
            else:
                up.records_order_by = ""
#            if cd.get("default_country", ""):
#                up.default_country = cd["default_country"]
#                if cd.get("default_region", ""):
#                    try:
#                        region = GeoRegion.objects.get(country=cd["default_country"], name__iexact=cd["default_region"])
#                    except ObjectDoesNotExist:
#                        region = GeoRegion()
#                        region.country = cd["default_country"]
#                        region.name = cd["default_region"].capitalize()
#                        region.save()
#                    up.default_region = region
#                    if cd.get("default_city", ""):
#                        try:
#                            city = GeoCity.objects.get(region=region, name__iexact=cd["default_city"])
#                        except ObjectDoesNotExist:
#                            city = GeoCity()
#                            city.country = cd["default_country"]
#                            city.region = region
#                            city.name = cd["default_city"].capitalize()
#                            city.save()
#                        up.default_city = city
            up.save()
            return redirect("/profile/")
    else:
        if hasattr(request.user, "userprofile"):
            profile = request.user.userprofile
            initial_data = {}
            if profile.default_cemetery:
                initial_data["cemetery"] = profile.default_cemetery
            if profile.default_operation:
                initial_data["operation"] = profile.default_operation
                initial_data["hoperation"] = profile.default_operation.uuid
#            if profile.default_country:
#                initial_data["default_country"]= profile.default_country
#            if profile.default_region:
#                initial_data["default_region"]= profile.default_region.name
#            if profile.default_city:
#                initial_data["default_city"]= profile.default_city.name
            if profile.records_per_page:
                initial_data["records_per_page"]= profile.records_per_page
            if profile.records_order_by:
                initial_data["records_order_by"]= profile.records_order_by
            form = UserProfileForm(initial=initial_data)
        else:
            form = UserProfileForm()
    return direct_to_template(request, 'profile2.html', {"form": form})



@login_required
#@permission_required('common.change_burial')
#@is_in_group("management")
def management(request):
    """
    Общая страница выбора вариантов управления.
    """
    user = request.user
    if not user.is_superuser:
        return HttpResponseForbidden("Forbidden")
    return direct_to_template(request, 'management.html')


@login_required
#@permission_required('common.change_burial')
#@is_in_group("management_user")
@transaction.commit_on_success
def management_user(request):
    """
    Страница управления пользователями (создание нового, показ существующих).
    """
    user = request.user
    if not user.is_superuser:
        return HttpResponseForbidden("Forbidden")
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            person = Person(last_name=cd['last_name'].capitalize(),
                            creator=request.user.userprofile.soul)
            if cd.get("first_name", ""):
                person.first_name = cd['first_name'].capitalize()
            if cd.get("patronymic", ""):
                person.patronymic = cd['patronymic'].capitalize()
            password = cd['password1']
            person.save()
            if cd.get('phone', ""):
                phone = Phone(soul=person.soul_ptr, f_number=cd['phone'])
                phone.save()
#            person_role = PersonRole(person=person, role=cd['role'],
#                                     creator=request.user.userprofile.soul)
#            person_role.save()
            user = User.objects.create_user(username=cd['username'], email="",
                                            password=password)
            user.last_name = cd['last_name'].capitalize()
            if cd.get("first_name", ""):
                user.first_name = cd['first_name'].capitalize()
            profile = UserProfile(user=user, soul=person.soul_ptr)
            profile.save()
            # Добавление пользователя во все существующие django-группы.
            dgroups = Group.objects.all()
            for dgr in dgroups:
                user.groups.add(dgr)
#            if hasattr(cd['role'], "djgroups") and cd['role'].djgroups.all():
#                for djgr in cd['role'].djgroups.all():
#                    user.groups.add(djgr)  # Добавляем человека в django-группу, связанную с его ролью.
#            user.is_staff = True
            user.save()
            return redirect("/management/user/")
    else:
        form = NewUserForm()
    users = User.objects.all().order_by('last_name')
#    users = PersonRole.objects.all().order_by('person__last_name', 'person__first_name')
    return direct_to_template(request, 'management_user.html',
                              {'form': form, "users": users})


@login_required
#@is_in_group("management_edit_user")
@transaction.commit_on_success
def management_edit_user(request, uuid):
    """
    Редактирование данных исполнителя.
    """
    user = request.user
    if not user.is_superuser:
        return HttpResponseForbidden("Forbidden")
    try:
        person = Person.objects.get(uuid=uuid)
    except ObjectDoesNotExist:
        raise Http404
    user = person.userprofile.user
    PhoneFormSet = modelformset_factory(Phone, exclude=("soul",), extra=3)
    if request.method == "POST":
        phoneset = PhoneFormSet(request.POST, request.FILES, queryset=Phone.objects.filter(soul=person.soul_ptr))
        form = EditUserForm(request.POST)
        if phoneset.is_valid() and form.is_valid():
            cd = form.cleaned_data
            person.last_name = cd["last_name"].capitalize()
            if cd.get("first_name", ""):
                person.first_name = cd['first_name'].capitalize()
            if cd.get("patronymic", ""):
                person.patronymic = cd['patronymic'].capitalize()
            person.save()
            user.username = cd["username"]
#            if cd.get("phone", ""):
#                try:
#                    phone = Phone.objects.filter(soul=person.soul_ptr)[0]
#                except KeyError:
#                    phone = Phone(soul=person.soul_ptr)
#                phone.f_number = cd["phone"]
#                phone.save()
            for phone in phoneset.save(commit=False):
                phone.soul = person.soul_ptr
                phone.save()
            if cd.get("password1", ""):
                user.set_password(cd['password1'])
#            is_staff = cd.get("is_staff", None)
#            if is_staff is not None:
#                user.is_staff = is_staff
            # Roles processing.
#            if cd.get("default_rights", False):
                # Если сбрасываем все права на дефолтные.
#                user.groups.clear()
#                for r in person.roles.all():
#                    for djgr in r.djgroups.all():
#                        user.groups.add(djgr)
#            # Если оставляем кастомные наборы прав.
#            roles = cd["role"]
#            groups_to_remove = set()
#            groups_to_remain = set()
#            # Удаление удаленных ролей исполнителя.
#            for r in person.roles.all():
#                if r not in roles:
#                    # Роль удалена.
#                    old_pr = PersonRole.objects.get(person=person, role=r)
#                    old_pr.delete()
#                    # удаление исполнителя из соответствующих django-групп.
#                    for djgr in r.djgroups.all():
#                        groups_to_remove.add(djgr)
#                else:
#                    for djgr in r.djgroups.all():
#                        groups_to_remain.add(djgr)
#            # Безопасное удаление django-групп.
#            safe_gr_to_remove = groups_to_remove - groups_to_remain
#            for djgr in safe_gr_to_remove:
#                user.groups.remove(djgr)
#            # Назначение Исполнителя на новые роли.
#            for r in roles:
#                if r not in person.roles.all():
#                    # Новая роль.
#                    new_pr = PersonRole(creator=request.user.userprofile.soul, hire_date=datetime.date.today())
#                    new_pr.person = person
#                    new_pr.role = r
#                    new_pr.save()
#                    # добавление исполнителя в соответствующие django-группы.
#                    for djgr in r.djgroups.all():
#                        user.groups.add(djgr)
            user.save()
            return redirect('/management/user/')
    else:
        phoneset = PhoneFormSet(queryset=Phone.objects.filter(soul=person.soul_ptr))
        initial_data = {"last_name": person.last_name,
                        "username": user.username
#                        "is_staff": user.is_staff,
                        }
#        phones = Phone.objects.filter(soul=person.soul_ptr)
#        if phones:
#            initial_data["phone"] = phones[0]
#        if person.personrole_set.all():
#            prs = PersonRole.objects.filter(person=person)
#            roles = []
#            for pr in prs:
#                roles.append(pr.role)
#            initial_data["role"] = roles
        if person.first_name:
            initial_data["first_name"] = person.first_name
        if person.patronymic:
            initial_data["patronymic"] = person.patronymic
        form = EditUserForm(initial=initial_data)
    return direct_to_template(request, 'management_edit_user.html', {'form': form, 'phoneset': phoneset})


@login_required
#@permission_required('common.change_burial')
#@is_in_group("management_cemetery")
@transaction.commit_on_success
def management_cemetery(request):
    """
    Страница управления кладбищами.
    """
    user = request.user
    if not user.is_superuser:
        return HttpResponseForbidden("Forbidden")
    if request.method == "POST":
        form = CemeteryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            location = Location()
            location.save()
            cemetery = Cemetery()
            cemetery.organization = cd["organization"]
            cemetery.location = location
            cemetery.name = cd["name"]
            cemetery.creator = request.user.userprofile.soul
            cemetery.save()
            location_street = cd.get("street", "")
            location_city = cd.get("city", "")
            location_region = cd.get("region", "")
            location_country = cd.get("country", "")
            location_house = cd.get("house", "")
            location_block = cd.get("block", "")
            location_building = cd.get("building", "")
            location_post_index = cd.get("post_index", "")
            if location_street and location_city and location_region and location_country:
                # Есть все для создания непустого Location.
                # Страна.
                try:
                    country = GeoCountry.objects.get(name__iexact=location_country)
                except ObjectDoesNotExist:
                    country = GeoCountry(name=location_country.capitalize())
                    country.save()
                # Регион.
                try:
                    region = GeoRegion.objects.get(name__iexact=location_region,
                                                   country=country)
                except ObjectDoesNotExist:
                    region = GeoRegion(name=location_region.capitalize(), country=country)
                    region.save()
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(name__iexact=location_city, region=region)
                except ObjectDoesNotExist:
                    city = GeoCity(name=location_city.capitalize(), country=country,
                                   region=region)
                    city.save()
                # Улица.
                try:
                    street = Street.objects.get(name__iexact=location_street, city=city)
                except ObjectDoesNotExist:
                    street = Street(name=location_street.capitalize(), city=city)
                    street.save()
                # Продолжаем с Location.
                location.street = street
                if location_house:
                    location.house = location_house
                    if location_block:
                        location.block = location_block
                    if location_building:
                        location.building = location_building
            if location_post_index:
                location.post_index = location_post_index
            location.save()
            return redirect("/management/cemetery/")
    else:
        form = CemeteryForm()
    cemeteries = Cemetery.objects.all()
    return direct_to_template(request, 'management_add_cemetery.html',
                              {'form': form,
                               "cemeteries": cemeteries})


@login_required
#@permission_required('common.change_burial')
#@is_in_group("management_edit_cemetery")
@transaction.commit_on_success
def management_edit_cemetery(request, uuid):
    """
    Редактирование данных кладбища.
    """
    user = request.user
    if not user.is_superuser:
        return HttpResponseForbidden("Forbidden")
    try:
        cemetery = Cemetery.objects.get(uuid=uuid)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == "POST":
        form = CemeteryForm(request.POST)
        if form.is_valid():
            location = cemetery.location
            cd = form.cleaned_data
            cemetery.name = cd["name"]
            cemetery.organization = cd["organization"]
            cemetery.save()
            location_street = cd.get("street", "")
            location_city = cd.get("city", "")
            location_region = cd.get("region", "")
            location_country = cd.get("country", "")
            location_house = cd.get("house", "")
            location_block = cd.get("block", "")
            location_building = cd.get("building", "")
            location_post_index = cd.get("post_index", "")
            # Очищаем Location.
            location.street = None
            location.house = ""
            location.block = ""
            location.building = ""
            location.flat = ""
#            location.save()
            if location_street and location_city and location_region and location_country:
                # Есть все для создания непустого Location.
                # Страна.
                try:
                    country = GeoCountry.objects.get(name__iexact=location_country)
                except ObjectDoesNotExist:
                    country = GeoCountry(name=location_country.capitalize())
                    country.save()
                # Регион.
                try:
                    region = GeoRegion.objects.get(name__iexact=location_region,
                                                   country=country)
                except ObjectDoesNotExist:
                    region = GeoRegion(name=location_region.capitalize(), country=country)
                    region.save()
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(name__iexact=location_city, region=region)
                except ObjectDoesNotExist:
                    city = GeoCity(name=location_city.capitalize(), country=country,
                                   region=region)
                    city.save()
                # Улица.
                try:
                    street = Street.objects.get(name__iexact=location_street, city=city)
                except ObjectDoesNotExist:
                    street = Street(name=location_street.capitalize(), city=city)
                    street.save()
                # Продолжаем с Location.
                location.street = street
                if location_house:
                    location.house = location_house
                    if location_block:
                        location.block = location_block
                    if location_building:
                        location.building = location_building
            if location_post_index:
                location.post_index = location_post_index
            location.save()
            return redirect('/management/cemetery/')
    else:
        initial_data = {
            "organization": cemetery.organization,
            "name": cemetery.name,
        }
        if cemetery.location.street:
            initial_data["country"] = cemetery.location.street.city.country.name
            initial_data["region"] = cemetery.location.street.city.region.name
            initial_data["city"] = cemetery.location.street.city.name
            initial_data["street"] = cemetery.location.street.name
            if cemetery.location.house:
                initial_data["house"] = cemetery.location.house
            if cemetery.location.block:
                initial_data["block"] = cemetery.location.block
            if cemetery.location.building:
                initial_data["building"] = cemetery.location.building
        if cemetery.location.post_index:
            initial_data["post_index"] = cemetery.location.post_index
        form = CemeteryForm(initial=initial_data)
    return direct_to_template(request, 'management_edit_cemetery.html',
                              {'form': form,})



@login_required
@transaction.commit_on_success
def init(request):
    """
    Страница ввода инициализационных данных.
    """
    user = request.user
    if not user.is_superuser:
        return HttpResponseForbidden("Forbidden")

    try:
        env = Env.objects.get()
        organization = Organization.objects.get(uuid=env.uuid)
    except:
        organization = None
        env = None

    bank_formset = InitBankFormset(instance=organization, data=request.POST or None)

    if request.method == "POST":
        form = InitalForm(request.POST)
        if form.is_valid() and bank_formset.is_valid():
            cd = form.cleaned_data
            # Создаем уникальный uuid сервера.
            env = Env()
            env.save()
            # Создаем организацию.
            if not organization:
                organization = Organization(
                    creator=request.user.userprofile.soul,
                )
            organization.name = cd["org_name"]
            organization.kpp = cd["kpp"]
            organization.save()

            bank_formset = InitBankFormset(instance=organization, data=request.POST or None)
            for f in bank_formset.forms:
                if f.is_valid():
                    f.save()

            # Создаем объект Phone для организации.
            org_phone = cd.get("org_phone", "")
            if org_phone:
                org_phone_obj = Phone(soul=organization.soul_ptr, f_number=org_phone)
                org_phone_obj.save()
            # Создаем объекты SoulProducttypeOperation.
            operations = Operation.objects.all()
            p_type = ProductType.objects.get(uuid=settings.PLACE_PRODUCTTYPE_ID)
            for op in operations:
                spo = SoulProducttypeOperation()
                spo.soul = organization.soul_ptr
                spo.p_type = p_type
                spo.operation = op
                spo.save()
            # Создаем Location для организации.
            org_location = Location()
            org_location_country = cd.get("country", "")
            org_location_region = cd.get("region", "")
            org_location_city = cd.get("city", "")
            org_location_street = cd.get("street", "")
            org_location_house = cd.get("house", "")
            org_location_block = cd.get("block", "")
            org_location_building = cd.get("building", "")
            org_location_flat = cd.get("flat", "")
            org_location_post_index = cd.get("post_index", "")
            if org_location_country and org_location_region and org_location_city and org_location_street:
                # Есть все для создания непустого Location.
                # Страна.
                try:
                    country = GeoCountry.objects.get(name__iexact=org_location_country)
                except ObjectDoesNotExist:
                    country = GeoCountry(name=org_location_country.capitalize())
                    country.save()
                # Регион.
                try:
                    region = GeoRegion.objects.get(name__iexact=org_location_region,
                                                   country=country)
                except ObjectDoesNotExist:
                    region = GeoRegion(name=org_location_region.capitalize(), country=country)
                    region.save()
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(name__iexact=org_location_city, region=region)
                except ObjectDoesNotExist:
                    city = GeoCity(name=org_location_city.capitalize(), country=country,
                                   region=region)
                    city.save()
                # Улица.
                try:
                    street = Street.objects.get(name__iexact=org_location_street, city=city)
                except ObjectDoesNotExist:
                    street = Street(name=org_location_street.capitalize(), city=city)
                    street.save()
                # Продолжаем с Location.
                org_location.street = street
                if org_location_house:
                    org_location.house = org_location_house
                    if org_location_block:
                        org_location.block = org_location_block
                    if org_location_building:
                        org_location.building = org_location_building
                    if org_location_flat:
                        org_location.flat = org_location_flat
            if org_location_post_index:
                org_location.post_index = org_location_post_index
            org_location.save()
            organization.location = org_location
            organization.save()

            # Кладбище.
            cemetery = Cemetery(creator=request.user.userprofile.soul, organization=organization, name=cd["cemetery"])
            # Создаем Location для организации.
            cem_location = Location()
            cem_location_country = cd.get("cem_country", "")
            cem_location_region = cd.get("cem_region", "")
            cem_location_city = cd.get("cem_city", "")
            cem_location_street = cd.get("cem_street", "")
            cem_location_house = cd.get("cem_house", "")
            cem_location_block = cd.get("cem_block", "")
            cem_location_building = cd.get("cem_building", "")
            cem_location_post_index = cd.get("cem_post_index", "")
            if cem_location_country and cem_location_region and cem_location_city and cem_location_street:
                # Есть все для создания непустого Location.
                # Страна.
                try:
                    country = GeoCountry.objects.get(name__iexact=cem_location_country)
                except ObjectDoesNotExist:
                    country = GeoCountry(name=cem_location_country.capitalize())
                    country.save()
                # Регион.
                try:
                    region = GeoRegion.objects.get(name__iexact=cem_location_region,
                                                   country=country)
                except ObjectDoesNotExist:
                    region = GeoRegion(name=cem_location_region.capitalize(), country=country)
                    region.save()
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(name__iexact=cem_location_city, region=region)
                except ObjectDoesNotExist:
                    city = GeoCity(name=cem_location_city.capitalize(), country=country,
                                   region=region)
                    city.save()
                # Улица.
                try:
                    street = Street.objects.get(name__iexact=cem_location_street, city=city)
                except ObjectDoesNotExist:
                    street = Street(name=cem_location_street.capitalize(), city=city)
                    street.save()
                # Продолжаем с Location.
                cem_location.street = street
                if cem_location_house:
                    cem_location.house = cem_location_house
                    if cem_location_block:
                        cem_location.block = cem_location_block
                    if cem_location_building:
                        cem_location.building = cem_location_building
            if cem_location_post_index:
                cem_location.post_index = cem_location_post_index
            cem_location.save()
            cemetery.location = cem_location
            cemetery.save()
            
            # Директор.
            # Создаем объект Person.
            person = Person(creator=request.user.userprofile.soul, last_name=cd["last_name"].capitalize())
            first_name = cd.get("first_name", "")
            patronymic = cd.get("patronymic", "")
            phone = cd.get("phone", "")
            if first_name:
                person.first_name = first_name.capitalize()
                if patronymic:
                    person.patronymic = patronymic.capitalize()
            person.save()
            # Создаем объект Phone.
            if phone:
                dir_phone = Phone(soul=person.soul_ptr, f_number=phone)
                dir_phone.save()
            # Системный пользователь django.
            user = User.objects.create_user(username=cd["username"], email="", password=cd["password1"])
#            user.is_staff = True
            user.last_name = cd["last_name"].capitalize()
            if first_name:
                user.first_name = first_name.capitalize()
            user.save()
            # Создаем объект UserProfile.
            profile = UserProfile(user=user, soul=person.soul_ptr)
            profile.save()

            # Добавление пользователя во все существующие django-группы.
            dgroups = Group.objects.all()
            for dgr in dgroups:
                user.groups.add(dgr)

            try:
                env = Env.objects.get()
            except Env.MultipleObjectsReturned:
                Env.objects.all().delete()
                env = Env.objects.create()
            env.uuid = organization.uuid
            env.save()

            return redirect("/management/")
    else:
        try:
            env = Env.objects.get()
            org = Organization.objects.get(uuid=env.uuid)
        except:
            initial = None
        else:
            phones = org.phone_set.all()
            cemeteries = org.cemetery.all()
            cemetery = cemeteries and cemeteries[0] or None
            profile = UserProfile.objects.get(user=user)
            try:
                person = request.user.userprofile.soul.person
            except Person.DoesNotExist:
                person = None
            initial = dict(
                org_name = org.name,
                org_phone = phones and phones[0] or None,
                post_index = org.location.post_index,
                new_street = False,
                new_city = False,
                new_region = False,
                new_country = False,
                house = org.location.house,
                block = org.location.block,
                building = org.location.building,
                flat = org.location.flat,
                cemetery = cemetery,
                cem_post_index = cemetery and cemetery.location.post_index,
                cem_new_street = False,
                cem_new_city = False,
                cem_new_region = False,
                cem_new_country = False,
                cem_house = cemetery and cemetery.location.house,
                cem_block = cemetery and cemetery.location.block,
                cem_building = cemetery and cemetery.location.building,
                username = request.user.username,
                last_name = request.user.last_name,
                first_name = request.user.first_name,
                patronymic = person and person.patronymic,
                password1 = '',
                password2 = '',
                phone = len(phones) > 1 and phones[1] or None,
                kpp = org.kpp,
            )
            if cemetery and cemetery.location and cemetery.location.street:
                initial['cem_street'] = cemetery.location.street.name
                if cemetery.location.street and cemetery.location.street.city:
                    initial['cem_city'] = cemetery.location.street.city.name
                    if cemetery.location.street.city and cemetery.location.street.city.region:
                        initial['cem_region'] = cemetery.location.street.city.region.name
                        if cemetery.location.street.city.region and cemetery.location.street.city.region.country:
                            initial['cem_country'] = cemetery.location.street.city.region.country.name
            if org and org.location and org.location.street:
                initial['street'] = org.location.street.name
                if org.location.street and org.location.street.city:
                    initial['city'] = org.location.street.city.name
                    if org.location.street.city and org.location.street.city.region:
                        initial['region'] = org.location.street.city.region.name
                        if org.location.street.city.region and org.location.street.city.region.country:
                            initial['country'] = org.location.street.city.region.country.name

        form = InitalForm(initial = initial)
    return direct_to_template(request, "init.html", {
        "form": form,
        "bank_formset": bank_formset,
    })


@login_required
#@is_in_group("import_csv")
@transaction.commit_manually
def import_csv(request):
    """
    Импорт захоронений из csv-файла.
    """
    user = request.user
    if not user.is_superuser:
        return HttpResponseForbidden("Forbidden")
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["creator"]:
                creator = cd["creator"].userprofile.soul
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=import_result.csv'
            temp_file = StringIO()
#            writer = csv.writer(response, "4mysql")
#            writer = csv.writer(temp_file, "4mysqlout")
            writer = csv.writer(temp_file, "4mysql")
            err_descrs = []
            good_nr = 0
            bad_nr = 0
            s_time = datetime.datetime.now()
            r = csv.reader(cd["csv_file"], "4mysql")
            for l in r:
                db.reset_queries()
                if l:
                    try:
                        (str_id,
                        n,
                        ln, fn, ptrc, initials,
                        bur_date, area, row, seat,
                        cust_ln, cust_fn, cust_ptrc, cust_initials,
                        city, street, house, block, flat,
                        comment) = l
                        # ID записи в таблице MySQL.
                        str_id = int(str_id)
                        # Номер в книге учета.
                        n = n.decode(settings.CSV_ENCODING).strip().lower()
                        # Фамилия захороненного.
                        if ln == "N":
                            ln = u""
                        else:
                            ln = ln.decode(settings.CSV_ENCODING).strip().capitalize()
                            ln = re.sub(r'ё', r'е', ln)
                            ln = re.sub(r'Ё', r'Е', ln)
                        # Имя захороненного.
                        if fn == "N":
                            fn = u""
                        else:
                            fn = fn.decode(settings.CSV_ENCODING).strip().capitalize()
                        # Отчество захороненного.
                        if ptrc == "N":
                            ptrc = u""
                        else:
                            ptrc = ptrc.decode(settings.CSV_ENCODING).strip().capitalize()
                        # Инициалы захороненного.
                        if initials == "N":
                            initials = u""
                        else:
                            initials = initials.decode(settings.CSV_ENCODING).strip().upper()
                        # Дата захоронения
                        try:
                            bur_date = datetime.datetime.strptime(bur_date[0:10], "%Y-%m-%d")
                        except ValueError:
                            bur_date = datetime.datetime.strptime(bur_date[0:10], "%d.%m.%Y")
                        # Участок/ряд/место.
                        if area == "N":
                            area = u"0"
                        else:
                            area = area.decode(settings.CSV_ENCODING).strip()
                        if row == "N":
                            row = u"0"
                        else:
                            row = row.decode(settings.CSV_ENCODING).strip()
                        if seat == "N":
                            seat = u"0"
                        else:
                            seat = seat.decode(settings.CSV_ENCODING).strip()
                        # Фамилия заказчика.
                        if cust_ln == "N":
                            cust_ln = u"НЕИЗВЕСТЕН"  # Если в базе был Null
                        else:
                            cust_ln = cust_ln.decode(settings.CSV_ENCODING).strip().capitalize()
                            cust_ln = re.sub(r'ё', r'е', cust_ln)
                            cust_ln = re.sub(r'Ё', r'Е', cust_ln)
                        # Имя заказчика.
                        if cust_fn == "N":
                            cust_fn = u""
                        else:
                            cust_fn = cust_fn.decode(settings.CSV_ENCODING).strip().capitalize()
                        # Отчество заказчика.
                        if cust_ptrc == "N":
                            cust_ptrc = u""
                        else:
                            cust_ptrc = cust_ptrc.decode(settings.CSV_ENCODING).strip().capitalize()
                        # Инициалы заказчика.
                        if cust_initials == "N":
                            cust_initials = u""
                        else:
                            cust_initials = cust_initials.decode(settings.CSV_ENCODING).strip().upper()
                        # Город.
                        if city == "N":
                            city = u"НЕИЗВЕСТЕН"  # Если в базе был Null.
                        else:
                            city = city.decode(settings.CSV_ENCODING).strip().capitalize()
                        if not city:
                            city = u"НЕИЗВЕСТЕН"  # Если в базе была пустая строка.
                        if street == "N":
                            street = u""
                        else:
                            street = street.decode(settings.CSV_ENCODING).strip().capitalize()
                            street = re.sub(r'ё', r'е', street)
                            street = re.sub(r'Ё', r'Е', street)
                        if house == "N":
                            house = u""
                        else:
                            house = house.decode(settings.CSV_ENCODING).strip().lower()
                        if block == "N":
                            block = u""
                        if flat == "N":
                            flat = u""

                        # Захороненный.
                        deadman = Person(creator=creator)
                        deadman.last_name = ln
                        if fn:
                            deadman.first_name = fn
                            if ptrc:
                                deadman.patronymic = ptrc
                        else:
                            initials = re.sub(r"[\.\,]", " ", initials.strip()).split()
                            if initials:
                                deadman.first_name = initials[0]
                                if len(initials) > 1:
                                    deadman.patronymic = initials[1]
                        deadman.save()

                        # Заказчик.
                        customer = Person(creator=creator)
                        customer.last_name = cust_ln
                        if cust_fn:
                            customer.first_name = cust_fn
                            if cust_ptrc:
                                customer.patronymic = cust_ptrc
                        else:
                            cust_initials = re.sub(r"[\.\,]", " ", cust_initials).split()
                            if cust_initials:
                                customer.first_name = cust_initials[0]
                                if len(cust_initials) > 1:
                                    customer.patronymic = cust_initials[1]

                        # Адрес заказчика.
                        location = Location()
                        if street:
                            # Присутствуют город и улица - будем создавать Location.
                            cities = GeoCity.objects.filter(name__iexact=city)
                            if cities:
                                cust_city = cities[0]
                            else:
                                cust_city = GeoCity()
                                cust_city.country = GeoCountry.objects.get(name__iexact="НЕИЗВЕСТЕН")
                                cust_city.region = GeoRegion.objects.get(name__iexact="НЕИЗВЕСТЕН")
                                cust_city.name = city
                                cust_city.save()
                            try:
                                cust_street = Street.objects.get(city=cust_city, name__iexact=street)
                            except ObjectDoesNotExist:
                                cust_street = Street(city=cust_city, name=street)
                                cust_street.save()
                            location.street = cust_street
                            if house:
                                location.house = house
                                if block:
                                    location.block = block
                                if flat:
                                    location.flat = flat
                        location.save()
                        customer.location = location
                        customer.save()

                        # Место.
                        cemetery = cd["cemetery"]
                        try:
                            place = Place.objects.get(cemetery=cemetery, area__iexact=area, row__iexact=row,
                                                      seat__iexact=seat)
                        except ObjectDoesNotExist:
                            place = Place(creator=creator)
                            place.cemetery = cemetery
                            place.area = area
                            place.row = row
                            place.seat = seat
                            place.soul = cemetery.organization.soul_ptr
                            place.name = u"%s.уч%sряд%sместо%s" % (place.cemetery.name, place.area, place.row, place.seat)
                            place.p_type = ProductType.objects.get(uuid=settings.PLACE_PRODUCTTYPE_ID)
                            place.save()

                        # Захоронение.
                        burial = Burial(creator=creator)
                        burial.person = deadman
                        burial.account_book_n = n
                        burial.responsible = place.cemetery.organization.soul_ptr
                        burial.customer = customer
                        burial.doer = creator
                        burial.date_fact = bur_date
#                        try:
#                            test_date = datetime.datetime.date(bur_date).strftime("%d.%m.%Y")
                        burial.product = place.product_ptr
                        operation = Operation.objects.get(uuid=settings.OPER_1) # Захоронение
                        if comment == "N":
                            comment = u""
                        else:
                            comment = comment.decode(settings.CSV_ENCODING).strip()
                            comment = re.sub(r'ё', r'е', comment)
                            comment = re.sub(r'Ё', r'Е', comment)
                            if u"захоронение детское" in comment.lower():
                                operation = Operation.objects.get(uuid=settings.OPER_6)
                            elif u"захоронение в существ" in comment.lower():
                                operation = Operation.objects.get(uuid=settings.OPER_3)
                            elif u"почетное захоронение" in comment.lower():
                                operation = Operation.objects.get(uuid=settings.OPER_2)
                            elif u"подзахоронение" in comment.lower():
                                operation = Operation.objects.get(uuid=settings.OPER_4)
                            elif u"захоронение" in comment.lower():
                                operation = Operation.objects.get(uuid=settings.OPER_1)
                            elif u"урна" in comment.lower():
                                operation = Operation.objects.get(uuid=settings.OPER_5)
                        burial.operation = operation
                        burial.save()
                        if comment != u"":
                            burial.add_comment(comment, creator)
                    except Exception, err_descr:
                        # Откатываем транзакцию.
                        transaction.rollback()
                        # Сохраняем описание ошибки.
                        err_descrs.append(err_descr)
#                        # Пишем в выходной csv файл.
                        writer.writerow(l)
                        bad_nr += 1
                    else:
                        # Коммитим все.
                        transaction.commit()
                        good_nr += 1
            myseparator = u'=== ОПИСАНИЕ ОШИБОК ==='
            writer.writerow([myseparator.encode('utf8')])
            for err in err_descrs:
                writer.writerow((err,))
            response.write("Начало/Конец: %s/%s\n" % (s_time, datetime.datetime.now()))
            response.write("Всего/Удачно/Ошибок: %d/%d/%d\n" % (good_nr+bad_nr, good_nr, bad_nr))
            response.write("=== СТРОКИ С ОШИБКАМИ ===\n")
            response.write(temp_file.getvalue())
            return response
#            else:
#                return redirect("/management/import/")
    else:
        form = ImportForm()
    return direct_to_template(request, "import.html", {"form": form})



@login_required
@is_in_group("delete_orderfile")
def delete_orderfile(request, ouuid, fuuid):
    """
    Удаление файла ордера.
    """
    try:
        f = OrderFiles.objects.get(order__uuid=ouuid, uuid=fuuid)
    except ObjectDoesNotExist:
        raise Http404
    f.delete()
    return redirect("/burial/%s/" % ouuid)


def get_customer_ln(request):
    """
    Получение уникального списка фамилий всех заказчиков.
    """
    person_lns = []
    q = request.GET.get('q', None)
    if q is not None:
        rezult = Person.objects.filter(ordr_customer__isnull=False,
                                   last_name__istartswith=q).values("last_name").order_by("last_name").distinct()[:16]
        person_lns = [item["last_name"] for item in rezult]
    return direct_to_template(request, 'ajax.html', {'objects': person_lns,})


def get_deadman(request):
    """
    Получение уникального списка ФИО захороненных.
    """
    persons = []
    q = request.GET.get('q', None)
    if q is not None:
        rezult = Person.objects.filter(buried__isnull=False, last_name__istartswith=q).values("last_name",
                          "first_name", "patronymic").order_by("last_name", "first_name", "patronymic").distinct()[:16]
        persons = ["%s %s %s" % (item["last_name"], item["first_name"], item["patronymic"]) for item in rezult]
    return direct_to_template(request, 'ajax.html', {'objects': persons,})


def get_oper(request):
    """
    Получение списка доступных операций для выбранного кладбища.
    """
    rez = []
    if request.method == "GET" and request.GET.get("id", False):
        try:
            cemetery = Cemetery.objects.get(uuid=request.GET["id"])
        except:
            pass
        else:
            orgsoul=cemetery.organization.soul_ptr
            choices = SoulProducttypeOperation.objects.filter(soul=orgsoul,
                              p_type=settings.PLACE_PRODUCTTYPE_ID).values_list("operation__uuid", "operation__op_type")
            for c in choices:
                rez.append({"optionValue": c[0], "optionDisplay": c[1]})
            rez.insert(0, {"optionValue": 0, "optionDisplay": u'---------'})
    return HttpResponse(JSONEncoder().encode(rez))

def get_agents(request):
    """
    Список доступных агентов для выбранной организации.
    """
    rez = []
    if request.method == "GET" and request.GET.get("id", False):
        try:
            org = Organization.objects.get(uuid=request.GET["id"])
        except:
            pass
        else:
            orgsoul = org.soul_ptr
            choices = Agent.objects.filter(organization=org)
            for c in choices:
                rez.append({"optionValue": c.uuid, "optionDisplay": c.person.full_name()})
            rez.insert(0, {"optionValue": 0, "optionDisplay": u'---------'})
    return HttpResponse(JSONEncoder().encode(rez))

def get_dover(request):
    try:
        agent = Agent.objects.get(pk=request.GET.get('agent'))
    except Agent.DoesNotExist:
        rez = {}
    else:
        rez = {
            'number': agent.dover_number,
            'date': agent.dover_date and agent.dover_date.strftime('%d.%m.%Y') or '',
            'expire': agent.dover_expire and agent.dover_expire.strftime('%d.%m.%Y') or '',
        }
    return HttpResponse(JSONEncoder().encode(rez))

def get_street(request):
    """
    Получение улицы с городом, регионом и страной.
    """
    streets = []
    q = request.GET.get('term', None)
    if q is not None:
        rezult = Street.objects.filter(name__istartswith=q).order_by("name", "city__name", "city__region__name",
                                                                     "city__region__country__name")[:24]
        for s in rezult:
            streets.append(u"%s/%s/%s/%s" % (s.name, s.city.name, s.city.region.name, s.city.region.country.name))
    return HttpResponse(JSONEncoder().encode(streets))


def get_countries(request):
    """
    Получение списка стран с пом. AJAX-запроса.
    """
    countries = []
    q = request.GET.get('term', None)
    if q is not None:
        rezult = GeoCountry.objects.filter(name__istartswith=q).order_by("name")[:8]
        for s in rezult:
            countries.append(s.name)
    return HttpResponse(JSONEncoder().encode(countries))


def get_cities(request):
    """
    Получение списка нас. пунктов с пом. AJAX-запроса.
    """
    cities = []
    q = request.GET.get('term', None)
    if q is not None:
        rezult = GeoCity.objects.filter(name__istartswith=q).order_by("name", "region__name",
                                                                      "region__country__name")[:24]
        for s in rezult:
            cities.append(u"%s/%s/%s" % (s.name, s.region.name, s.region.country.name))
    return HttpResponse(JSONEncoder().encode(cities))


def get_regions(request):
    """
    Получение списка регионов с пом. AJAX-запроса.
    """
    regions = []
    q = request.GET.get('term', None)
    if q is not None:
        rezult = GeoRegion.objects.filter(name__istartswith=q).order_by("name", "country__name")[:24]
        for s in rezult:
            regions.append(u"%s/%s" % (s.name, s.country.name))
    return HttpResponse(JSONEncoder().encode(regions))

