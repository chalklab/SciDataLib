from scidata.model import *
import os
import django

django.setup()
from scidata.dsstoxdb import *
from scidata.crosswalks import *

path = r"/Users/n01448636/Documents/chembl django/scidata/JSON_dumps"
os.chdir(path)

dbname = 'dsstox'
query_crosswalks_dsstox = list(Ncct.objects.using('crosswalks').values())
query_crosswalks_ontterms = list(Ontterms.objects.using('crosswalks').values())
query_crosswalks_nspaces = list(Nspaces.objects.using('crosswalks').values())

dssChemicalListID = 127

dssGenericSubstances = set()
for x in GenericSubstances.objects.values().using('dsstox').filter(sourcegenericsubstancemappings__fk_source_substance__fk_chemical_list_id=dssChemicalListID):
    dssGenericSubstances.add(x['id'])

dssGenericSubstances = {20001}

#
for dssGS in dssGenericSubstances:
    dsschemlist = {}
    dsschemlist.update(ChemicalLists.objects.using('dsstox').values().get(id=dssChemicalListID))

    authors = [{'name':dsschemlist['ncct_contact']},{'name':dsschemlist['source_contact']}]

    namespace = {}

    ###############################

    test = SciData(str(dssChemicalListID))
    test.context('context HERE')
    test.base({"@base": "http://BASE.jsonld"})
    test.doc_id("@ID HERE")
    test.graph_id("@graph_ID HERE")
    test.graph_uid("@unique_ID HERE")
    test.title(dssGS)
    test.author(authors)
    test.description(dsschemlist['label'])
    test.publisher(dsschemlist['created_by'])
    test.version('X.X')
    test.permalink("http://PERMALINK.jsonld")
    test.related("http://RELATED.jsonld")
    test.discipline('science')
    test.subdiscipline('subscience')
    test.source([{"citation1": "Johnson Research Group http://CITATION.edu", "url": "http://CITATION.jsonld"}])
    test.rights("http://creativecommons.org/publicdomain/zero/1.0/")
#
#     ####
#
#     test.add_context("added context")
#     # test.add_namespace({"namespace2": "http://NAMESPACE.owl#"}) #content is replaced by test.namespace further in script
#     # test.add_keyword('keyword 2')
#     test.add_source([{"citation2": "Chalk Research Group http://chalk.coas.unf.edu",
#                       "url": "http://stuchalk.github.io/scidata/examples/ph.jsonld"}])
#     test.add_rights("rights 2")
#
#     ###############################
#
#     # activity_id_list = Docs.objects.get(doc_id=DocumentNumber).activities_set.all()
#
    crosswalks = []
    crosswalksA = {}
#
    # for ont in query_crosswalks_dsstox:
    #     crosswalksA = ont
    #     if crosswalksA['sdsection'] is None:
    #         for onto in query_crosswalks_ontterms:
    #             if crosswalksA['ontterm_id'] == onto['id']:
    #                 for x,y in onto.items():
    #                     crosswalksA.update({x:y})
    #     else:
    #         for onto in query_crosswalks_ontterms:
    #             if crosswalksA['ontterm_id'] == onto['id']:
    #                 for x,y in onto.items():
    #                     if x not in ['sdsection', 'sdsubsection']:
    #                         crosswalksA.update({x:y})
    #     crosswalks.append(crosswalksA)
#

#
#     molregno_set = set()
#     for mo in Activities.objects.values().filter(doc_id=DocumentNumber):
#         molregno_set.add(mo['molregno_id'])
#     molregno_set = {81741}
#     for mol in molregno_set:
    SciData.meta['@graph']['toc'] = []
#         activity_list = Activities.objects.values().filter(doc_id=DocumentNumber, molregno_id=mol)
#
    allunsorted = {}
    datapoint = []
    datagroup = []
    datagroupA = []
    methodology = []
    methodologyx = []
    system = []
    systemx = []
#
#
#         for ac in activity_list:
#             if ac['herg'] == 1:
#
    datapointA = {}

    meta = {}
    exptmeta = {}
    derivedmeta = {}
    suppmeta = {}
    nspaces = set()
    experimentaldata = {}
    deriveddata = {}
    suppdata = {}
#
#                 chembl = (Activities.objects.values('molregno_id__chembl_id').get(activity_id=ac['activity_id']))
#

    serialized = serialize(GenericSubstances.objects.using(dbname).get(id=dssGS), dbname)
#
#
#
    for serial in serialized:
        print(serial)
#                     allunsorted.update(serial)
#                     for serial_table, serial_dict in serial.items():
#                         if serial_table == 'activities':
#                             datagroupA.append('datapoint')
#                             for cross in crosswalks:
#                                 if cross['sdsection'] == 'dataset':
#                                     if cross['table'] == serial_table:
#                                         for k, v in serial_dict.items():
#                                             if k == cross['field']:
#                                                 nspaces.add(cross['nspace_id'])
#
#                                                 if v is not None:
#                                                     if cross['sdsubsection'] == 'metadata':
#                                                         meta.update({str(k): str(v)})
#
#                                                     if cross['sdsubsection'] == 'exptdata':
#                                                         if cross['meta'] is '1':
#                                                             exptmeta.update({str(k): str(v)})
#                                                         if cross['meta'] is not None:
#                                                             if cross['meta'] is not '1':
#                                                                 exptmeta.update({str(cross['meta']): str(v)})
#                                                         if cross['meta'] is None:
#                                                             experimentaldata.update({k: str(v)})
#                                                             experimentaldata.update({'@id': 'value', '@type': 'sci:value'})
#
#                                                     if cross['sdsubsection'] == 'deriveddata':
#                                                         if cross['meta'] is '1':
#                                                             derivedmeta.update({str(k): str(v)})
#                                                         if cross['meta'] is not None:
#                                                             if cross['meta'] is not '1':
#                                                                 derivedmeta.update({str(cross['meta']): str(v)})
#                                                         if cross['meta'] is None:
#                                                             deriveddata.update({k: str(v)})
#                                                             deriveddata.update({'@id': 'value', '@type': 'sci:value'})
#
#                                                     if cross['sdsubsection'] == 'suppdata':
#                                                         if cross['meta'] is '1':
#                                                             suppmeta.update({str(k): str(v)})
#                                                         if cross['meta'] is not None:
#                                                             if cross['meta'] is not '1':
#                                                                 suppmeta.update({str(cross['meta']): str(v)})
#                                                         if cross['meta'] is None:
#                                                             suppdata.update({k: str(v)})
#                                                             suppdata.update({'@id': 'value', '@type': 'sci:value'})
#
#                             dataall = []
#                             if experimentaldata:
#                                 exptdataall = exptmeta
#                                 exptdataall.update({
#                                             '@id': 'datum',
#                                             '@type': 'sci:exptdata',
#                                             'value': experimentaldata
#                                             })
#
#                                 dataall.append(exptdataall)
#                             if deriveddata:
#                                 deriveddataall = derivedmeta
#                                 deriveddataall.update({
#                                             '@id': 'datum',
#                                             '@type': 'sci:deriveddata',
#                                             'value': deriveddata
#                                             })
#
#                                 dataall.append(deriveddataall)
#                             if suppdata:
#                                 suppdataall = suppmeta
#                                 suppdataall.update({
#                                             '@id': 'datum',
#                                             '@type': 'sci:suppdata',
#                                             'value': suppdata
#                                             })
#                                 dataall.append(suppdataall)
#
#                             datapointA.update(meta)
#                             datapointA.update({
#                                 '@id': 'datapoint',
#                                 '@type': 'sci:datapoint',
#                                 'activity_id': ac['activity_id'],
#                                 'data': dataall
#                             })
#
#                             datapoint.append(datapointA)
#
#                 methodology_set = set()
#                 methodologyA = {}
#                 for serial in serialized:
#                     for serial_table, serial_dict in serial.items():
#                         for cross in crosswalks:
#                             if cross['sdsection'] == 'methodology':
#                                 if cross['table'] == serial_table:
#                                     methodology_set.add(cross['sdsubsection'])
#                 for met in methodology_set:
#                     methodologyA = ({
#                         '@id': met,
#                         '@type': 'sci:' + met})
#                     for serial in serialized:
#                         for serial_table, serial_dict in serial.items():
#                             for cross in crosswalks:
#                                 if cross['sdsection'] == 'methodology':
#                                     if cross['table'] == serial_table:
#                                         if cross['sdsubsection'] == met:
#                                             for k, v in serial_dict.items():
#                                                 if k == cross['field']:
#                                                     if v is not None:
#                                                         methodologyA.update({k: str(v)})
#                     methodology.append(methodologyA)
#                     methodologyx = [i for n, i in enumerate(methodology) if i not in methodology[n + 1:]]
#
#                 system_set = set()
#                 systemA = {}
#                 for serial in serialized:
#
#                     for serial_table, serial_dict in serial.items():
#
#                         for cross in crosswalks:
#
#
#                             if cross['sdsection'] == 'system':
#
#                                 if cross['table'] == serial_table:
#
#                                     system_set.add(cross['sdsubsection'])
#                 for sys in system_set:
#                     systemA = ({
#                         '@id': sys,
#                         '@type': 'sci:' + sys})
#                     for serial in serialized:
#                         for serial_table, serial_dict in serial.items():
#                             for cross in crosswalks:
#                                 if cross['sdsection'] == 'system':
#                                     if cross['table'] == serial_table:
#                                         if cross['sdsubsection'] == sys:
#                                             for k, v in serial_dict.items():
#                                                 if k == cross['field']:
#                                                     if v:
#                                                         systemA.update({k:v})
#                     system.append(systemA)
#                     systemx = [i for n, i in enumerate(system) if i not in system[n + 1:]]
#
#                 metadata = []
#                 for serial in serialized:
#                     for serial_table, serial_dict in serial.items():
#                         for cross in crosswalks:
#                             if cross['sdsection'] == 'metadata':
#                                 if cross['table'] == serial_table:
#                                     for k, v in serial_dict.items():
#                                         if k == cross['field']:
#                                             metadata.append({k: v, 'type': cross['sdsubsection']})
#
#
#
#         if datagroupA:
#             datagroup.append(
#                 {'@id': 'datagroup', '@type': 'sci:datagroup', 'chembl_id': str(mol), 'datapoints': datagroupA})
#
#         if methodology:
#             test.aspects(methodologyx)
#         if system:
#             test.facets(systemx)
#         if datapoint:
#             test.datapoint(datapoint)
#         if datagroup:
#             test.datagroup(datagroup)
#
#         if nspaces:
#             for x in nspaces:
#                 for y in query_crosswalks_nspaces:
#                         if y['id'] == x:
#                             namespace.update({y['ns']:y['path']})
#         if namespace:
#             namespaces = ", ".join(repr(e) for e in namespace)
#             test.namespace(namespace)
#         test.starttime()
#
#
#         try:
#             test.add_keyword(allunsorted['activities']['type'])
#         except:
#             pass
#         try:
#             test.add_keyword(allunsorted['target_dictionary']['pref_name'])
#         except:
#             pass
#         try:
#             test.add_keyword(allunsorted['cell_dictionary']['cell_name'])
#         except:
#             pass
#         try:
#             test.add_keyword(allunsorted['molecule_dictionary']['molecule_type'])
#         except:
#             pass
#
#         if datapoint:
#             put = test.output
#             with open(str(DocumentNumber) + '_' + str(mol) + '.json', 'w') as f:
#                 json.dump(put, f)

    put = test.output
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

