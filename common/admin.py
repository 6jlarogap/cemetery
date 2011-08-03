# -*- coding: utf-8 -*-

from django.contrib import admin
from common.models import *

class PersonAdmin(admin.ModelAdmin):
    raw_id_fields = ['location', 'creator', ]
    
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
    model = Agent
    raw_id_fields = ['person', ]

class OrganizationPhoneInline(admin.StackedInline):
    model = Phone

class OrganizationAdmin(admin.ModelAdmin):
    raw_id_fields = ['location', 'creator', ]

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

class LocationAdmin(admin.ModelAdmin):
    raw_id_fields = ['street', ]

class StreetAdmin(admin.ModelAdmin):
    raw_id_fields = ['city', ]

class MetroAdmin(admin.ModelAdmin):
    raw_id_fields = ['city', ]

class ProductCommentsAdmin(admin.ModelAdmin):
    raw_id_fields = ['product', 'creator', ]

class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ['responsible', 'responsible_customer', 'responsible_agent', 'customer', 'doer', 'product', 'creator', ]

class OperationAdmin(admin.ModelAdmin):
    pass

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

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Soul, SoulAdmin)
admin.site.register(PersonRole, PersonRoleAdmin)
admin.site.register(ProductType)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Cemetery, CemeteryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(GeoCountry)
admin.site.register(GeoCity)
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
admin.site.register(GeoRegion)
admin.site.register(DeathCertificate, DeathCertificateAdmin)
admin.site.register(ZAGS)
admin.site.register(IDDocumentType)

admin.site.register(Person, PersonAdmin)
admin.site.register(Burial, BurialAdmin)
admin.site.register(OrderFiles, OFAdmin)
admin.site.register(OrderComments, OCAdmin)
#admin.site.register(Role, RoleAdmin)

admin.site.register(OrderProduct)
