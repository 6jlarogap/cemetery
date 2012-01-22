# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Agent.dover_date'
        db.alter_column('common_agent', 'dover_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Agent.dover_expire'
        db.alter_column('common_agent', 'dover_expire', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Agent.dover_number'
        db.alter_column('common_agent', 'dover_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Agent.dover_date'
        raise RuntimeError("Cannot reverse this migration. 'Agent.dover_date' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Agent.dover_expire'
        raise RuntimeError("Cannot reverse this migration. 'Agent.dover_expire' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Agent.dover_number'
        raise RuntimeError("Cannot reverse this migration. 'Agent.dover_number' and its values cannot be restored.")


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
        'common.agent': {
            'Meta': {'object_name': 'Agent'},
            'dover_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dover_expire': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dover_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agents'", 'to': "orm['common.Organization']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'is_agent_of'", 'to': "orm['common.Person']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'bankname': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'bik': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ks': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Organization']"}),
            'rs': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'common.burial': {
            'Meta': {'object_name': 'Burial', '_ormbases': ['common.Order']},
            'account_book_n': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'exhumated_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_sync_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'order_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Order']", 'unique': 'True', 'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buried'", 'to': "orm['common.Person']"})
        },
        'common.burial1': {
            'Meta': {'managed': 'False', 'object_name': 'Burial1', '_ormbases': ['common.Order']},
            'account_book_n': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'order_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Order']", 'unique': 'True', 'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Person']"}),
            's1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            's2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            's3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'common.cemetery': {
            'Meta': {'object_name': 'Cemetery'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_sync_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cemetery'", 'to': "orm['common.Organization']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.deathcertificate': {
            'Meta': {'object_name': 'DeathCertificate'},
            'release_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            's_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'series': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'soul': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'zags': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ZAGS']", 'null': 'True', 'blank': 'True'})
        },
        'common.email': {
            'Meta': {'object_name': 'Email'},
            'e_addr': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.env': {
            'Meta': {'object_name': 'Env'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'common.geocity': {
            'Meta': {'unique_together': "(('region', 'name'),)", 'object_name': 'GeoCity'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCountry']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoRegion']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.geocountry': {
            'Meta': {'ordering': "['name']", 'object_name': 'GeoCountry'},
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.georegion': {
            'Meta': {'unique_together': "(('country', 'name'),)", 'object_name': 'GeoRegion'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCountry']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.impbur': {
            'Meta': {'object_name': 'ImpBur'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bur_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'burial_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ImpCem']"}),
            'deadman_pk': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seat': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'common.impcem': {
            'Meta': {'object_name': 'ImpCem'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'cem_pk': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'f_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'blank': 'True'}),
            'post_index': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '99', 'blank': 'True'})
        },
        'common.location': {
            'Meta': {'object_name': 'Location'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'flat': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'post_index': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Street']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.media': {
            'Meta': {'object_name': 'Media'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.metro': {
            'Meta': {'ordering': "['city', 'name']", 'object_name': 'Metro'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCity']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.operation': {
            'Meta': {'object_name': 'Operation'},
            'op_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.order': {
            'Meta': {'object_name': 'Order'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': "orm['common.Soul']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordr_customer'", 'to': "orm['common.Soul']"}),
            'date_fact': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_plan': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'doer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'doerorder'", 'null': 'True', 'to': "orm['common.Soul']"}),
            'is_trash': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Operation']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': "orm['common.Product']"}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ordr_responsible'", 'to': "orm['common.Soul']"}),
            'responsible_agent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Agent']", 'null': 'True', 'blank': 'True'}),
            'responsible_customer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ordr_responsible_customer'", 'null': 'True', 'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.ordercomments': {
            'Meta': {'ordering': "['date_of_creation']", 'object_name': 'OrderComments'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Order']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.orderfiles': {
            'Meta': {'object_name': 'OrderFiles'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '96', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']", 'null': 'True'}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ofile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Order']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.organization': {
            'Meta': {'ordering': "['uuid']", 'object_name': 'Organization', '_ormbases': ['common.Soul']},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'kpp': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99'}),
            'ogrn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'soul_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True', 'primary_key': 'True'})
        },
        'common.person': {
            'Meta': {'ordering': "['uuid']", 'object_name': 'Person', '_ormbases': ['common.Soul']},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['common.Role']", 'through': "orm['common.PersonRole']", 'symmetrical': 'False'}),
            'soul_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True', 'primary_key': 'True'})
        },
        'common.personrole': {
            'Meta': {'unique_together': "(('person', 'role'),)", 'object_name': 'PersonRole'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hire_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'personrole'", 'to': "orm['common.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Role']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.phone': {
            'Meta': {'unique_together': "(('soul', 'f_number'),)", 'object_name': 'Phone'},
            'f_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.place': {
            'Meta': {'unique_together': "(('cemetery', 'area', 'row', 'seat'),)", 'object_name': 'Place', '_ormbases': ['common.Product']},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Cemetery']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seat': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'common.place1': {
            'Meta': {'managed': 'False', 'object_name': 'Place1', '_ormbases': ['common.Product']},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Cemetery']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {}),
            'gps_x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gps_z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            's1': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            's2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            's3': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            's4': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            's5': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            's6': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            's7': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            's8': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            's9': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'seat': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'common.product': {
            'Meta': {'object_name': 'Product'},
            'measure': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'p_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ProductType']"}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.productcomments': {
            'Meta': {'ordering': "['date_of_creation']", 'object_name': 'ProductComments'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Product']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.productfiles': {
            'Meta': {'object_name': 'ProductFiles'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']", 'null': 'True'}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'pfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Product']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.producttype': {
            'Meta': {'object_name': 'ProductType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.role': {
            'Meta': {'object_name': 'Role'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'djgroups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orgrole'", 'to': "orm['common.Organization']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.roletree': {
            'Meta': {'object_name': 'RoleTree'},
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rltree_master'", 'to': "orm['common.Role']"}),
            'slave': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rltree_slave'", 'to': "orm['common.Role']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.soul': {
            'Meta': {'ordering': "['uuid']", 'object_name': 'Soul'},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']", 'null': 'True', 'blank': 'True'}),
            'date_of_creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'death_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Location']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.soulproducttypeoperation': {
            'Meta': {'unique_together': "(('soul', 'p_type', 'operation'),)", 'object_name': 'SoulProducttypeOperation'},
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Operation']"}),
            'p_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.ProductType']"}),
            'soul': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Soul']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.street': {
            'Meta': {'ordering': "['city', 'name']", 'unique_together': "(('city', 'name'),)", 'object_name': 'Street'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCity']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
        },
        'common.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'default_cemetery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Cemetery']", 'null': 'True', 'blank': 'True'}),
            'default_city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCity']", 'null': 'True', 'blank': 'True'}),
            'default_country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoCountry']", 'null': 'True', 'blank': 'True'}),
            'default_operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Operation']", 'null': 'True', 'blank': 'True'}),
            'default_region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.GeoRegion']", 'null': 'True', 'blank': 'True'}),
            'records_order_by': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'records_per_page': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'soul': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'common.zags': {
            'Meta': {'object_name': 'ZAGS'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']