# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Datasets(models.Model):
    name = models.CharField(max_length=64)
    sourcecode = models.CharField(max_length=16, blank=True, null=True)
    source = models.CharField(max_length=64)
    sourceurl = models.CharField(max_length=256)
    datasetname = models.CharField(max_length=16, blank=True, null=True)
    uniqueidformat = models.CharField(max_length=128, blank=True, null=True)
    protected = models.CharField(max_length=3)
    count = models.PositiveSmallIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'datasets'
#

# class AspectsActlog(models.Model):
#     aspects_lookup_id = models.IntegerField()
#     aspects_file_id = models.IntegerField()
#     activitycode = models.CharField(max_length=16)
#     comment = models.CharField(max_length=256)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'aspects_actlog'
#
#
# class AspectsErrors(models.Model):
#     aspects_lookup_id = models.IntegerField()
#     aspects_file_id = models.IntegerField()
#     errorcode = models.CharField(max_length=16)
#     comment = models.CharField(max_length=256)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'aspects_errors'
#
#
# class AspectsFiles(models.Model):
#     aspects_lookup_id = models.IntegerField()
#     file = models.TextField()
#     type = models.CharField(max_length=32)
#     version = models.IntegerField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'aspects_files'
#
#
# class AspectsLookup(models.Model):
#     uniqueid = models.CharField(max_length=128)
#     title = models.CharField(max_length=256)
#     type = models.CharField(max_length=16)
#     graphname = models.CharField(max_length=256)
#     currentversion = models.IntegerField()
#     auth_user_id = models.PositiveIntegerField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'aspects_lookup'
#
#
# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'
#
#
# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)
#
#
# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)
#
#
# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user'
#
#
# class AuthUserGroups(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)
#
#
# class AuthUserUserPermissions(models.Model):
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)
#
#
# class Descriptors(models.Model):
#     substance_id = models.SmallIntegerField()
#     type = models.CharField(max_length=128)
#     value = models.CharField(max_length=500)
#     source = models.CharField(max_length=16, blank=True, null=True)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'descriptors'
#         unique_together = (('substance_id', 'type', 'value', 'source'),)
#
#
# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'
#
#
# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)
#
#
# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'
#
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_session'
#
#
# class FacetsActlog(models.Model):
#     facets_lookup_id = models.IntegerField()
#     facets_file_id = models.IntegerField()
#     activitycode = models.CharField(max_length=16)
#     comment = models.CharField(max_length=256)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'facets_actlog'
#
#
# class FacetsErrors(models.Model):
#     facets_lookup_id = models.IntegerField()
#     facets_file_id = models.IntegerField()
#     errorcode = models.CharField(max_length=16)
#     comment = models.CharField(max_length=256)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'facets_errors'
#
#
# class FacetsFiles(models.Model):
#     facets_lookup_id = models.IntegerField()
#     file = models.TextField()
#     type = models.CharField(max_length=32)
#     version = models.IntegerField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'facets_files'
#
#
# class FacetsLookup(models.Model):
#     uniqueid = models.CharField(max_length=128)
#     title = models.CharField(max_length=256)
#     type = models.CharField(max_length=16)
#     graphname = models.CharField(max_length=256)
#     currentversion = models.IntegerField()
#     auth_user_id = models.PositiveIntegerField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'facets_lookup'
#
#
# class Identifiers(models.Model):
#     substance_id = models.SmallIntegerField()
#     type = models.CharField(max_length=18)
#     value = models.CharField(max_length=750)
#     source = models.CharField(max_length=16, blank=True, null=True)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'identifiers'
#         unique_together = (('type', 'value', 'source'),)
#
#
# class JsonActlog(models.Model):
#     json_lookup_id = models.IntegerField()
#     json_file_id = models.IntegerField()
#     activitycode = models.CharField(max_length=16)
#     comment = models.CharField(max_length=256)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'json_actlog'
#
#
# class JsonAspects(models.Model):
#     json_lookup_id = models.IntegerField()
#     aspects_lookup_id = models.IntegerField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'json_aspects'
#
#
# class JsonErrors(models.Model):
#     json_lookup_id = models.IntegerField(blank=True, null=True)
#     json_file_id = models.IntegerField(blank=True, null=True)
#     errorcode = models.CharField(max_length=128)
#     comment = models.CharField(max_length=256)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'json_errors'
#
#
# class JsonFacets(models.Model):
#     json_lookup_id = models.IntegerField()
#     facets_lookup_id = models.IntegerField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'json_facets'
#
#
# class JsonFiles(models.Model):
#     json_lookup_id = models.IntegerField()
#     file = models.TextField()
#     type = models.CharField(max_length=32)
#     version = models.IntegerField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'json_files'
#
#
# class JsonLookup(models.Model):
#     dataset_id = models.IntegerField()
#     uniqueid = models.CharField(max_length=128)
#     title = models.CharField(max_length=256)
#     graphname = models.CharField(max_length=256)
#     currentversion = models.IntegerField()
#     auth_user_id = models.PositiveIntegerField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'json_lookup'
#
#
# class Metadata(models.Model):
#     table = models.CharField(max_length=128)
#     field = models.CharField(max_length=128)
#     label = models.CharField(max_length=16, blank=True, null=True)
#     ontterm_id = models.SmallIntegerField(blank=True, null=True)
#     sdsection = models.CharField(max_length=11, blank=True, null=True)
#     sdsubsection = models.CharField(max_length=32, blank=True, null=True)
#     sdsubsubsection = models.CharField(max_length=64, blank=True, null=True)
#     category = models.CharField(max_length=64, blank=True, null=True)
#     unit = models.CharField(max_length=32, blank=True, null=True)
#     datatype = models.CharField(max_length=22, blank=True, null=True)
#     output = models.CharField(max_length=6)
#     group = models.CharField(max_length=512, blank=True, null=True)
#     intlinks = models.CharField(max_length=1024, blank=True, null=True)
#     meta = models.CharField(max_length=64, blank=True, null=True)
#     ignore = models.CharField(max_length=32, blank=True, null=True)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'metadata'
#
#
# class Mixtures(models.Model):
#     type = models.CharField(max_length=8, blank=True, null=True)
#     system_id = models.IntegerField()
#     comments = models.CharField(max_length=256, blank=True, null=True)
#     updated = models.DateTimeField()
#     phase = models.CharField(max_length=16, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'mixtures'
#
#
# class Nspaces(models.Model):
#     id = models.SmallAutoField(primary_key=True)
#     name = models.CharField(max_length=64)
#     ns = models.CharField(max_length=8)
#     path = models.CharField(unique=True, max_length=64)
#     homepage = models.CharField(max_length=128)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'nspaces'
#
#
# class Ontterms(models.Model):
#     id = models.SmallAutoField(primary_key=True)
#     title = models.CharField(max_length=256)
#     definition = models.CharField(max_length=2048, blank=True, null=True)
#     code = models.CharField(max_length=64)
#     nspace_id = models.SmallIntegerField()
#     sdsection = models.CharField(max_length=11, blank=True, null=True)
#     sdsubsection = models.CharField(max_length=64, blank=True, null=True)
#     to_remove = models.CharField(max_length=8, blank=True, null=True)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'ontterms'
#
#
# class SocialAuthAssociation(models.Model):
#     server_url = models.CharField(max_length=255)
#     handle = models.CharField(max_length=255)
#     secret = models.CharField(max_length=255)
#     issued = models.IntegerField()
#     lifetime = models.IntegerField()
#     assoc_type = models.CharField(max_length=64)
#
#     class Meta:
#         managed = False
#         db_table = 'social_auth_association'
#         unique_together = (('server_url', 'handle'),)
#
#
# class SocialAuthCode(models.Model):
#     email = models.CharField(max_length=254)
#     code = models.CharField(max_length=32)
#     verified = models.IntegerField()
#     timestamp = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'social_auth_code'
#         unique_together = (('email', 'code'),)
#
#
# class SocialAuthNonce(models.Model):
#     server_url = models.CharField(max_length=255)
#     timestamp = models.IntegerField()
#     salt = models.CharField(max_length=65)
#
#     class Meta:
#         managed = False
#         db_table = 'social_auth_nonce'
#         unique_together = (('server_url', 'timestamp', 'salt'),)
#
#
# class SocialAuthPartial(models.Model):
#     token = models.CharField(max_length=32)
#     next_step = models.PositiveSmallIntegerField()
#     backend = models.CharField(max_length=32)
#     data = models.TextField()
#     timestamp = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'social_auth_partial'
#
#
# class SocialAuthUsersocialauth(models.Model):
#     provider = models.CharField(max_length=32)
#     uid = models.CharField(max_length=255)
#     extra_data = models.TextField()
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     created = models.DateTimeField()
#     modified = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'social_auth_usersocialauth'
#         unique_together = (('provider', 'uid'),)
#
#
# class Sources(models.Model):
#     id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
#     substance = models.ForeignKey('Substances', models.DO_NOTHING)
#     source = models.CharField(max_length=32)
#     result = models.CharField(max_length=1)
#     notes = models.TextField(blank=True, null=True)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'sources'
#
#
# class Substances(models.Model):
#     id = models.SmallAutoField(primary_key=True)
#     name = models.CharField(max_length=1024)
#     formula = models.CharField(max_length=256)
#     molweight = models.FloatField(blank=True, null=True)
#     monomass = models.FloatField(blank=True, null=True)
#     casrn = models.CharField(max_length=16, blank=True, null=True)
#     graphdb = models.CharField(max_length=256, blank=True, null=True)
#     facets_lookup_id = models.IntegerField(blank=True, null=True)
#     comments = models.CharField(max_length=256, blank=True, null=True)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'substances'
#
#
# class SubstancesSystems(models.Model):
#     substance_id = models.SmallIntegerField()
#     system_id = models.SmallIntegerField()
#     role = models.CharField(max_length=13, blank=True, null=True)
#     constituent = models.PositiveIntegerField(blank=True, null=True)
#     mixture_id = models.IntegerField(blank=True, null=True)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'substances_systems'
#
#
# class Systems(models.Model):
#     name = models.CharField(max_length=1024)
#     composition = models.CharField(max_length=19, blank=True, null=True)
#     identifier = models.CharField(max_length=128)
#     substance1_id = models.SmallIntegerField(blank=True, null=True)
#     substance2_id = models.SmallIntegerField(blank=True, null=True)
#     substance3_id = models.SmallIntegerField(blank=True, null=True)
#     substance4_id = models.SmallIntegerField(blank=True, null=True)
#     substance5_id = models.SmallIntegerField(blank=True, null=True)
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'systems'
#
#
# class Templates(models.Model):
#     type = models.CharField(max_length=16)
#     json = models.TextField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'templates'
#
#
# class UsersRequest(models.Model):
#     type = models.CharField(max_length=200)
#     action = models.CharField(max_length=200)
#     content = models.CharField(max_length=200)
#     object = models.CharField(max_length=200)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'users_request'
