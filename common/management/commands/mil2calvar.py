from common.models import *

class MoveMil(BaseCommand):
    def handle(self, *args, **kwargs):
        src = Cemetery.objects.get(pk='711af094-44af-11e0-9558-08002790de4f').using('voennoe')
