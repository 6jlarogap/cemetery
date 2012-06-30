from optparse import make_option
import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings
from cemetery.models import Operation, Cemetery
from geo.models import Country, Region, City, Street, Location

from old_common import models as old_models
from organizations.models import Organization
from persons.models import ZAGS, DocumentSource, Person

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--skip-users', dest='skip_users', default=None, help='Skips auth.User'),
        make_option('--skip-zags', dest='skip_zags', default=None, help='Skips ZAGS'),
        make_option('--skip-locations', dest='skip_locations', default=None, help='Skips all geo data'),
        make_option('--skip-persons', dest='skip_persons', default=None, help='Skips Persons'),
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

    def import_zags(self):
        for old in old_models.ZAGS.objects.all().using('old'):
            ZAGS.objects.get_or_create(name=old.name)
        print 'ZAGS:', old_models.ZAGS.objects.all().using('old').count()

        for old in old_models.DocumentSource.objects.all().using('old'):
            DocumentSource.objects.get_or_create(name=old.name)
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
            Country.objects.get_or_create(name=old.name)
        print 'Countries:', old_models.GeoCountry.objects.all().using('old').count()

        for old in old_models.GeoRegion.objects.all().select_related().using('old'):
            try:
                Region.objects.get(name=old.name)
            except Region.DoesNotExist:
                Region.objects.create(name=old.name, country=Country.objects.get(name=old.country.name))
        print 'Regions:', old_models.GeoRegion.objects.all().using('old').count()

        old_cities = old_models.GeoCity.objects.all().select_related(depth=1).using('old')
        if old_cities.count() > City.objects.all().count():
            for old in old_cities:
                try:
                    City.objects.get(name=old.name, region__name=old.region.name)
                except City.DoesNotExist:
                    City.objects.create(name=old.name, region=Region.objects.get(name=old.region.name))
            print 'Cities:', old_models.GeoCity.objects.all().using('old').count()
        else:
            print 'Cities skipped'

        old_streets = old_models.Street.objects.all().select_related(depth=1).using('old')
        if old_streets.count() > Street.objects.all().count():
            for old in old_streets:
                try:
                    Street.objects.get(name=old.name, city__name=old.city.name)
                except Street.DoesNotExist:
                    Street.objects.create(name=old.name, city=City.objects.get(name=old.city.name, region__name=old.city.region.name))
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
                except Location.DoesNotExist:
                    address = Location.objects.create(
                        country=old.location.country and Country.objects.get(name=old.location.country.name) or None,
                        region=old.location.region and Region.objects.get(name=old.location.region.name) or None,
                        city=old.location.city and City.objects.get(name=old.location.city.name, region__name=old.location.region.name) or None,
                        street=old.location.street and Street.objects.get(name=old.location.street.name, city__name=old.location.city.name) or None,
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
                        kwargs['country'] = Country.objects.get(name=old.location.country.name)
                    if old.location.region:
                        kwargs['region'] = Region.objects.get(name=old.location.region.name)
                    if old.location.city:
                        kwargs['city'] = City.objects.get(name=old.location.city.name, region__name=old.location.city.region.name)
                    if old.location.street:
                        kwargs['street'] = Street.objects.get(name=old.location.street.name, city__name=old.location.street.city.name)

                    address, _tmp = Location.objects.get_or_create(**kwargs)
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

