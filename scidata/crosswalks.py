# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ccdc(models.Model):
    field = models.CharField(max_length=128)
    ontterm_id = models.SmallIntegerField(blank=True, null=False, primary_key=True)
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=32, blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=32, blank=True, null=True)
    datatype = models.CharField(max_length=64, blank=True, null=True)
    intlinks = models.CharField(max_length=1024, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ccdc'


class Chembl(models.Model):
    table = models.CharField(max_length=128)
    field = models.CharField(max_length=128)
    ontterm_id = models.SmallIntegerField(blank=True, null=False, primary_key=True)
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'chembl'


class Ncct(models.Model):
    database = models.CharField(max_length=64)
    table = models.CharField(max_length=128)
    field = models.CharField(max_length=128)
    ontterm_id = models.SmallIntegerField(blank=True, null=False, primary_key=True)
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ncct'


class Nspaces(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    ns = models.CharField(max_length=8)
    path = models.CharField(unique=True, max_length=64)
    homepage = models.CharField(max_length=128)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'nspaces'


class Ontterms(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    definition = models.CharField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=64)
    url = models.CharField(max_length=512)
    nspace_id = models.SmallIntegerField()
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=64, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ontterms'


class Sol(models.Model):
    field = models.CharField(max_length=128)
    ontterm_id = models.SmallIntegerField(blank=True, null=False, primary_key=True)
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sol'


class Trc(models.Model):
    table = models.CharField(max_length=128)
    field = models.CharField(max_length=256)
    meaning = models.CharField(max_length=128)
    ontlink = models.IntegerField(null=False, primary_key=True)
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'trc'
