# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from common.models import *

class StreetForm(forms.ModelForm):
    combine_with = forms.ModelChoiceField(
        queryset=Street.objects.all(), label=u"Слить с улицей", help_text=u"Текущая улица будет удалена", required=False)
    really_combine = forms.BooleanField(label=u"Подтвердить слияние", required=False)

    class Meta:
        model = Street

    def __init__(self, *args, **kwargs):
        Street.__unicode__ = lambda s: u'%s %s' % (s.name, s.city)
        super(StreetForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.instance and self.cleaned_data.get('combine_with') and self.cleaned_data.get('really_combine'):
            new_street = self.cleaned_data.get('combine_with')
            Location.objects.filter(street=self.instance).update(
                street=new_street,
                city=new_street.city,
                region=new_street.city and new_street.city.region,
                country=new_street.city and new_street.city.region and new_street.city.region.country,
            )
            self.instance.delete()
        else:
            return super(StreetForm, self).save(*args, **kwargs)

    def save_m2m(self, *args, **kwargs):
        return

class PersonAdmin(admin.ModelAdmin):
    raw_id_fields = ['location', 'creator', ]

    lookup_allowed = lambda *args: True

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ("creator", "location")
        return super(PersonAdmin, self).get_form(request, obj=None, **kwargs)


class BurialAdmin(admin.ModelAdmin):
    raw_id_fields = ['responsible', 'responsible_customer', 'responsible_agent', 'customer', 'doer', 'product', 'creator', 'person', ]
    
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ("person", "responsible", "customer",  "doer",  "date_plan", "date_fact", "product",
                            "operation", "is_trash", "creator", "date_of_creation", "last_sync_date")
        return super(BurialAdmin, self).get_form(request, obj=None, **kwargs)


class OFAdmin(admin.ModelAdmin):
    raw_id_fields = ['order', 'creator', ]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
#            self.exclude = ()
            self.exclude = ("order", "creator")
        else:
            self.exclude = ("order", "creator")
        return super(OFAdmin, self).get_form(request, obj=None, **kwargs)


class OCAdmin(admin.ModelAdmin):
    raw_id_fields = ['order', 'creator', ]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ("order", "creator")
        return super(OCAdmin, self).get_form(request, obj=None, **kwargs)

#class RoleAdmin(admin.ModelAdmin):
#    def get_form(self, request, obj=None, **kwargs):
#        if request.user.is_superuser:
#            self.exclude = ()
#        else:
#            self.exclude = ("creator")
#        return super(RoleAdmin, self).get_form(request, obj=None, **kwargs)

class OrganizationAgentInline(admin.StackedInline):
    fk_name = 'organization'
    model = Agent
    exclude = ['creator', 'birth_date', 'death_date', 'location', ]

class OrganizationPhoneInline(admin.StackedInline):
    model = Phone

class OrganizationAdmin(admin.ModelAdmin):
    raw_id_fields = ['location', 'creator', ]
    exclude = ['birth_date', 'death_date', ]

    inlines = [OrganizationPhoneInline, OrganizationAgentInline, ]

class SoulAdmin(admin.ModelAdmin):
    raw_id_fields = ['location', 'creator', ]

class RoleAdmin(admin.ModelAdmin):
    raw_id_fields = ['organization', 'creator', ]

class PersonRoleAdmin(admin.ModelAdmin):
    raw_id_fields = ['person', 'creator', ]

class PlaceAdmin(admin.ModelAdmin):
    raw_id_fields = ['cemetery', 'creator', ]

class CemeteryAdmin(admin.ModelAdmin):
    raw_id_fields = ['organization', 'location', 'creator', ]
    list_display = ['name', 'organization', 'ordering']
    list_editable = ['ordering']

class LocationAdmin(admin.ModelAdmin):
    raw_id_fields = ['street', ]

class GeoAdmin(admin.ModelAdmin):
    ordering = ['name', ]
    search_fields = ['name', ]

class StreetAdmin(admin.ModelAdmin):
    form = StreetForm
    raw_id_fields = ['city', ]
    ordering = ['name', ]
    search_fields = ['name', ]

    def save_model(self, request, obj, form, change):
        if not obj:
            return
        else:
            super(StreetAdmin, self).save_model(request, obj, form, change)

    def log_change(self, request, object, message):
        if not object:
            return
        else:
            return super(StreetAdmin, self).log_change(request, object, message)

    def response_change(self, request, obj):
        if not obj:
            return HttpResponseRedirect('..')
        return super(StreetAdmin, self).response_change(request, obj)

class MetroAdmin(admin.ModelAdmin):
    raw_id_fields = ['city', ]

class ProductCommentsAdmin(admin.ModelAdmin):
    raw_id_fields = ['product', 'creator', ]

class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ['responsible', 'responsible_customer', 'responsible_agent', 'customer', 'doer', 'product', 'creator', ]

class OperationAdmin(admin.ModelAdmin):
    list_display = ['op_type', 'ordering']
    list_editable = ['ordering']

class ProductCommentsAdmin(admin.ModelAdmin):
    raw_id_fields = ['product', 'creator', ]

class PhoneAdmin(admin.ModelAdmin):
    raw_id_fields = ['soul', ]

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'soul', 'default_cemetery', 'default_city', ]

class SoulProducttypeOperationAdmin(admin.ModelAdmin):
    raw_id_fields = ['soul', ]

class ProductFilesAdmin(admin.ModelAdmin):
    raw_id_fields = ['product', 'creator', ]

class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ['soul', ]

class DeathCertificateAdmin(admin.ModelAdmin):
    raw_id_fields = ['soul', ]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'ordering', ]
    list_editable = ['ordering', ]
    ordering = ['ordering', 'name']

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'object_link', 'user', ]

    def object_link(self, obj):
        o = obj.get_edited_object()
        if isinstance(o, Burial):
            return u'<a href="%s">Захоронение %s (%s)</a>' % (reverse('edit_burial', args=[o.pk]), o.account_book_n, o.person)
        else:
            return u'%s' % o
    object_link.allow_tags = True

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Soul, SoulAdmin)
admin.site.register(PersonRole, PersonRoleAdmin)
admin.site.register(ProductType)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Cemetery, CemeteryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(GeoCountry, GeoAdmin)
admin.site.register(GeoCity, GeoAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Metro, MetroAdmin)
admin.site.register(ProductComments, ProductCommentsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(SoulProducttypeOperation, SoulProducttypeOperationAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ProductFiles, ProductFilesAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(GeoRegion, GeoAdmin)
admin.site.register(DeathCertificate, DeathCertificateAdmin)
admin.site.register(ZAGS)
admin.site.register(IDDocumentType)
admin.site.register(DocumentSource)


admin.site.register(Person, PersonAdmin)
admin.site.register(Burial, BurialAdmin)
admin.site.register(OrderFiles, OFAdmin)
admin.site.register(OrderComments, OCAdmin)
#admin.site.register(Role, RoleAdmin)

admin.site.register(OrderProduct, OrderProductAdmin)

admin.site.register(LogEntry, LogEntryAdmin)