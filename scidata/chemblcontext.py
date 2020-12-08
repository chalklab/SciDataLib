""" context file code """
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from scidata.model import *
from scidata.crosswalks import *

path = r"/Users/n01448636/Documents/GoogleDrive/PycharmProjects/SciDataLib/scidata/JSON_dumps"
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
context_assay = []
context_compound = []
context_organism = []
context_target = []

vocab = {'@vocab':'https://www.w3.org/2001/XMLSchema#'}

content = {}
namespaces = []

content_assay = {}
namespaces_assay = []
content_compound = {}
namespaces_compound = []
content_organism = {}
namespaces_organism = []
content_target = {}
namespaces_target = []

for x in crosswalks:
    try:
        content.update({x['field']:{'@id':x['url'],'@type':x['datatype']}})
        namespaces.append(x['nspace_id'])
        if x['sdsubsection'] == 'assay':
            content_assay.update({x['field']:{'@id':x['url'],'@type':x['datatype']}})
            namespaces_assay.append(x['nspace_id'])
        elif x['sdsubsection'] == 'compound':
            content_compound.update({x['field']:{'@id':x['url'],'@type':x['datatype']}})
            namespaces_compound.append(x['nspace_id'])
        elif x['sdsubsection'] == 'organism':
            content_organism.update({x['field']:{'@id':x['url'],'@type':x['datatype']}})
            namespaces_organism.append(x['nspace_id'])
        elif x['sdsubsection'] == 'target':
            content_target.update({x['field']:{'@id':x['url'],'@type':x['datatype']}})
            namespaces_target.append(x['nspace_id'])

    except:
        print('failed')
        print(x)

nspaces = {}
nspaces_assay = {}
nspaces_compound = {}
nspaces_organism = {}
nspaces_target = {}

for y in query_crosswalks_nspaces:
    for x in namespaces:
        if x == y['id']:
            nspaces.update({y['ns']:y['path']})
    for x in namespaces_assay:
        if x == y['id']:
            nspaces_assay.update({y['ns']:y['path']})
    for x in namespaces_compound:
        if x == y['id']:
            nspaces_compound.update({y['ns']:y['path']})
    for x in namespaces_organism:
        if x == y['id']:
            nspaces_organism.update({y['ns']:y['path']})
    for x in namespaces_target:
        if x == y['id']:
            nspaces_target.update({y['ns']:y['path']})

all = {}
all.update(vocab)
all.update(nspaces)
all.update(content)

all_assay = {}
all_assay.update(vocab)
all_assay.update(nspaces_assay)
all_assay.update(content_assay)

all_compound = {}
all_compound.update(vocab)
all_compound.update(nspaces_compound)
all_compound.update(content_compound)

all_organism = {}
all_organism.update(vocab)
all_organism.update(nspaces_organism)
all_organism.update(content_organism)

all_target = {}
all_target.update(vocab)
all_target.update(nspaces_target)
all_target.update(content_target)


if context:
    context.append(all)
    final = {'@context':context}
else:
    final = {'@context':all}
with open('chembl.jsonld', 'w') as f:
    json.dump(final, f)

if context_assay:
    context_assay.append(all_assay)
    final = {'@context':context_assay}
else:
    final = {'@context':all_assay}
with open('chembl_assay.jsonld', 'w') as f:
    json.dump(final, f)

if context_compound:
    context_compound.append(all_compound)
    final = {'@context':context_compound}
else:
    final = {'@context':all_compound}
with open('chembl_compound.jsonld', 'w') as f:
    json.dump(final, f)

if context_organism:
    context_organism.append(all_organism)
    final = {'@context':context_organism}
else:
    final = {'@context':all_organism}
with open('chembl_organism.jsonld', 'w') as f:
    json.dump(final, f)

if context_target:
    context_target.append(all_target)
    final = {'@context':context_target}
else:
    final = {'@context':all_target}
with open('chembl_target.jsonld', 'w') as f:
    json.dump(final, f)


# test = json.dumps(final, indent=4, ensure_ascii=False)
# print(test)
# types = ['chembl', 'chembl_assay', 'chembl_compound', 'chembl_organism', 'chembl_target']