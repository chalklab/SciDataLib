# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActionType(models.Model):
    action_type = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=200)
    parent_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action_type'


class Activities(models.Model):
    activity_id = models.BigIntegerField(primary_key=True)
    assays = models.ForeignKey('Assays', models.DO_NOTHING, db_column='assay_id')
    docs = models.ForeignKey('Docs', models.DO_NOTHING, related_name='activities', blank=True, null=True, db_column='doc_id')
    compound_records = models.ForeignKey('CompoundRecords', models.DO_NOTHING, db_column='record_id')
    # molregno = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', blank=True, null=True)
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', blank=True, null=True)
    standard_relation = models.CharField(max_length=50, blank=True, null=True)
    standard_value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    standard_units = models.CharField(max_length=100, blank=True, null=True)
    standard_flag = models.IntegerField(blank=True, null=True)
    standard_type = models.CharField(max_length=250, blank=True, null=True)
    activity_comment = models.CharField(max_length=4000, blank=True, null=True)
    data_validity_lookup = models.ForeignKey('DataValidityLookup', models.DO_NOTHING, db_column='data_validity_comment', blank=True, null=True)
    potential_duplicate = models.IntegerField(blank=True, null=True)
    pchembl_value = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    bioassay_ontology = models.ForeignKey('BioassayOntology', models.DO_NOTHING, db_column='bao_endpoint', blank=True, null=True)
    uo_units = models.CharField(max_length=10, blank=True, null=True)
    qudt_units = models.CharField(max_length=70, blank=True, null=True)
    toid = models.IntegerField(blank=True, null=True)
    upper_value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    standard_upper_value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    source = models.ForeignKey('Source', models.DO_NOTHING, blank=True, null=True, db_column='src_id')
    type = models.CharField(max_length=250)
    relation = models.CharField(max_length=50, blank=True, null=True)
    value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    units = models.CharField(max_length=100, blank=True, null=True)
    text_value = models.CharField(max_length=1000, blank=True, null=True)
    standard_text_value = models.CharField(max_length=1000, blank=True, null=True)
    herg = models.IntegerField(blank=True, null=True)
    ace = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activities'


class ActivityProperties(models.Model):
    ap_id = models.BigIntegerField(primary_key=True)
    activities = models.ForeignKey(Activities, models.DO_NOTHING, db_column="activity_id")
    type = models.CharField(max_length=250)
    relation = models.CharField(max_length=50, blank=True, null=True)
    value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    units = models.CharField(max_length=100, blank=True, null=True)
    text_value = models.CharField(max_length=1000, blank=True, null=True)
    standard_type = models.CharField(max_length=250, blank=True, null=True)
    standard_relation = models.CharField(max_length=50, blank=True, null=True)
    standard_value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    standard_units = models.CharField(max_length=100, blank=True, null=True)
    standard_text_value = models.CharField(max_length=1000, blank=True, null=True)
    comments = models.CharField(max_length=4000, blank=True, null=True)
    result_flag = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'activity_properties'
        unique_together = (('activities', 'type'),)


class ActivitySmid(models.Model):
    smid = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'activity_smid'


class ActivityStdsLookup(models.Model):
    std_act_id = models.BigIntegerField(primary_key=True)
    standard_type = models.CharField(max_length=250)
    definition = models.CharField(max_length=500, blank=True, null=True)
    standard_units = models.CharField(max_length=100)
    normal_range_min = models.DecimalField(max_digits=24, decimal_places=12, blank=True, null=True)
    normal_range_max = models.DecimalField(max_digits=24, decimal_places=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_stds_lookup'
        unique_together = (('standard_type', 'standard_units'),)


class ActivitySupp(models.Model):
    as_id = models.BigIntegerField(primary_key=True)
    rgid = models.BigIntegerField()
    activity_smid = models.ForeignKey(ActivitySmid, models.DO_NOTHING, db_column='smid', blank=True, null=True)
    type = models.CharField(max_length=250)
    relation = models.CharField(max_length=50, blank=True, null=True)
    value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    units = models.CharField(max_length=100, blank=True, null=True)
    text_value = models.CharField(max_length=1000, blank=True, null=True)
    standard_type = models.CharField(max_length=250, blank=True, null=True)
    standard_relation = models.CharField(max_length=50, blank=True, null=True)
    standard_value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    standard_units = models.CharField(max_length=100, blank=True, null=True)
    standard_text_value = models.CharField(max_length=1000, blank=True, null=True)
    comments = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_supp'
        unique_together = (('rgid', 'type'),)


class ActivitySuppMap(models.Model):
    actsm_id = models.BigIntegerField(primary_key=True)
    activities = models.ForeignKey(Activities, models.DO_NOTHING, db_column="activity_id")
    activity_smid = models.ForeignKey(ActivitySmid, models.DO_NOTHING, db_column='smid')

    class Meta:
        managed = False
        db_table = 'activity_supp_map'


class AssayClassMap(models.Model):
    ass_cls_map_id = models.BigIntegerField(primary_key=True)
    assays = models.ForeignKey('Assays', models.DO_NOTHING, db_column='assay_id')
    assay_classification = models.ForeignKey('AssayClassification', models.DO_NOTHING, db_column='assay_class_id')

    class Meta:
        managed = False
        db_table = 'assay_class_map'
        unique_together = (('assaysZ', 'assay_classification'),)


class AssayClassification(models.Model):
    assay_class_id = models.BigIntegerField(primary_key=True)
    l1 = models.CharField(max_length=100, blank=True, null=True)
    l2 = models.CharField(max_length=100, blank=True, null=True)
    l3 = models.CharField(unique=True, max_length=1000, blank=True, null=True)
    class_type = models.CharField(max_length=50, blank=True, null=True)
    bao_id = models.CharField(max_length=11, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assay_classification'


class AssayParameters(models.Model):
    assay_param_id = models.BigIntegerField(primary_key=True)
    assays = models.ForeignKey('Assays', models.DO_NOTHING, db_column="assay_id")
    type = models.CharField(max_length=250)
    relation = models.CharField(max_length=50, blank=True, null=True)
    value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    units = models.CharField(max_length=100, blank=True, null=True)
    text_value = models.CharField(max_length=4000, blank=True, null=True)
    standard_type = models.CharField(max_length=250, blank=True, null=True)
    standard_relation = models.CharField(max_length=50, blank=True, null=True)
    standard_value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)
    standard_units = models.CharField(max_length=100, blank=True, null=True)
    standard_text_value = models.CharField(max_length=4000, blank=True, null=True)
    comments = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assay_parameters'
        unique_together = (('assay', 'type'),)


class AssayType(models.Model):
    assay_type = models.CharField(primary_key=True, max_length=1)
    assay_desc = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assay_type'


class Assays(models.Model):
    assay_id = models.BigIntegerField(primary_key=True)
    docs = models.ForeignKey('Docs', models.DO_NOTHING, db_column="doc_id")
    description = models.CharField(max_length=4000, blank=True, null=True)
    assay_type = models.ForeignKey(AssayType, models.DO_NOTHING, db_column='assay_type', blank=True, null=True)
    assay_test_type = models.CharField(max_length=20, blank=True, null=True)
    assay_category = models.CharField(max_length=20, blank=True, null=True)
    assay_organism = models.CharField(max_length=250, blank=True, null=True)
    assay_tax_id = models.BigIntegerField(blank=True, null=True)
    assay_strain = models.CharField(max_length=200, blank=True, null=True)
    assay_tissue = models.CharField(max_length=100, blank=True, null=True)
    assay_cell_type = models.CharField(max_length=100, blank=True, null=True)
    assay_subcellular_fraction = models.CharField(max_length=100, blank=True, null=True)
    target_dictionary = models.ForeignKey('TargetDictionary', models.DO_NOTHING, db_column='tid', blank=True, null=True)
    relationship_type = models.ForeignKey('RelationshipType', models.DO_NOTHING, db_column='relationship_type', blank=True, null=True)
    confidence_score = models.ForeignKey('ConfidenceScoreLookup', models.DO_NOTHING, db_column='confidence_score', blank=True, null=True)
    curated_by = models.ForeignKey('CurationLookup', models.DO_NOTHING, db_column='curated_by', blank=True, null=True)
    activity_count = models.BigIntegerField(blank=True, null=True)
    assay_source = models.CharField(max_length=50, blank=True, null=True)
    source = models.ForeignKey('Source', models.DO_NOTHING, db_column="src_id")
    src_assay_id = models.CharField(max_length=50, blank=True, null=True)
    chembl_id_lookup = models.ForeignKey('ChemblIdLookup', models.DO_NOTHING, unique=True, db_column="chembl_id")
    # chembl_id_lookup = models.OneToOneField('ChemblIdLookup', models.DO_NOTHING, db_column="chembl_id")
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=250, blank=True, null=True)
    orig_description = models.CharField(max_length=4000, blank=True, null=True)
    mc_tax_id = models.BigIntegerField(blank=True, null=True)
    mc_organism = models.CharField(max_length=100, blank=True, null=True)
    mc_target_type = models.CharField(max_length=28, blank=True, null=True)
    mc_target_name = models.CharField(max_length=4000, blank=True, null=True)
    mc_target_accession = models.CharField(max_length=255, blank=True, null=True)
    cell_dictionary = models.ForeignKey('CellDictionary', models.DO_NOTHING, blank=True, null=True,db_column='cell_id')
    bioassay_ontology = models.ForeignKey('BioassayOntology', models.DO_NOTHING, db_column='bao_format', blank=True, null=True)
    tissue_dictionary = models.ForeignKey('TissueDictionary', models.DO_NOTHING, blank=True, null=True, db_column="tissue_id")
    curation_comment = models.CharField(max_length=4000, blank=True, null=True)
    variant_sequences = models.ForeignKey('VariantSequences', models.DO_NOTHING, blank=True, null=True, db_column="variant_id")
    aidx = models.CharField(max_length=200)
    job_id = models.IntegerField()
    log_id = models.IntegerField()
    ridx = models.CharField(max_length=200)
    tid_fixed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'assays'


class AtcClassification(models.Model):
    who_name = models.CharField(max_length=2000, blank=True, null=True)
    level1 = models.CharField(max_length=10, blank=True, null=True)
    level2 = models.CharField(max_length=10, blank=True, null=True)
    level3 = models.CharField(max_length=10, blank=True, null=True)
    level4 = models.CharField(max_length=10, blank=True, null=True)
    level5 = models.CharField(primary_key=True, max_length=10)
    level1_description = models.CharField(max_length=2000, blank=True, null=True)
    level2_description = models.CharField(max_length=2000, blank=True, null=True)
    level3_description = models.CharField(max_length=2000, blank=True, null=True)
    level4_description = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atc_classification'


class BindingSites(models.Model):
    site_id = models.BigIntegerField(primary_key=True)
    site_name = models.CharField(max_length=200, blank=True, null=True)
    tid = models.ForeignKey('TargetDictionary', models.DO_NOTHING, db_column='tid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'binding_sites'


class BioComponentSequences(models.Model):
    component_id = models.BigIntegerField(primary_key=True)
    component_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    sequence_md5sum = models.CharField(max_length=32, blank=True, null=True)
    tax_id = models.BigIntegerField(blank=True, null=True)
    organism = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bio_component_sequences'


class BioassayOntology(models.Model):
    bao_id = models.CharField(primary_key=True, max_length=11)
    label = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'bioassay_ontology'


class BiotherapeuticComponents(models.Model):
    biocomp_id = models.BigIntegerField(primary_key=True)
    biotherapeutics = models.ForeignKey('Biotherapeutics', models.DO_NOTHING, db_column='molregno')
    bio_component_sequences = models.ForeignKey(BioComponentSequences, models.DO_NOTHING, db_column="component_id")

    class Meta:
        managed = False
        db_table = 'biotherapeutic_components'
        unique_together = (('biotherapeutics', 'bio_component_sequences'),)


class Biotherapeutics(models.Model):
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', primary_key=True)
    # molecule_dictionary = models.OneToOneField('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', primary_key=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    helm_notation = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biotherapeutics'


class CellDictionary(models.Model):
    cell_id = models.BigIntegerField(primary_key=True)
    cell_name = models.CharField(max_length=50)
    cell_description = models.CharField(max_length=200, blank=True, null=True)
    cell_source_tissue = models.CharField(max_length=50, blank=True, null=True)
    cell_source_organism = models.CharField(max_length=150, blank=True, null=True)
    cell_source_tax_id = models.BigIntegerField(blank=True, null=True)
    clo_id = models.CharField(max_length=11, blank=True, null=True)
    efo_id = models.CharField(max_length=12, blank=True, null=True)
    cellosaurus_id = models.CharField(max_length=15, blank=True, null=True)
    cl_lincs_id = models.CharField(max_length=8, blank=True, null=True)
    chembl_id_lookup = models.ForeignKey('ChemblIdLookup', models.DO_NOTHING, unique=True, blank=True, null=True, db_column="chembl_id")
    # chembl_id_lookup = models.OneToOneField('ChemblIdLookup', models.DO_NOTHING, blank=True, null=True, db_column="chembl_id")
    cell_ontology_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cell_dictionary'
        unique_together = (('cell_name', 'cell_source_tax_id'),)


class ChemblIdLookup(models.Model):
    chembl_id = models.CharField(primary_key=True, max_length=20)
    entity_type = models.CharField(max_length=50)
    entity_id = models.BigIntegerField()
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'chembl_id_lookup'
        unique_together = (('entity_type', 'entity_id'),)


class ComponentClass(models.Model):
    component_sequences = models.ForeignKey('ComponentSequences', models.DO_NOTHING, db_column="component_id")
    protein_classification = models.ForeignKey('ProteinClassification', models.DO_NOTHING, db_column="protein_class_id")
    comp_class_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'component_class'
        unique_together = (('component_sequences', 'protein_classification'),)


class ComponentDomains(models.Model):
    compd_id = models.BigIntegerField(primary_key=True)
    domains = models.ForeignKey('Domains', models.DO_NOTHING, blank=True, null=True, db_column="domain_id")
    component_sequences = models.ForeignKey('ComponentSequences', models.DO_NOTHING, db_column="component_id")
    start_position = models.BigIntegerField(blank=True, null=True)
    end_position = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'component_domains'
        unique_together = (('domains', 'component_sequences', 'start_position'),)


class ComponentGo(models.Model):
    comp_go_id = models.BigIntegerField(primary_key=True)
    component_sequences = models.ForeignKey('ComponentSequences', models.DO_NOTHING, db_column="component_id")
    go_classification = models.ForeignKey('GoClassification', models.DO_NOTHING, db_column="go_id")

    class Meta:
        managed = False
        db_table = 'component_go'
        unique_together = (('component_sequences', 'go_classification'),)


class ComponentSequences(models.Model):
    component_id = models.BigIntegerField(primary_key=True)
    component_type = models.CharField(max_length=50, blank=True, null=True)
    accession = models.CharField(unique=True, max_length=25, blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    sequence_md5sum = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    tax_id = models.BigIntegerField(blank=True, null=True)
    organism = models.CharField(max_length=150, blank=True, null=True)
    db_source = models.CharField(max_length=25, blank=True, null=True)
    db_version = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'component_sequences'


class ComponentSynonyms(models.Model):
    compsyn_id = models.BigIntegerField(primary_key=True)
    component_sequences = models.ForeignKey(ComponentSequences, models.DO_NOTHING, db_column="component_id")
    component_synonym = models.CharField(max_length=500, blank=True, null=True)
    syn_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'component_synonyms'
        unique_together = (('component_sequences', 'component_synonym', 'syn_type'),)


class CompoundProperties(models.Model):
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', primary_key=True)
    # molecule_dictionary = models.OneToOneField('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', primary_key=True, related_name='molecule_dictionary_related')
    mw_freebase = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    alogp = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    hba = models.IntegerField(blank=True, null=True)
    hbd = models.IntegerField(blank=True, null=True)
    psa = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    rtb = models.IntegerField(blank=True, null=True)
    ro3_pass = models.CharField(max_length=3, blank=True, null=True)
    num_ro5_violations = models.IntegerField(blank=True, null=True)
    cx_most_apka = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    cx_most_bpka = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    cx_logp = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    cx_logd = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    molecular_species = models.CharField(max_length=50, blank=True, null=True)
    full_mwt = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    aromatic_rings = models.IntegerField(blank=True, null=True)
    heavy_atoms = models.IntegerField(blank=True, null=True)
    qed_weighted = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    mw_monoisotopic = models.DecimalField(max_digits=11, decimal_places=4, blank=True, null=True)
    full_molformula = models.CharField(max_length=100, blank=True, null=True)
    hba_lipinski = models.IntegerField(blank=True, null=True)
    hbd_lipinski = models.IntegerField(blank=True, null=True)
    num_lipinski_ro5_violations = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compound_properties'


class CompoundRecords(models.Model):
    record_id = models.BigIntegerField(primary_key=True)
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', blank=True, null=True)
    docs = models.ForeignKey('Docs', models.DO_NOTHING, db_column="doc_id")
    compound_key = models.CharField(max_length=250, blank=True, null=True)
    compound_name = models.CharField(max_length=4000, blank=True, null=True)
    source = models.ForeignKey('Source', models.DO_NOTHING, db_column="src_id")
    src_compound_id = models.CharField(max_length=150, blank=True, null=True)
    cidx = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'compound_records'


class CompoundStructuralAlerts(models.Model):
    cpd_str_alert_id = models.BigIntegerField(primary_key=True)
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno')
    # structural_alerts = models.ForeignKey('StructuralAlerts', models.DO_NOTHING, db_column="cpd_str_alert_id")

    class Meta:
        managed = False
        db_table = 'compound_structural_alerts'
        unique_together = (('molecule_dictionary', 'structural_alerts'),)


class CompoundStructures(models.Model):
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', primary_key=True)
    # molecule_dictionary = models.OneToOneField('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', primary_key=True)
    molfile = models.TextField(blank=True, null=True)
    standard_inchi = models.CharField(max_length=4000, blank=True, null=True)
    standard_inchi_key = models.CharField(unique=True, max_length=27)
    canonical_smiles = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compound_structures'


class ConfidenceScoreLookup(models.Model):
    confidence_score = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    target_mapping = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'confidence_score_lookup'


class CurationLookup(models.Model):
    curated_by = models.CharField(primary_key=True, max_length=32)
    description = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'curation_lookup'


class DataValidityLookup(models.Model):
    data_validity_comment = models.CharField(primary_key=True, max_length=30)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_validity_lookup'


class DefinedDailyDose(models.Model):
    atc_classification = models.ForeignKey(AtcClassification, models.DO_NOTHING, db_column='atc_code')
    ddd_units = models.CharField(max_length=200, blank=True, null=True)
    ddd_admr = models.CharField(max_length=1000, blank=True, null=True)
    ddd_comment = models.CharField(max_length=2000, blank=True, null=True)
    ddd_id = models.BigIntegerField(primary_key=True)
    ddd_value = models.DecimalField(max_digits=64, decimal_places=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'defined_daily_dose'


class Docs(models.Model):
    doc_id = models.BigIntegerField(primary_key=True)
    journal = models.CharField(max_length=50, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    volume = models.CharField(max_length=50, blank=True, null=True)
    issue = models.CharField(max_length=50, blank=True, null=True)
    first_page = models.CharField(max_length=50, blank=True, null=True)
    last_page = models.CharField(max_length=50, blank=True, null=True)
    pubmed_id = models.BigIntegerField(unique=True, blank=True, null=True)
    doi = models.CharField(max_length=100, blank=True, null=True)
    chembl_id_lookup = models.ForeignKey(ChemblIdLookup, models.DO_NOTHING, unique=True, db_column='chembl_id')
    # chembl_id_lookup = models.OneToOneField(ChemblIdLookup, models.DO_NOTHING, db_column='chembl_id')
    title = models.CharField(max_length=500, blank=True, null=True)
    doc_type = models.CharField(max_length=50)
    authors = models.CharField(max_length=4000, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    patent_id = models.CharField(max_length=20, blank=True, null=True)
    ridx = models.CharField(max_length=200)
    src_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'docs'


class Domains(models.Model):
    domain_id = models.BigIntegerField(primary_key=True)
    domain_type = models.CharField(max_length=20)
    source_domain_id = models.CharField(max_length=20)
    domain_name = models.CharField(max_length=20, blank=True, null=True)
    domain_description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domains'


class DrugIndication(models.Model):
    drugind_id = models.BigIntegerField(primary_key=True)
    compound_records = models.ForeignKey(CompoundRecords, models.DO_NOTHING, db_column="record_id")
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', blank=True, null=True)
    max_phase_for_ind = models.IntegerField(blank=True, null=True)
    mesh_id = models.CharField(max_length=20)
    mesh_heading = models.CharField(max_length=200)
    efo_id = models.CharField(max_length=20, blank=True, null=True)
    efo_term = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug_indication'
        unique_together = (('compound_records', 'mesh_id', 'efo_id'),)


class DrugMechanism(models.Model):
    mec_id = models.BigIntegerField(primary_key=True)
    compound_records = models.ForeignKey(CompoundRecords, models.DO_NOTHING, db_column="record_id")
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', blank=True, null=True)
    mechanism_of_action = models.CharField(max_length=250, blank=True, null=True)
    target_dictionary = models.ForeignKey('TargetDictionary', models.DO_NOTHING, db_column='tid', blank=True, null=True)
    binding_sites = models.ForeignKey(BindingSites, models.DO_NOTHING, blank=True, null=True, db_column="sites")
    action_type = models.ForeignKey(ActionType, models.DO_NOTHING, db_column='action_type', blank=True, null=True)
    direct_interaction = models.IntegerField(blank=True, null=True)
    molecular_mechanism = models.IntegerField(blank=True, null=True)
    disease_efficacy = models.IntegerField(blank=True, null=True)
    mechanism_comment = models.CharField(max_length=2000, blank=True, null=True)
    selectivity_comment = models.CharField(max_length=1000, blank=True, null=True)
    binding_site_comment = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drug_mechanism'


class Formulations(models.Model):
    products = models.ForeignKey('Products', models.DO_NOTHING, db_column="product_id")
    ingredient = models.CharField(max_length=200, blank=True, null=True)
    strength = models.CharField(max_length=300, blank=True, null=True)
    compound_records = models.ForeignKey(CompoundRecords, models.DO_NOTHING, db_column="compound_id")
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno', blank=True, null=True)
    formulation_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'formulations'
        unique_together = (('products', 'compound_records'),)


class FracClassification(models.Model):
    frac_class_id = models.BigIntegerField(primary_key=True)
    active_ingredient = models.CharField(max_length=500)
    level1 = models.CharField(max_length=2)
    level1_description = models.CharField(max_length=2000)
    level2 = models.CharField(max_length=2)
    level2_description = models.CharField(max_length=2000, blank=True, null=True)
    level3 = models.CharField(max_length=6)
    level3_description = models.CharField(max_length=2000, blank=True, null=True)
    level4 = models.CharField(max_length=7)
    level4_description = models.CharField(max_length=2000, blank=True, null=True)
    level5 = models.CharField(unique=True, max_length=8)
    frac_code = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'frac_classification'


class GoClassification(models.Model):
    go_id = models.CharField(primary_key=True, max_length=10)
    parent_go_id = models.CharField(max_length=10, blank=True, null=True)
    pref_name = models.CharField(max_length=200, blank=True, null=True)
    class_level = models.IntegerField(blank=True, null=True)
    aspect = models.CharField(max_length=1, blank=True, null=True)
    path = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'go_classification'


class HracClassification(models.Model):
    hrac_class_id = models.BigIntegerField(primary_key=True)
    active_ingredient = models.CharField(max_length=500)
    level1 = models.CharField(max_length=2)
    level1_description = models.CharField(max_length=2000)
    level2 = models.CharField(max_length=3)
    level2_description = models.CharField(max_length=2000, blank=True, null=True)
    level3 = models.CharField(unique=True, max_length=5)
    hrac_code = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'hrac_classification'


class IndicationRefs(models.Model):
    indref_id = models.BigIntegerField(primary_key=True)
    drug_indication = models.ForeignKey(DrugIndication, models.DO_NOTHING, db_column="drugind")
    ref_type = models.CharField(max_length=50)
    ref_id = models.CharField(max_length=4000)
    ref_url = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'indication_refs'


class IracClassification(models.Model):
    irac_class_id = models.BigIntegerField(primary_key=True)
    active_ingredient = models.CharField(max_length=500)
    level1 = models.CharField(max_length=1)
    level1_description = models.CharField(max_length=2000)
    level2 = models.CharField(max_length=3)
    level2_description = models.CharField(max_length=2000)
    level3 = models.CharField(max_length=6)
    level3_description = models.CharField(max_length=2000)
    level4 = models.CharField(unique=True, max_length=8)
    irac_code = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'irac_classification'


class LigandEff(models.Model):
    activities = models.ForeignKey(Activities, models.DO_NOTHING, primary_key=True, db_column="activity_id")
    # activities = models.OneToOneField(Activities, models.DO_NOTHING, primary_key=True, db_column="activity_id")
    bei = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    sei = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    le = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    lle = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ligand_eff'


class MechanismRefs(models.Model):
    mecref_id = models.BigIntegerField(primary_key=True)
    drug_mechanism = models.ForeignKey(DrugMechanism, models.DO_NOTHING, db_column="mec_id")
    ref_type = models.CharField(max_length=50)
    ref_id = models.CharField(max_length=200, blank=True, null=True)
    ref_url = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mechanism_refs'
        unique_together = (('mec', 'ref_type', 'ref_id'), ('mec', 'ref_type', 'ref_id'),)


class Metabolism(models.Model):
    met_id = models.BigIntegerField(primary_key=True)
    compound_records = models.ForeignKey(CompoundRecords, models.DO_NOTHING, blank=True, null=True, db_column="drug_record")
    substrate_record = models.ForeignKey(CompoundRecords, models.DO_NOTHING, blank=True, null=True)
    metabolite_record = models.ForeignKey(CompoundRecords, models.DO_NOTHING, blank=True, null=True)
    pathway_id = models.BigIntegerField(blank=True, null=True)
    pathway_key = models.CharField(max_length=50, blank=True, null=True)
    enzyme_name = models.CharField(max_length=200, blank=True, null=True)
    target_dictionary = models.ForeignKey('TargetDictionary', models.DO_NOTHING, db_column='enzyme_tid', blank=True, null=True)
    met_conversion = models.CharField(max_length=200, blank=True, null=True)
    organism = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.BigIntegerField(blank=True, null=True)
    met_comment = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metabolism'
        unique_together = (('compound_records', 'substrate_record', 'metabolite_record', 'pathway_id', 'enzyme_name', 'enzyme_tid', 'tax_id'),)


class MetabolismRefs(models.Model):
    metref_id = models.BigIntegerField(primary_key=True)
    metabolism = models.ForeignKey(Metabolism, models.DO_NOTHING, db_column="met_id")
    ref_type = models.CharField(max_length=50)
    ref_id = models.CharField(max_length=200, blank=True, null=True)
    ref_url = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metabolism_refs'
        unique_together = (('met', 'ref_type', 'ref_id'),)


class MoleculeAtcClassification(models.Model):
    mol_atc_id = models.BigIntegerField(primary_key=True)
    atc_classification = models.ForeignKey(AtcClassification, models.DO_NOTHING, db_column='level5')
    molecule_dictionary = models.ForeignKey('MoleculeDictionary', models.DO_NOTHING, db_column='molregno')

    class Meta:
        managed = False
        db_table = 'molecule_atc_classification'


class MoleculeDictionary(models.Model):
    molregno = models.BigIntegerField(primary_key=True)
    pref_name = models.CharField(max_length=255, blank=True, null=True)
    chembl_id_lookup = models.ForeignKey(ChemblIdLookup, models.DO_NOTHING, unique=True, db_column='chembl_id')
    # chembl_id_lookup = models.OneToOneField(ChemblIdLookup, models.DO_NOTHING, db_column='chembl_id')
    max_phase = models.IntegerField()
    therapeutic_flag = models.IntegerField()
    dosed_ingredient = models.IntegerField()
    structure_type = models.CharField(max_length=10)
    chebi_par_id = models.BigIntegerField(blank=True, null=True)
    molecule_type = models.CharField(max_length=30, blank=True, null=True)
    first_approval = models.IntegerField(blank=True, null=True)
    oral = models.IntegerField()
    parenteral = models.IntegerField()
    topical = models.IntegerField()
    black_box_warning = models.IntegerField()
    natural_product = models.IntegerField()
    first_in_class = models.IntegerField()
    chirality = models.IntegerField()
    prodrug = models.IntegerField()
    inorganic_flag = models.IntegerField()
    usan_year = models.IntegerField(blank=True, null=True)
    availability_type = models.IntegerField(blank=True, null=True)
    usan_stem = models.CharField(max_length=50, blank=True, null=True)
    polymer_flag = models.IntegerField(blank=True, null=True)
    usan_substem = models.CharField(max_length=50, blank=True, null=True)
    usan_stem_definition = models.CharField(max_length=1000, blank=True, null=True)
    indication_class = models.CharField(max_length=1000, blank=True, null=True)
    withdrawn_flag = models.IntegerField()
    withdrawn_year = models.IntegerField(blank=True, null=True)
    withdrawn_country = models.CharField(max_length=1000, blank=True, null=True)
    withdrawn_reason = models.CharField(max_length=1000, blank=True, null=True)
    withdrawn_class = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'molecule_dictionary'


class MoleculeFracClassification(models.Model):
    mol_frac_id = models.BigIntegerField(primary_key=True)
    frac_classification = models.ForeignKey(FracClassification, models.DO_NOTHING, db_column="frac_class_id")
    molecule_dictionary = models.ForeignKey(MoleculeDictionary, models.DO_NOTHING, db_column='molregno')

    class Meta:
        managed = False
        db_table = 'molecule_frac_classification'
        unique_together = (('frac_classification', 'molecule_dictionary'),)


class MoleculeHierarchy(models.Model):
    molecule_dictionary = models.ForeignKey(MoleculeDictionary, models.DO_NOTHING, db_column='molregno', primary_key=True)
    # molecule_dictionary = models.OneToOneField(MoleculeDictionary, models.DO_NOTHING, db_column='molregno', primary_key=True)
    parent_molregno = models.ForeignKey(MoleculeDictionary, models.DO_NOTHING, db_column='parent_molregno', blank=True, null=True)
    active_molregno = models.ForeignKey(MoleculeDictionary, models.DO_NOTHING, db_column='active_molregno', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'molecule_hierarchy'


class MoleculeHracClassification(models.Model):
    mol_hrac_id = models.BigIntegerField(primary_key=True)
    hrac_classification = models.ForeignKey(HracClassification, models.DO_NOTHING, db_column="hrac_class_id")
    molecule_dictionary = models.ForeignKey(MoleculeDictionary, models.DO_NOTHING, db_column='molregno')

    class Meta:
        managed = False
        db_table = 'molecule_hrac_classification'
        unique_together = (('hrac_classification', 'molecule_dictionary'),)


class MoleculeIracClassification(models.Model):
    mol_irac_id = models.BigIntegerField(primary_key=True)
    irac_classification = models.ForeignKey(IracClassification, models.DO_NOTHING, db_column="irac_class_id")
    molecule_dictionary = models.ForeignKey(MoleculeDictionary, models.DO_NOTHING, db_column='molregno')

    class Meta:
        managed = False
        db_table = 'molecule_irac_classification'
        unique_together = (('irac_classification', 'molecule_dictionary'),)


class MoleculeSynonyms(models.Model):
    molecule_dictionary = models.ForeignKey(MoleculeDictionary, models.DO_NOTHING, db_column='molregno')
    syn_type = models.CharField(max_length=50)
    molsyn_id = models.BigIntegerField(primary_key=True)
    research_stem = models.ForeignKey('ResearchStem', models.DO_NOTHING, blank=True, null=True, db_column="res_stem")
    synonyms = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'molecule_synonyms'
        unique_together = (('molecule_dictionary', 'syn_type', 'synonyms'),)


class OrganismClass(models.Model):
    oc_id = models.BigIntegerField(primary_key=True)
    tax_id = models.BigIntegerField(unique=True, blank=True, null=True)
    l1 = models.CharField(max_length=200, blank=True, null=True)
    l2 = models.CharField(max_length=200, blank=True, null=True)
    l3 = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organism_class'


class PatentUseCodes(models.Model):
    patent_use_code = models.CharField(primary_key=True, max_length=8)
    definition = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'patent_use_codes'


class PredictedBindingDomains(models.Model):
    predbind_id = models.BigIntegerField(primary_key=True)
    activities = models.ForeignKey(Activities, models.DO_NOTHING, blank=True, null=True, db_column="activity_id")
    binding_sites = models.ForeignKey(BindingSites, models.DO_NOTHING, blank=True, null=True, db_column="site_id")
    prediction_method = models.CharField(max_length=50, blank=True, null=True)
    confidence = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predicted_binding_domains'


class ProductPatents(models.Model):
    prod_pat_id = models.BigIntegerField(primary_key=True)
    products = models.ForeignKey('Products', models.DO_NOTHING, db_column="product_id")
    patent_no = models.CharField(max_length=20)
    patent_expire_date = models.DateTimeField()
    drug_substance_flag = models.IntegerField()
    drug_product_flag = models.IntegerField()
    patent_use_codes = models.ForeignKey(PatentUseCodes, models.DO_NOTHING, db_column='patent_use_code', blank=True, null=True)
    delist_flag = models.IntegerField()
    submission_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_patents'
        unique_together = (('products', 'patent_no', 'patent_expire_date', 'patent_use_codes'),)


class Products(models.Model):
    dosage_form = models.CharField(max_length=200, blank=True, null=True)
    route = models.CharField(max_length=200, blank=True, null=True)
    trade_name = models.CharField(max_length=200, blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    ad_type = models.CharField(max_length=5, blank=True, null=True)
    oral = models.IntegerField(blank=True, null=True)
    topical = models.IntegerField(blank=True, null=True)
    parenteral = models.IntegerField(blank=True, null=True)
    black_box_warning = models.IntegerField(blank=True, null=True)
    applicant_full_name = models.CharField(max_length=200, blank=True, null=True)
    innovator_company = models.IntegerField(blank=True, null=True)
    product_id = models.CharField(primary_key=True, max_length=30)
    nda_type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class ProteinClassSynonyms(models.Model):
    protclasssyn_id = models.BigIntegerField(primary_key=True)
    protein_classification = models.ForeignKey('ProteinClassification', models.DO_NOTHING, db_column="protein_class_id")
    protein_class_synonym = models.CharField(max_length=1000, blank=True, null=True)
    syn_type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protein_class_synonyms'


class ProteinClassification(models.Model):
    protein_class_id = models.BigIntegerField(primary_key=True)
    parent_id = models.BigIntegerField(blank=True, null=True)
    pref_name = models.CharField(max_length=500, blank=True, null=True)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    protein_class_desc = models.CharField(max_length=410)
    definition = models.CharField(max_length=4000, blank=True, null=True)
    class_level = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'protein_classification'


class ProteinFamilyClassification(models.Model):
    protein_class_id = models.BigIntegerField(primary_key=True)
    protein_class_desc = models.CharField(unique=True, max_length=810)
    l1 = models.CharField(max_length=100)
    l2 = models.CharField(max_length=100, blank=True, null=True)
    l3 = models.CharField(max_length=100, blank=True, null=True)
    l4 = models.CharField(max_length=100, blank=True, null=True)
    l5 = models.CharField(max_length=100, blank=True, null=True)
    l6 = models.CharField(max_length=100, blank=True, null=True)
    l7 = models.CharField(max_length=100, blank=True, null=True)
    l8 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'protein_family_classification'
        unique_together = (('l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8'),)


class RelationshipType(models.Model):
    relationship_type = models.CharField(primary_key=True, max_length=1)
    relationship_desc = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relationship_type'


class ResearchCompanies(models.Model):
    co_stem_id = models.BigIntegerField(primary_key=True)
    research_stem = models.ForeignKey('ResearchStem', models.DO_NOTHING, blank=True, null=True, db_column="res_stem")
    company = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    previous_company = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'research_companies'
        unique_together = (('research_stem', 'company'),)


class ResearchStem(models.Model):
    res_stem_id = models.BigIntegerField(primary_key=True)
    research_stem = models.CharField(unique=True, max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'research_stem'


class SiteComponents(models.Model):
    sitecomp_id = models.BigIntegerField(primary_key=True)
    binding_sites = models.ForeignKey(BindingSites, models.DO_NOTHING, db_column="site_id")
    component_sequences = models.ForeignKey(ComponentSequences, models.DO_NOTHING, blank=True, null=True, db_column="component")
    domains = models.ForeignKey(Domains, models.DO_NOTHING, blank=True, null=True, db_column="domain_id")
    site_residues = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_components'
        unique_together = (('binding_sites', 'component_sequences', 'domains'),)


class Source(models.Model):
    src_id = models.IntegerField(primary_key=True)
    src_description = models.CharField(max_length=500, blank=True, null=True)
    src_short_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source'


class StructuralAlertSets(models.Model):
    alert_set_id = models.BigIntegerField(primary_key=True)
    set_name = models.CharField(unique=True, max_length=100)
    priority = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'structural_alert_sets'


class StructuralAlerts(models.Model):
    alert_id = models.BigIntegerField(primary_key=True)
    structural_alert_sets = models.ForeignKey(StructuralAlertSets, models.DO_NOTHING, db_column="alert_set")
    alert_name = models.CharField(max_length=100)
    smarts = models.CharField(max_length=4000)

    class Meta:
        managed = False
        db_table = 'structural_alerts'


class TargetComponents(models.Model):
    target_dictionary = models.ForeignKey('TargetDictionary', models.DO_NOTHING, db_column='tid')
    component_sequences = models.ForeignKey(ComponentSequences, models.DO_NOTHING, db_column="component_sequences")
    targcomp_id = models.BigIntegerField(primary_key=True)
    homologue = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'target_components'
        unique_together = (('target_dictionary', 'component_sequences'),)


class TargetDictionary(models.Model):
    tid = models.BigIntegerField(primary_key=True)
    target_type = models.ForeignKey('TargetType', models.DO_NOTHING, db_column='target_type', blank=True, null=True)
    pref_name = models.CharField(max_length=200)
    tax_id = models.BigIntegerField(blank=True, null=True)
    organism = models.CharField(max_length=150, blank=True, null=True)
    chembl_id_lookup = models.ForeignKey(ChemblIdLookup, models.DO_NOTHING, unique=True, db_column="chembl_id")
    # chembl_id_lookup = models.OneToOneField(ChemblIdLookup, models.DO_NOTHING, db_column="chembl_id")
    species_group_flag = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'target_dictionary'


class TargetRelations(models.Model):
    target_dictionary = models.ForeignKey(TargetDictionary, models.DO_NOTHING, db_column='tid')
    relationship = models.CharField(max_length=20)
    related_tid = models.ForeignKey(TargetDictionary, models.DO_NOTHING, db_column='related_tid')
    targrel_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'target_relations'


class TargetType(models.Model):
    target_type = models.CharField(primary_key=True, max_length=30)
    target_desc = models.CharField(max_length=250, blank=True, null=True)
    parent_type = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'target_type'


class TissueDictionary(models.Model):
    tissue_id = models.BigIntegerField(primary_key=True)
    uberon_id = models.CharField(max_length=15, blank=True, null=True)
    pref_name = models.CharField(max_length=200)
    efo_id = models.CharField(max_length=20, blank=True, null=True)
    chembl_id_lookup = models.ForeignKey(ChemblIdLookup, models.DO_NOTHING, unique=True, db_column="chembl_id")
    # chembl_id_lookup = models.OneToOneField(ChemblIdLookup, models.DO_NOTHING, db_column="chembl_id")
    bto_id = models.CharField(max_length=20, blank=True, null=True)
    caloha_id = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tissue_dictionary'
        unique_together = (('uberon_id', 'efo_id'),)


class UsanStems(models.Model):
    usan_stem_id = models.BigIntegerField(primary_key=True)
    stem = models.CharField(max_length=100)
    subgroup = models.CharField(max_length=100)
    annotation = models.CharField(max_length=2000, blank=True, null=True)
    stem_class = models.CharField(max_length=100, blank=True, null=True)
    major_class = models.CharField(max_length=100, blank=True, null=True)
    who_extra = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usan_stems'
        unique_together = (('stem', 'subgroup'),)


class VariantSequences(models.Model):
    variant_id = models.BigIntegerField(primary_key=True)
    mutation = models.CharField(max_length=2000, blank=True, null=True)
    accession = models.CharField(max_length=25, blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)
    isoform = models.BigIntegerField(blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    organism = models.CharField(max_length=200, blank=True, null=True)
    tax_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variant_sequences'


class Version(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    creation_date = models.DateTimeField(blank=True, null=True)
    comments = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'version'
