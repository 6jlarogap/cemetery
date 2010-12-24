# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^youmemory/', include('youmemory.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    # Нужно для работы нашего виджета календаря.
    (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),

    (r'^$', 'common.views.main_page'),
    (r'^login/$', 'common.views.ulogin'),
    (r'^logout/$', 'common.views.ulogout'),
    (r'^profile/$', 'common.views.profile'),
    (r'^journal/$', 'common.views.journal'),
    (r'^burial/(.{36})/$', 'common.views.edit_burial'),
    (r'^management/$', 'common.views.management'),
    (r'^management/import/$', 'common.views.import_csv'),
    (r'^management/user/$', 'common.views.management_user'),
    (r'^management/user/edit/(.{36})/$', 'common.views.management_edit_user'),
    #(r'^management/user/delete/(.{36})/$',
     #'common.views.management_delete_user'),
    (r'^management/cemetery/$', 'common.views.management_cemetery'),
    #(r'^management/cemetery/delete/(.{36})/$',
     #'common.views.management_delete_cemetery'),
    (r'^management/cemetery/edit/(.{36})/$',
     'common.views.management_edit_cemetery'),
    # ajax.
    (r'^getcountries/$', 'common.views.get_countries'),
    (r'^getregions/$', 'common.views.get_regions'),
    (r'^getcities/$', 'common.views.get_cities'),
    #(r'^get_streets/$', 'common.views.get_streets'),
    # Уникальный список фамилий заказчиков.
    (r'^getpersonunln/$', 'common.views.get_customer_ln'),
    # Уникальный список фамилий захороненных.
    (r'^getdeadman/$', 'common.views.get_deadman'),
    # Список доступных операций для выбранного кладбища.
    (r'^getoper/$', 'common.views.get_oper'),

    (r'^orderfile/delete/(.{36})/(.{36})/$',
     'common.views.delete_orderfile'),
    #TEMP
    (r'^getstreets/$', 'common.views.get_street'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
)
