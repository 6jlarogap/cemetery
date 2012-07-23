# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IDDocumentType'
        db.create_table('persons_iddocumenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('persons', ['IDDocumentType'])

        # Adding model 'Person'
        db.create_table('persons_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('birth_date_no_month', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('birth_date_no_day', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('death_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Location'])),
        ))
        db.send_create_signal('persons', ['Person'])

        # Adding model 'DocumentSource'
        db.create_table('persons_documentsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('persons', ['DocumentSource'])

        # Adding model 'PersonID'
        db.create_table('persons_personid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['persons.Person'], unique=True)),
            ('id_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.IDDocumentType'])),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.DocumentSource'], null=True, blank=True)),
            ('when', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('persons', ['PersonID'])

        # Adding model 'ZAGS'
        db.create_table('persons_zags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('persons', ['ZAGS'])

        # Adding model 'DeathCertificate'
        db.create_table('persons_deathcertificate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['persons.Person'], unique=True)),
            ('s_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('series', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('release_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('zags', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['persons.ZAGS'], null=True)),
        ))
        db.send_create_signal('persons', ['DeathCertificate'])


    def backwards(self, orm):
        # Deleting model 'IDDocumentType'
        db.delete_table('persons_iddocumenttype')

        # Deleting model 'Person'
        db.delete_table('persons_person')

        # Deleting model 'DocumentSource'
        db.delete_table('persons_documentsource')

        # Deleting model 'PersonID'
        db.delete_table('persons_personid')

        # Deleting model 'ZAGS'
        db.delete_table('persons_zags')

        # Deleting model 'DeathCertificate'
        db.delete_table('persons_deathcertificate')


    models = {
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
        'persons.deathcertificate': {
            'Meta': {'object_name': 'DeathCertificate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['persons.Person']", 'unique': 'True'}),
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            's_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'zags': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.ZAGS']", 'null': 'True'})
        },
        'persons.documentsource': {
            'Meta': {'object_name': 'DocumentSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'persons.iddocumenttype': {
            'Meta': {'object_name': 'IDDocumentType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        },
        'persons.personid': {
            'Meta': {'object_name': 'PersonID'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.IDDocumentType']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['persons.Person']", 'unique': 'True'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['persons.DocumentSource']", 'null': 'True', 'blank': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'persons.zags': {
            'Meta': {'ordering': "['name']", 'object_name': 'ZAGS'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['persons']