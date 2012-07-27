from optparse import make_option
import sys

from django.core.management.base import BaseCommand
from cemetery.models import Burial

from organizations.models import Organization, Agent
from persons.models import Person

class Command(BaseCommand):
    def handle(self, *args, **options):
        for_delete = []
        for a in list(Agent.objects.all()):
            other_agents = Agent.objects.exclude(pk=a.pk).filter(
                person__last_name=a.person.last_name,
                person__first_name=a.person.first_name,
                person__middle_name=a.person.middle_name,
                organization=a.organization,
            )
            if other_agents.count():
                print 'Deleting %s duplicates of %s' % (other_agents.count(), a)
                old_burials = Burial.objects.filter(agent__in=other_agents)
                if old_burials.count():
                    old_burials.update(agent=a)
                    for_delete += list(other_agents)

        for d in for_delete:
            d.delete()