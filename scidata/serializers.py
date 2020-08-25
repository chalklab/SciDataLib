import os
import django
from rest_framework.relations import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

import json
from rest_framework import serializers
from scidata.chembldb27 import *
from itertools import chain

# class NonNullModelSerializer(serializers.ModelSerializer):
#     def to_representation(self, instance):
#         result = super(NonNullModelSerializer, self).to_representation(instance)
#         return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class ActivitySuppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySupp
        fields = '__all__'
        depth = 0

class ActivitySmidSerializer(serializers.ModelSerializer):
    activity_supp = ActivitySuppSerializer(many=True, required=False)
    class Meta:
        model = ActivitySmid
        fields = '__all__'
        depth = 1

class ActivitySuppMapSerializer(serializers.ModelSerializer):
    activity_smid = ActivitySmidSerializer()
    class Meta:
        model = ActivitySuppMap
        exclude = ['activities']
        depth = 1

class CompoundPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompoundProperties
        fields = '__all__'
        depth = 0

class CompoundRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompoundRecords
        fields = '__all__'
        depth = 0

class CompoundStructuralAlertsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompoundStructuralAlerts
        fields = '__all__'
        depth = 0

class CompoundStructuresSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompoundStructures
        fields = '__all__'
        depth = 0

class DrugIndicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugIndication
        fields = '__all__'
        depth = 0

class BiotherapeuticsComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiotherapeuticComponents
        fields = '__all__'
        depth = 1

class BiotherapeuticsSerializer(serializers.ModelSerializer):
    biotherapeutic_components = BiotherapeuticsComponentsSerializer(source='biotherapeutic_components_set', many=True, required=False)

    class Meta:
        model = Biotherapeutics
        fields = '__all__'
        depth = 0

class MoleculeDictionarySerializer(serializers.ModelSerializer):
    biotherapeutics = BiotherapeuticsSerializer(source='molecule_dictionary_biotherapeutics', required=False)
    compound_properties = CompoundPropertiesSerializer(source='molecule_dictionary_compound_properties', required=False)
    # compound_properties = CompoundPropertiesSerializer(source='compoundproperties_set', many=True, required=False)
    # compound_records = CompoundRecordsSerializer(source='compoundrecords_set', many=True, required=False)
    compound_structural_alerts = CompoundStructuralAlertsSerializer(source='compoundstructuralalerts_set', many=True, required=False)
    compound_structures = CompoundStructuresSerializer(source='molecule_dictionary_compound_structures', required=False)
    # drug_indication = DrugIndicationSerializer(source='compoundproperties_set', many=True, required=False)
    class Meta:
        model = MoleculeDictionary
        fields = '__all__'
        # extra_fields = ['compoundproperties_set']
        # extra_fields = ['compound_properties']
        depth = 1

    # def get_field_names(self, declared_fields, info):
    #     expanded_fields = super(MoleculeDictionarySerializer, self).get_field_names(declared_fields, info)
    #
    #     if getattr(self.Meta, 'extra_fields', None):
    #         return expanded_fields + self.Meta.extra_fields
    #     else:
    #         return expanded_fields

class ActivitiesSerializer(serializers.ModelSerializer):
    activity_supp_map = ActivitySuppMapSerializer(many=True, required=False)
    molecule_dictionary = MoleculeDictionarySerializer()
    class Meta:
        model = Activities
        fields = '__all__'
        depth = 5


# class AssaysSerializer(serializers.ModelSerializer):
#     activities = ActivitiesSerializer(many=True, required=False)
#     class Meta:
#         model = Activities
#         fields = ['activities']
#         depth = 1

class DocsSerializer(serializers.ModelSerializer):
    # assays = AssaysSerializer(many=True, required=False)
    activities = ActivitiesSerializer(many=True)

    class Meta:
        model = Docs
        fields = '__all__'
        extra_fields = ['activities']
        depth = 1

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(DocsSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


x = ActivitiesSerializer()
# x = DocsSerializer()
# x = MoleculeDictionarySerializer()
# print(repr(x))


# test = MoleculeDictionarySerializer(MoleculeDictionary.objects.first())
# print(json.dumps(test.data, indent=4))

# ActivitiesObjectA = ActivitiesSerializer(Activities.objects.get(activity_id='12645960'))
# print(json.dumps(ActivitiesObjectA.data, indent=4))
# DocsObjectA = DocsSerializer(Docs.objects.get(doc_id=5535)).data
# for x in DocsObjectA.items():
#     print(x)



# ActivitiesObjectA = ActivitiesSerializer(Activities.objects.get(activity_id=17126237))
# ActivitiesObjectA_JSON = JSONRenderer().render(ActivitiesObjectA.data)
# print(ActivitiesObjectA_JSON)
# print(json.dumps(ActivitiesObjectA.data))




