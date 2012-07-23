# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cemetery'
        db.create_table('cemetery_cemetery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cemetery', to=orm['organizations.Organization'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Location'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=99, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ordering', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, blank=True)),
        ))
        db.send_create_signal('cemetery', ['Cemetery'])

        # Adding model 'Place'
        db.create_table('cemetery_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cemetery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cemetery.Cemetery'])),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('row', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('seat', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('gps_x', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gps_y', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('rooms', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('cemetery', ['Place'])

        # Adding model 'Operation'
        db.create_table('cemetery_operation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('op_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ordering', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal('cemetery', ['Operation'])

        # Adding model 'Burial'
        db.create_table('cemetery_burial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account_book_n', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('operation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cemetery.Operation'])),
            ('date_fact', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cemetery.Place'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buried', to=orm['persons.Person'])),
            ('client_person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ordr_customer', null=True, to=orm['persons.Person'])),
            ('client_organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ordr_customer', null=True, to=orm['organizations.Organization'])),
            ('doverennost', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['organizations.Doverennost'], null=True)),
            ('agent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='orders', null=True, to=orm['organizations.Agent'])),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.Person'], null=True, blank=True)),
            ('acct_num_str1', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('acct_num_num', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('acct_num_str2', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
            ('print_info', self.gf('django.db.models.fields.TextField')(null=True)),
            ('is_trash', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cemetery', ['Burial'])

        # Adding model 'UserProfile'
        db.create_table('cemetery_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('default_cemetery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cemetery.Cemetery'], null=True, blank=True)),
            ('default_operation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cemetery.Operation'], null=True, blank=True)),
            ('default_country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Country'], null=True, blank=True)),
            ('default_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Region'], null=True, blank=True)),
            ('default_city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.City'], null=True, blank=True)),
            ('records_per_page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('records_order_by', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('catafalque_text', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('naryad_text', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('cemetery', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'Cemetery'
        db.delete_table('cemetery_cemetery')

        # Deleting model 'Place'
        db.delete_table('cemetery_place')

        # Deleting model 'Operation'
        db.delete_table('cemetery_operation')

        # Deleting model 'Burial'
        db.delete_table('cemetery_burial')

        # Deleting model 'UserProfile'
        db.delete_table('cemetery_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cemetery.burial': {
            'Meta': {'object_name': 'Burial'},
            'account_book_n': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'acct_num_num': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'acct_num_str1': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'acct_num_str2': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'orders'", 'null': 'True', 'to': "orm['organizations.Agent']"}),
            'client_organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ordr_customer'", 'null': 'True', 'to': "orm['organizations.Organization']"}),
            'client_person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ordr_customer'", 'null': 'True', 'to': "orm['persons.Person']"}),
            'date_fact': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'doverennost': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['organizations.Doverennost']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cemetery.Operation']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buried'", 'to': "orm['persons.Person']"}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cemetery.Place']"}),
            'print_info': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Person']", 'null': 'True', 'blank': 'True'})
        },
        'cemetery.cemetery': {
            'Meta': {'ordering': "['ordering', 'name']", 'object_name': 'Cemetery'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cemetery'", 'to': "orm['organizations.Organization']"})
        },
        'cemetery.operation': {
            'Meta': {'ordering': "['ordering', 'op_type']", 'object_name': 'Operation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'op_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        'cemetery.place': {
            'Meta': {'object_name': 'Place'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cemetery.Cemetery']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rooms': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'blank': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'seat': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'cemetery.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'catafalque_text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'default_cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cemetery.Cemetery']", 'null': 'True', 'blank': 'True'}),
            'default_city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']", 'null': 'True', 'blank': 'True'}),
            'default_country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'null': 'True', 'blank': 'True'}),
            'default_operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cemetery.Operation']", 'null': 'True', 'blank': 'True'}),
            'default_region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Region']", 'null': 'True', 'blank': 'True'}),
            'naryad_text': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'records_order_by': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'records_per_page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'geo.city': {
            'Meta': {'unique_together': "(('region', 'name'),)", 'object_name': 'City', 'db_table': "'common_geocity'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Region']"})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country', 'db_table': "'common_geocountry'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24', 'db_index': 'True'})
        },
        'geo.location': {
            'Meta': {'object_name': 'Location'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'null': 'True', 'blank': 'True'}),
            'flat': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'post_index': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Region']", 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Street']", 'null': 'True', 'blank': 'True'})
        },
        'geo.region': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'Region', 'db_table': "'common_georegion'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'})
        },
        'geo.street': {
            'Meta': {'ordering': "['city', 'name']", 'unique_together': "(('city', 'name'),)", 'object_name': 'Street'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'db_index': 'True'})
        },
        'organizations.agent': {
            'Meta': {'object_name': 'Agent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agents'", 'to': "orm['organizations.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.Person']"})
        },
        'organizations.doverennost': {
            'Meta': {'object_name': 'Doverennost'},
            'agent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'doverennosti'", 'to': "orm['organizations.Agent']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expire': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'organizations.organization': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organization'},
            'ceo_document': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ceo_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ceo_name_who': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'kpp': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99'}),
            'ogrn': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        },
        'persons.person': {
            'Meta': {'ordering': "['last_name', 'first_name', 'middle_name']", 'object_name': 'Person'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Location']"}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birth_date_no_day': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birth_date_no_month': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['cemetery']