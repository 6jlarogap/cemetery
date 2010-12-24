# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Organization, Role, Soul, Person, PersonRole, Burial
from models import Place, Cemetery, Location, GeoCountry, GeoRegion, Street, Metro
from models import ProductType, ProductComments, Order  #, OrderPosition
from models import Operation, SoulProducttypeOperation, Phone, UserProfile
from models import ProductFiles, Product, GeoCity, DeathCertificate, OrderFiles, OrderComments

#MAIN_ORGANIZATION = Organization.objects.get(main=True)
#
#class SPOAdmin(admin.ModelAdmin):
#    list_display = ('soul', 'p_type', 'operation',)
#    # Показ единственной Soul - нашей организации.
#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == "soul":
#            kwargs["queryset"] = Soul.objects.filter(organization=MAIN_ORGANIZATION)
#        return super(SPOAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
#
class PersonAdmin(admin.ModelAdmin):
#    exclude = ("creator", "location")
    exclude = ("location",)


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
#admin.site.register(OrderPosition)
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

