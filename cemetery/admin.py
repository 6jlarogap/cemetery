# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.core.urlresolvers import reverse
from django import forms

from cemetery.models import *
from organizations.models import BankAccount
from persons.models import ZAGS, IDDocumentType

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'object_link', 'user', ]

    def object_link(self, obj):
        o = obj.get_edited_object()
        if isinstance(o, Burial):
            return u'<a href="%s">Захоронение %s (%s)</a>' % (reverse('edit_burial', args=[o.pk]), o.account_number, o.person)
        else:
            return u'%s' % o
    object_link.allow_tags = True

class PersonAdmin(admin.ModelAdmin):
    lookup_allowed = lambda *args: True

class OrganizationAgentForm(forms.ModelForm):
    last_name = forms.CharField(label=u'Фамилия')
    first_name = forms.CharField(required=False, label=u'Имя')
    middle_name = forms.CharField(required=False, label=u'Отчество')

    class Meta:
        model = Agent
        fields = ['id']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            i = kwargs.get('instance')
            kwargs.setdefault('initial', {}).update({
                'last_name': i.person.last_name,
                'middle_name': i.person.middle_name,
                'first_name': i.person.first_name,
            })
        super(OrganizationAgentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(OrganizationAgentForm, self).save(commit=commit)
        if self.instance.person_id:
            self.instance.person.last_name = self.cleaned_data['last_name']
            self.instance.person.middle_name = self.cleaned_data['middle_name']
            self.instance.person.first_name = self.cleaned_data['first_name']
            self.instance.person.save()
        else:
            self.instance.person = Person.objects.create(
                last_name=self.cleaned_data['last_name'],
                middle_name=self.cleaned_data['middle_name'],
                first_name=self.cleaned_data['first_name']
            )
            self.instance.save()
        return obj

class OrganizationAgentInline(admin.StackedInline):
    fk_name = 'organization'
    model = Agent
    form = OrganizationAgentForm

class OrganizationAccountInline(admin.StackedInline):
    model = BankAccount

#class OrganizationPhoneInline(admin.StackedInline):
#    model = Phone

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [OrganizationAccountInline, OrganizationAgentInline, ]

class CemeteryAdmin(admin.ModelAdmin):
    raw_id_fields = ['organization', 'location', ]
    list_display = ['name', 'organization', 'ordering']
    list_editable = ['ordering']

admin.site.register(Agent)
admin.site.register(Burial)
admin.site.register(Cemetery, CemeteryAdmin)
admin.site.register(DeathCertificate)
admin.site.register(Doverennost)
admin.site.register(Operation)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Location)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(ZAGS)
admin.site.register(IDDocumentType)
admin.site.register(Person, PersonAdmin)
admin.site.register(LogEntry, LogEntryAdmin)