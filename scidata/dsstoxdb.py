# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ChemicalLists(models.Model):
    name = models.CharField(unique=True, max_length=50)
    label = models.CharField(max_length=255)
    long_description = models.TextField(blank=True, null=True)
    ncct_contact = models.CharField(max_length=255)
    source_contact = models.CharField(max_length=255)
    source_contact_email = models.CharField(max_length=255)
    source_website = models.CharField(max_length=1024, blank=True, null=True)
    source_chemical_url_prefix = models.CharField(max_length=1024, blank=True, null=True)
    source_reference = models.CharField(max_length=1024, blank=True, null=True)
    source_doi = models.CharField(max_length=255, blank=True, null=True)
    input_weighting = models.CharField(max_length=255, blank=True, null=True)
    list_type = models.CharField(max_length=255)
    list_update_mechanism = models.CharField(max_length=255)
    list_accessibility = models.CharField(max_length=255)
    curation_complete = models.IntegerField()
    source_data_updated_at = models.DateField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    block_updates = models.IntegerField(blank=True, null=True)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    fk_list_type = models.ForeignKey('ListTypes', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chemical_lists'


class CompoundRelationshipTypes(models.Model):
    name = models.CharField(unique=True, max_length=50)
    label_forward = models.CharField(max_length=255)
    short_description_forward = models.CharField(max_length=500)
    long_description_forward = models.TextField()
    label_backward = models.CharField(max_length=255)
    short_description_backward = models.CharField(max_length=500)
    long_description_backward = models.TextField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'compound_relationship_types'


class CompoundRelationships(models.Model):
    fk_compound_id_predecessor = models.ForeignKey('Compounds', models.DO_NOTHING, db_column='fk_compound_id_predecessor')
    fk_compound_id_successor = models.ForeignKey('Compounds', models.DO_NOTHING, db_column='fk_compound_id_successor')
    source = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    fk_compound_relationship_type = models.ForeignKey(CompoundRelationshipTypes, models.DO_NOTHING, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'compound_relationships'


class Compounds(models.Model):
    dsstox_compound_id = models.CharField(max_length=255, blank=True, null=True)
    chiral_stereo = models.CharField(max_length=255, blank=True, null=True)
    double_stereo = models.CharField(max_length=255, blank=True, null=True)
    chemical_type = models.CharField(max_length=255, blank=True, null=True)
    organic_form = models.CharField(max_length=255, blank=True, null=True)
    mrv_file = models.TextField()
    smiles = models.TextField(blank=True, null=True)
    inchi = models.TextField(blank=True, null=True)
    jchem_inchi_key = models.CharField(unique=True, max_length=255, blank=True, null=True)
    indigo_inchi_key = models.CharField(max_length=255, blank=True, null=True)
    acd_iupac_name = models.CharField(max_length=5000, blank=True, null=True)
    acd_index_name = models.CharField(max_length=5000, blank=True, null=True)
    pubchem_iupac_name = models.CharField(max_length=5000, blank=True, null=True)
    mol_formula = models.CharField(max_length=255, blank=True, null=True)
    mol_weight = models.FloatField(blank=True, null=True)
    monoisotopic_mass = models.FloatField(blank=True, null=True)
    fragment_count = models.IntegerField(blank=True, null=True)
    has_defined_isotope = models.IntegerField(blank=True, null=True)
    radical_count = models.IntegerField(blank=True, null=True)
    pubchem_cid = models.IntegerField(blank=True, null=True)
    chemspider_id = models.IntegerField(blank=True, null=True)
    chebi_id = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    mol_image_png = models.TextField(blank=True, null=True)
    has_stereochemistry = models.IntegerField(blank=True, null=True)
    pubchem_sources = models.IntegerField(blank=True, null=True)
    indigo_inchi = models.TextField(blank=True, null=True)
    jchem_inchi = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compounds'


class GenericSubstanceCompounds(models.Model):
    fk_generic_substance = models.ForeignKey('GenericSubstances', models.DO_NOTHING, blank=True, null=True)
    fk_compound = models.ForeignKey(Compounds, models.DO_NOTHING, blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'generic_substance_compounds'


class GenericSubstances(models.Model):
    fk_qc_level = models.ForeignKey('QcLevels', models.DO_NOTHING, blank=True, null=True)
    dsstox_substance_id = models.CharField(max_length=255, blank=True, null=True)
    casrn = models.CharField(unique=True, max_length=255)
    preferred_name = models.CharField(unique=True, max_length=255)
    substance_type = models.CharField(max_length=255)
    qc_notes = models.CharField(max_length=1024, blank=True, null=True)
    qc_notes_private = models.CharField(max_length=1024, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'generic_substances'


class ListTypes(models.Model):
    name = models.CharField(unique=True, max_length=50)
    label = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'list_types'


class OtherCasrns(models.Model):
    fk_generic_substance = models.ForeignKey(GenericSubstances, models.DO_NOTHING)
    casrn = models.CharField(max_length=255)
    cas_type = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    qc_notes = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'other_casrns'


class QcLevels(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'qc_levels'


class SchemaChanges(models.Model):
    filename = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schema_changes'


class SchemaDataCopy(models.Model):
    filename_yaml = models.CharField(max_length=255)
    dbms_src = models.CharField(max_length=255)
    dbms_dst = models.CharField(max_length=255)
    db_src = models.CharField(max_length=255)
    db_dst = models.CharField(max_length=255)
    number_of_tables_src = models.IntegerField()
    number_of_tables_dst = models.IntegerField()
    success = models.IntegerField()
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schema_data_copy'


class SchemaMigrations(models.Model):
    version = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'schema_migrations'


class SourceGenericSubstanceMappings(models.Model):
    fk_source_substance = models.ForeignKey('SourceSubstances', models.DO_NOTHING, blank=True, null=True)
    fk_generic_substance = models.ForeignKey(GenericSubstances, models.DO_NOTHING, blank=True, null=True)
    connection_reason = models.CharField(max_length=255, blank=True, null=True)
    linkage_score = models.FloatField(blank=True, null=True)
    curator_validated = models.IntegerField(blank=True, null=True)
    qc_notes = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'source_generic_substance_mappings'


class SourceSubstanceIdentifiers(models.Model):
    fk_source_substance = models.ForeignKey('SourceSubstances', models.DO_NOTHING, blank=True, null=True)
    identifier = models.CharField(max_length=1024, blank=True, null=True)
    identifier_type = models.CharField(max_length=255, blank=True, null=True)
    fk_source_substance_identifier_parent = models.ForeignKey('self', models.DO_NOTHING, db_column='fk_source_substance_identifier_parent', blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    label = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_substance_identifiers'


class SourceSubstances(models.Model):
    fk_chemical_list = models.ForeignKey(ChemicalLists, models.DO_NOTHING, blank=True, null=True)
    dsstox_record_id = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    warnings = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    qc_notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_substances'


class SubstanceRelationshipTypes(models.Model):
    name = models.CharField(unique=True, max_length=50)
    label_forward = models.CharField(max_length=255)
    short_description_forward = models.CharField(max_length=500)
    long_description_forward = models.TextField()
    label_backward = models.CharField(max_length=255)
    short_description_backward = models.CharField(max_length=500)
    long_description_backward = models.TextField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'substance_relationship_types'


class SubstanceRelationships(models.Model):
    fk_generic_substance_id_predecessor = models.ForeignKey(GenericSubstances, models.DO_NOTHING, db_column='fk_generic_substance_id_predecessor', blank=True, null=True)
    fk_generic_substance_id_successor = models.ForeignKey(GenericSubstances, models.DO_NOTHING, db_column='fk_generic_substance_id_successor', blank=True, null=True)
    relationship = models.CharField(max_length=255, blank=True, null=True)
    fk_substance_relationship_type = models.ForeignKey(SubstanceRelationshipTypes, models.DO_NOTHING, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    qc_notes = models.CharField(max_length=1024, blank=True, null=True)
    mixture_percentage = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    percentage_type = models.CharField(max_length=255, blank=True, null=True)
    is_nearest_structure = models.IntegerField(blank=True, null=True)
    is_nearest_casrn = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'substance_relationships'


class SynonymMv(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_generic_substance = models.ForeignKey(GenericSubstances, models.DO_NOTHING, blank=True, null=True)
    identifier = models.CharField(max_length=2000, blank=True, null=True)
    synonym_type = models.CharField(max_length=50, blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'synonym_mv'


class Synonyms(models.Model):
    fk_generic_substance = models.ForeignKey(GenericSubstances, models.DO_NOTHING)
    identifier = models.CharField(max_length=1024)
    synonym_quality = models.CharField(max_length=255)
    synonym_type = models.CharField(max_length=255, blank=True, null=True)
    qc_notes = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    source = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'synonyms'
