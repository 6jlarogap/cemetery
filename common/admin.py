# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Organization, Role, Soul, Person, PersonRole, Burial, Place, Cemetery, Location, GeoCountry, Metro
from models import GeoRegion, Street, ProductType, ProductComments, Order, Operation, SoulProducttypeOperation, Phone
from models import UserProfile, ProductFiles, Product, GeoCity, DeathCertificate, OrderFiles, OrderComments

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['last_name', 'first_name', 'patronymic']
    raw_id_fields = ['location', 'creator']
    list_display = ['last_name', 'first_name', 'patronymic', 'location']

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ("creator", "location")
        return super(PersonAdmin, self).get_form(request, obj=None, **kwargs)


class BurialAdmin(admin.ModelAdmin):
#    fields = ("account_book_n",)
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ("person", "responsible", "customer",  "doer",  "date_plan", "date_fact", "product",
                            "operation", "is_trash", "creator", "date_of_creation", "last_sync_date")
        return super(BurialAdmin, self).get_form(request, obj=None, **kwargs)


class OFAdmin(admin.ModelAdmin):
#    exclude = ("order",)
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
#            self.exclude = ()
            self.exclude = ("order", "creator")
        else:
            self.exclude = ("order", "creator")
        return super(OFAdmin, self).get_form(request, obj=None, **kwargs)


class OCAdmin(admin.ModelAdmin):
#    exclude = ("order",)
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

class StreetAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Soul)
admin.site.register(PersonRole)
admin.site.register(ProductType)
admin.site.register(Place)
admin.site.register(Cemetery)
admin.site.register(Location)
admin.site.register(GeoCountry)
admin.site.register(GeoCity)
admin.site.register(Street, StreetAdmin)
admin.site.register(Metro)
admin.site.register(ProductComments)
admin.site.register(Order)
admin.site.register(Operation)
admin.site.register(SoulProducttypeOperation)
admin.site.register(Phone)
admin.site.register(UserProfile)
admin.site.register(ProductFiles)
admin.site.register(Product)
admin.site.register(GeoRegion)
admin.site.register(DeathCertificate)

admin.site.register(Person, PersonAdmin)
admin.site.register(Burial, BurialAdmin)
admin.site.register(OrderFiles, OFAdmin)
admin.site.register(OrderComments, OCAdmin)
#admin.site.register(Role, RoleAdmin)

