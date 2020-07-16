import os
import django
from rest_framework.relations import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

import json
import ast
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
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

class ActivitiesSerializer(serializers.ModelSerializer):
    activity_supp_map = ActivitySuppMapSerializer(many=True, required=False)
    class Meta:
        model = Activities
        fields = '__all__'
        depth = 5

# ActivitiesObjectA = ActivitiesSerializer(Activities.objects.get(activity_id=17126237))
# ActivitiesObjectA_JSON = JSONRenderer().render(ActivitiesObjectA.data)
# print(ActivitiesObjectA_JSON)

# object = {}
# activities = {}
# nested = {}
# test = dict(ActivitiesObjectA.data)
# for k,v in test.items():
#     if type(v) in [int, str, None.__class__]:
#         activities.update({k:v})
#     else:
#         nested.update({k:v})
# object.update({'activities':activities})
# object.update(nested)
# x = json.dumps(object)
# y = json.loads(x)
# print(x)


# def custom_to_dict(instance, fields=None, exclude=None):
#     opts = instance._meta
#     data = {}
#     for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
#         if not getattr(f, 'editable', False):
#             continue
#         if fields and f.attname not in fields:
#             continue
#         if exclude and f.attname in exclude:
#             continue
#         data[f.attname] = f.value_from_object(instance)
#     return data
#
# def serialize(modelobj1):
#     def serialized(modelobj):
#         opts = modelobj._meta.get_fields()
#
#         dbt = modelobj._meta.db_table
#         modeldict = custom_to_dict(modelobj)
#         keyrev = modelobj.__class__
#         keyvalrev = modelobj.pk
#
#         for m in opts:
#             if not m.one_to_many:
#                 foreignk = getattr(modelobj, m.name)
#                 if foreignk:
#                     try:
#                         dbt = foreignk._meta.db_table
#                         modeldict[dbt] = serialize(foreignk)
#                     except:
#                         pass
#             if m.one_to_many:
#                 set = str(str(m.name) + '_set')
#                 test = getattr(keyrev.objects.get(pk=keyvalrev), set)
#                 if test.values().exists():
#                     try:
#                         if test.values()[1]:
#                             pass
#                     except:
#                         for n in test.all():
#                             key = n._meta.db_table
#                             modeldict1 = custom_to_dict(n)
#                             value = modeldict1.copy()
#                             valu = {}
#                             for i, o in value.items():
#                                 valu.update({i: str(o)})
#                             try:
#                                 modeldict[key].append(valu)
#                             except:
#                                 modeldict.update({key: valu})
#         return (modeldict)
#     opts = modelobj1._meta.get_fields()
#     dbt = modelobj1._meta.db_table
#     modeldict = {dbt:custom_to_dict(modelobj1)}
#
#     keyrev = modelobj1.__class__
#     keyvalrev = modelobj1.pk
#     for m in opts:
#
#         if not m.one_to_many:
#             foreignkey = getattr(modelobj1, m.name)
#             if foreignkey:
#
#                 try:
#                     dbt = foreignkey._meta.db_table
#                     modeldict[dbt] = serialized(foreignkey)
#                 except:
#                     pass
#         if m.one_to_many:
#             set = str(str(m.name) + '_set')
#             test = getattr(keyrev.objects.get(pk=keyvalrev), set)
#             if test.values().exists():
#                 try:
#                     if test.values()[1]:
#                         pass
#                 except:
#                     for n in test.all():
#                         key = n._meta.db_table
#                         modeldict1 = custom_to_dict(n)
#                         value = modeldict1.copy()
#                         valu = {}
#                         for i, o in value.items():
#                             valu.update({i:str(o)})
#                         try:
#                             modeldict[key].append(valu)
#                         except:
#                             modeldict.update({key:valu})
#     return(modeldict)
#
#
# serializedprex = serialize(Activities.objects.get(activity_id=17126237))
# print(serializedprex)