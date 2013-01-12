from optparse import make_option
import sys

from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q

from old_common import models as old_models
from persons.models import DeathCertificate, Person, ZAGS

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.import_deathcerts()

    def import_deathcerts(self):
        for old in old_models.DeathCertificate.objects.all().using('old').select_related():
            try:
                DeathCertificate.objects.get(
                    person__last_name=old.soul.person.last_name,
                    person__first_name=old.soul.person.first_name,
                    person__middle_name=old.soul.person.patronymic,
                )
            except DeathCertificate.DoesNotExist:
                DeathCertificate.objects.create(
                    person = Person.objects.filter(
                        last_name=old.soul.person.last_name,
                        first_name=old.soul.person.first_name,
                        middle_name=old.soul.person.patronymic,
                        birth_date=old.soul.person.birth_date,
                        birth_date_no_month=old.soul.person.birth_date_no_month,
                        birth_date_no_day=old.soul.person.birth_date_no_day,
                        death_date=old.soul.person.death_date,
                    )[0],
                    s_number = old.s_number,
                    series = old.series,
                    release_date = old.release_date,
                    zags = ZAGS.objects.get(name=old.zags.name)
                )
        print 'ZAGS:', old_models.DeathCertificate.objects.all().using('old').count()
