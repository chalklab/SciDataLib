from model import *
import os
import django

django.setup()
from scidata.chembldb26 import *
from scidata.crosswalks import *

path = r"/Users/n01448636/Documents/PycharmProjects/chembl_django/scidata/JSON_dumps"
os.chdir(path)

dbname = 'default'
query_crosswalks_chembl = list(Chembl.objects.using('crosswalks').values())
query_crosswalks_ontterms = list(Ontterms.objects.using('crosswalks').values())
query_crosswalks_nspaces = list(Nspaces.objects.using('crosswalks').values())


'''
Filter Docs by Target ChemblID
HERG gene Chembl is 240 
BAD gene Chembl is 3817. 
'''
targetchembl = 'CHEMBL240'
Documents = set()
AssaySet = set()
for x in TargetDictionary.objects.values().filter(chembl_id=targetchembl):
    for y in Assays.objects.values().filter(tid=x['tid']):
        AssaySet.add(y['assay_id'])
        Documents.add(y['doc_id'])
AssayList = list(AssaySet)

'''Specify document(s) explicitly. Specified Document must contain a molregno that targets the specified targetchembl'''
Documents = {51366} # Hash this line to process all documents

for DocumentNumber in Documents:
    doc_data = {}
    doc_data.update(Docs.objects.values().get(doc_id=DocumentNumber))
    try:
        auth = doc_data['authors'].split(', ')
    except:
        auth = ['Anonymous']
        # print(DocumentNumber)
    authors = []
    for a in auth:
        authors.append({'name':a})
    namespace = {}

    ###############################

    test = SciData(doc_data['doc_id'])
    test.context(['https://stuchalk.github.io/scidata/contexts/chembl.jsonld','https://stuchalk.github.io/scidata/contexts/scidata.jsonld'])
    test.base({"@base": "http://BASE.jsonld"})
    # test.doc_id("@ID HERE")
    test.graph_id("graph_ID_HERE")
    test.title(doc_data['title'])
    test.author(authors)
    test.description(doc_data['abstract'])
    test.publisher(doc_data['journal'])
    test.version('1.0')
    test.permalink("http://PERMALINK.jsonld")
    # test.related("http://RELATED.jsonld")
    test.discipline('w3i:Chemistry')
    test.subdiscipline('w3i:MedicinalChemistry')
    # test.source([{"citation1": "Johnson Research Group http://CITATION.edu", "url": "http://CITATION.jsonld"}])
    test.rights("https://creativecommons.org/licenses/by-nc-nd/4.0/")
    addnamespace = {'w3i':'https://w3id.org/skgo/modsci#'}

    ####

    # test.add_context("added context")
    # test.add_namespace({"namespace2": "http://NAMESPACE.owl#"}) #content is replaced by test.namespace further in script
    # test.add_keyword('keyword 2')
    # test.add_source([{"citation2": "Chalk Research Group http://chalk.coas.unf.edu",
    #                   "url": "http://stuchalk.github.io/scidata/examples/ph.jsonld"}])
    # test.add_rights("rights 2")

    ###############################

    '''Integrate chembl and ontterms crosswalks'''
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


    '''Query molregnos for the specified targetchembl and Documents (if specified)'''
    molregno_set = set()
    for x in TargetDictionary.objects.values().filter(chembl_id=targetchembl):
        for y in Assays.objects.values().filter(tid=x['tid'], doc_id=DocumentNumber):
            for z in Activities.objects.values().filter(assay_id=y['assay_id']):
                molregno_set.add(z['molregno_id'])
    ''''''

    ''' limiter to process only one molregno from each doc number. Hash out to process all molregnos'''
    molregno_set = {list(molregno_set)[0]}
    print(molregno_set)

    # '''Manual molregno set override. Must target specified targetchembl. Hash out to use defaults'''
    # molregno_set = [632150]

    for mol in molregno_set:
        SciData.meta['@graph']['toc'] = []
        activity_list = Activities.objects.values().filter(doc_id=DocumentNumber, molregno_id=mol, assay_id__in=AssayList) #list of activity_ids for each molregno for each doc_id
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

            serializedpre = serialize(Activities.objects.get(activity_id=ac['activity_id'])) #Pulls in all data linked to specifiy activity_id. serialize definition in model file.

            '''creates list of crosswalks tables that crosswalk entries are sorted into after merging based on crosswalks category value if present'''
            serializedsetpre = set()
            for cross in crosswalks:
                if cross['category']:
                    serializedsetpre.add(cross['category'])
                else:
                    serializedsetpre.add(cross['table'])


            '''Remove nesting and convert to a list of dictionaries where each dictionary corresponds to one crosswalks table'''
            serialized = []
            for x,y in serializedpre.items():
                den = denester(x,y)
                serialized.append(den)


            '''Reassigns list of dictionaries based on category designation'''
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

            '''removes duplication'''
            serializednew2 = []
            for x in serializednew:
                if x not in serializednew2:
                    serializednew2.append(x)
            serializednew = serializednew2
            # print(serializednew)

            '''creates new list of tables present with data'''
            serializedset = set()
            for cross in crosswalks:
                if cross['category']:
                    serializedset.add(cross['category'])
                else:
                    serializedset.add(cross['table'])

            '''Merges list of dictionaries with same table'''
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

            '''creates list of sdsubsections'''
            datapoint_set = set()
            for serial in serializedgrouped:
                for serial_table, serial_dict in serial.items():
                    for cross in crosswalks:
                        if cross['ignore'] is None:
                            if cross['sdsection'] == 'dataset':
                                if cross['category']:
                                    if cross['category'] == serial_table:
                                        datapoint_set.add(cross['sdsubsection'])
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
                        exptmeta = {'table_name__placeholder':''}
                        experimentaldata = {}
                        exptdataall = {}

                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'dataset':
                                    if cross['category']:
                                        if cross['category'] == serial_table:

                                            for k, v in serial_dict.items():

                                                if k == cross['field']:

                                                    if v not in ['None']:
                                                        nspaces.add(cross['nspace_id'])
                                                        nspacestoc.add(cross['url'])
                                                        if cross['sdsubsection'] == 'metadata':
                                                            meta.update({str(k): str(v)})
                                                        if cross['sdsubsection'] == dat:
                                                            if cross['meta'] == '1':
                                                                exptmeta.update({str(k): str(v)})
                                                            if cross['meta'] is not None:
                                                                if cross['meta'] != '1':
                                                                    exptmeta.update({str(cross['meta']): str(v)})
                                                            if cross['meta'] is None:
                                                                if not exptmeta['table_name__placeholder']:
                                                                    exptmeta.update({'table_name__placeholder': cross['table']})
                                                                experimentaldata.update({k: str(v)})
                                                                experimentaldata.update(
                                                                    {'@id': 'value', '@type': 'sci:value'})
                                    else:
                                        if cross['table'] == serial_table:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:

                                                    if v not in ['None']:
                                                        nspaces.add(cross['nspace_id']) #$$$
                                                        nspacestoc.add(cross['url'])
                                                        if cross['sdsubsection'] == 'metadata':
                                                            meta.update({str(k): str(v)})
                                                        if cross['sdsubsection'] == dat:
                                                            if cross['meta'] == '1':
                                                                exptmeta.update({str(k): str(v)})
                                                            if cross['meta'] is not None:
                                                                if cross['meta'] != '1':
                                                                    exptmeta.update({str(cross['meta']): str(v)})
                                                            if cross['meta'] is None:
                                                                if not exptmeta['table_name__placeholder']:
                                                                    exptmeta.update({'table_name__placeholder': cross['table']})
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
                methodologyA = {}
                for serial in serializedgrouped:
                    for serial_table, serial_dict in serial.items():
                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'methodology':
                                    if cross['table'] == serial_table:
                                        if cross['sdsubsection'] == met:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:

                                                    if v not in ['None']:
                                                        nspaces.add(cross['nspace_id'])
                                                        nspacestoc.add(cross['url'])
                                                        methodologyA.update({
                                                            '@id': met,
                                                            '@type': 'sci:' + met})
                                                        methodologyA.update({k: str(v)})
                if methodologyA:
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
                systemA = {}
                for serial in serializedgrouped:
                    for serial_table, serial_dict in serial.items():
                        for cross in crosswalks:
                            if cross['ignore'] is None:
                                if cross['sdsection'] == 'system':
                                    if cross['table'] == serial_table:
                                        if cross['sdsubsection'] == sys:
                                            for k, v in serial_dict.items():
                                                if k == cross['field']:
                                                    if v not in ['None']:
                                                        if cross['sdsubsubsection'] is not None:
                                                            nspaces.add(cross['nspace_id'])
                                                            nspacestoc.add(cross['url'])
                                                            try:
                                                                systemA[cross['sdsubsubsection']].update({k:v})
                                                            except:
                                                                systemA.update({cross['sdsubsubsection']: {}})
                                                                systemA[cross['sdsubsubsection']].update({
                                                                    "@id": cross['sdsubsubsection'],
                                                                    "@type": "sci:"+cross['sdsubsubsection'],
                                                                    k: v})
                                                        else:
                                                            nspaces.add(cross['nspace_id'])
                                                            nspacestoc.add(cross['url'])
                                                            systemA.update({
                                                                '@id': sys,
                                                                '@type': 'sci:' + sys})
                                                            systemA.update({k:v})
                if systemA:
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
                {'@id': 'datagroup', '@type': 'sci:datagroup', 'chembl_id': str(allunsorted['molecule_dictionary']['chembl_id']), 'datapoints': datagroupA})
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
            test.add_namespace(addnamespace)

        if namespacetoc:
            test.ids(namespacetoc)

        relate = ''
        if relate:
            test.related(relate)



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
            test.doc_id('scidata:chembl'+allunsorted['docs']['doc_id']+'_'+allunsorted['molecule_dictionary']['chembl_id'])
            test.source([{'title':allunsorted['docs']['title'],
                          'doi':allunsorted['docs']['doi'],
                          'journal':allunsorted['docs']['journal'],
                          'year':allunsorted['docs']['year'],
                          'volume':allunsorted['docs']['volume'],
                          'issue':allunsorted['docs']['issue']}])
            test.add_source([{"url": "https://www.ebi.ac.uk/chembl/document_report_card/"+allunsorted['docs']['chembl_id']+"/"}])
            test.graph_uid('scidata:chembl'+allunsorted['docs']['doc_id']+'_'+allunsorted['molecule_dictionary']['chembl_id'])
            put = test.output
            with open(str(DocumentNumber) + '_' + str(allunsorted['molecule_dictionary']['chembl_id']) + '.jsonld', 'w') as f:
                json.dump(put, f)




