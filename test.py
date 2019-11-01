from model import *
import re
import os
import django

django.setup()
from scidata.mariadb import *
from scidata.crosswalks import *

path = r"/Users/n01448636/Documents/django project 1/scidata/JSON_dumps"
os.chdir(path)

query_crosswalks_chembl = list(Chembl.objects.using('crosswalks').values())
query_crosswalks_ontterms = list(Ontterms.objects.using('crosswalks').values())

DocumentNumber = 36053
doc_data = {}

# Adds Docs data to all_data dictionary
doc_data.update(Docs.objects.values().get(doc_id=DocumentNumber))

auth = doc_data['authors'].split(',')
authors = []
for a in auth:
    authors.append({'Name': a})

###############################

test = SciData(doc_data['doc_id'])
test.context('context HERE')
test.namespace({"namespace": "http://NAMESPACE.owl#"})
test.base({"@base": "http://BASE.jsonld"})
test.doc_id("@ID HERE")
test.graph_id("@graph_ID HERE")
test.graph_uid("@unique_ID HERE")
test.title(doc_data['title'])
test.author(authors)
test.description(doc_data['abstract'])
test.publisher(doc_data['journal'])
test.version('X.X')
test.keywords(['keyword1', 'keyword3'])
test.permalink("http://PERMALINK.jsonld")
test.related("http://RELATED.jsonld")
test.discipline('science')
test.subdiscipline('subscience')
test.source([{"citation1": "Johnson Research Group http://CITATION.edu", "url": "http://CITATION.jsonld"}])
test.rights([{"license": "http://creativecommons.org/publicdomain/zero/1.0/"}])

####

test.add_context("first context")
test.add_namespace({"namespace2": "http://NAMESPACE.owl#"})
test.add_keyword('keyword 2')
test.add_source([{"citation2": "Chalk Research Group http://chalk.coas.unf.edu",
                  "url": "http://stuchalk.github.io/scidata/examples/ph.jsonld"}])
test.add_rights([{"license2": "http://creativecommons.org/publicdomain/zero/1.0/"}])

###############################

# activity_id_list = Docs.objects.get(doc_id=DocumentNumber).activities_set.all()


crosswalks = []
crosswalksA = {}
crosswalksB = {}
for ont in query_crosswalks_chembl:
    crosswalksA.update(ont)
    for onto in query_crosswalks_ontterms:
        if ont['ontterm_id'] == onto['id']:
            crosswalksB.update(onto)

            # ont['title'] = onto['title']
            # ont['definition'] = onto['definition']
            # ont['code'] = onto['code']
            # ont['url'] = onto['url']
            # ont['nspace_id'] = onto['nspace_id']
            # ont['category'] = 'Category1'

            if ont['sdsection'] is None:
                ont['sdsection'] = onto['sdsection']
                ont['sdsubsection'] = onto['sdsubsection']
                # add other properties from ontterms table here if needed
                # ie. nspace_id, code, title, definition
                crosswalks.append(ont)

###############################


molregno_set = set()
for mo in Activities.objects.values().filter(doc_id=DocumentNumber):
    molregno_set.add(mo['molregno_id'])
for mol in molregno_set:
    activity_list = Activities.objects.values().filter(doc_id=DocumentNumber, molregno_id=mol)
    datapoint = []
    datagroup = []
    datagroupA = []
    for ac in activity_list:
        chembl = (Activities.objects.values('molregno_id__chembl_id').get(activity_id=ac['activity_id']))

        serialized = serialize(Activities.objects.get(activity_id=ac['activity_id']))

        for serial in serialized:
            for serial_table, serial_dict in serial.items():
                if serial_table == 'activities':

                    experimentaldata = {'@id': 'value', '@type': 'sci:value'}
                    deriveddata = {'@id': 'value', '@type': 'sci:value'}
                    for cross in crosswalks:
                        if cross['sdsection'] == 'dataset':
                            if cross['table'] == serial_table:
                                for k, v in serial_dict.items():
                                    if k == cross['field']:
                                        if k not in ['type','bao_endpoint','standard_type']:
                                            if v is not None:
                                                if k.startswith('standard'):
                                                    deriveddata.update({k: str(v)})
                                                else:
                                                    experimentaldata.update({k: str(v)})
                    datapoint.append({
                        '@id': 'datapoint',
                        '@type': 'sci:datapoint',
                        'activity_id': ac['activity_id'],
                        'data': [
                            {
                                '@id': 'datum',
                                '@type': 'sci:exptdata',
                                'property': ac['type'],
                                'bao_endpoint': ac['bao_endpoint_id'],
                                'value': experimentaldata
                            },
                            {
                                '@id': 'datum',
                                '@type': 'sci:deriveddata',
                                'property': ac['standard_type'],
                                'deriveddata': deriveddata
                            }
                        ]
                    })
        datagroupA.append('datapoint')

        methodology = []
        methodology_set = set()
        methodologyA = {}
        for serial in serialized:
            for serial_table, serial_dict in serial.items():
                for cross in crosswalks:
                    if cross['sdsection'] == 'methodology':
                        if cross['table'] == serial_table:
                            methodology_set.add(cross['sdsubsection'])
        for met in methodology_set:
            methodologyA = ({
                '@id': met,
                '@type': 'sci:' + met})
            for serial in serialized:
                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['sdsection'] == 'methodology':
                            if cross['sdsubsection'] == met:
                                for k, v in serial_dict.items():
                                    if k == cross['field']:
                                        if v is not None:
                                            methodologyA.update({k: v})
            methodology.append(methodologyA)


        system = []
        system_set = set()
        systemA = {}
        for serial in serialized:
            for serial_table, serial_dict in serial.items():
                for cross in crosswalks:
                    if cross['sdsection'] == 'system':
                        if cross['table'] == serial_table:
                            system_set.add(cross['sdsubsection'])
        for sys in system_set:
            systemA = ({
                '@id': sys,
                '@type': 'sci:' + sys})
            for serial in serialized:
                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['sdsection'] == 'system':
                            if cross['sdsubsection'] == sys:
                                for k, v in serial_dict.items():
                                    if k == cross['field']:
                                        if v is not None:
                                            systemA.update({k:v})
            system.append(systemA)


        metadata = []
        for serial in serialized:
            for serial_table, serial_dict in serial.items():
                for cross in crosswalks:
                    if cross['sdsection'] == 'metadata':
                        if cross['table'] == serial_table:
                            for k, v in serial_dict.items():
                                if k == cross['field']:
                                    metadata.append({k: v, 'type': cross['sdsubsection']})

    datagroup.append({'@id': 'datagroup', '@type': 'sci:datagroup', 'chembl_id': str(chembl['molregno_id__chembl_id']), 'datapoints': datagroupA})
    test.starttime()
    test.aspects(methodology)
    test.facets(system)
    test.datapoint(datapoint)
    test.datagroup(datagroup)

    put = test.output
    with open(str(DocumentNumber) + '_' + str(chembl['molregno_id__chembl_id']) + '.json', 'w') as f:
        json.dump(put, f)

    break
    #
    # other = []
    # for serial in serialized:
    #     for serial_table, serial_dict in serial.items():
    #         for cross in crosswalks:
    #             if cross['sdsection'] == 'other':
    #                 if cross['table'] == serial_table:
    #                     for k,v in serial_dict.items():
    #                         if k == cross['field']:
    #                             other.append({k:v,'type':cross['sdsubsection']})
    # print(other)

# for x in crosswalks:
#     print(x)