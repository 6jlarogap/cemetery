# -*- coding: utf-8 -*-

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, ContentType
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.http import Http404, HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils.simplejson.encoder import JSONEncoder
from django.forms.models import modelformset_factory
from django import db
from django.db.models import Q
from django.core.urlresolvers import reverse

from common.forms import *
from contrib.constants import UNKNOWN_NAME
from common.models import *

from simplepagination import paginate
from annoying.decorators import render_to

import math
import re
import datetime
import time
import csv
from cStringIO import StringIO


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

@login_required
@render_to()
@paginate(style='digg')
def main_page(request):
    """
    Главная страница.
    """

    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, soul=Soul.objects.create())

    form_data = request.GET or None
    form = SearchForm(form_data)
    trash = bool(request.GET.get("trash", False))
    if request.GET.has_key("cemetery") or trash:
        first = False
        burials = Burial.objects.filter(is_trash=trash).order_by("person__last_name",
                                                                  "person__first_name",
                                                                  "person__patronymic")
    else:
        first = True
        burials_nr = Burial.objects.filter(is_trash=trash).count()
        burials = Burial.objects.none()
    pp = None
    if form.is_valid():
        cd = form.cleaned_data
        sort_order = cd.get("records_order_by", "-account_book_n")
        if sort_order:
            if sort_order == u'account_book_n':
                burials = burials.order_by('acct_num_str1', 'acct_num_num', 'acct_num_str2')
            elif sort_order == u'-account_book_n':
                burials = burials.order_by('-acct_num_str1', '-acct_num_num', '-acct_num_str2')
            elif sort_order == u'product__place__area':
                burials = burials.order_by('product__place__area_str1', 'product__place__area_num',
                                           'product__place__area_str2')
            elif sort_order == u'-product__place__area':
                burials = burials.order_by('-product__place__area_str1', '-product__place__area_num',
                                           '-product__place__area_str2')
            elif sort_order == u'product__place__row':
                burials = burials.order_by('product__place__row_str1', 'product__place__row_num',
                                           'product__place__row_str2')
            elif sort_order == u'-product__place__row':
                burials = burials.order_by('-product__place__row_str1', '-product__place__row_num',
                                           '-product__place__row_str2')
            elif sort_order == u'product__place__seat':
                burials = burials.order_by('product__place__seat_str1', 'product__place__seat_num',
                                           'product__place__seat_str2')
            elif sort_order == u'-product__place__seat':
                burials = burials.order_by('-product__place__seat_str1', '-product__place__seat_num',
                                           '-product__place__seat_str2')
            else:
                burials = burials.order_by(sort_order)
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
                burials = burials.filter(date_fact__lt=cd["burial_date_from"] + datetime.timedelta(1))
        if cd["burial_date_to"]:
            burials = burials.filter(date_fact__lt=cd["burial_date_to"] + datetime.timedelta(1))
#        if cd["death_certificate"]:
#            burials = burials.filter(person__soul_ptr__deathcertificate__s_number=cd["death_certificate"])
        if cd["account_book_n_from"]:
            if not cd["account_book_n_to"]:
                burials = burials.filter(account_book_n__gte=cd["account_book_n_from"])
            else:   # account_n_book_to is true
                burials = burials.filter(account_book_n__gte=cd["account_book_n_from"], account_book_n__lte=cd["account_book_n_to"])
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
            burials = burials.filter(
                Q(customer__person__last_name__iregex=regex) |
                Q(responsible_agent__last_name__iregex=regex) |
                Q(responsible_agent__organization__name__icontains=cd["customer"]) |
                Q(responsible_agent__organization__full_name__icontains=cd["customer"])
            )
        if cd["owner"]:
            burials = burials.filter(creator=cd["owner"].userprofile.soul)
        if cd["area"]:
            if cd["area"] == 'NULL':
                burials = burials.filter(product__place__area='')
            else:
                burials = burials.filter(product__place__area=cd["area"])
        if cd["row"]:
            if cd["row"] == 'NULL':
                burials = burials.filter(product__place__row='')
            else:
                burials = burials.filter(product__place__row=cd["row"])
        if cd["seat"]:
            if cd["seat"] == 'NULL':
                burials = burials.filter(product__place__seat='')
            else:
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

        result['close'] = request.GET.get('close')
    return result


@login_required
@is_in_group("journal")
@transaction.commit_on_success
def journal(request):
    """
    Страница ввода нового захоронения.
    """
    PhoneFormSet = modelformset_factory(Phone, form=PhoneForm, extra=3)

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
        'rooms': 1,
        'rooms_free': 0,
    }

    responsible_address = None
    if request.GET.get('burial'):
        burial = get_object_or_404(Burial, pk=request.GET.get('burial'))
        place = burial.product.place
        initial.update({
            'cemetery': place.cemetery,
            'area': place.area,
            'row': place.row,
            'seat': place.seat,
        })
        if burial.responsible_customer:
            rc = burial.responsible_customer.person
            initial.update({
                'responsible_myself': False,
                'responsible_last_name': rc.last_name,
                'responsible_first_name': rc.first_name,
                'responsible_patronymic': rc.patronymic,
            })

            if rc.location:
                responsible_address = {}
                for k in ['post_index', 'house', 'block', 'building', 'flat', 'info', 'street', 'city', 'region', 'country']:
                    responsible_address[k] = getattr(rc.location, k, None)

    form = JournalForm(cem=cem, oper=oper, data=request.POST or None, files=request.FILES or None, initial=initial)

    if request.GET.get('burial'):
        form.fields['operation'].queryset = Operation.objects.exclude(op_type=u'Захоронение').order_by('ordering', 'op_type')

    location_form = AddressForm(prefix='address', data=request.POST or None)
    registration_form = AddressForm(prefix='registration', data=request.POST or None)
    responsible_form = AddressForm(prefix='responsible', data=request.POST or None, initial=responsible_address)
    cert_form = CertificateForm(prefix='certificate', data=request.POST or None)
    id_form = IDForm(prefix='id', data=request.POST or None)

    phoneset = PhoneFormSet(prefix='phones', data=request.POST or None, queryset=Phone.objects.none())

    id_valid = request.POST.get('opf') != 'fizik' or id_form.is_valid()

    customer_addr_valid = request.POST.get('opf') != 'fizik' or \
                          request.POST.get('customer_last_name') in [None, '', UNKNOWN_NAME] or \
                          location_form.is_valid()
    responsible_valid = request.POST.get('responsible_myself') or \
                        request.POST.get('responsible_last_name') in [None, '', UNKNOWN_NAME] or \
                        responsible_form.is_valid()
    registration_valid = request.POST.get('last_name') in [None, '', UNKNOWN_NAME] or \
                         registration_form.is_valid()
    forms_valid = form.is_valid() and customer_addr_valid and registration_valid and cert_form.is_valid() and id_valid

    duplicates = []
    if request.method == "POST" and form.is_valid() and not request.REQUEST.get('duplicates_ok'):
        cd = form.cleaned_data
        params = dict(
            product__place__cemetery = cd["cemetery"],
            person__birth_date = cd["birth_date"],
            person__death_date = cd["death_date"],
            date_fact = cd["burial_date"],
        )
        if cd["last_name"].lower() != UNKNOWN_NAME.lower():
            params['person__last_name__iexact'] = cd["last_name"]
        duplicates = Burial.objects.filter(**params)

    duplicates_ok = not duplicates or request.REQUEST.get('duplicates_ok')

    if request.method == "POST" and forms_valid and responsible_valid and duplicates_ok:
        cd = form.cleaned_data
        # Try to get Place.
        try:
            place = Place.objects.get(cemetery=cd["cemetery"], area=cd["area"], row=cd["row"], seat=cd["seat"])
            place.rooms = cd["rooms"]
            place.rooms_free = cd["rooms_free"]
            place.save()
        except ObjectDoesNotExist:
            # Create new Place.
            place = Place(creator=request.user.userprofile.soul)
            place.cemetery = cd["cemetery"]
            place.area = cd["area"]
            place.row = cd["row"]
            place.seat = cd["seat"]
            place.rooms = cd["rooms"]
            place.rooms_free = cd["rooms_free"]
            place.soul = cd["cemetery"].organization.soul_ptr
            place.name = u"%s.уч%sряд%sместо%s" % (place.cemetery.name, place.area, place.row, place.seat)
            place.p_type = ProductType.objects.get(uuid=settings.PLACE_PRODUCTTYPE_ID)
            place.save()
        # Create new Person for dead man.
        new_person = Person(creator=request.user.userprofile.soul)
        new_person.last_name = cd["last_name"].capitalize()
        new_person.first_name = cd["first_name"].capitalize()
        new_person.patronymic = cd["patronymic"].capitalize()

        new_person.birth_date = cd.get("birth_date")
        new_person.birth_date_no_month = new_person.birth_date and form.fields['birth_date'].widget.no_month or False
        new_person.birth_date_no_day = new_person.birth_date and form.fields['birth_date'].widget.no_day or False

        new_person.death_date = cd.get("death_date") or None
        new_person.save()

        # Create new Person for customer.
        customer = Person(creator=request.user.userprofile.soul)
        customer.last_name = cd["customer_last_name"].capitalize()
        if cd.get("customer_first_name", ""):
            customer.first_name = cd["customer_first_name"].capitalize()
        if cd.get("customer_patronymic", ""):
            customer.patronymic = cd["customer_patronymic"].capitalize()

        customer.location = location_form.is_valid() and location_form.save() or None
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

        new_burial.exhumated_date = cd.get("exhumated_date")
        new_burial.account_book_n = cd["account_book_n"]
        new_burial.customer = customer.soul_ptr
        new_burial.responsible = cd["cemetery"].organization.soul_ptr  #ставить орг-ию кладбища
        new_burial.doer = request.user.userprofile.soul
        new_burial.operation = cd["operation"]

        new_burial.person.location = registration_form.save()
        new_burial.person.save()


        if request.REQUEST.get('responsible_myself'):
            new_burial.responsible_customer = new_burial.customer
        else:
            new_burial.responsible_customer = Person.objects.create(
                creator=request.user.userprofile.soul,
                last_name=cd["responsible_last_name"].capitalize(),
                first_name=cd.get("responsible_first_name", "").capitalize(),
                patronymic=cd.get("responsible_patronymic", "").capitalize(),
                location = responsible_form.is_valid() and responsible_form.save() or None,
            )

        if not request.REQUEST.get('opf') == 'fizik':
            agent = cd['agent']
            if agent:
                new_burial.doverennost, created = agent.doverennosti.get_or_create(
                    number = cd['dover_number'],
                    date = cd['dover_date'],
                    expire = cd['dover_expire'],
                )

            new_burial.responsible_agent = agent
            new_burial.organization = cd['organization']

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
            if cd.get("file1_comment", ""):
                of.comment = cd["file1_comment"]
            of.ofile.save(unicode(nfile.name).encode('utf-8'), nfile, save=True)

        if cert_form.cleaned_data.get('zags'):
            ds = cert_form.save(commit=False)
            ds.soul_id=new_burial.person.pk
            ds.save()

        LogEntry.objects.log_action(
            user_id = request.user.pk,
            content_type_id = ContentType.objects.get_for_model(new_burial).pk,
            object_id = new_burial.pk,
            object_repr = u'%s' % new_burial,
            action_flag = ADDITION,
        )

        if request.POST.get('and_print'):
            return redirect("print_burial", new_burial.pk)
        return redirect(".")

    today = datetime.date.today()
    burials = Burial.objects.filter(is_trash=False, creator=request.user.userprofile.soul).order_by('-date_of_creation')[:15]
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
        'customer_addr_valid': customer_addr_valid,
        'registration_valid': registration_valid,
        'additional_burial': request.GET.get('burial'),
    })

@login_required
@is_in_group("edit_burial")
@transaction.commit_on_success
def separate_burial(request, uuid):
    one = get_object_or_404(Burial, uuid=uuid)
    other = one.relative_burials()
    params = {
        'one': one,
        'other': other,
    }
    if not list(other):
        return redirect('edit_burial', [uuid, ])

    if one.product.place.seat != one.account_book_n:
        params.update({
            'separate': 'one',
            'seat_number': one.generate_seat_number(),
        })
        if request.POST:
            old_place = one.product.place
            new_place = Place.objects.create(
                soul = old_place.soul,
                name = old_place.name,
                measure = old_place.measure,
                p_type = old_place.p_type,
                cemetery = old_place.cemetery,
                area = old_place.area,
                row = old_place.row,
                seat = one.generate_seat_number(),
                rooms = max(old_place.rooms - 1, 1),
                rooms_free = old_place.rooms_free,
                creator = old_place.creator or request.user.userprofile.soul,
            )

            one.product = new_place
            one.save()
    else:
        params.update({
            'separate': 'other',
            'seat_number': min([b.account_book_n for b in other]),
        })
        if request.POST:
            old_place = one.product.place
            new_place = Place.objects.create(
                soul = old_place.soul,
                name = old_place.name,
                measure = old_place.measure,
                p_type = old_place.p_type,
                cemetery = old_place.cemetery,
                area = old_place.area,
                row = old_place.row,
                seat = one.generate_seat_number(),
                rooms = max(old_place.rooms - 1, 1),
                rooms_free = old_place.rooms_free,
                creator = old_place.creator or request.user.userprofile.soul,
            )

            for i, o in enumerate(other):
                o.product = new_place
                o.save()

                if i == 0:
                    o.operation = Operation.objects.get(op_type=u'Захоронение')
                    o.save()

    if request.POST:
        return redirect('edit_burial', uuid)
    return direct_to_template(request, 'burial_separate.html', params)


@login_required
@is_in_group("edit_burial")
@transaction.commit_on_success
def edit_burial(request, uuid):
    """
    Страница редактирования существующего захоронения.
    """
    burial = get_object_or_404(Burial, uuid=uuid)

    if request.REQUEST.get('delete_ordercomment'):
        burial.ordercomments_set.filter(uuid=request.REQUEST.get('delete_ordercomment')).delete()
        return HttpResponseRedirect('.')

    if request.REQUEST.get('delete_orderfile'):
        burial.orderfiles_set.filter(uuid=request.REQUEST.get('delete_orderfile')).delete()
        return HttpResponseRedirect('.')

    if request.REQUEST.get('delete'):
        burial.is_trash = True
        burial.save()
        return HttpResponseRedirect(reverse("main_page") + '?close=1')

    if request.REQUEST.get('undelete'):
        burial.is_trash = False
        burial.save()
        return HttpResponseRedirect(reverse("main_page") + '?close=1')

    PhoneFormSet = modelformset_factory(Phone, form=PhoneForm, extra=3)

    cem = burial.product.place.cemetery
    oper = burial.operation

    initial = {
        'account_book_n': burial.account_book_n,
        'burial_date': burial.date_fact and burial.date_fact.strftime('%d.%m.%Y'),
        'burial_time': burial.date_fact and burial.date_fact.strftime('%H:%M'),
        'birth_date': burial.person.unclear_birth_date,
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
        'rooms': burial.product.place.rooms or 1,
        'rooms_free': burial.product.place.rooms_free or 0,
        'family_burial': burial.product.place.count_burials() > 1,
        'customer_last_name': burial.customer.person.last_name,
        'customer_first_name': burial.customer.person.first_name,
        'customer_patronymic': burial.customer.person.patronymic,

        'responsible_last_name': burial.responsible_customer and burial.responsible_customer.person.last_name,
        'responsible_first_name': burial.responsible_customer and burial.responsible_customer.person.first_name,
        'responsible_patronymic': burial.responsible_customer and burial.responsible_customer.person.patronymic,
        'responsible_myself': burial.responsible_customer == burial.customer and not burial.responsible_agent,

        'opf': burial.organization and 'yurik' or 'fizik',
        'organization': burial.responsible_agent and burial.responsible_agent.organization or burial.organization,
        'agent': burial.responsible_agent,
        'agent_director': burial.organization and not burial.responsible_agent,
        'dover_number': burial.doverennost and burial.doverennost.number or '',
        'dover_date': burial.doverennost and burial.doverennost.date or '',
        'dover_expire': burial.doverennost and burial.doverennost.expire or '',
    }
    form = JournalForm(cem=cem, oper=oper, data=request.POST or None, files=request.FILES or None, initial=initial, instance=burial)
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
    id_form = IDForm(prefix='id', data=request.POST or None, instance=id, initial={'who': id and id.source})

    burial.customer.phone_set.filter(f_number='').delete()
    burial.customer.phone_set.filter(f_number__isnull=True).delete()
    phoneset = PhoneFormSet(prefix='phones', data=request.POST or None, queryset=burial.customer.phone_set.all())

    id_valid = request.POST.get('opf') != 'fizik' or id_form.is_valid()
    customer_addr_valid = request.POST.get('opf') != 'fizik' or \
                          request.POST.get('customer_last_name') in [None, '', UNKNOWN_NAME] or \
                          location_form.is_valid()
    registration_valid = not registration_form['country'].data or registration_form.is_valid()
    
    forms_valid = form.is_valid() and customer_addr_valid and registration_valid and cert_form.is_valid() and id_valid
    responsible_valid = request.POST.get('responsible_myself') or \
                        request.POST.get('responsible_last_name') in [None, '', UNKNOWN_NAME] or \
                        responsible_form.is_valid()

    everything_valid = request.method == "POST" and forms_valid and responsible_valid
    if everything_valid:
        cd = form.cleaned_data

        if request.POST.get('split_burial'):
            place = Place(creator=request.user.userprofile.soul)
            place.rooms = 1
            place.rooms_free = 0

            place.cemetery = cd["cemetery"]
            place.area = cd["area"]
            place.row = cd["row"]
            place.seat = ''

            place.soul = cd["cemetery"].organization.soul_ptr
            place.name = u"%s.уч%sряд%sместо%s" % (place.cemetery.name, place.area, place.row, place.seat)
            place.p_type = ProductType.objects.get(uuid=settings.PLACE_PRODUCTTYPE_ID)

            place.save()

            if cd['seat'] != cd['account_book_n']:
                # отделяем текущее от остальных
                burial.product.place.rooms -= 1
                burial.product.place.save()

                place.seat = burial.account_book_n
            else:
                # переносим остальные
                others = Burial.objects.filter(product__place__seat=cd['seat']).exclude(pk=burial.pk)
                if others:
                    seat = min(*others.values_list('account_book_n', flat=True))
                    o = others[0]
                    o.product.place.seat = seat
                    o.product.place.rooms -= 1
                    o.product.place.save()

            burial.product = place.product_ptr
            burial.save()

            if not burial.product.place.seat:
                burial.product.place.generate_seat()

            burial.product.place.save()

        else:
            place = burial.product.place

            place.rooms = cd["rooms"] or 1
            place.rooms_free = cd["rooms_free"] or 0

            place.cemetery = cd["cemetery"]
            place.area = cd["area"]
            place.row = cd["row"]
            place.seat = cd["seat"]

            place.soul = cd["cemetery"].organization.soul_ptr
            place.name = u"%s.уч%sряд%sместо%s" % (place.cemetery.name, place.area, place.row, place.seat)
            place.save()

        # Create new Person for dead man.
        new_person = burial.person
        new_person.last_name = cd["last_name"].capitalize()
        new_person.first_name = cd["first_name"].capitalize()
        new_person.patronymic = cd["patronymic"].capitalize()

        new_person.birth_date = cd.get("birth_date")
        new_person.birth_date_no_month = new_person.birth_date and form.fields['birth_date'].widget.no_month or False
        new_person.birth_date_no_day = new_person.birth_date and form.fields['birth_date'].widget.no_day or False

        new_person.death_date = cd.get("death_date") or None
        new_person.save()

        # Create new Person for customer.
        customer = burial.customer.person
        customer.last_name = cd["customer_last_name"].capitalize()
        if cd.get("customer_first_name", ""):
            customer.first_name = cd["customer_first_name"].capitalize()
        if cd.get("customer_patronymic", ""):
            customer.patronymic = cd["customer_patronymic"].capitalize()

        customer.location = location_form.is_valid() and location_form.save() or None
        customer.save()

        if id_form.is_valid():
            id = id_form.save(commit=False)
            id.person = customer
            id.save()

        # Customer phone
        for pf in phoneset.forms:
            if pf.is_valid() and pf.cleaned_data.get('f_number'):
                phone = pf.save(commit=False)
                phone.soul = customer.soul_ptr
                phone.save()
            elif pf.instance:
                pf.instance.delete()

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

        if request.POST.get('responsible_myself'):
            new_burial.responsible_customer = new_burial.customer
        else:
            if cd["responsible_last_name"].strip() != UNKNOWN_NAME:
                new_burial.responsible_customer = Person.objects.create(
                    creator=request.user.userprofile.soul,
                    last_name=cd["responsible_last_name"].capitalize(),
                    first_name=cd.get("responsible_first_name", "").capitalize(),
                    patronymic=cd.get("responsible_patronymic", "").capitalize(),
                    location = responsible_form.is_valid() and responsible_form.save() or None,
                )

        if new_burial.responsible_customer:
            new_burial.relative_burials().update(responsible_customer=new_burial.responsible_customer)

        if not request.REQUEST.get('opf') == 'fizik':
            agent = cd['agent']
            if agent:
                new_burial.doverennost, created = agent.doverennosti.get_or_create(
                    number = cd['dover_number'],
                    date = cd['dover_date'],
                    expire = cd['dover_expire'],
                )

            new_burial.responsible_agent = agent
            new_burial.organization = cd['organization']
        else:
            new_burial.responsible_agent = None
            new_burial.organization = None



        new_burial.save()

        new_burial.person.location = registration_form.save()
        new_burial.person.save()

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

        if cert_form.cleaned_data.get('zags'):
            ds = cert_form.save(commit=False)
            ds.soul_id = new_burial.person.pk
            ds.save()

        LogEntry.objects.log_action(
            user_id = request.user.pk,
            content_type_id = ContentType.objects.get_for_model(new_burial).pk,
            object_id = new_burial.pk,
            object_repr = u'%s' % new_burial,
            action_flag = CHANGE,
        )

        return HttpResponseRedirect(reverse("edit_burial", args=[new_burial.pk, ]) + '?close=1')

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
        'close': request.GET.get('close'),
    })


def get_positions(burial):
    positions = []
    for product in OrderProduct.objects.all().order_by('ordering', 'name'):
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
    initials = burial.get_print_info()

    def is_same(i, p):
        i1 = isinstance(i['order_product'], OrderProduct) and i['order_product'].name or i['order_product']
        p1 = isinstance(p['order_product'], OrderProduct) and p['order_product'].name or p['order_product']
        return i1 == p1

    if initials and initials.setdefault('positions', []):
        for p in positions:
            if not any(filter(lambda i: is_same(i, p), initials['positions'])):
                initials['positions'].append(p)

    payment_form = OrderPaymentForm(instance=burial, data=request.POST or None)
    positions_fs = OrderPositionsFormset(initial=initials.get('positions') or positions, data=request.POST or None)
    print_form = PrintOptionsForm(data=request.POST or None, initial=initials['print'], burial=burial)
    try:
        env = Env.objects.get()
        org = Organization.objects.get(uuid=env.uuid)
    except (Env.DoesNotExist, Organization.DoesNotExist):
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
                    pos = OrderPosition.objects.get(order_product=f.initial['order_product'], order=burial)
                except OrderPosition.DoesNotExist:
                    pos = OrderPosition.objects.create(
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
                    pos = OrderPosition.objects.get(order_product=f.initial['order_product'], order=burial)
                except OrderPosition.DoesNotExist:
                    pass
                else:
                    pos.delete()

        transaction.commit()

        payment_form.save()

        positions = get_positions(burial)
        positions = filter(lambda p: p['order_product'].pk in print_positions, positions)

        try:
            burial_creator = u'%s' % burial.creator.person
        except Exception:
            try:
                u = burial.creator.userprofile.user
                burial_creator = (u'%s %s' % (u.last_name, u.first_name)).strip()
            except Exception, e:
                burial_creator = u''

        try:
            current_user = u'%s' % request.user.userprofile.soul.person
        except Exception:
            try:
                u = request.user
                current_user = (u'%s %s' % (u.last_name, u.first_name)).strip()
            except Exception, e:
                current_user = u''

        spaces = mark_safe('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')

        if print_form.cleaned_data.get('receipt'):
            return direct_to_template(request, 'reports/spravka.html', {
                'burial': burial,
                'current_user': current_user or spaces,
                'now': datetime.datetime.now(),
                'org': org,
            })

        if print_form.cleaned_data.get('dogovor'):

            return direct_to_template(request, 'reports/dogovor.html', {
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
            return direct_to_template(request, 'reports/act.html', {
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

    return direct_to_template(request, 'burial_print.html', {
        'burial': burial,
        'positions_fs': positions_fs,
        'payment_form': payment_form,
        'print_form': print_form,
        'time_check_failed': time_check_failed,
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
    if hasattr(request.user, "userprofile"):
        up = request.user.userprofile
    else:
        # this case could not happen - we creating profile with user creation!
        soul = Soul(creator=request.user.userprofile.soul)
        soul.save()
        up = UserProfile(user=request.user, soul=soul)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=up)
        if form.is_valid():
            form.save()
            return redirect("/profile/")
    else:
        form = UserProfileForm(instance=up)
    return direct_to_template(request, 'profile2.html', {"form": form})



@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def management(request):
    """
    Общая страница выбора вариантов управления.
    """
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
            user.is_staff = True
            user.save()
            return redirect("/management/user/")
    else:
        form = NewUserForm()
    users = User.objects.all().order_by('last_name')
#    users = PersonRole.objects.all().order_by('person__last_name', 'person__first_name')
    return direct_to_template(request, 'management_user.html',
                              {'form': form, "users": users})


@user_passes_test(lambda u: u.is_superuser)
@transaction.commit_on_success
def management_edit_user(request, uuid):
    """
    Редактирование данных исполнителя.
    """
    person = get_object_or_404(Person, uuid=uuid)
    user = person.userprofile.user
    PhoneFormSet = modelformset_factory(Phone, exclude=("soul",), extra=3)
    if request.method == "POST":
        phoneset = PhoneFormSet(request.POST, request.FILES, queryset=Phone.objects.filter(soul=person.soul_ptr))
        form = EditUserForm(data=request.POST, instance=user)
        if phoneset.is_valid() and form.is_valid():
            form.save()
            for phone in phoneset.save(commit=False):
                phone.soul = person.soul_ptr
                phone.save()
            return redirect('/management/user/')
    else:
        phoneset = PhoneFormSet(queryset=Phone.objects.filter(soul=person.soul_ptr))
        form = EditUserForm(instance=user)
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
            if location_city and location_region and location_country:
                # Есть все для создания непустого Location.
                # Страна.
                try:
                    country = GeoCountry.objects.get(name__exact=location_country)
                except ObjectDoesNotExist:
                    country = GeoCountry(name=location_country.capitalize())
                    country.save()
                location.country = country
                # Регион.
                try:
                    region = GeoRegion.objects.get(name__exact=location_region,
                                                   country=country)
                except ObjectDoesNotExist:
                    region = GeoRegion(name=location_region.capitalize(), country=country)
                    region.save()
                location.region = region
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(name__exact=location_city, region=region)
                except ObjectDoesNotExist:
                    city = GeoCity(name=location_city.capitalize(), country=country,
                                   region=region)
                    city.save()
                location.city = city
                if location_street:
                    # Улица.
                    try:
                        street = Street.objects.get(name__exact=location_street, city=city)
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
            location.info = cd.get('info') or ''
            location.save()
            return redirect("/management/cemetery/")
    else:
        try:
            env = Env.objects.get()
            organization = Organization.objects.get(uuid=env.uuid)
        except:
            organization = None
            env = None
        form = CemeteryForm(initial={'organization': organization})
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
    initial_data = {
        "organization": cemetery.organization,
        "name": cemetery.name,
        "info": cemetery.location.info,
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
    if request.method == "POST":
        form = CemeteryForm(request.POST, initial=initial_data)
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

            """
            # Очищаем Location.
            location.street = None
            location.house = ""
            location.block = ""
            location.building = ""
            location.flat = ""
#            location.save()
            """
            if location_city and location_region and location_country:
                # Есть все для создания непустого Location.
                # Страна.
                try:
                    country = GeoCountry.objects.get(name__exact=location_country)
                except ObjectDoesNotExist:
                    country = GeoCountry(name=location_country.capitalize())
                    country.save()
                location.country = country
                # Регион.
                try:
                    region = GeoRegion.objects.get(name__exact=location_region,
                                                   country=country)
                except ObjectDoesNotExist:
                    region = GeoRegion(name=location_region.capitalize(), country=country)
                    region.save()
                location.region = region
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(name__exact=location_city, region=region)
                except ObjectDoesNotExist:
                    city = GeoCity(name=location_city.capitalize(), country=country,
                                   region=region)
                    city.save()
                location.city = city
            if location_street:
                # Улица.
                try:
                    street = Street.objects.get(name__exact=location_street, city=city)
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
            location.info = cd.get('info') or ''
            location.save()
            return redirect('/management/cemetery/')
    else:
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
        bank_formset = InitBankFormset(instance=None, data=request.POST or None)
    else:
        organization.bankaccount_set.filter(rs='').delete()
        organization.bankaccount_set.filter(rs__isnull=True).delete()
        bank_formset = InitBankFormset(instance=organization, data=request.POST or None)

    if request.method == "POST":
        form = InitalForm(request.POST)
        if form.is_valid() and bank_formset.is_valid():
            cd = form.cleaned_data
            # Создаем уникальный uuid сервера.
            env = env or Env.objects.create()

            # Создаем организацию.
            if not organization:
                organization = Organization(
                    creator=request.user.userprofile.soul,
                )
            organization.name = cd["org_name"]
            organization.full_name = cd["org_full_name"]
            organization.kpp = cd["kpp"]
            organization.inn = cd["inn"]
            organization.ogrn = cd["ogrn"]
            organization.ceo_name = cd["ceo_name"]
            organization.ceo_name_who = cd["ceo_name_who"]
            organization.ceo_document = cd["ceo_document"]
            organization.save()

            bank_formset = InitBankFormset(instance=organization, data=request.POST or None)
            for i,f in enumerate(bank_formset.forms):
                if f.instance and f.instance.pk and f.data.get('bankaccount_set-%s-DELETE' % i):
                    f.instance.delete()
                elif f.is_valid():
                    f.save()


            # Создаем объект Phone для организации.
            org_phone = cd.get("org_phone", "")
            if org_phone:
                org_phone_obj, created = Phone.objects.get_or_create(soul=organization.soul_ptr)
                org_phone_obj.f_number = org_phone
                org_phone_obj.save()
            else:
                Phone.objects.filter(soul=organization.soul_ptr).delete()
            # Создаем объекты SoulProducttypeOperation.
            operations = Operation.objects.all()
            p_type = ProductType.objects.get(uuid=settings.PLACE_PRODUCTTYPE_ID)
            for op in operations:
                spo = SoulProducttypeOperation.objects.get_or_create(
                    soul = organization.soul_ptr,
                    p_type = p_type,
                    operation = op,
                )
            # Создаем Location для организации.
            org_location = organization.location or Location()
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
                    country = GeoCountry.objects.get(name__exact=org_location_country)
                except ObjectDoesNotExist:
                    country = GeoCountry(name=org_location_country.capitalize())
                    country.save()
                # Регион.
                try:
                    region = GeoRegion.objects.get(name__exact=org_location_region,
                                                   country=country)
                except ObjectDoesNotExist:
                    region = GeoRegion(name=org_location_region.capitalize(), country=country)
                    region.save()
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(name__exact=org_location_city, region=region)
                except ObjectDoesNotExist:
                    city = GeoCity(name=org_location_city.capitalize(), country=country,
                                   region=region)
                    city.save()
                # Улица.
                try:
                    street = Street.objects.get(name__exact=org_location_street, city=city)
                except ObjectDoesNotExist:
                    street = Street(name=org_location_street.capitalize(), city=city)
                    street.save()
                # Продолжаем с Location.
                org_location.street = street
                org_location.country = country
                org_location.region = region
                org_location.city = city

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
            org_location.info = cd.get('info') or ''
            org_location.save()
            organization.location = org_location
            organization.save()

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
            initial = dict(
                org_name = org.name,
                org_full_name = org.full_name,
                org_phone = phones and phones[0] or None,
                ceo_name = org.ceo_name,
                ceo_name_who = org.ceo_name_who,
                ceo_document = org.ceo_document,
                post_index = org.location.post_index,
                new_street = False,
                new_city = False,
                new_region = False,
                new_country = False,
                house = org.location.house,
                block = org.location.block,
                building = org.location.building,
                info = org.location.info,
                flat = org.location.flat,
                kpp = org.kpp,
                inn = org.inn,
                ogrn = org.ogrn,
            )
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
                            cust_ln = UNKNOWN_NAME  # Если в базе был Null
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
                            city = UNKNOWN_NAME  # Если в базе был Null.
                        else:
                            city = city.decode(settings.CSV_ENCODING).strip().capitalize()
                        if not city:
                            city = UNKNOWN_NAME  # Если в базе была пустая строка.
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
                            cities = GeoCity.objects.filter(name__exact=city)
                            if cities:
                                cust_city = cities[0]
                            else:
                                cust_city = GeoCity()
                                cust_city.country = GeoCountry.objects.get(name__exact=UNKNOWN_NAME)
                                cust_city.region = GeoRegion.objects.get(name__exact=UNKNOWN_NAME)
                                cust_city.name = city
                                cust_city.save()
                            try:
                                cust_street = Street.objects.get(city=cust_city, name__exact=street)
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
                            place = Place.objects.get(cemetery=cemetery, area__exact=area, row__exact=row, seat__exact=seat)
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


@login_required
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


@login_required
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


@login_required
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
                              p_type=settings.PLACE_PRODUCTTYPE_ID)
            if request.GET.get('parent'):
                choices = choices.exclude(operation__op_type=u'Захоронение')

            for c in choices.values_list("operation__uuid", "operation__op_type"):
                rez.append({"optionValue": c[0], "optionDisplay": c[1]})
            rez.insert(0, {"optionValue": 0, "optionDisplay": u'---------'})
    return HttpResponse(JSONEncoder().encode(rez))

@login_required
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

@login_required
def get_dover(request):
    try:
        dover = Doverennost.objects.exclude(expire__isnull=True).exclude(expire__lt=datetime.datetime.now())
        current = dover.filter(agent__pk=request.GET.get('agent')).order_by('-number')[0]
    except IndexError:
        rez = {}
    else:
        rez = {
            'number': current.number,
            'date': current.date and current.date.strftime('%d.%m.%Y') or '',
            'expire': current.expire and current.expire.strftime('%d.%m.%Y') or '',
        }
    return HttpResponse(JSONEncoder().encode(rez))

@login_required
def get_passport_sources(request):
    docs = DocumentSource.objects.all()
    q = request.GET.get('term', None)
    if q:
        docs = docs.filter(name__istartswith=q)
    return HttpResponse(simplejson.dumps(list(docs.values_list('name', flat=True))))

@login_required
def get_street(request):
    """
    Получение улицы с городом, регионом и страной.
    """
    streets = []
    q = request.GET.get('term', None)
    if q is not None:
        kwargs = dict(name__istartswith=q)
        if request.GET.get('country'):
            kwargs['city__region__country__name__iexact'] = request.GET['country']
        if request.GET.get('region'):
            kwargs['city__region__name__iexact'] = request.GET['region']
        if request.GET.get('city'):
            kwargs['city__name__iexact'] = request.GET['city']
        rezult = Street.objects.filter(**kwargs).order_by("name", "city__name", "city__region__name",
                                                                     "city__region__country__name")[:24]
        for s in rezult:
            streets.append(u"%s/%s/%s/%s" % (s.name, s.city.name, s.city.region.name, s.city.region.country.name))
    return HttpResponse(JSONEncoder().encode(streets))


@login_required
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


@login_required
def get_cities(request):
    """
    Получение списка нас. пунктов с пом. AJAX-запроса.
    """
    cities = []
    q = request.GET.get('term', None)
    if q is not None:
        kwargs = dict(name__istartswith=q)
        if request.GET.get('country'):
            kwargs['region__country__name__iexact'] = request.GET['country']
        if request.GET.get('region'):
            kwargs['region__name__iexact'] = request.GET['region']
        rezult = GeoCity.objects.filter(**kwargs).order_by("name", "region__name", "region__country__name")[:24]
        for s in rezult:
            cities.append(u"%s/%s/%s" % (s.name, s.region.name, s.region.country.name))
    return HttpResponse(JSONEncoder().encode(cities))


@login_required
def get_regions(request):
    """
    Получение списка регионов с пом. AJAX-запроса.
    """
    regions = []
    q = request.GET.get('term', None)
    if q is not None:
        kwargs = dict(name__istartswith=q)
        if request.GET.get('country'):
            kwargs['country__name__iexact'] = request.GET['country']
        rezult = GeoRegion.objects.filter(**kwargs).order_by("name", "country__name")[:24]
        for s in rezult:
            regions.append(u"%s/%s" % (s.name, s.country.name))
    return HttpResponse(JSONEncoder().encode(regions))

