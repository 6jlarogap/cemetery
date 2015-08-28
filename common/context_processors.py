# coding: utf-8

from django.conf import settings

def context_processor(request):
    return {
            'global_context_SITE_READONLY': settings.SITE_READONLY,
           }
