# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GeoCountry'
        db.create_table('common_geocountry', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=24, db_index=True)),
        ))
        db.send_create_signal('common', ['GeoCountry'])

        # Adding model 'GeoRegion'
        db.create_table('common_georegion', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeoCountry'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=36, db_index=True)),
        ))
        db.send_create_signal('common', ['GeoRegion'])

        # Adding unique constraint on 'GeoRegion', fields ['country', 'name']
        db.create_unique('common_georegion', ['country_id', 'name'])

        # Adding model 'GeoCity'
        db.create_table('common_geocity', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeoCountry'])),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeoRegion'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=36, db_index=True)),
        ))
        db.send_create_signal('common', ['GeoCity'])

        # Adding unique constraint on 'GeoCity', fields ['region', 'name']
        db.create_unique('common_geocity', ['region_id', 'name'])

        # Adding model 'Metro'
        db.create_table('common_metro', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeoCity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=99)),
        ))
        db.send_create_signal('common', ['Metro'])

        # Adding model 'Street'
        db.create_table('common_street', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeoCity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=99, db_index=True)),
        ))
        db.send_create_signal('common', ['Street'])

        # Adding unique constraint on 'Street', fields ['city', 'name']
        db.create_unique('common_street', ['city_id', 'name'])

        # Adding model 'Location'
        db.create_table('common_location', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('post_index', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('street', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Street'], null=True, blank=True)),
            ('house', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('block', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('flat', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('gps_x', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gps_y', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gps_z', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('common', ['Location'])

        # Adding model 'Soul'
        db.create_table('common_soul', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('death_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Location'], null=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'], null=True, blank=True)),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['Soul'])

        # Adding model 'Phone'
        db.create_table('common_phone', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('soul', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('f_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('common', ['Phone'])

        # Adding unique constraint on 'Phone', fields ['soul', 'f_number']
        db.create_unique('common_phone', ['soul_id', 'f_number'])

        # Adding model 'Email'
        db.create_table('common_email', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('soul', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('e_addr', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('common', ['Email'])

        # Adding model 'Person'
        db.create_table('common_person', (
            ('soul_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Soul'], unique=True, primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('patronymic', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('common', ['Person'])

        # Adding model 'DeathCertificate'
        db.create_table('common_deathcertificate', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('soul', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Soul'], unique=True)),
            ('s_number', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal('common', ['DeathCertificate'])

        # Adding model 'Organization'
        db.create_table('common_organization', (
            ('soul_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Soul'], unique=True, primary_key=True)),
            ('ogrn', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('inn', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=99)),
        ))
        db.send_create_signal('common', ['Organization'])

        # Adding model 'Role'
        db.create_table('common_role', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orgrole', to=orm['common.Organization'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['Role'])

        # Adding M2M table for field djgroups on 'Role'
        db.create_table('common_role_djgroups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('role', models.ForeignKey(orm['common.role'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('common_role_djgroups', ['role_id', 'group_id'])

        # Adding model 'RoleTree'
        db.create_table('common_roletree', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rltree_master', to=orm['common.Role'])),
            ('slave', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rltree_slave', to=orm['common.Role'])),
        ))
        db.send_create_signal('common', ['RoleTree'])

        # Adding model 'PersonRole'
        db.create_table('common_personrole', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='personrole', to=orm['common.Person'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Role'])),
            ('hire_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('discharge_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['PersonRole'])

        # Adding unique constraint on 'PersonRole', fields ['person', 'role']
        db.create_unique('common_personrole', ['person_id', 'role_id'])

        # Adding model 'Cemetery'
        db.create_table('common_cemetery', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cemetery', to=orm['common.Organization'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Location'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=99, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_sync_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2000, 1, 1, 0, 0))),
        ))
        db.send_create_signal('common', ['Cemetery'])

        # Adding model 'ProductType'
        db.create_table('common_producttype', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=24)),
        ))
        db.send_create_signal('common', ['ProductType'])

        # Adding model 'Product'
        db.create_table('common_product', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('soul', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('measure', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('p_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.ProductType'])),
        ))
        db.send_create_signal('common', ['Product'])

        # Adding model 'ProductFiles'
        db.create_table('common_productfiles', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Product'])),
            ('pfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'], null=True)),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['ProductFiles'])

        # Adding model 'ProductComments'
        db.create_table('common_productcomments', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Product'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['ProductComments'])

        # Adding model 'Place'
        db.create_table('common_place', (
            ('product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Product'], unique=True, primary_key=True)),
            ('cemetery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Cemetery'])),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('row', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('seat', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('gps_x', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gps_y', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gps_z', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['Place'])

        # Adding unique constraint on 'Place', fields ['cemetery', 'area', 'row', 'seat']
        db.create_unique('common_place', ['cemetery_id', 'area', 'row', 'seat'])

        # Adding model 'Operation'
        db.create_table('common_operation', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('op_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('common', ['Operation'])

        # Adding model 'Order'
        db.create_table('common_order', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ordr_responsible', to=orm['common.Soul'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ordr_customer', to=orm['common.Soul'])),
            ('doer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='doerorder', null=True, to=orm['common.Soul'])),
            ('date_plan', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_fact', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', to=orm['common.Product'])),
            ('operation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Operation'])),
            ('is_trash', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', to=orm['common.Soul'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['Order'])

        # Adding model 'OrderFiles'
        db.create_table('common_orderfiles', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Order'])),
            ('ofile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=96, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'], null=True)),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['OrderFiles'])

        # Adding model 'OrderComments'
        db.create_table('common_ordercomments', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Order'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('date_of_creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('common', ['OrderComments'])

        # Adding model 'Burial'
        db.create_table('common_burial', (
            ('order_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Order'], unique=True, primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='buried', to=orm['common.Person'])),
            ('account_book_n', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('last_sync_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2000, 1, 1, 0, 0))),
        ))
        db.send_create_signal('common', ['Burial'])

        # Adding model 'UserProfile'
        db.create_table('common_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('soul', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.Soul'], unique=True)),
            ('default_cemetery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Cemetery'], null=True, blank=True)),
            ('default_operation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Operation'], null=True, blank=True)),
            ('default_country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeoCountry'], null=True, blank=True)),
            ('default_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeoRegion'], null=True, blank=True)),
            ('default_city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.GeoCity'], null=True, blank=True)),
            ('records_per_page', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('records_order_by', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('common', ['UserProfile'])

        # Adding model 'SoulProducttypeOperation'
        db.create_table('common_soulproducttypeoperation', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('soul', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('p_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.ProductType'])),
            ('operation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Operation'])),
        ))
        db.send_create_signal('common', ['SoulProducttypeOperation'])

        # Adding unique constraint on 'SoulProducttypeOperation', fields ['soul', 'p_type', 'operation']
        db.create_unique('common_soulproducttypeoperation', ['soul_id', 'p_type_id', 'operation_id'])

        # Adding model 'Env'
        db.create_table('common_env', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
        ))
        db.send_create_signal('common', ['Env'])

        # Adding model 'ImpCem'
        db.create_table('common_impcem', (
            ('cem_pk', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=99, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=99, blank=True)),
            ('post_index', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('house', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('block', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('f_number', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
        ))
        db.send_create_signal('common', ['ImpCem'])

        # Adding model 'ImpBur'
        db.create_table('common_impbur', (
            ('deadman_pk', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('bur_pk', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('patronymic', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('death_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('burial_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cemetery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.ImpCem'])),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('row', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('seat', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('gps_x', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gps_y', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('gps_z', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('common', ['ImpBur'])

        # Adding model 'Media'
        db.create_table('common_media', (
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('soul', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Soul'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('common', ['Media'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'SoulProducttypeOperation', fields ['soul', 'p_type', 'operation']
        db.delete_unique('common_soulproducttypeoperation', ['soul_id', 'p_type_id', 'operation_id'])

        # Removing unique constraint on 'Place', fields ['cemetery', 'area', 'row', 'seat']
        db.delete_unique('common_place', ['cemetery_id', 'area', 'row', 'seat'])

        # Removing unique constraint on 'PersonRole', fields ['person', 'role']
        db.delete_unique('common_personrole', ['person_id', 'role_id'])

        # Removing unique constraint on 'Phone', fields ['soul', 'f_number']
        db.delete_unique('common_phone', ['soul_id', 'f_number'])

        # Removing unique constraint on 'Street', fields ['city', 'name']
        db.delete_unique('common_street', ['city_id', 'name'])

        # Removing unique constraint on 'GeoCity', fields ['region', 'name']
        db.delete_unique('common_geocity', ['region_id', 'name'])

        # Removing unique constraint on 'GeoRegion', fields ['country', 'name']
        db.delete_unique('common_georegion', ['country_id', 'name'])

        # Deleting model 'GeoCountry'
        db.delete_table('common_geocountry')

        # Deleting model 'GeoRegion'
        db.delete_table('common_georegion')

        # Deleting model 'GeoCity'
        db.delete_table('common_geocity')

        # Deleting model 'Metro'
        db.delete_table('common_metro')

        # Deleting model 'Street'
        db.delete_table('common_street')

        # Deleting model 'Location'
        db.delete_table('common_location')

        # Deleting model 'Soul'
        db.delete_table('common_soul')

        # Deleting model 'Phone'
        db.delete_table('common_phone')

        # Deleting model 'Email'
        db.delete_table('common_email')

        # Deleting model 'Person'
        db.delete_table('common_person')

        # Deleting model 'DeathCertificate'
        db.delete_table('common_deathcertificate')

        # Deleting model 'Organization'
        db.delete_table('common_organization')

        # Deleting model 'Role'
        db.delete_table('common_role')

        # Removing M2M table for field djgroups on 'Role'
        db.delete_table('common_role_djgroups')

        # Deleting model 'RoleTree'
        db.delete_table('common_roletree')

        # Deleting model 'PersonRole'
        db.delete_table('common_personrole')

        # Deleting model 'Cemetery'
        db.delete_table('common_cemetery')

        # Deleting model 'ProductType'
        db.delete_table('common_producttype')

        # Deleting model 'Product'
        db.delete_table('common_product')

        # Deleting model 'ProductFiles'
        db.delete_table('common_productfiles')

        # Deleting model 'ProductComments'
        db.delete_table('common_productcomments')

        # Deleting model 'Place'
        db.delete_table('common_place')

        # Deleting model 'Operation'
        db.delete_table('common_operation')

        # Deleting model 'Order'
        db.delete_table('common_order')

        # Deleting model 'OrderFiles'
        db.delete_table('common_orderfiles')

        # Deleting model 'OrderComments'
        db.delete_table('common_ordercomments')

        # Deleting model 'Burial'
        db.delete_table('common_burial')

        # Deleting model 'UserProfile'
        db.delete_table('common_userprofile')

        # Deleting model 'SoulProducttypeOperation'
        db.delete_table('common_soulproducttypeoperation')

        # Deleting model 'Env'
        db.delete_table('common_env')

        # Deleting model 'ImpCem'
        db.delete_table('common_impcem')

        # Deleting model 'ImpBur'
        db.delete_table('common_impbur')

        # Deleting model 'Media'
        db.delete_table('common_media')


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
        'common.burial': {
            'Meta': {'object_name': 'Burial', '_ormbases': ['common.Order']},
            'account_book_n': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
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
            's_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'soul': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['common.Soul']", 'unique': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'})
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
            'inn': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '99'}),
            'ogrn': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['common.Location']", 'null': 'True', 'blank': 'True'}),
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['common']
