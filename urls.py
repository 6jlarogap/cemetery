# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('common.views',
    url(r'^$', 'main_page', name='main_page'),
    url(r'^create/$', 'new_burial', name='new_burial'),
    url(r'^create/place/$', 'new_burial_place', name='new_burial_place'),
    url(r'^create/person/$', 'new_burial_person', name='new_burial_person'),
    url(r'^create/customer/$', 'new_burial_customer', name='new_burial_customer'),
    url(r'^create/responsible/$', 'new_burial_responsible', name='new_burial_responsible'),
    url(r'^edit/(?P<pk>.*)/$', 'edit_burial', name='edit_burial'),
    url(r'^print/(?P<pk>.*)/$', 'print_burial', name='print_burial'),

    url(r'^burial/(?P<pk>.*)/$', 'view_burial', name='view_burial'),
    url(r'^place/(?P<pk>.*)/$', 'view_place', name='view_place'),

    url(r'^profile/$', 'profile', name='profile'),

    url(r'^login/$', 'ulogin', name='ulogin'),
    url(r'^logout/$', 'ulogout', name='ulogout'),

    url(r'^geo/', include('geo.urls')),
)
urlpatterns += patterns('',
    (r'^sentry/', include('sentry.web.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )