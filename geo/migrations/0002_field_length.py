# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Region.name'
        db.alter_column('common_georegion', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'City.name'
        db.alter_column('common_geocity', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Country.name'
        db.alter_column('common_geocountry', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

        # Changing field 'Location.building'
        db.alter_column('geo_location', 'building', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Location.flat'
        db.alter_column('geo_location', 'flat', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Location.post_index'
        db.alter_column('geo_location', 'post_index', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Location.house'
        db.alter_column('geo_location', 'house', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Location.block'
        db.alter_column('geo_location', 'block', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Street.name'
        db.alter_column('geo_street', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'Region.name'
        db.alter_column('common_georegion', 'name', self.gf('django.db.models.fields.CharField')(max_length=36))

        # Changing field 'City.name'
        db.alter_column('common_geocity', 'name', self.gf('django.db.models.fields.CharField')(max_length=36))

        # Changing field 'Country.name'
        db.alter_column('common_geocountry', 'name', self.gf('django.db.models.fields.CharField')(max_length=24, unique=True))

        # Changing field 'Location.building'
        db.alter_column('geo_location', 'building', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Location.flat'
        db.alter_column('geo_location', 'flat', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Location.post_index'
        db.alter_column('geo_location', 'post_index', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Location.house'
        db.alter_column('geo_location', 'house', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Location.block'
        db.alter_column('geo_location', 'block', self.gf('django.db.models.fields.CharField')(max_length=16))

        # Changing field 'Street.name'
        db.alter_column('geo_street', 'name', self.gf('django.db.models.fields.CharField')(max_length=99))

    models = {
        'geo.city': {
            'Meta': {'unique_together': "(('region', 'name'),)", 'object_name': 'City', 'db_table': "'common_geocity'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Region']"})
        },
        'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country', 'db_table': "'common_geocountry'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'geo.location': {
            'Meta': {'object_name': 'Location'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']", 'null': 'True', 'blank': 'True'}),
            'flat': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'post_index': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Region']", 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Street']", 'null': 'True', 'blank': 'True'})
        },
        'geo.region': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'Region', 'db_table': "'common_georegion'"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'geo.street': {
            'Meta': {'ordering': "['city', 'name']", 'unique_together': "(('city', 'name'),)", 'object_name': 'Street'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['geo']