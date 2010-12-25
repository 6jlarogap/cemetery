# -*- coding: utf-8 -*-

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.db import transaction
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
#from django.utils import simplejson
from django.utils.simplejson.encoder import JSONEncoder
from forms import SearchForm, NewUserForm, EditUserForm, ImportForm
from forms import CemeteryForm, JournalForm, EditOrderForm
from django.forms.models import modelformset_factory, formset_factory, inlineformset_factory
from models import Soul, Person, PersonRole, UserProfile, Burial, Burial1
from models import Cemetery, GeoCountry, GeoRegion, GeoCity, Street, Location, Operation
from models import OrderFiles, Phone, Place, ProductType, SoulProducttypeOperation

from simplepagination import paginate
from annoying.decorators import render_to

import re
import datetime
import csv
from common.forms import UserProfileForm


#MAIN_ORGANIZATION = Organization.objects.get(main=True)
csv.register_dialect("4mysql", escapechar="\\", quoting=csv.QUOTE_NONE)

def is_in_group(group_name):
    """
    Декоратор для проверки на то, что пользователь является членом указанной группы.
    """
    def _dec(f):
        def _check_group(request, *args, **kwargs):
            try:
                group = request.user.groups.get(name=group_name)
            except ObjectDoesNotExist:
                return HttpResponseForbidden("Forbidden")
            else:
                return f(request, *args, **kwargs)
        return _check_group
    return _dec


@render_to()
#@paginate(style='digg', per_page=1)
@paginate(style='digg')
def main_page(request):
    """
    Главная страница.
    """
    form_data = request.GET or None
    form = SearchForm(form_data)
    burials = Burial1.objects.filter(is_trash=False).order_by("person__last_name",
                                                              "person__first_name",
                                                              "person__patronymic")
    #if request.method == "GET":
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
            # Сохраняем в профиль значение records_order_by.
            if cd.get("records_order_by", ""):
                if request.user.userprofile.records_order_by != cd["records_order_by"]:
                    request.user.userprofile.records_order_by = cd["records_order_by"]
                    request.user.userprofile.save()
        if cd.get("records_order_by", ""):
            if cd["records_order_by"] == u'account_book_n':
                burials = burials.order_by('s1', 's2', 's3')
            elif cd["records_order_by"] == u'-account_book_n':
                burials = burials.order_by('-s1', '-s2', '-s3')
            elif cd["records_order_by"] == u'product__place__area':
                burials = burials.order_by('product__place1__s1', 'product__place1__s2',
                                           'product__place1__s3')
            elif cd["records_order_by"] == u'-product__place__area':
                burials = burials.order_by('-product__place1__s1', '-product__place1__s2',
                                           '-product__place1__s3')
            elif cd["records_order_by"] == u'product__place__row':
                burials = burials.order_by('product__place1__s4', 'product__place1__s5',
                                           'product__place1__s6')
            elif cd["records_order_by"] == u'-product__place__row':
                burials = burials.order_by('-product__place1__s4', '-product__place1__s5',
                                           '-product__place1__s6')
            elif cd["records_order_by"] == u'product__place__seat':
                burials = burials.order_by('product__place1__s7', 'product__place1__s8',
                                           'product__place1__s9')
            elif cd["records_order_by"] == u'-product__place__seat':
                burials = burials.order_by('-product__place1__s7', '-product__place1__s8',
                                           '-product__place1__s9')
            else:
                burials = burials.order_by(cd["records_order_by"])
#        if cd.get("last_name", ""):
#            regex = re.sub(r'\?', r'.', cd["last_name"])
#            regex = re.sub(r'\*', r'.*', regex)
#            if not (regex.startswith("?") or regex.startswith("*")):
#                regex = u"^%s" % regex
#            if not (regex.endswith("?") or regex.endswith("*")):
#                regex = u"%s$" % regex
#            burials = burials.filter(person__last_name__iregex=regex)
#        if cd["first_name"]:
#            regex = re.sub(r'\?', r'.', cd["first_name"])
#            regex = re.sub(r'\*', r'.*', regex)
#            if not (regex.startswith("?") or regex.startswith("*")):
#                regex = u"^%s" % regex
#            if not (regex.endswith("?") or regex.endswith("*")):
#                regex = u"%s$" % regex
#            burials = burials.filter(person__first_name__iregex=regex)
#        if cd["patronymic"]:
#            regex = re.sub(r'\?', r'.', cd["patronymic"])
#            regex = re.sub(r'\*', r'.*', regex)
#            if not (regex.startswith("?") or regex.startswith("*")):
#                regex = u"^%s" % regex
#            if not (regex.endswith("?") or regex.endswith("*")):
#                regex = u"%s$" % regex
#            burials = burials.filter(person__patronymic__iregex=regex)
        if cd.get("fio", ""):
            text = re.sub(r"\.", " ", cd["fio"])
            parts = text.split()
            fname = ""
            patr = ""
            lname = parts[0].strip(",")
            if len(parts) > 1:
                fname = parts[1].strip(",")
#                if not fname[-1].isalpha():
#                    fname = "%s*" % fname
            if len(parts) > 2:
                patr = parts[2].strip(",")
            regex = re.sub(r'\?', r'.', lname)
            regex = re.sub(r'\*', r'.*', regex)
            if not (regex.startswith("?") or regex.startswith("*")):
                regex = u"^%s" % regex
            if not (regex.endswith("?") or regex.endswith("*")):
                regex = u"%s$" % regex
            burials = burials.filter(person__last_name__iregex=regex)
            if fname:
                regex = re.sub(r'\?', r'.', fname)
                regex = re.sub(r'\*', r'.*', regex)
                if not (regex.startswith("?") or regex.startswith("*")):
                    regex = u"^%s" % regex
#                if not (regex.endswith("?") or regex.endswith("*")):
#                    regex = u"%s$" % regex
                burials = burials.filter(person__first_name__iregex=regex)
            if patr:
                regex = re.sub(r'\?', r'.', patr)
                regex = re.sub(r'\*', r'.*', regex)
                if not (regex.startswith("?") or regex.startswith("*")):
                    regex = u"^%s" % regex
#                if not (regex.endswith("?") or regex.endswith("*")):
#                    regex = u"%s$" % regex
                burials = burials.filter(person__patronymic__iregex=regex)

        if cd["cemetery"]:
            burials = burials.filter(product__place__cemetery=cd["cemetery"])
        if cd["birth_date_from"]:
            burials = burials.filter(person__birth_date__gte=cd["birth_date_from"])
        if cd["birth_date_to"]:
            burials = burials.filter(person__birth_date__lte=cd["birth_date_to"])
        if cd["death_date_from"]:
            burials = burials.filter(person__birth_date__gte=cd["death_date_from"])
        if cd["death_date_to"]:
            burials = burials.filter(person__birth_date__lte=cd["death_date_to"])
        if cd["burial_date_from"]:
            burials = burials.filter(date_fact__gte=cd["burial_date_from"])
        if cd["burial_date_to"]:
            burials = burials.filter(date_fact__lte=cd["burial_date_to"])
        if cd["death_certificate"]:
            burials = burials.filter(person__soul_ptr__deathcertificate__s_number=cd["death_certificate"])
        if cd["account_book_n"]:
            burials = burials.filter(account_book_n=cd["account_book_n"])
        if cd["customer"]:
            regex = re.sub(r'\?', r'.', cd["customer"])
            regex = re.sub(r'\*', r'.*', regex)
            if not (regex.startswith("?") or regex.startswith("*")):
                regex = u"^%s" % regex
            if not (regex.endswith("?") or regex.endswith("*")):
                regex = u"%s$" % regex
            burials = burials.filter(customer__person__last_name__iregex=regex)
        if cd["owner"]:
            burials = burials.filter(creator=cd["owner"])
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
            regex = re.sub(r'\?', r'.', cd["comment"])
            regex = re.sub(r'\*', r'.*', regex)
            if not (regex.startswith("?") or regex.startswith("*")):
                regex = u"^%s" % regex
            if not (regex.endswith("?") or regex.endswith("*")):
                regex = u"%s$" % regex
            burials = burials.filter(all_comments__iregex=regex)
    else:
        #if request.user.is_authenticated() and not request.user.is_superuser and not form_data:
        if request.user.is_authenticated() and not form_data:
            pp = request.user.userprofile.records_per_page
            ob = request.user.userprofile.records_order_by
            redirect_str = "/?print=0"
            if pp:
                redirect_str = "%s&per_page=%d" % (redirect_str, pp)
            if ob:
                redirect_str = "%s&records_order_by=%s" % (redirect_str, ob)
            return redirect(redirect_str)

    to_print = request.GET.get("print", "")
    if to_print == u"1":
        result = {"form": form,
                  "object_list": burials,
                  "obj_nr": len(burials),
                  "TEMPLATE": "burials_print.html",
                  }
    else:
        result = {"form": form,
                  "object_list": burials,
                  "obj_nr": len(burials),
                  "TEMPLATE": "burials.html",
                  }
        #if pp:
            #result["per_page"] = pp
    return result


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
                soul = Soul(creator=request.user)
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
                initial_data["hoperation"] = profile.default_operation.id
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


#@login_required
#@is_in_group("руководство")
#def show_all_users(request):
#    persons = Person.objects.all()
#    return direct_to_template(request, 'show_all_users.html', {"persons": persons})


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





@login_required
#@permission_required('common.change_burial')
@is_in_group("management")
def management(request):
    """
    Общая страница выбора вариантов управления.
    """
    return direct_to_template(request, 'management.html')

#_ok
@login_required
#@permission_required('common.change_burial')
@is_in_group("management_user")
@transaction.commit_on_success
def management_user(request):
    """
    Страница управления пользователями (создание нового, показ существующих).
    """
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            person = Person(last_name=cd['last_name'].capitalize(),
                            creator=request.user)
            if cd.get("first_name", ""):
                person.first_name = cd['first_name'].capitalize()
            if cd.get("patronymic", ""):
                person.patronymic = cd['patronymic'].capitalize()
            password = cd['password1']
            person.save()
            if cd.get('phone', ""):
                phone = Phone(soul=person.soul_ptr, f_number=cd['phone'])
                phone.save()
            person_role = PersonRole(person=person, role=cd['role'],
                                     creator=request.user)
            person_role.save()
            user = User.objects.create_user(username=cd['username'], email="",
                                            password=password)
            user.last_name = cd['last_name'].capitalize()
            if cd.get("first_name", ""):
                user.first_name = cd['first_name'].capitalize()
            profile = UserProfile(user=user, soul=person.soul_ptr)
            profile.save()
            if hasattr(cd['role'], "djgroups") and cd['role'].djgroups.all():
                if cd.get("is_staff", False):
                    user.is_staff = True
                for djgr in cd['role'].djgroups.all():
                    user.groups.add(djgr)  # Добавляем человека в django-группу, связанную с его ролью.
            #if cd['role'].name == u'Руководство':
                #user.is_staff = True
                #user.save()
                #g = Group.objects.get(name=u'руководство')
                #user.groups.add(g)  # Добавляем человека в группу `руководство`.
                #can_change_burial = Permission.objects.get(codename='change_burial')  # To remove.
                #user.user_permissions.add(can_change_burial)
            user.save()
            return redirect("/management/user/")
    else:
        form = NewUserForm()
    users = PersonRole.objects.all().order_by('person__last_name', 'person__first_name')
    return direct_to_template(request, 'management_user.html',
                              {'form': form, "users": users})


#@login_required
#@permission_required('common.change_burial')
#@transaction.commit_on_success
#def management_delete_user(request, uuid):
    #"""
    #Удаление исполнителя.
    #"""
    #try:
        #PersonRole.objects.get(person__uuid=uuid).delete()
        #Person.objects.get(uuid=uuid).delete()
    #except ObjectDoesNotExist:
        #raise Http404
    #else:
        #return redirect('/management/user/')

#_ok
@login_required
@is_in_group("management_edit_user")
@transaction.commit_on_success
def management_edit_user(request, uuid):
    """
    Редактирование данных исполнителя.
    """
    try:
        person = Person.objects.get(uuid=uuid)
    except ObjectDoesNotExist:
        raise Http404
    user = person.userprofile.user
    if request.method == "POST":
        form = EditUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            person.last_name = cd["last_name"].capitalize()
            if cd.get("first_name", ""):
                person.first_name = cd['first_name'].capitalize()
            if cd.get("patronymic", ""):
                person.patronymic = cd['patronymic'].capitalize()
            person.save()
            user.username = cd["username"]
            if cd.get("phone", ""):
                try:
                    phone = Phone.objects.filter(soul=person.soul_ptr)[0]
                except KeyError:
                    phone = Phone(soul=person.soul_ptr)
                phone.f_number = cd["phone"]
                phone.save()
            if cd.get("password1", ""):
                user.set_password(cd['password1'])
            is_staff = cd.get("is_staff", None)
            if is_staff is not None:
                user.is_staff = is_staff
            # Roles processing.
            if cd.get("default_rights", False):
                # Если сбрасываем все права на дефолтные.
                user.groups.clear()
                for r in person.roles.all():
                    for djgr in r.djgroups.all():
                        user.groups.add(djgr)
            # Если оставляем кастомные наборы прав.
            roles = cd["role"]
            groups_to_remove = set()
            groups_to_remain = set()
            # Удаление удаленных ролей исполнителя.
            for r in person.roles.all():
                if r not in roles:
                    # Роль удалена.
                    old_pr = PersonRole.objects.get(person=person, role=r)
                    old_pr.delete()
                    # удаление исполнителя из соответствующих django-групп.
                    for djgr in r.djgroups.all():
                        groups_to_remove.add(djgr)
                else:
                    for djgr in r.djgroups.all():
                        groups_to_remain.add(djgr)
            # Безопасное удаление django-групп.
            safe_gr_to_remove = groups_to_remove - groups_to_remain
            for djgr in safe_gr_to_remove:
                user.groups.remove(djgr)
            # Создание новых ролей исполнителя.
            for r in roles:
                if r not in person.roles.all():
                    # Новая роль.
                    new_pr = PersonRole(creator=request.user, hire_date=datetime.date.today())
                    new_pr.person = person
                    new_pr.role = r
                    new_pr.save()
                    # добавление исполнителя в соответствующие django-группы.
                    for djgr in r.djgroups.all():
                        user.groups.add(djgr)
            user.save()
            return redirect('/management/user/')
    else:
        initial_data = {"last_name": person.last_name,
                        "username": user.username,
                        "is_staff": user.is_staff,
                        }
        phones = Phone.objects.filter(soul=person.soul_ptr)
        if phones:
            initial_data["phone"] = phones[0]
        if person.personrole_set.all():
            prs = PersonRole.objects.filter(person=person)
            roles = []
            for pr in prs:
                roles.append(pr.role)
            initial_data["role"] = roles
        if person.first_name:
            initial_data["first_name"] = person.first_name
        if person.patronymic:
            initial_data["patronymic"] = person.patronymic
        form = EditUserForm(initial=initial_data)
    return direct_to_template(request, 'management_edit_user.html',
                              {'form': form,})


@login_required
#@permission_required('common.change_burial')
@is_in_group("management_cemetery")
@transaction.commit_on_success
def management_cemetery(request):
    """
    Страница управления кладбищами.
    """
    if request.method == "POST":
        form = CemeteryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            city = GeoCity(country=cd["country"], name=cd["city"])
            city.save()
            #if cd.get("street", ""):
            street = Street(city=city, name=cd["street"])
            street.save()
            location = Location(street=street)
            if cd.get("house", ""):
                location.house = cd["house"]
            if cd.get("block", ""):
                location.block = cd["block"]
            if cd.get("building", ""):
                location.building = cd["building"]
            location.save()
            cemetery = Cemetery()
            cemetery.organization = request.user.userprofile.soul.person.roles.all()[0].organization  # To fix!!!
            cemetery.location = location
            cemetery.name = cd["name"]
            cemetery.creator = request.user
            cemetery.save()
            return redirect("/management/cemetery/")
    else:
        form = CemeteryForm()
    cemeteries = Cemetery.objects.all()
#    print cemeteries
    return direct_to_template(request, 'management_add_cemetery.html',
                              {'form': form,
                               "cemeteries": cemeteries})


#@login_required
#@permission_required('common.change_burial')
#@transaction.commit_on_success
#def management_delete_cemetery(request, uuid):
    #"""
    #Удаление кладбища.
    #"""
    #try:
        #cemetery = Cemetery.objects.get(uuid=uuid)
    #except ObjectDoesNotExist:
        #raise Http404
    #else:
        #location = cemetery.location
        #cemetery.delete()
        #location.delete()
        #return redirect('/management/cemetery/')


@login_required
#@permission_required('common.change_burial')
@is_in_group("management_edit_cemetery")
@transaction.commit_on_success
def management_edit_cemetery(request, uuid):
    """
    Редактирование данных кладбища.
    """
    try:
        cemetery = Cemetery.objects.get(uuid=uuid)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == "POST":
        form = CemeteryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            location = cemetery.location
            location.street.name = cd["street"]
            location.street.save()
            location.street.city.name = cd["city"]
            location.street.city.country = cd["country"]
            location.street.city.save()
            if cd.get("house", ""):
                location.house = cd["house"]
            if cd.get("block", ""):
                location.block = cd["block"]
            if cd.get("building", ""):
                location.building = cd["building"]
            location.save()
            cemetery.name = cd["name"]
            cemetery.save()
            return redirect('/management/cemetery/')
    else:
        initial_data = {
            "organization": cemetery.organization,
            "name": cemetery.name,
        }
        if cemetery.location:
            initial_data["country"] = cemetery.location.street.city.country
            initial_data["city"] = cemetery.location.street.city.name
            initial_data["street"] = cemetery.location.street.name
            if cemetery.location.house:
                initial_data["house"] = cemetery.location.house
            if cemetery.location.block:
                initial_data["block"] = cemetery.location.block
            if cemetery.location.building:
                initial_data["building"] = cemetery.location.building
        form = CemeteryForm(initial=initial_data)
    return direct_to_template(request, 'management_edit_cemetery.html',
                              {'form': form,})



#def get_streets(request):
    #"""
    #Получение списка улиц для нас. пункта.
    #"""
    #streets = []
    #try:
        #city = request.GET.get('city')
        #q = request.GET.get('q')
        #city_obj = City.objects.get(name__iexact=region)
    #except Country.DoesNotExist:
        #pass
    #else:
        #cursor = City.objects.filter(region=region_obj).filter(name__istartswith=q).order_by("name")[:24]
        #streets = [item.name for item in cursor]
    #return direct_to_template(request, 'ajax.html', {'objects': streets,})


@login_required
@is_in_group("journal")
@transaction.commit_on_success
def journal(request):
    """
    Страница ввода нового захоронения.
    """
    if request.method == "POST":
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            # Try to get Place.
            try:
                place = Place.objects.get(cemetery=cd["cemetery"], area=cd["area"], row=cd["row"], seat=cd["seat"])
            except ObjectDoesNotExist:
                # Create new Place.
                place = Place(creator=request.user)
                place.cemetery = cd["cemetery"]
                place.area = cd["area"]
                place.row = cd["row"]
                place.seat = cd["seat"]
                place.soul = cd["cemetery"].organization.soul_ptr  # писать ту орг-ию, что у Cemetery!!!
                place.name = u"Место захоронения"
                place.p_type = ProductType.objects.get(id=settings.PLACE_PRODUCTTYPE_ID)
                place.save()
            # Create new Person for dead man.
            new_person = Person(creator=request.user)
            new_person.last_name = cd["last_name"].capitalize()
            new_person.first_name = cd["first_name"].capitalize()
            new_person.patronymic = cd["patronymic"].capitalize()
            new_person.save()
            # Create new Person for customer.
            customer = Person(creator=request.user)
            customer.last_name = cd["customer_last_name"].capitalize()
            if cd.get("customer_first_name", ""):
                customer.first_name = cd["customer_first_name"].capitalize()
            if cd.get("customer_patronymic", ""):
                customer.patronymic = cd["patronymic"].capitalize()
            customer.save()
            # Create customer's Phone.
            if cd.get("customer_phone", ""):
                phone = Phone(soul=customer.soul_ptr)
                phone.f_number = cd["customer_phone"]
                phone.save()
            # Create customer's location.
            new_location = Location()
#            if (cd.get("customer_country", "") and cd.get("customer_region", "") and
#                cd.get("customer_city", "") and cd.get("customer_street", "")):
#                try:
#                    street = Street.objects.get(city=cd["customer_city"], name__iexact=cd["customer_street"])
#                except ObjectDoesNotExist:
#                    street = Street(city=cd["customer_city"], name=cd["customer_street"].capitalize())
#                    street.save()
#                new_location.street = street
#                if cd.get("customer_house", ""):
#                    new_location.house = cd["customer_house"]
#                if cd.get("customer_block", ""):
#                    new_location.block = cd["customer_block"]
#                if cd.get("customer_building", ""):
#                    new_location.building = cd["customer_building"]
#                if cd.get("customer_flat", ""):
#                    new_location.flat = cd["customer_flat"]
            if cd.get("country", ""):
                # Страна.
                try:
                    country = GeoCountry.objects.get(name__iexact=cd["country"])
                except ObjectDoesNotExist:
                    country = GeoCountry(name=cd["country"].capitalize())
                    country.save()
                # Регион.
                try:
                    region = GeoRegion.objects.get(country=country, name__iexact=cd["region"])
                except ObjectDoesNotExist:
                    region = GeoRegion(country=country, name=cd["region"].capitalize())
                    region.save()
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(region=region, name__iexact=cd["city"])
                except ObjectDoesNotExist:
                    city = GeoCity(country=country, region=region, name=cd["city"].capitalize())
                    city.save()
                # Улица.
                try:
                    street = Street.objects.get(city=city, name__iexact=cd["street"])
                    print "a1"
                except ObjectDoesNotExist:
                    street = Street(city=city, name=cd["street"].capitalize())
                    street.save()
                    print "a2"
                # Сохраняем Location.
                new_location.street = street
                if cd.get("customer_house", ""):
                    new_location.house = cd["customer_house"]
                if cd.get("customer_block", ""):
                    new_location.block = cd["customer_block"]
                if cd.get("customer_building", ""):
                    new_location.building = cd["customer_building"]
                if cd.get("customer_flat", ""):
                    new_location.flat = cd["customer_flat"]
            new_location.save()
#            customer.soul_ptr.location = new_location
#            customer.soul_ptr.save()
            customer.location = new_location
            customer.save()

            #АДРЕС customer'а!!! идет в customer.soul_ptr.location

            # Create new Burial.
            new_burial = Burial(creator=request.user)
            new_burial.person = new_person
            new_burial.product = place.product_ptr
            new_burial.date_plan = cd["burial_date"]
            new_burial.date_fact = cd["burial_date"]
            new_burial.account_book_n = cd["account_book_n"]
            new_burial.customer = customer.soul_ptr
#            new_burial.name = u"Захоронение"
#            new_burial.p_type = ProductType.objects.get(id=settings.BURIAL_PRODUCTTYPE_ID)
            new_burial.responsible = cd["cemetery"].organization.soul_ptr  #ставить орг-ию кладбища
            new_burial.doer = request.user.userprofile.soul
            new_burial.operation = cd["operation"]
            new_burial.save()
            # Create comment.
            if cd.get("comment", ""):
                new_burial.add_comment(cd["comment"], request.user)
            # Save images.
            for nf in request.FILES:
                nfile = request.FILES[nf]
                of = OrderFiles(creator=request.user)
                of.order = new_burial.order_ptr
                of.ofile = nfile
                if cd.get("file1_comment", ""):
                    of.comment = cd["file1_comment"]
                of.save()

#            # Create new Order.
#            new_order = Order(creator=request.user)
#            new_order.responsible = MAIN_ORGANIZATION.soul_ptr
##            new_order.customer = customer
#            #new_order.doer = request.user
#            new_order.save()

#            # Create new OrderPosition.
#            new_op = OrderPosition(creator=request.user)
#            new_op.order = new_order
#            new_op.product = new_burial.product_ptr
#            new_op.operation = cd["service"].operation
#            new_op.save()
            return redirect("/journal/")
    else:
        #form = JournalForm(initial={'last_name': 'НЕИЗВЕСТЕН'})
        initial={"burial_date": datetime.date.today().strftime("%d.%m.%Y"),
                 "last_name": 'НЕИЗВЕСТНО'}
        if request.user.userprofile.default_cemetery:
            initial["cemetery"] = request.user.userprofile.default_cemetery
        if request.user.userprofile.default_operation:
            initial["operation"] = request.user.userprofile.default_operation
        form = JournalForm(initial)
    today = datetime.date.today()
    burials = Burial.objects.filter(is_trash=False, creator=request.user,
                            date_of_creation__gte=datetime.datetime(year=today.year, month=today.month, day=today.day)).order_by('-date_of_creation', 'person__last_name')
    return direct_to_template(request, 'journal.html', {'form': form,
                                                        'burials': burials})


@login_required
@is_in_group("edit_burial")
@transaction.commit_on_success
def edit_burial(request, uuid):
    """
    Страница редактирования существующего захоронения.
    """
    try:
        burial = Burial.objects.get(uuid=uuid)
    except ObjectDoesNotExist:
        raise Http404
#    CommentFormSet = modelformset_factory(OrderComments, OrderCommentsForm, can_delete=False, extra=1)
#    formset = CommentFormSet(queryset=OrderComments.objects.filter(order=burial.order_ptr))
    PhoneFormSet = modelformset_factory(Phone, exclude=("soul",), extra=1)
#    OrderFormSet = formset_factory(CustomerPhoneForm, extra=2)
#    OrderFormSet = modelformset_factory(Phone)
#    MyFormSet = inlineformset_factory(Soul, Phone, extra=1, form=CustomerPhoneForm)
#    soul = burial.customer.person.soul_ptr
#    formset = MyFormSet(instance=soul)
    if request.method == "POST":
        formset = PhoneFormSet(request.POST, request.FILES,
                               queryset=Phone.objects.filter(soul=burial.customer.person.soul_ptr))
#        form = EditOrderForm(request.POST, request.FILES, orgsoul=burial.product.place.cemetery.organization.soul_ptr)
        form = EditOrderForm(request.POST, request.FILES)
        if formset.is_valid() and form.is_valid():
            print "form is valid"
            for phone in formset.save(commit=False):
                phone.soul = burial.customer.person.soul_ptr
                phone.save()
            cd = form.cleaned_data
#            print repr(cd["street"])
            burial.date_fact = cd["burial_date"]
#            operation = Operation.objects.get(id=cd["operation"])
            operation = cd["operation"]
            burial.operation = operation
#            print operation
            burial.save()
            try:
                place = Place.objects.get(cemetery=cd["cemetery"], area=cd["area"], row=cd["row"], seat=cd["seat"])
            except ObjectDoesNotExist:
                place = Place(cemetery=cd["cemetery"], area=cd["area"], row=cd["row"], seat=cd["seat"],
                              creator=request.user)
                place.soul = cd["cemetery"].organization.soul_ptr  # писать ту орг-ию, что у Cemetery!!!
                place.name = u"Место захоронения"
                place.p_type = ProductType.objects.get(id=settings.PLACE_PRODUCTTYPE_ID)
                place.save()
#            burial.product.place = place
#            burial.product.place.area = cd["area"]
#            burial.product.place.row = cd["row"]
#            burial.product.place.seat = cd["seat"]
#            burial.product.save()
            burial.product = place.product_ptr
            burial.save()
            # Обработка Location заказчика.
            # TEMP! Пока есть заказчики без Location.
            if not hasattr(burial.customer, "location") or burial.customer.location is None:
                location = Location()
                location.save()
                burial.customer.location = location
                burial.customer.save()
                print location.uuid
            else:
                print "ee"
                location = burial.customer.location
            # Поля модели Location.
            if cd.get("country", ""):
                print "xx"
                # Страна.
                try:
                    country = GeoCountry.objects.get(name__iexact=cd["country"])
                except ObjectDoesNotExist:
                    country = GeoCountry(name=cd["country"].capitalize())
                    country.save()
                # Регион.
                try:
                    region = GeoRegion.objects.get(country=country, name__iexact=cd["region"])
                except ObjectDoesNotExist:
                    region = GeoRegion(country=country, name=cd["region"].capitalize())
                    region.save()
                # Нас. пункт.
                try:
                    city = GeoCity.objects.get(region=region, name__iexact=cd["city"])
                except ObjectDoesNotExist:
                    city = GeoCity(country=country, region=region, name=cd["city"].capitalize())
                    city.save()
                # Улица.
                try:
                    street = Street.objects.get(city=city, name__iexact=cd["street"])
                    print "a1"
                except ObjectDoesNotExist:
                    street = Street(city=city, name=cd["street"].capitalize())
                    street.save()
                    print "a2"
                # Сохраняем Location.
                location.street = street
                location.save()
                print "Location saved!"
            if cd.get("comment", ""):
                burial.add_comment(cd["comment"], request.user)
            if "file1" in request.FILES:
                nfile = request.FILES["file1"]
                of = OrderFiles(creator=request.user)
                of.order = burial.order_ptr
                of.ofile = nfile
                if cd.get("file1_comment", ""):
                    of.comment = cd["file1_comment"]
                of.save()
            return redirect("/burial/%s/" % uuid)
    else:
#        phones = Phone.objects.filter(soul=burial.customer.person.soul_ptr)
#        formset = OrderFormSet(ins)
        formset = PhoneFormSet(queryset=Phone.objects.filter(soul=burial.customer.person.soul_ptr))
        initial_data = {
            "burial_date": datetime.datetime.date(burial.date_fact).strftime("%d.%m.%Y"),
            "cemetery": burial.product.place.cemetery,
            "area": burial.product.place.area,
            "row": burial.product.place.row,
            "seat": burial.product.place.seat,
            "operation": burial.operation,
            "hoperation": burial.operation.id,
#            "street": burial.customer.location.street.name,
#            "city": burial.customer.location.street.city.name,
#            "region": burial.customer.location.street.city.region.name,
#            "country": burial.customer.location.street.city.region.country.name
        }
        if burial.customer.location and hasattr(burial.customer.location, "street") and burial.customer.location.street:
            initial_data["street"] = burial.customer.location.street.name
            initial_data["city"] = burial.customer.location.street.city.name
            initial_data["region"] = burial.customer.location.street.city.region.name
            initial_data["country"] = burial.customer.location.street.city.region.country.name
#        form = EditOrderForm(initial=initial_data, orgsoul=burial.product.place.cemetery.organization.soul_ptr)
        form = EditOrderForm(initial=initial_data)
    return direct_to_template(request, 'burial.html', {'burial': burial, 'form': form, 'formset': formset})


@login_required
@is_in_group("delete_orderfile")
def delete_orderfile(request, ouuid, fuuid):
    """
    Удаление картинки ордера.
    """
    try:
        f = OrderFiles.objects.get(order__uuid=ouuid, uuid=fuuid)
    except ObjectDoesNotExist:
        raise Http404
    f.delete()
    return redirect("/burial/%s/" % ouuid)


#def get_all_person_ln_old(request):
#    """
#    Получение уникального списка фамилий всех персон.
#    """
#    person_lns = []
#    q = request.GET.get('q', None)
#    if q is not None:
#        rezult = Person.objects.filter(last_name__istartswith=q).values("last_name").order_by("last_name").distinct()[:16]
#        person_lns = [item["last_name"] for item in rezult]
#    return direct_to_template(request, 'ajax.html', {'objects': person_lns,})


def get_customer_ln(request):
    """
    Получение уникального списка фамилий всех заказчиков.
    """
    person_lns = []
    q = request.GET.get('q', None)
    if q is not None:
        rezult = Person.objects.filter(ordr_customer__isnull=False, last_name__istartswith=q).values("last_name").order_by("last_name").distinct()[:16]
        person_lns = [item["last_name"] for item in rezult]
    return direct_to_template(request, 'ajax.html', {'objects': person_lns,})


def get_deadman(request):
    """
    Получение уникального списка ФИО захороненных.
    """
    persons = []
    q = request.GET.get('q', None)
    if q is not None:
        rezult = Person.objects.filter(buried__isnull=False, last_name__istartswith=q).values("last_name", "first_name", "patronymic").order_by("last_name", "first_name", "patronymic").distinct()[:16]
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
            choices = SoulProducttypeOperation.objects.filter(soul=orgsoul, p_type=settings.PLACE_PRODUCTTYPE_ID).values_list("operation__id", "operation__op_type")
            print repr(choices)
            for c in choices:
                rez.append({"optionValue": c[0], "optionDisplay": c[1]})
            rez.insert(0, {"optionValue": 0, "optionDisplay": u'---------'})
    return HttpResponse(JSONEncoder().encode(rez))


def get_street(request):
    """
    Получение улицы с городом, регионом и страной.
    """
    streets = []
    q = request.GET.get('term', None)
    if q is not None:
        rezult = Street.objects.filter(name__istartswith=q).order_by("name", "city__name", "city__region__name", "city__region__country__name")[:24]
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
        rezult = GeoCity.objects.filter(name__istartswith=q).order_by("name", "region__name", "region__country__name")[:24]
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


@login_required
@is_in_group("import_csv")
@transaction.commit_manually
def import_csv(request):
    """
    Импорт захоронений из csv-файла.
    """
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            r = csv.reader(cd["csv_file"], "4mysql")
            for l in r:
                if l:
                    (n,
                     ln, fn, ptrc, initials,
                     bur_date, area, row, seat,
                     cust_ln, cust_fn, cust_ptrc, cust_initials,
                     city, street, house, block, flat,
                     comment) = l
                    # Номер в книге учета.
                    n = n.decode("utf8").strip().lower()
                    # Фамилия захороненного.
                    if ln == "N":
                        ln = u""
                    else:
                        ln = ln.decode("utf8").strip().capitalize()
                    # Имя захороненного.
                    if fn == "N":
                        fn = u""
                    else:
                        fn = fn.decode("utf8").strip().capitalize()
                    # Отчество захороненного.
                    if ptrc == "N":
                        ptrc = u""
                    else:
                        ptrc = ptrc.decode("utf8").strip().capitalize()
                    # Инициалы захороненного.
                    if initials == "N":
                        initials = u""
                    else:
                        initials = initials.decode("utf8").strip().upper()
                    # Участок/ряд/место.
                    area = area.decode("utf8").strip()
                    row = row.decode("utf8").strip()
                    seat = seat.decode("utf8").strip()
                    # Фамилия заказчика.
                    if cust_ln == "N":
                        cust_ln = u""
                    else:
                        cust_ln = cust_ln.decode("utf8").strip().capitalize()
                    # Имя заказчика.
                    if cust_fn == "N":
                        cust_fn = u""
                    else:
                        cust_fn = cust_fn.decode("utf8").strip().capitalize()
                    # Отчество заказчика.
                    if cust_ptrc == "N":
                        cust_ptrc = u""
                    else:
                        cust_ptrc = cust_ptrc.decode("utf8").strip().capitalize()
                    # Инициалы заказчика.
                    if cust_initials == "N":
                        cust_initials = u""
                    else:
                        cust_initials = cust_initials.decode("utf8").strip().upper()
                    if city == "N":
                        city = u""
                    else:
                        city = city.decode("utf8").strip().capitalize()
                    if street == "N":
                        street = u""
                    else:
                        street = street.decode("utf8").strip().capitalize()
                    if house == "N":
                        house = u""
                    else:
                        house = house.decode("utf8").strip().lower()
                    if block == "N":
                        block = ""
                    if flat == "N":
                        flat = ""
                    if comment == "N":
                        comment = u""
                    else:
                        comment = comment.decode("utf8").strip()

                    # Захороненный.
                    deadman = Person(creator=request.user)
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
                    customer = Person(creator=request.user)
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
#                        cities = GeoCity.objects.filter(name__iexact=city.strip()).order_by("country__id")
                        cities = GeoCity.objects.filter(name__iexact=city)
                        if cities:
                            cust_city = cities[0]
                        else:
                            cust_city = GeoCity.objects.get(name__iexact="НЕИЗВЕСТЕН")
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
                    customer.location = location  # Проверить, работает ли!!!
                    customer.save()

                    # Место.
                    cemetery = cd["cemetery"]
                    try:
                        place = Place.objects.get(cemetery=cemetery, area__iexact=area, row__iexact=row,
                                                  seat__iexact=seat)
                    except ObjectDoesNotExist:
                        place = Place(creator=request.user)
                        place.cemetery = cemetery
                        place.area = area
                        place.row = row
                        place.seat = seat
                        place.soul = cemetery.organization.soul_ptr  # To check!
                        place.name = u"Место захоронения"
                        place.p_type = ProductType.objects.get(id=settings.PLACE_PRODUCTTYPE_ID)
                        place.save()

                    # Захоронение.
                    burial = Burial(creator=request.user)
                    burial.person = deadman
                    burial.account_book_n = n
                    burial.responsible = place.cemetery.organization.soul_ptr
                    burial.customer = customer
                    burial.doer = request.user.userprofile.soul
                    burial.date_fact = datetime.datetime.strptime(bur_date, "%Y-%m-%d  %H:%M:%S")
                    burial.product = place.product_ptr
                    if "урн" in comment.lower():
                        operation = Operation.objects.get(id=5)
                    elif "подзахоронение" in comment.lower():
                        operation = Operation.objects.get(id=4)
                    elif "захоронение в " in comment.lower():
                        operation = Operation.objects.get(id=6)
                    else:
                        operation = Operation.objects.get(id=7)
                    burial.operation = operation
                    burial.save()
                    burial.add_comment(comment, request.user)
                    # Коммитим все.
                    transaction.commit()

            return redirect("/management/import/")
    else:
        form = ImportForm()
    return direct_to_template(request, "import.html", {"form": form,})
