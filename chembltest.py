from model import *
import os
import django
import ast

django.setup()
from scidata.chembldb import *
from scidata.crosswalks import *

path = r"/Users/n01448636/Documents/chembl django/scidata/JSON_dumps"
os.chdir(path)

dbname = 'default'
query_crosswalks_chembl = list(Chembl.objects.using('crosswalks').values())
query_crosswalks_ontterms = list(Ontterms.objects.using('crosswalks').values())
query_crosswalks_nspaces = list(Nspaces.objects.using('crosswalks').values())

Documents = set()
for x in Activities.objects.values().filter(herg=1):
    Documents.add(x['doc_id'])

# Documents = {36053, 5535, 5706, 6642, 6305, 50275} ###Remove this line to process all documents###
Documents = {5535}

for DocumentNumber in Documents:
    doc_data = {}
    doc_data.update(Docs.objects.values().get(doc_id=DocumentNumber))

    auth = doc_data['authors'].split(', ')
    authors = []
    for a in auth:
        authors.append({'name':a})

    namespace = {}


    ###############################

    test = SciData(doc_data['doc_id'])
    test.context('https://stuchalk.github.io/scidata/contexts/scidata.jsonld')
    test.base({"@base": "http://BASE.jsonld"})
    # test.doc_id("@ID HERE")
    test.graph_id("@graph_ID HERE")
    test.graph_uid("@unique_ID HERE")
    test.title(doc_data['title'])
    test.author(authors)
    test.description(doc_data['abstract'])
    test.publisher(doc_data['journal'])
    test.version('1.0')
    test.permalink("http://PERMALINK.jsonld")
    test.related("http://RELATED.jsonld")
    test.discipline('https://w3id.org/skgo/modsci#Chemistry')
    test.subdiscipline('https://w3id.org/skgo/modsci#MedicinalChemistry')
    # test.source([{"citation1": "Johnson Research Group http://CITATION.edu", "url": "http://CITATION.jsonld"}])
    test.rights("https://creativecommons.org/licenses/by-sa/3.0/legalcode")

    ####

    # test.add_context("added context")
    # test.add_namespace({"namespace2": "http://NAMESPACE.owl#"}) #content is replaced by test.namespace further in script
    # test.add_keyword('keyword 2')
    # test.add_source([{"citation2": "Chalk Research Group http://chalk.coas.unf.edu",
    #                   "url": "http://stuchalk.github.io/scidata/examples/ph.jsonld"}])
    # test.add_rights("rights 2")

    ###############################

    # activity_id_list = Docs.objects.get(doc_id=DocumentNumber).activities_set.all()

    crosswalks = []
    crosswalksA = {}

    for ont in query_crosswalks_chembl:
        crosswalksA = ont
        if crosswalksA['sdsection'] is None:
            for onto in query_crosswalks_ontterms:
                if crosswalksA['ontterm_id'] == onto['id']:
                    for x,y in onto.items():
                        crosswalksA.update({x:y})
        else:
            for onto in query_crosswalks_ontterms:
                if crosswalksA['ontterm_id'] == onto['id']:
                    for x,y in onto.items():
                        if x not in ['sdsection', 'sdsubsection']:
                            crosswalksA.update({x:y})
        crosswalks.append(crosswalksA)

    molregno_set = set()
    for mo in Activities.objects.values().filter(doc_id=DocumentNumber):
        molregno_set.add(mo['molregno_id'])
    # molregno_set = {610143}
    for mol in molregno_set:
        SciData.meta['@graph']['toc'] = []
        activity_list = Activities.objects.values().filter(doc_id=DocumentNumber, molregno_id=mol, herg=1)


        allunsorted = {}
        datapoint = []
        datagroup = []
        datagroupA = []
        namespacetoc = []
        methodology = []
        methodologyx = []
        system = []
        systemx = []
        nspaces = set()
        nspacestoc = set()

        for ac in activity_list:

            chembl = (Activities.objects.values('molregno_id__chembl_id').get(activity_id=ac['activity_id']))

            # serialized = serialize(Activities.objects.get(activity_id=ac['activity_id']), dbname)
            serializedpre = serialize(Activities.objects.get(activity_id=ac['activity_id']))


            serializedsetpre = set()
            for cross in crosswalks:
                if cross['category']:
                    serializedsetpre.add(cross['category'])
                else:
                    serializedsetpre.add(cross['table'])


            serialized = []
            for x,y in serializedpre.items():
                den = denester(x,y)
                serialized.append(den)

            serializednew = []
            for x in serialized:
                for y in x:
                    empty = {}
                    for sersetpre in serializedsetpre:
                        emptee = {sersetpre: {}}
                        for cross in crosswalks:
                            if cross['category']:
                                if cross['category'] == sersetpre:
                                    for serial_table, serial_dict in y.items():
                                        if cross['table'] == serial_table:
                                            emptee[sersetpre].update(serial_dict)

                            else:
                                if cross['table'] == sersetpre:
                                    for serial_table, serial_dict in y.items():
                                        if cross['table'] == serial_table:
                                            emptee[sersetpre].update(serial_dict)

                        if emptee[sersetpre]:
                            empty.update(emptee)

                    if empty:

                        serializednew.append(empty)

            serializedset = set()
            for cross in crosswalks:
                if cross['category']:
                    serializedset.add(cross['category'])
                else:
                    serializedset.add(cross['table'])


            serializedgrouped = []
            for serset in serializedset:
                ser1 = {serset:{}}
                for cross in crosswalks:
                    if cross['category']:
                        if cross['category'] == serset:
                            for serial in serializednew:
                                for serial_table,serial_dict in serial.items():
                                    if cross['table'] == serial_table:
                                        ser1[serset].update(serial_dict)
                    else:
                        if cross['table'] == serset:
                            for serial in serializednew:
                                for serial_table, serial_dict in serial.items():
                                    if cross['table'] == serial_table:
                                        ser1[serset].update(serial_dict)
                if ser1[serset]:
                    serializedgrouped.append(ser1)



            datapoint_set = set()
            for serial in serializedgrouped:

                # print(serial)

                allunsorted.update(serial)
                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['ignore'] is None:
                            if cross['sdsection'] == 'dataset':
                                if cross['table'] == serial_table:
                                    datapoint_set.add(cross['sdsubsection'])

            for serial in serializedgrouped:
                allunsorted.update(serial)
                for serial_table, serial_dict in serial.items():

                    dataall = []
                    datapointA = {}

                    for dat in datapoint_set:

                        datapointA = {}
                        meta = {}
                        exptmeta = {}
                        experimentaldata = {}
                        exptdataall = {}

                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'dataset':
                                    if cross['category']:
                                        if cross['category'] == serial_table:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:
                                                    nspaces.add(cross['nspace_id'])
                                                    nspacestoc.add(cross['url'])

                                                    if v not in ['None']:
                                                        if cross['sdsubsection'] == 'metadata':
                                                            meta.update({str(k): str(v)})
                                                        if cross['sdsubsection'] == dat:
                                                            if cross['meta'] is '1':
                                                                exptmeta.update({str(k): str(v)})
                                                            if cross['meta'] is not None:
                                                                if cross['meta'] is not '1':
                                                                    exptmeta.update({str(cross['meta']): str(v)})
                                                            if cross['meta'] is None:
                                                                experimentaldata.update({k: str(v)})
                                                                experimentaldata.update(
                                                                    {'@id': 'value', '@type': 'sci:value'})
                                    else:
                                        if cross['table'] == serial_table:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:
                                                    nspaces.add(cross['nspace_id'])
                                                    nspacestoc.add(cross['url'])

                                                    if v not in ['None']:
                                                        if cross['sdsubsection'] == 'metadata':
                                                            meta.update({str(k): str(v)})
                                                        if cross['sdsubsection'] == dat:
                                                            if cross['meta'] is '1':
                                                                exptmeta.update({str(k): str(v)})
                                                            if cross['meta'] is not None:
                                                                if cross['meta'] is not '1':
                                                                    exptmeta.update({str(cross['meta']): str(v)})
                                                            if cross['meta'] is None:
                                                                experimentaldata.update({k: str(v)})
                                                                experimentaldata.update(
                                                                    {'@id': 'value', '@type': 'sci:value'})

                        if experimentaldata:

                            exptdataall.update(exptmeta)
                            exptdataall.update({
                                '@id': 'datum',
                                '@type': 'sci:' + dat,
                                'value': experimentaldata
                            })

                            dataall.append(exptdataall)

                    if dataall:
                        datapointA.update(meta)
                        datapointA.update({
                            '@id': 'datapoint',
                            '@type': 'sci:datapoint',
                            'activity_id': ac['activity_id'],
                            'data': dataall
                        })

                    if datapointA:
                        datapoint.append(datapointA)
                        datagroupA.append('datapoint')
                        datapointA={}



            methodology_set = set()
            for serial in serializedgrouped:
                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['ignore'] is None:
                            if cross['sdsection'] == 'methodology':
                                if cross['table'] == serial_table:
                                    methodology_set.add(cross['sdsubsection'])
            for met in methodology_set:
                methodologyA = ({
                    '@id': met,
                    '@type': 'sci:' + met})
                for serial in serializedgrouped:
                    for serial_table, serial_dict in serial.items():
                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'methodology':
                                    if cross['table'] == serial_table:
                                        if cross['sdsubsection'] == met:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:
                                                    nspaces.add(cross['nspace_id'])
                                                    nspacestoc.add(cross['url'])
                                                    if v not in ['None']:
                                                        methodologyA.update({k: str(v)})
                methodology.append(methodologyA)
                methodologyx = [i for n, i in enumerate(methodology) if i not in methodology[n + 1:]]

            system_set = set()
            systemA = {}
            for serial in serializedgrouped:

                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['ignore'] is None:
                            if cross['sdsection'] == 'system':
                                if cross['table'] == serial_table:
                                    system_set.add(cross['sdsubsection'])
            for sys in system_set:
                systemA = ({
                    '@id': sys,
                    '@type': 'sci:' + sys})
                for serial in serializedgrouped:
                    for serial_table, serial_dict in serial.items():
                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'system':
                                    if cross['table'] == serial_table:
                                        if cross['sdsubsection'] == sys:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:
                                                    nspaces.add(cross['nspace_id'])
                                                    nspacestoc.add(cross['url'])
                                                    if v not in ['None']:
                                                        systemA.update({k:v})
                system.append(systemA)
                systemx = [i for n, i in enumerate(system) if i not in system[n + 1:]]

            metadata = []
            for serial in serializedgrouped:
                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['sdsection'] == 'metadata':
                            if cross['table'] == serial_table:
                                for k, v in serial_dict.items():
                                    if k == cross['field']:
                                        metadata.append({k: v, 'type': cross['sdsubsection']})
        #
            # print('xxx',metadata)

        if datagroupA:
            datagroup.append(
                {'@id': 'datagroup', '@type': 'sci:datagroup', 'chembl_id': str(mol), 'datapoints': datagroupA})
        #

        if methodology:
            test.aspects(methodologyx)
        if system:
            test.facets(systemx)
        if datapoint:
            test.datapoint(datapoint)
        if datagroup:
            test.datagroup(datagroup)
        #
        if nspaces:
            for x in nspaces:
                for y in query_crosswalks_nspaces:
                    if y['id'] == x:
                        namespace.update({y['ns']:y['path']})

        if nspacestoc:
            for x in nspacestoc:
                namespacetoc.append(x)


        if namespace:
            namespaces = ", ".join(repr(e) for e in namespace)
            test.namespace(namespace)
        if namespacetoc:
            test.ids(namespacetoc)



        try:
            test.add_keyword(allunsorted['activities']['type'])
        except:
            pass
        try:
            test.add_keyword(allunsorted['target_dictionary']['pref_name'])
        except:
            pass
        try:
            test.add_keyword(allunsorted['cell_dictionary']['cell_name'])
        except:
            pass
        try:
            test.add_keyword(allunsorted['molecule_dictionary']['molecule_type'])
        except:
            pass

        if datapoint:

            test.starttime()
            test.doc_id('scidata:chembl'+allunsorted['docs']['doc_id']+'_'+allunsorted['molecule_dictionary']['chembl'])
            test.source([{'doi':allunsorted['docs']['doi']}])
            put = test.output
            with open(str(DocumentNumber) + '_' + str(allunsorted['molecule_dictionary']['chembl']) + '.json', 'w') as f:
                json.dump(put, f)



                #
                # other = []
                # for serial in serializedgrouped:
                #     for serial_table, serial_dict in serial.items():
                #         for cross in crosswalks:
                #             if cross['sdsection'] == 'other':
                #                 if cross['table'] == serial_table:
                #                     for k,v in serial_dict.items():
                #                         if k == cross['field']:
                #                             other.append({k:v,'type':cross['sdsubsection']})
                # print(other)

