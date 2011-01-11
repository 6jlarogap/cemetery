# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Organization, Role, Soul, Person, PersonRole, Burial, Place, Cemetery, Location, GeoCountry, Metro
from models import GeoRegion, Street, ProductType, ProductComments, Order, Operation, SoulProducttypeOperation, Phone
from models import UserProfile, ProductFiles, Product, GeoCity, DeathCertificate, OrderFiles, OrderComments

class PersonAdmin(admin.ModelAdmin):
#    exclude = ("creator", "location")
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ('location',)
        return super(PersonAdmin, self).get_form(request, obj=None, **kwargs)


class BurialAdmin(admin.ModelAdmin):
#    list_display = ('soul', 'p_type', 'operation',)
    fields = ("account_book_n",)


admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Soul)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonRole)
admin.site.register(Burial, BurialAdmin)
admin.site.register(ProductType)
admin.site.register(Place)
admin.site.register(Cemetery)
admin.site.register(Location)
admin.site.register(GeoCountry)
admin.site.register(GeoCity)
admin.site.register(Street)
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

class OFAdmin(admin.ModelAdmin):
    exclude = ("order",)
class OCAdmin(admin.ModelAdmin):
    exclude = ("order",)
admin.site.register(OrderFiles, OFAdmin)
admin.site.register(OrderComments, OCAdmin)

