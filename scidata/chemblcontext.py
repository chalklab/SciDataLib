""" context file code """
from scidata.model import *
import os
import django

django.setup()
from scidata.crosswalks import *

path = r"/Users/n01448636/Documents/PycharmProjects/scidata_python/scidata/JSON_dumps"
os.chdir(path)

dbname = 'default'
query_crosswalks_chembl = list(Chembl.objects.using('crosswalks').values())
query_crosswalks_ontterms = list(Ontterms.objects.using('crosswalks').values())
query_crosswalks_nspaces = list(Nspaces.objects.using('crosswalks').values())

crosswalks = []
for ont in query_crosswalks_chembl:
    crosswalksA = ont
    if crosswalksA['sdsection'] is None:
        for onto in query_crosswalks_ontterms:
            if crosswalksA['ontterm_id'] == onto['id']:
                for x, y in onto.items():
                    crosswalksA.update({x: y})
    else:
        for onto in query_crosswalks_ontterms:
            if crosswalksA['ontterm_id'] == onto['id']:
                for x, y in onto.items():
                    if x not in ['sdsection', 'sdsubsection']:
                        crosswalksA.update({x: y})
    crosswalks.append(crosswalksA)

# context = ["https://stuchalk.github.io/scidata/contexts/scidata_general.jsonld",
#         "https://stuchalk.github.io/scidata/contexts/scidata_methodology.jsonld",
#         "https://stuchalk.github.io/scidata/contexts/scidata_system.jsonld",
#         "https://stuchalk.github.io/scidata/contexts/scidata_dataset.jsonld"]

context = []

vocab = {'@vocab':'https://www.w3.org/2001/XMLSchema#'}

content = {}
namespaces = []
for x in crosswalks:
    try:
        content.update({x['field']:{'@id':x['url'],'@type':x['datatype']}})
        namespaces.append(x['nspace_id'])
    except:
        print('failed')
        print(x)

nspaces = {}
for x in namespaces:
    for y in query_crosswalks_nspaces:
        if x == y['id']:
            nspaces.update({y['ns']:y['path']})

z = {}
z.update(vocab)
z.update(nspaces)
z.update(content)

if context:
    context.append(z)
    final = {'@context':context}
else:
    final = {'@context':z}

test = json.dumps(final, indent=4, ensure_ascii=False)
print(test)

with open('chembl_context.jsonld', 'w') as f:
    json.dump(final, f)