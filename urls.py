# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'common.views.main_page'),
    url(r'^init/$', 'common.views.init'),
    url(r'^login/$', 'common.views.ulogin'),
    url(r'^logout/$', 'common.views.ulogout'),
    url(r'^profile/$', 'common.views.profile'),

    url(r'^journal/$', 'common.views.journal', name="add_burial"),
    url(r'^burial/(.{36})/$', 'common.views.edit_burial'),
    url(r'^burial/(.{36})/print/$', 'common.views.print_burial', name='print_burial'),

    url(r'^ordercomment/(.{36})/$', 'common.views.order_comment_edit'),
    url(r'^orderfilecomment/(.{36})/$', 'common.views.order_filecomment_edit'),
    url(r'^management/$', 'common.views.management'),
    url(r'^management/import/$', 'common.views.import_csv'),
    url(r'^management/user/$', 'common.views.management_user'),
    url(r'^management/user/edit/(.{36})/$', 'common.views.management_edit_user'),
    url(r'^management/cemetery/$', 'common.views.management_cemetery'),
    url(r'^management/cemetery/edit/(.{36})/$', 'common.views.management_edit_cemetery'),

    # ajax.
    url(r'^getcountries/$', 'common.views.get_countries'),
    url(r'^getregions/$', 'common.views.get_regions'),
    url(r'^getcities/$', 'common.views.get_cities'),
    url(r'^getstreets/$', 'common.views.get_street'),

    # Уникальный список фамилий заказчиков.
    url(r'^getpersonunln/$', 'common.views.get_customer_ln'),
    # Уникальный список фамилий захороненных.
    url(r'^getdeadman/$', 'common.views.get_deadman'),
    # Список доступных операций для выбранного кладбища.
    url(r'^getoper/$', 'common.views.get_oper'),
    # Список доступных агентов для выбранной организации.
    url(r'^getagents/$', 'common.views.get_agents'),

    url(r'^orderfile/delete/(.{36})/(.{36})/$', 'common.views.delete_orderfile'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )