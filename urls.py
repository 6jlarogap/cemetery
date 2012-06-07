# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('common.views',
    url(r'^$', 'main_page', name='main_page'),
    url(r'^create/$', 'new_burial', name='new_burial'),

    url(r'^login/$', 'ulogin'),
    url(r'^logout/$', 'ulogout'),

    url(r'^geo/', include('geo.urls')),
)

urlpatterns += patterns('',
    (r'^sentry/', include('sentry.web.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )