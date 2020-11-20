import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from scidata.model import *
from scidata.sciflowdb import Datasets
from scidata.crosswalks import *
from scidata.serializers import *
from pyld import jsonld
import datetime

path = r"/Users/n01448636/Documents/GoogleDrive/PycharmProjects/SciDataLib/scidata/JSON_dumps"
os.chdir(path)

dbname = 'default'
query_crosswalks_chembl = list(Chembl.objects.using('crosswalks').values())
query_crosswalks_ontterms = list(Ontterms.objects.using('crosswalks').values())
query_crosswalks_nspaces = list(Nspaces.objects.using('crosswalks').values())

'''Dataset Identifiers'''
datasetname = 'herg'
sourcecode = Datasets.objects.using('sciflow').values('sourcecode').get(datasetname=datasetname)['sourcecode']


'''Filter Docs by Target ChemblID, HERG gene is 240, SARS-COV-2 is 4303835, PSEN1 is 2473'''
targetchembl = 'CHEMBL2176846'
targetchemblid = targetchembl.replace("CHEMBL","")


'''Special Cases. Leave False for general use'''
populateall = False #Generate data for all fields that have crosswalk entry
fast_doc = False #Test script quickly by only processing one unspecified doc_id
fast_mol = False #Test script quickly by only processing one unspecified molregno
specific_document = 92795 #internal doc_id for specific document
specific_molregno = False #molregno of molecule of interest
specific_activity = False #activity_id of specific activity of interest
specific_target_organism = False #assay target organism

# '''Special Cases. Leave False for general use'''
# populateall = False #Generate data for all fields that have crosswalk entry
# fast_doc = False #Test script quickly by only processing one unspecified doc_id
# fast_mol = True #Test script quickly by only processing one unspecified molregno
# specific_document = 5535 #internal doc_id for specific document
# specific_molregno = False #molregno of molecule of interest
# specific_activity = False #activity_id of specific activity of interest
# specific_target_organism = 'Homo sapiens' #assay target organism



# DocSer = DocsSerializer(Docs.objects.get(doc_id=specific_document, activities__herg=1))

# x = JSONRenderer().render(DocSer.data)
# print(x)
#
# exit()



Documents = set()
for x in TargetDictionary.objects.values().filter(chembl_id_lookup=targetchembl):
    for y in Assays.objects.values().filter(target_dictionary=x['tid']):
        Documents.add(y['docs_id'])

# Documents = [specific_document]
# for document in Documents:
#     DocSer = DocsSerializer(Docs.objects.get(doc_id=document))
#     print(DocSer)

# exit()

if populateall:
    Documents = {list(Documents)[0]}
if fast_doc:
    Documents = {list(Documents)[0]}
if specific_document:
    Documents = {specific_document}

for DocumentNumber in Documents:

    doc_data = {}
    doc_data.update(Docs.objects.values().get(doc_id=DocumentNumber))
    try:
        auth = doc_data['authors'].split(', ')
    except:
        auth = ['Anonymous']
    authors = []
    for a in auth:
        authors.append({'name':a})
    namespace = {}

    ###############################

    test = SciData(doc_data['doc_id'])

    test.context(['https://stuchalk.github.io/scidata/contexts/chembl.jsonld','https://stuchalk.github.io/scidata/contexts/scidata.jsonld'])
    # test.doc_id("@ID HERE")
    test.graph_id("")
    test.generatedAt(str(datetime.datetime.now()))
    test.version('1')
    test.dateTime()
    test.graph_type("sdo:scidata")
    test.title(doc_data['title'])
    test.author(authors)
    test.description(doc_data['abstract'])
    test.publisher(doc_data['journal'])
    test.graphversion('version from GraphDB')
    # test.related("http://RELATED.jsonld")
    test.discipline('w3i:Chemistry')
    test.subdiscipline('w3i:MedicinalChemistry')
    test.rights("https://creativecommons.org/licenses/by-nc-nd/4.0/","European Bioinformatics Institute")
    addnamespace = {'sdo': 'https://stuchalk.github.io/scidata/ontology/scidata.owl#','w3i':'https://w3id.org/skgo/modsci#'}

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

    allgroupedtableset = set()
    for x in crosswalks:
        allgroupedtableset.add(x['table'])
    allgrouped = []  # replaces serializednew
    for table in allgroupedtableset:
        entries = {}
        for x in crosswalks:
            if x['table'] == table:
                entries.update({x['field']:x['field']+'_data'})
        allgrouped.append({table:entries})

    '''Query molregnos for the specified targetchembl and Documents (if specified)'''
    molregno_set = set()
    assays_set = set()
    for x in TargetDictionary.objects.values().filter(chembl_id_lookup=targetchembl):
        for y in Assays.objects.values().filter(target_dictionary=x['tid'], docs_id=DocumentNumber):
            assays_set.add(y['assay_id'])
            for z in Activities.objects.values().filter(assays_id=y['assay_id'], docs_id=DocumentNumber):
                molregno_set.add(z['molecule_dictionary_id'])
    AssayList = list(assays_set)

    if populateall:
        molregno_set = {list(molregno_set)[0]}
    if fast_mol:
        molregno_set = {list(molregno_set)[0]}
    if specific_molregno:
        molregno_set = [specific_molregno]

    for mol in molregno_set:

        # for eachassay in AssayList: #for further division of output by assay

            SciData.meta['@graph']['toc'] = []
            activity_list = Activities.objects.values().filter(docs_id=DocumentNumber, molecule_dictionary_id=mol, assays_id__in=AssayList) #list of activity_ids for each molregno for each doc_id
            # activity_list = Activities.objects.values().filter(docs_id=DocumentNumber, molecule_dictionary_id=mol, assays_id=eachassay) #list of activity_ids for each molregno for each doc_id
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

            if specific_activity:
                activity_list = activity_list.values().filter(activity_id=specific_activity)
            for ac in activity_list:

                ActivitiesObjectA = ActivitiesSerializer(Activities.objects.get(activity_id=ac['activity_id']))
                x = (ActivitiesObjectA.data)
                # print(json.dumps(x))
                pre1 = {}
                activities = {}
                nested = {}

                pre2 = dict(ActivitiesObjectA.data)
                # print(pre2)
                for k, v in pre2.items():
                    if v is None:
                        pass
                    elif type(v) in [int, str]:
                        activities.update({k: v})
                    else:
                        nested.update({k: v})
                pre1.update({'activities': activities})
                pre1.update(nested)
                allunsorted = json.dumps(pre1)
                serializedprepre = json.loads(allunsorted)
                assaylink = serializedprepre["assays"]["chembl_id_lookup"]["chembl_id"]


                def chemblidmod(input):
                    dictA = {}
                    def chemblidmod2(a,b):
                        dictB = {}
                        for c,d in b.items():
                            # if c == "chembl_id_lookup":
                            if c in ["chembl_id_lookup", "bioassay_ontology"]:
                                # new = b.items().copy()
                                # new[c].update(d)
                                dictB.update(d)
                            elif type(d) is dict:
                                dictB.update(chemblidmod2(c, d))
                            else:
                                dictB.update({c: d})
                        if dictB:
                            dictC = {a:dictB}
                            return dictC
                    for x, y in input.items():
                        if type(y) is dict:
                            dictA.update(chemblidmod2(x,y))
                        else:
                            dictA.update({x: y})
                    return dictA

                serializedpre = chemblidmod(serializedprepre)
                # print(json.dumps(serializedpre))

                '''creates list of crosswalks tables that crosswalk entries are sorted into after merging based on crosswalks category value if present'''
                serializedsetpre = set()
                for cross in crosswalks:
                    if cross['category']:
                        serializedsetpre.add(cross['category'])
                    else:
                        serializedsetpre.add(cross['table'])

                '''Remove nesting and convert to a list of dictionaries where each dictionary corresponds to one crosswalks table'''
                serialized = {}
                for x,y in serializedpre.items():
                    den = denester(x,y)
                    if den:
                        serialized.update(den)

                '''Reassigns list of dictionaries based on category designation'''
                serializednew = {}
                for serial_table, serial_dict in serialized.items():

                    empty = {}
                    for sersetpre in serializedsetpre:
                        emptee = {sersetpre: {}}
                        for cross in crosswalks:
                            if cross['category']:
                                if cross['category'] == sersetpre:
                                    if cross['table'] == serial_table:
                                        emptee[sersetpre].update(serial_dict)

                            else:
                                if cross['table'] == sersetpre:
                                    if cross['table'] == serial_table:
                                        emptee[sersetpre].update(serial_dict)

                        if emptee[sersetpre]:
                            empty.update(emptee)

                    if empty:
                        serializednew.update(empty)
                # print(json.dumps(serializednew))
                '''removes duplication'''

                if populateall:
                    serializednew = allgrouped

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
                                for serial_table,serial_dict in serializednew.items():
                                    if cross['table'] == serial_table:
                                        ser1[serset].update(serial_dict)
                        else:
                            if cross['table'] == serset:
                                for serial_table, serial_dict in serializednew.items():
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
                                'assay_link': assaylink,
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

            if datagroupA:
                datagroup.append(
                    {'@id': 'datagroup', '@type': 'sci:datagroup', 'chembl_id': serializedpre['molecule_dictionary']['chembl_id'], 'datapoints': datagroupA})

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
                test.namespace(addnamespace)
                test.add_namespace(namespace)

            if namespacetoc:
                test.ids(namespacetoc)

            relate = ''
            if relate:
                test.related(relate)

            # if serializedpre['activities']['type']:
            #     test.add_keyword(serializedpre['activities']['type'])

            try:
                test.add_keyword(serializedpre['activities']['type'])
            except:
                pass
            try:
                test.add_keyword(serializedpre['assays']['target_dictionary']['pref_name'])
            except:
                pass
            try:
                test.add_keyword(serializedpre['cell_dictionary']['cell_name'])
            except:
                pass
            try:
                test.add_keyword(serializedpre['molecule_dictionary']['molecule_type'])
            except:
                pass

            if datapoint:

                test.toc()
                documentchemblid = str(serializedpre['docs']['chembl_id'].replace("CHEMBL", "_"))
                moleculechemblid = str(serializedpre['molecule_dictionary']['chembl_id'].replace("CHEMBL", "_"))
                assaychemblid = str(serializedpre['assays']['assay_id'])
                unique_id = targetchemblid+documentchemblid+moleculechemblid

                test.base({"@base": "https://scidata.unf.edu/" + sourcecode + "/" + datasetname + unique_id + "/"})
                test.permalink("https://scidata.unf.edu/" + sourcecode + "/" + datasetname + unique_id + "/")

                test.doc_id("https://scidata.unf.edu/" + sourcecode + "/"+ datasetname + unique_id+"/")
                if doc_data['doi']:
                    test.source([{'title': doc_data['title'],
                                  'doi':'https://doi.org/'+doc_data['doi'],
                                  'type': doc_data['doc_type']}])
                else:
                    test.source([{'title':doc_data['title'],
                                  'type': doc_data['doc_type'],
                                  'journal':doc_data['journal'],
                                  'year':doc_data['year'],
                                  'volume':doc_data['volume'],
                                  'issue':doc_data['issue']}])
                test.add_source([{'type': 'database', "url": "https://www.ebi.ac.uk/chembl/document_report_card/"+serializedpre['docs']['chembl_id']+"/"}])
                test.graph_uid("scidata:"+sourcecode+":"+datasetname+":"+unique_id)
                test.sourcecode(sourcecode)
                test.datasetname(datasetname)

                put = test.output

                linkinglist = ['assay_link']

                def link(input):
                    def finddict(a, f):
                        for key, value in a.items():
                            if value == f:
                                if key not in linkinglist:
                                    return(a["@id"])

                            if isinstance(value, list):
                                if findlist(value, f):
                                    return findlist(value, f)
                            if isinstance(value, dict):
                                if finddict(value, f):
                                    return finddict(value, f)

                    def findlist(a, f):
                        for x in a:
                            if isinstance(x, dict):
                                if finddict(x, f):
                                    return finddict(x,f)
                            if isinstance(x, list):
                                if findlist(x, f):
                                    return findlist(x, f)

                    def finder(f):
                        for key, value in input["@graph"].items():
                            if value == f:
                                return input["@graph"]["@id"]
                            if isinstance(value, dict):
                                if finddict(value, f):
                                    return finddict(value, f)
                            if isinstance(value, list):
                                if findlist(value, f):
                                    return findlist(value, f)

                    def linkdict(a):
                        for key, value in a.items():
                            if key in linkinglist:
                                a[key] = finder(value)
                                return finder(value)
                            if isinstance(value, list):
                                linklist(value)
                            if isinstance(value, dict):
                                linkdict(value)

                    def linklist(a):
                        for x in a:
                            if isinstance(x, dict):
                                linkdict(x)
                            if isinstance(x, list):
                                linklist(x)

                    for key, value in input['@graph'].items():
                        if isinstance(value, dict):
                            linkdict(value)
                        if isinstance(value, list):
                            linklist(value)
                    return input


                newput = link(put)

                try:
                    # jsonld.to_rdf(json.dumps(newput), {"processingMode": "json-ld-1.0"})

                    if populateall:
                        # with open('populated_'+targetchemblid+'_'+documentchemblid+'_'+assaychemblid+ '.jsonld', 'w') as f:
                        with open('populated_' + targetchemblid + documentchemblid + '.jsonld', 'w') as f:

                            json.dump(newput, f)
                    else:
                        # with open(targetchemblid+'_'+documentchemblid+moleculechemblid+'_'+assaychemblid+ '.jsonld', 'w') as f:
                        with open(targetchemblid + documentchemblid + moleculechemblid + '.jsonld', 'w') as f:
                            json.dump(newput, f)
                except:
                    print('Invalid JSON-LD')



