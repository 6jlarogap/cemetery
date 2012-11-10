from optparse import make_option
import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings
from cemetery.models import Operation, Cemetery, Burial, Place
from django.db.models import Q
from geo.models import Country, Region, City, Street, Location, cleanup_geo_name

from old_common import models as old_models
from organizations.models import Organization, Agent, Doverennost
from persons.models import ZAGS, DocumentSource, Person

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--skip-users', dest='skip_users', default=None, help='Skips auth.User'),
        make_option('--skip-zags', dest='skip_zags', default=None, help='Skips ZAGS'),
        make_option('--skip-locations', dest='skip_locations', default=None, help='Skips all geo data'),
        make_option('--skip-persons', dest='skip_persons', default=None, help='Skips Persons'),
        make_option('--skip-burials', dest='skip_burials', default=None, help='Skips Burials'),
        make_option('--skip-responsible', dest='skip_responsible', default=None, help='Skips responsibles'),
    )

    def handle(self, *args, **options):
        assert settings.DATABASES.get('old')

        if options['skip_users'] is None:
            self.import_users()
        if options['skip_zags'] is None:
            self.import_zags()
        if options['skip_locations'] is None:
            self.import_locations()
        if options['skip_persons'] is None:
            self.import_persons()

        self.import_organizations()
        self.import_cemeteries()

        if options['skip_burials'] is None:
            self.import_burials()

        if options['skip_responsible'] is None:
            self.import_responsible()

    def import_zags(self):
        for old in old_models.ZAGS.objects.all().using('old'):
            ZAGS.objects.get_or_create(name=old.name)
        print 'ZAGS:', old_models.ZAGS.objects.all().using('old').count()

        for old in old_models.DocumentSource.objects.all().using('old'):
            DocumentSource.objects.get_or_create(name=old.name.upper())
        print 'DocumentSource:', old_models.DocumentSource.objects.all().using('old').count()

    def import_users(self):
        for old in User.objects.all().using('old'):
            try:
                User.objects.get(username = old.username)
            except User.DoesNotExist:
                User.objects.create(
                    username=old.username,
                    email=old.email,
                    password=old.password,
                    is_active=old.is_active,
                    is_staff=old.is_staff,
                    is_superuser=old.is_superuser,
                )

        print 'Users:', User.objects.all().using('old').count()

    def import_locations(self):
        for old in old_models.GeoCountry.objects.all().using('old'):
            try:
                Country.objects.filter(Q(name=old.name) | Q(name=cleanup_geo_name(old.name)))[0]
            except IndexError:
                Country.objects.create(name=old.name)
        print 'Countries:', old_models.GeoCountry.objects.all().using('old').count()

        for old in old_models.GeoRegion.objects.all().select_related().using('old'):
            try:
                Region.objects.filter(Q(name=old.name) | Q(name=cleanup_geo_name(old.name)))[0]
            except IndexError:
                Region.objects.create(name=old.name, country=Country.objects.filter(Q(name=old.country.name) | Q(name=cleanup_geo_name(old.country.name)))[0])
        print 'Regions:', old_models.GeoRegion.objects.all().using('old').count()

        old_cities = old_models.GeoCity.objects.all().select_related(depth=1).using('old')
        if old_cities.count() > City.objects.all().count():
            for old in old_cities:
                try:
                    City.objects.filter(Q(name=old.name) | Q(name=cleanup_geo_name(old.name)), Q(region__name=old.region.name) | Q(region__name=cleanup_geo_name(old.region.name)))[0]
                except IndexError:
                    City.objects.create(name=old.name, region=Region.objects.filter(Q(name=old.region.name) | Q(name=cleanup_geo_name(old.region.name)))[0])
            print 'Cities:', old_models.GeoCity.objects.all().using('old').count()
        else:
            print 'Cities skipped'

        old_streets = old_models.Street.objects.all().select_related(depth=1).using('old')
        if old_streets.count() > Street.objects.all().count():
            for old in old_streets:
                try:
                    Street.objects.filter(Q(name=old.name) | Q(name=cleanup_geo_name(old.name)), Q(city__name=old.city.name) | Q(city__name=cleanup_geo_name(old.city.name)))[0]
                except IndexError:
                    Street.objects.create(name=old.name, city=City.objects.filter(
                        Q(name=old.city.name) | Q(name=cleanup_geo_name(old.city.name)),
                        Q(region__name=old.city.region.name) | Q(region__name=cleanup_geo_name(old.city.region.name))
                    )[0])
            print 'Streets:', old_models.Street.objects.all().using('old').count()
        else:
            print 'Streets skipped'

    def import_persons(self):
        for old in old_models.Person.objects.all().select_related().using('old'):
            address = None

            if old.last_name.replace(' ', '') == '***':
                continue

            if old.location and old.location.country:
                kwargs = dict(
                    country__name=old.location.country.name,
                    region__name=old.location.region.name,
                    city__name=old.location.city.name,
                    post_index=old.location.post_index,

                    house=old.location.house,
                    block=old.location.block,
                    building=old.location.building,
                    flat=old.location.flat,
                    info=old.location.info,
                )
                if old.location.street:
                    kwargs['street__name'] = old.location.street.name
                try:
                    address = Location.objects.get(**kwargs)
                except Location.MultipleObjectsReturned:
                    address = Location.objects.filter(**kwargs)[0]
                except Location.DoesNotExist:
                    if old.location.country:
                        country = Country.objects.filter(Q(name=old.location.country.name) | Q(name=cleanup_geo_name(old.location.country.name)))[0]
                    else:
                        country = None
                    if old.location.region:
                        region = Region.objects.filter(Q(name=old.location.region.name) | Q(name=cleanup_geo_name(old.location.region.name)))[0]
                    else:
                        region = None
                    if old.location.city:
                        city = City.objects.filter(
                            Q(name=old.location.city.name) | Q(name=cleanup_geo_name(old.location.city.name)),
                            Q(region__name=old.location.region.name) | Q(region__name=cleanup_geo_name(old.location.region.name))
                        )[0]
                    else:
                        city = None
                    if old.location.street:
                        street = Street.objects.filter(
                            Q(name=old.location.street.name) | Q(name=cleanup_geo_name(old.location.street.name)),
                            Q(city__name=old.location.city.name) | Q(city__name=cleanup_geo_name(old.location.city.name))
                        )[0]
                    else:
                        street = None


                    address = Location.objects.create(
                        country=country,
                        region=region,
                        city=city,
                        street=street,
                        post_index=old.location.post_index,
                        house=old.location.house,
                        block=old.location.block,
                        building=old.location.building,
                        flat=old.location.flat,
                        gps_x=old.location.gps_x,
                        gps_y=old.location.gps_y,
                        info=old.location.info,
                    )

            kwargs = dict(
                first_name=old.first_name,
                middle_name=old.patronymic,
                last_name=old.last_name,
                birth_date=old.birth_date,
                death_date=old.death_date,
            )
            if old.location:
                if old.location.street:
                    kwargs.update(dict(
                        address__street__name=old.location.street.name,
                    ))
                kwargs.update(dict(
                    address__house=old.location.house,
                    address__flat=old.location.flat,
                ))
            try:
                Person.objects.get(**kwargs)
            except Person.MultipleObjectsReturned:
                pass
            except Person.DoesNotExist:
                Person.objects.create(
                    last_name=old.last_name,
                    first_name=old.first_name,
                    middle_name=old.patronymic,

                    birth_date=old.birth_date,
                    birth_date_no_month=old.birth_date_no_month,
                    birth_date_no_day=old.birth_date_no_day,
                    death_date=old.death_date,

                    address=address,
                )

        print 'Persons:', old_models.Person.objects.all().using('old').count()

    def import_organizations(self):
        for old in old_models.Operation.objects.all().select_related().using('old'):
            try:
                Operation.objects.get(op_type=old.op_type)
            except Operation.DoesNotExist:
                Operation.objects.create(op_type=old.op_type, ordering=old.ordering)
        print 'Operations:', old_models.Operation.objects.all().using('old').count()

        for old in old_models.Organization.objects.all().select_related().using('old'):
            try:
                Organization.objects.get(name=old.name, full_name=old.full_name)
            except Organization.DoesNotExist:
                Organization.objects.create(
                    ogrn=old.ogrn,
                    inn=old.inn,
                    kpp=old.kpp,
                    name=old.name,
                    full_name=old.full_name,
                    ceo_name=old.ceo_name,
                    ceo_name_who=old.ceo_name_who,
                    ceo_document=old.ceo_document,
                )
        print 'Organizations:', old_models.Operation.objects.all().using('old').count()

    def import_cemeteries(self):
        for old in old_models.Cemetery.objects.all().select_related().using('old'):
            try:
                Cemetery.objects.get(name=old.name)
            except Cemetery.DoesNotExist:
                if old.location:
                    kwargs = dict(
                        post_index=old.location.post_index,
                        house=old.location.house,
                        block=old.location.block,
                        building=old.location.building,
                        flat=old.location.flat,
                        gps_x=old.location.gps_x,
                        gps_y=old.location.gps_y,
                        info=old.location.info,
                    )
                    if old.location.country:
                        kwargs['country'] = Country.objects.filter(Q(name=old.location.country.name) | Q(name=cleanup_geo_name(old.location.country.name)))[0]
                    if old.location.region:
                        kwargs['region'] = Region.objects.filter(Q(name=old.location.region.name) | Q(name=cleanup_geo_name(old.location.region.name)),)[0]
                    if old.location.city:
                        kwargs['city'] = City.objects.filter(
                            Q(name=old.location.city.name) | Q(name=cleanup_geo_name(old.location.city.name)),
                            Q(region__name=old.location.region.name) | Q(region__name=cleanup_geo_name(old.location.region.name)),
                        )[0]
                    if old.location.street:
                        kwargs['street'] = Street.objects.filter(
                            Q(name=old.location.street.name) | Q(name=cleanup_geo_name(old.location.street.name)),
                            Q(city__name=old.location.street.city.name) | Q(city__name=cleanup_geo_name(old.location.street.city.name)),
                        )[0]

                    try:
                        address, _tmp = Location.objects.get_or_create(**kwargs)
                    except Location.MultipleObjectsReturned:
                        address = Location.objects.filter(**kwargs)[0]
                else:
                    address = None
                Cemetery.objects.create(
                    organization=Organization.objects.get(name=old.organization.name),
                    location=address,
                    name=old.name,
                    ordering=old.ordering,
                    creator=User.objects.all()[0],
                )
        print 'Cemeteries:', old_models.Cemetery.objects.all().using('old').count()

    def import_burials(self):
        for old in old_models.Burial.objects.all().select_related().using('old'):
            try:
                Burial.objects.get(account_number=old.account_book_n, place__cemetery__name=old.product.place.cemetery.name)
            except Burial.DoesNotExist:
                try:
                    place = Place.objects.get(
                        cemetery=Cemetery.objects.get(name=old.product.place.cemetery.name),
                        row=old.product.place.row,
                        area=old.product.place.area,
                        seat=old.product.place.seat,
                    )
                except Place.DoesNotExist:
                    place = Place.objects.create(
                        cemetery=Cemetery.objects.get(name=old.product.place.cemetery.name),
                        row=old.product.place.row,
                        area=old.product.place.area,
                        seat=old.product.place.seat,
                        rooms = old.product.place.rooms,
                        creator=User.objects.all()[0],
                    )
                if old.person.location:
                    kwargs = dict(
                        post_index=old.person.location.post_index,
                        house=old.person.location.house,
                        block=old.person.location.block,
                        building=old.person.location.building,
                        flat=old.person.location.flat,
                        gps_x=old.person.location.gps_x,
                        gps_y=old.person.location.gps_y,
                        info=old.person.location.info,
                    )
                    if old.person.location.country:
                        kwargs['country'] = Country.objects.filter(Q(name=old.person.location.country.name) | Q(name=cleanup_geo_name(old.person.location.country.name)))[0]
                    if old.person.location.region:
                        kwargs['region'] = Region.objects.filter(Q(name=old.person.location.region.name) | Q(name=cleanup_geo_name(old.person.location.region.name)))[0]
                    if old.person.location.city:
                        kwargs['city'] = City.objects.filter(
                            Q(name=old.person.location.city.name) | Q(name=cleanup_geo_name(old.person.location.city.name)),
                            Q(region__name=old.person.location.region.name) | Q(region__name=cleanup_geo_name(old.person.location.region.name)),
                        )[0]
                    if old.person.location.street:
                        kwargs['street'] = Street.objects.filter(
                            Q(name=old.person.location.street.name) | Q(name=cleanup_geo_name(old.person.location.street.name)),
                            Q(city__name=old.person.location.street.city.name) | Q(city__name=cleanup_geo_name(old.person.location.street.city.name)),
                        )[0]

                    if any(kwargs.values()):
                        try:
                            address, _tmp = Location.objects.get_or_create(**kwargs)
                        except Location.MultipleObjectsReturned:
                            address = Location.objects.filter(**kwargs)[0]
                    else:
                        address = None
                else:
                    address = None
                try:
                    person = Person.objects.get(
                        last_name=old.person.last_name,
                        first_name=old.person.first_name,
                        middle_name=old.person.patronymic,
    
                        birth_date=old.person.birth_date,
                        death_date=old.person.death_date,
                    )
                except Person.MultipleObjectsReturned:
                    person = Person.objects.filter(
                        last_name=old.person.last_name,
                        first_name=old.person.first_name,
                        middle_name=old.person.patronymic,

                        birth_date=old.person.birth_date,
                        death_date=old.person.death_date,
                    )[0]
                except Person.DoesNotExist:
                    person = Person.objects.create(
                        last_name=old.person.last_name,
                        first_name=old.person.first_name,
                        middle_name=old.person.patronymic,

                        birth_date=old.person.birth_date,
                        birth_date_no_month=old.person.birth_date_no_month,
                        birth_date_no_day=old.person.birth_date_no_day,
                        death_date=old.person.death_date,

                        address=address,
                    )
                Burial.objects.create(
                    account_number=old.account_book_n,
                    operation=Operation.objects.get(op_type=old.operation.op_type),
                    date_plan=old.date_plan,
                    date_fact=old.date_fact,
    
                    place=place,
                    person=person,
    
                    print_info=old.print_info,
                    payment_type=old.payment_type,
                    deleted=old.is_trash,
                    creator=User.objects.all()[0],
                )
        print 'Burials:', old_models.Burial.objects.all().using('old').count()

    def import_responsible(self):
        for old in old_models.Burial.objects.filter(responsible_customer__isnull=False).select_related().using('old'):
            new_burial = Burial.objects.get(
                account_number=old.account_book_n,
                place__cemetery__name=old.product.place.cemetery.name,
            )
            try:
                agent = old.responsible_agent
                org = old.responsible_agent.organization
                new_org = Organization.objects.get(name=org.name)
                try:
                    new_client = old.customer.organization
                except (old_models.Organization.DoesNotExist, TypeError, AttributeError):
                    new_client = new_org
                kwargs = dict(
                    first_name=agent.first_name,
                    middle_name=agent.patronymic,
                    last_name=agent.last_name,
                    birth_date=agent.birth_date,
                    death_date=agent.death_date,
                )
                new_agent, _created = Person.objects.get_or_create(**kwargs)

                new_burial.client_organization = new_client
                new_burial.agent, _created = Agent.objects.get_or_create(person=new_agent, organization=new_org)
                if old.doverennost:
                    new_burial.doverennost, _created = Doverennost.objects.get_or_create(
                        agent=new_burial.agent,
                        number=old.doverennost.number,
                        issue_date=old.doverennost.issue_date,
                        expire_date=old.doverennost.expire_date,
                    )
                new_burial.save()
            except (old_models.Organization.DoesNotExist, TypeError, AttributeError):
                person = old.responsible_customer.person
                if person.last_name.strip(' *') == '':
                    new_person = None
                else:
                    kwargs = dict(
                        first_name=person.first_name,
                        middle_name=person.patronymic,
                        last_name=person.last_name,
                        birth_date=person.birth_date,
                        death_date=person.death_date,
                    )
                    try:
                        new_person = Person.objects.get(**kwargs)
                    except Person.MultipleObjectsReturned:
                        new_person = Person.objects.filter(**kwargs)[0]

                person = old.customer.person
                if person.last_name.strip(' *') == '':
                    new_client = None
                else:
                    kwargs = dict(
                        first_name=person.first_name,
                        middle_name=person.patronymic,
                        last_name=person.last_name,
                        birth_date=person.birth_date,
                        death_date=person.death_date,
                    )
                    try:
                        new_client = Person.objects.get(**kwargs)
                    except Person.MultipleObjectsReturned:
                        new_client = Person.objects.filter(**kwargs)[0]

                new_burial.client_person = new_client
                new_burial.place.responsible = new_person
                new_burial.place.save()
                new_burial.save()

        print 'Responsibles:', old_models.Burial.objects.filter(responsible_customer__isnull=False).using('old').count()
