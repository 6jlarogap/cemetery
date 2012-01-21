# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('common.views',
    url(r'^$', 'main_page', name='main_page'),
    url(r'^init/$', 'init'),
    url(r'^login/$', 'ulogin'),
    url(r'^logout/$', 'ulogout'),
    url(r'^profile/$', 'profile'),

    url(r'^journal/$', 'journal', name="add_burial"),
    url(r'^burial/(.{36})/$', 'edit_burial', name='edit_burial'),
    url(r'^burial/(.{36})/print/$', 'print_burial', name='print_burial'),

    url(r'^ordercomment/(.{36})/$', 'order_comment_edit'),
    url(r'^orderfilecomment/(.{36})/$', 'order_filecomment_edit'),
    url(r'^management/$', 'management'),
    url(r'^management/import/$', 'import_csv'),
    url(r'^management/user/$', 'management_user'),
    url(r'^management/user/edit/(.{36})/$', 'management_edit_user'),
    url(r'^management/cemetery/$', 'management_cemetery'),
    url(r'^management/cemetery/edit/(.{36})/$', 'management_edit_cemetery'),

    # ajax.
    url(r'^getcountries/$', 'get_countries'),
    url(r'^getregions/$', 'get_regions'),
    url(r'^getcities/$', 'get_cities'),
    url(r'^getstreets/$', 'get_street'),

    # доверенности
    url(r'^getdover/$', 'get_dover', name='get_dover'),
    url(r'^getpassportsources/$', 'get_passport_sources', name='get_passport_sources'),

    # Уникальный список фамилий заказчиков.
    url(r'^getpersonunln/$', 'get_customer_ln'),
    # Уникальный список фамилий захороненных.
    url(r'^getdeadman/$', 'get_deadman'),
    # Список доступных операций для выбранного кладбища.
    url(r'^getoper/$', 'get_oper'),
    # Список доступных агентов для выбранной организации.
    url(r'^getagents/$', 'get_agents'),

    url(r'^orderfile/delete/(.{36})/(.{36})/$', 'delete_orderfile'),
)

urlpatterns += patterns('',
    (r'^sentry/', include('sentry.web.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )