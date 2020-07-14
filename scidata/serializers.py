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

class NonNullModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super(NonNullModelSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class ActivitySuppSerializer(NonNullModelSerializer):
    class Meta:
        model = ActivitySupp
        fields = '__all__'
        depth = 0

class ActivitySmidSerializer(NonNullModelSerializer):
    activity_supp = ActivitySuppSerializer(many=True, required=False)
    class Meta:
        model = ActivitySmid
        fields = '__all__'
        depth = 1

class ActivitySuppMapSerializer(NonNullModelSerializer):
    activity_smid = ActivitySmidSerializer()
    class Meta:
        model = ActivitySuppMap
        exclude = ['activities']
        depth = 1

class AssaySerializer(NonNullModelSerializer):
    class Meta:
        model = Assays
        exclude = ['activities']
        depth = 1


class ActivitiesSerializer(NonNullModelSerializer):
    activity_supp_map = ActivitySuppMapSerializer(many=True, required=False)
    class Meta:
        model = Activities
        fields = '__all__'
        blank = False
        depth = 5



ActivitiesObjectA = ActivitiesSerializer(Activities.objects.get(activity_id=17126237))
ActivitiesObjectA_JSON = JSONRenderer().render(ActivitiesObjectA.data)
print(ActivitiesObjectA_JSON)

object = {}
activities = {}
nested = {}
test = dict(ActivitiesObjectA.data)
for k,v in test.items():
    if type(v) in [int, str, None.__class__]:
        activities.update({k:v})
    else:
        nested.update({k:v})
object.update({'activities':activities})
object.update(nested)
x = json.dumps(object)
y = json.loads(x)
print(x)



# serializer = ActivitiesSerializer()
# print(repr(serializer))