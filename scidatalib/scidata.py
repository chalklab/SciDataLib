"""Python library for writing SciData JSON-LD files"""
from datetime import datetime


class SciData:
    """
    This class is used to create and populate a SciData object, to be
    output as a SciData JSON-LD document

    A SciData object is created by calling the SciData class
    i.e. SciDataObject = SciData(<uid>)

    The meta variable defines the keys that make up the backbone structure of
    the JSON-LD document. Class methods are called to populate the meta keys
    """

    def __init__(self, uid: str):
        """Initialize the instance using a unique id"""

        self.meta = {
            "@context": [],
            "@id": "",
            "generatedAt": "",
            "version": "",
            "@graph": {
                "@id": "",
                "@type": "sdo:scidataFramework",
                "uid": "",
                "title": "",
                "authors": [],
                "description": "",
                "publisher": "",
                "version": "",
                "keywords": [],
                "starttime": "",
                "permalink": "",
                "related": [],
                "toc": [],
                "ids": [],
                "scidata": {
                    "@id": "scidata/",
                    "@type": "sdo:scientificData",
                    "discipline": "",
                    "subdiscipline": "",
                    "methodology": {
                        "@id": "methodology/",
                        "@type": "sdo:methodology",
                        "evaluation": "",
                        "aspects": []},
                    "system": {
                        "@id": "system/",
                        "@type": "sdo:system",
                        "facets": []},
                    "dataset": {
                        "@id": "dataset/",
                        "@type": "sdo:dataset",
                        "scope": ""},
                },
                "sources": [],
                "rights": []
            }
        }
        self.contexts = [
            'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
        self.nspaces = {
            "sdo": "https://stuchalk.github.io/scidata/ontology/scidata.owl#",
            "w3i": "https://w3id.org/skgo/modsci#",
            "qudt": "http://qudt.org/vocab/unit/",
            "obo": "http://purl.obolibrary.org/obo/",
            "dc": "http://purl.org/dc/terms/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "sci": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"
        }
        self.baseurl = {}
        self.meta['@graph']['uid'] = uid
        self.uidindex = []

    # public class methods
    def context(self, context: [str, list], replace=False) -> list:
        """
        Add to or replace the list of external context files
        :param context - context URL string or list of context URL strings
        :param replace - boolean to replace or not the existing data

        When called, the content URL content of the @context JSON object will
        be replaced or updated with the supplied list of context urls
        Example:
        SciDataObject.context(
            ['https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
        )
        """
        if replace:
            self.contexts = []
            if isinstance(context, str):
                self.contexts = [context]
            if isinstance(context, list):
                self.contexts = context
        if not replace:
            if isinstance(context, str):
                self.contexts.append(context)
            if isinstance(context, list):
                self.contexts += context
        self.contexts = list(set(self.contexts))
        self.__make_context()
        return self.contexts

    def namespaces(self, namespaces: dict, replace=False) -> dict:
        """
        Add to or replace the dictionary of namespaces within @context.
        Namespaces are needed for values in a file that reference external
        resources the define something (vocabulary/taxonomy/ontology entries).
        :param namespaces - dictionary of namespaces (key->ns, val->URI start)
        :param replace - boolean to replace or not the existing data

        When called, the dictionary of namespaces within the @context key
        of the meta variable will be replaced or updated with the supplied
        dictionary of namespaces
        Example:
        SciDataObject.namespaces(
            {"sci": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"}
        )
        """
        if isinstance(namespaces, dict):
            if replace:
                self.nspaces = {}
                self.nspaces = namespaces
            if not replace:
                self.nspaces.update(namespaces)
        self.__make_context()
        return self.nspaces

    def base(self, base: str) -> dict:
        """
        Assign the JSON-LD @base URL
        (also defines '@id' under '@graph' for consistency)
        See: https://www.w3.org/TR/json-ld/#base-iri
        :param base - @base URL for a JSON-LD file

        Defines the base url for all internal unique identifiers
        (define though '@id's). For consistency, the codes also
        sets the '@id' field under '@graph' so that all triple
        subjects are unique and associated with the same graph
        Example:
        SciDataObject.graph_uid("<uniqueidentifier>")
        """
        if isinstance(base, str):
            if base == "":
                base = "https://scidata.unf.edu/update_your_base_URL"
            self.baseurl = {"@base": base}
        self.__make_context()
        self.__graphid(base)
        return self.baseurl

    def docid(self, docid: str) -> dict:
        """
        Assign the document identifier.  This will become the
        graph name if the file is uploaded to a graph database
        :param docid - the root level @id value
        """
        if isinstance(docid, str):
            self.meta['@id'] = docid
        return self.meta['@id']

    def version(self, version: str) -> dict:
        """
        Assign the version of this file (not the version of the data)
        :param version - the top level 'version' value
        """
        if isinstance(version, str):
            self.meta['version'] = version
        return self.meta['version']

    def graph_uid(self, guid: str) -> dict:
        """
        Assign the uid value within the @graph JSON object
        :param guid - the @graph uid value

        Normally the same as the unique id used in the @graph @id
        value and used to easily find the data in a file system.
        Example:
        SciDataObject.graph_uid("<uniqueidentifier>")
        """
        if isinstance(guid, str):
            self.meta['@graph']['uid'] = guid
        return self.meta['@graph']['uid']

    def author(self, authors: list, replace=False) -> list:
        """
        Add to or replace the list of authors within the @graph authors section
        :param authors - list of names, or list of dicts with multiple fields
        :param replace - boolean to replace or not the existing data
        Add the list of authors of a set of data with the following defined
        fields in the SciData context file: name, address, organization,
        email, orcid. Expects either:
        1)  a list of dictionaries where each dictionary contains
            at minimum of a key that is 'name'
            Example:
            [{'name': 'George Washington', 'ORCID': 1},
             {'name': 'John Adams', 'ORCID': 2}]
        2)  a list of strings which are author names
            Example: ['George Washington', 'John Adams']
        """
        if isinstance(authors, list):
            a = []
            if not replace:
                a += self.meta['@graph']['authors']
            for au in authors:
                auth = {'@id': ('author/' + str(len(a) + 1) + '/')}
                auth.update({'@type': 'dc:creator'})
                if isinstance(au, dict):
                    if 'name' in au:
                        auth.update(au)
                elif isinstance(au, str):
                    auth.update({'name': au})
                a.append(auth)
            self.meta['@graph']['authors'] = a
        return self.meta['@graph']['authors']

    def title(self, title: str) -> str:
        """
        Used to create or replace title key within @graph
        :param title - descriptive title of the dataset

        For a data source such as a journal article, this would
        typically be the title of the article
        Example:
        SciDataObject.title("The Hitchhiker's Guide to the Galaxy")
        """
        if isinstance(title, str):
            self.meta['@graph']['title'] = title
        return self.meta['@graph']['title']

    def description(self, description: str) -> str:
        """
        Assign the description field within @graph
        :param description - textual description of the dataset

        Used as a brief description of the type of data. For a
        journal article, this might house the abstract
        Example:
        SciDataObject.description('a brief description')
        """
        if isinstance(description, str):
            self.meta['@graph']['description'] = description
        return self.meta['@graph']['description']

    def publisher(self, publisher: str) -> str:
        """
        Assign the publisher field within @graph
        :param publisher - the name or title of the publisher of the data

        This is a person, project, research group, organization etc.
        Example:
        SciDataObject.publisher('The Daily Prophet')
        """
        if isinstance(publisher, str):
            self.meta['@graph']['publisher'] = publisher
        return self.meta['@graph']['publisher']

    def graphversion(self, version: str) -> str:
        """
        Assign the data version
        :param version - the version assigned to the data

        If a version is not available, the date it was accessed online
        can be used to indicate the 'state' of the data as downloaded
        Example:
        SciDataObject.graphversion('ChEMBL database v28')
        """
        if isinstance(version, str):
            self.meta['@graph']['version'] = version
        return self.meta['@graph']['version']

    def keywords(self, keywords: [str, list], replace=False) -> list:
        """
        Add to or replace the keywords of the instance
        :param keywords - important keywords to improve data findability
        :param replace - boolean to replace or not the existing data

        Example:
        SciDataObject.keywords('important')
        """
        keys = []
        if not replace:
            keys = self.meta['@graph']['keywords']
        if isinstance(keywords, str):
            keys.append(keywords)
        elif isinstance(keywords, list):
            keys += keywords
        keys.sort()
        self.meta['@graph']['keywords'] = keys
        return self.meta['@graph']['keywords']

    def starttime(self, stime: str) -> str:
        """
        Assign the start time
        :param stime - datetime string

        Typically in "%m-%d-%y %H:%M:%S" format
        Example:
        SciDataObject.starttime('04-05-21 06:14:53')
        """
        if isinstance(stime, str):
            self.meta['@graph']['starttime'] = stime
        return self.meta['@graph']['starttime']

    def permalink(self, link: str) -> dict:
        """
        Assign the document permanent link
        :param link - URL to the location where this document can be found

        Example:
        SciDataObject.permalink('https://permanent.link.com/data1')
        """
        if isinstance(link, str):
            self.meta['@graph']['permalink'] = link
        return self.meta['@graph']['permalink']

    def related(self, related: [str, list], replace=False) -> list:
        """
        Add to or replace the related URLs
        :param related - URLs to other data related to this dataset
        :param replace - boolean to replace or not the existing data

        Example:
        SciDataObject.related('http://example.com/greatdata.jsonld')
        """
        rels = []
        if not replace:
            rels = self.meta['@graph']['related']
        if isinstance(related, str):
            rels.append(related)
        elif isinstance(related, list):
            rels += related
        self.meta['@graph']['related'] = rels
        return self.meta['@graph']['related']

    def ids(self, ids: [str, list]) -> list:
        """
        Add to the ids list
        :param ids - string or list of strings that are external
        references to ontological concepts

        When called the contents of 'ids' is added to the ids list.
        Note that when the output function is called it iterates
        over instance content to find any values that are ontological
        references, in the format "<namespace>:<uniquevalue>", and
        adds them to ids. Only ids provided in this format will be added
        and duplicates are ignored. Remember to add namespaces for ids.
        Example
        SciDataObject.ids(['chebi:00001','qudt:GM'])
        (requires the addition of the 'chebi' namespace)
        """
        curr_ids = self.meta['@graph']['ids']
        if isinstance(ids, list):
            for idee in ids:
                if ':' in idee:
                    if idee.split(':')[0] not in self.nspaces.keys():
                        print('Namespace ' + idee.split(':')[0] + ' not set')
                        # raise EnvironmentError
                    curr_ids.append(idee)
        elif isinstance(ids, str):
            if ':' in ids:
                if ids.split(':')[0] not in self.nspaces.keys():
                    print('Namespace ' + ids.split(':')[0] +
                          ' not set ' + str(self.nspaces.keys()))
                    # raise EnvironmentError
                curr_ids.append(ids)
        self.meta['@graph']['ids'] = sorted(set(curr_ids))
        return self.meta['@graph']['ids']

    def discipline(self, disc: str) -> str:
        """
        Assign the discipline area of the data
        :param disc: a discipline name or identifier (preferred)

        Best practice is to use and entry in an ontology,
        i.e. the Modern Science Ontology (https://w3id.org/skgo/modsci#)
        Example:
        SciDataObject.discipline('w3i:Chemistry')
        """
        if isinstance(disc, str):
            self.__addid(disc)
            self.meta['@graph']['scidata']['discipline'] = disc
        return self.meta['@graph']['scidata']['discipline']

    def subdiscipline(self, subdisc: str) -> str:
        """
        Assign the subdiscipline area of the data
        :param subdisc: a subdiscipline name or identifier (preferred)

        Best practice is to use and entry in an ontology,
        i.e. the Modern Science Ontology (https://w3id.org/skgo/modsci#)
        Example:
        SciDataObject.subdiscipline('w3i:AnalyticalChemistry')
        """
        if isinstance(subdisc, str):
            self.__addid(subdisc)
            self.meta['@graph']['scidata']['subdiscipline'] = subdisc
        return self.meta['@graph']['scidata']['subdiscipline']

    def evaluation(self, evaln: str) -> str:
        """
        Assign the evaluation field
        :param evaln: the method of evaluation of research data

        Recommended values of this field are:
        experimental, theoretical, computational
        Example:
        SciDataObject.evaluation('experimental')
        """
        if isinstance(evaln, str):
            self.__addid(evaln)
            self.meta['@graph']['scidata']['methodology']['evaluation'] = evaln
        return self.meta['@graph']['scidata']['methodology']['evaluation']

    def aspects(self, aspects: list) -> list:
        """Add to or replace the aspects of the file"""
        new_aspects = []
        scidata: dict = self.meta['@graph']['scidata']
        meth: dict = scidata['methodology']
        curr_aspects: list = meth['aspects']
        for listentry in aspects:
            item = self.__iterate_function(listentry)
            item_noid = {k: item[k] for k in set(list(item.keys())) - {'@id'}}
            matched_aspect = 0
            for aspectitem in curr_aspects:
                aspect_item_noid = {
                    k: aspectitem[k] for k in set(
                        list(
                            aspectitem.keys())) -
                    {'@id'}}
                if aspect_item_noid == item_noid:
                    matched_aspect = aspectitem
                    # matched_aspect_id = aspectitem['@id']
            if matched_aspect:
                new_aspects.append(matched_aspect)
                self.uidindex.remove(item['@id'])
            else:
                new_aspects.append(item)
                curr_aspects.append(item)

        meth['aspects'] = curr_aspects
        scidata['methodology'] = meth
        self.meta['@graph']['scidata'] = scidata
        return new_aspects

    def facets(self, facets: list) -> list:
        """Add to or replace the facets of the file"""
        new_facets = []
        scidata: dict = self.meta['@graph']['scidata']
        system: dict = scidata['system']
        curr_facets: list = system['facets']
        for listentry in facets:
            item = self.__iterate_function(listentry)
            item_noid = {k: item[k] for k in set(list(item.keys())) - {'@id'}}
            matched_facet = 0
            for facetitem in curr_facets:
                facet_item_noid = {
                    k: facetitem[k] for k in set(
                        list(
                            facetitem.keys())) -
                    {'@id'}}
                if facet_item_noid == item_noid:
                    matched_facet = facetitem
            if matched_facet:
                new_facets.append(matched_facet)
                self.uidindex.remove(item['@id'])
            else:
                new_facets.append(item)
                curr_facets.append(item)
        system['facets'] = curr_facets
        scidata['system'] = system
        self.meta['@graph']['scidata'] = scidata
        return new_facets

    def scope(self, scope: [str, list]) -> str:
        """
        Assign what thing(s) the dataset relates to
        :param scope: str or list of internal unique id()s of
        entity(ies) in the system to which the data describes

        The scope of a datasets should be described in the 'system' 'facets'
        section, e.g. chemical system, organism, specimen, should be included
        as a scope using the defined unique '@id' for that section
        Example
        SciDataObject.scope('chemicalsystem/1/')
        """
        if isinstance(scope, str) or isinstance(scope, list):
            self.meta['@graph']['scidata']['dataset']['scope'] = scope
        return self.meta['@graph']['scidata']['dataset']['scope']

    def attribute(self, attributes: list) -> list:
        """Add one or more attributes"""
        new_attributes = []
        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']
        if 'attribute' in dataset.keys():
            curr_attributes: list = dataset['attribute']
        else:
            curr_attributes = []
        for listentry in attributes:
            item = self.__iterate_function(listentry)
            item_noid = {k: item[k] for k in set(list(item.keys())) - {'@id'}}
            matched_attribute = 0
            for attributeitem in curr_attributes:
                attribute_item_noid = {
                    k: attributeitem[k] for k in set(
                        list(
                            attributeitem.keys())) -
                    {'@id'}}
                if attribute_item_noid == item_noid:
                    matched_attribute = attributeitem
            if matched_attribute:
                new_attributes.append(matched_attribute)
                self.uidindex.remove(item['@id'])
            else:
                new_attributes.append(item)
                curr_attributes.append(item)

        dataset['attribute'] = curr_attributes
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return new_attributes

    def datapoint(self, points: list) -> list:
        """Add one or more datapoints"""
        new_points = []
        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']

        if 'datapoint' in dataset.keys():
            curr_points: list = dataset['datapoint']
        else:
            curr_points = []

        for listentry in points:
            item = self.__iterate_function(listentry)
            new_points.append(item)
            curr_points.append(item)

        dataset['datapoint'] = curr_points
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return new_points

    def dataseries(self, series: list) -> list:
        """Add one or more datapoints"""
        new_series = []
        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']
        if 'dataseries' in dataset.keys():
            curr_series: list = dataset['dataseries']
        else:
            curr_series = []
        for listentry in series:
            item = self.__iterate_function(listentry)
            item_noid = {k: item[k] for k in set(list(item.keys())) - {'@id'}}
            matched_serie = 0
            for serieitem in curr_series:
                serie_item_noid = {
                    k: serieitem[k] for k in set(
                        list(
                            serieitem.keys())) -
                    {'@id'}}
                if serie_item_noid == item_noid:
                    matched_serie = serieitem
            if matched_serie:
                new_series.append(matched_serie)
                self.uidindex.remove(item['@id'])
            else:
                new_series.append(item)
                curr_series.append(item)

        dataset['dataseries'] = curr_series
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return new_series

    def datagroup(self, group: list) -> list:
        """Add one or more datapoints"""
        new_group = []
        scidata: dict = self.meta['@graph']['scidata']
        dataset: dict = scidata['dataset']
        if 'datagroup' in dataset.keys():
            curr_group: list = dataset['datagroup']
        else:
            curr_group = []
        for listentry in group:
            item = self.__iterate_function(listentry)
            item_noid = {k: item[k] for k in set(list(item.keys())) - {'@id'}}
            matched_group = 0
            for groupitem in curr_group:
                group_item_noid = {
                    k: groupitem[k] for k in set(
                        list(
                            groupitem.keys())) -
                    {'@id'}}
                if group_item_noid == item_noid:
                    matched_group = groupitem
            if matched_group:
                new_group.append(matched_group)
                self.uidindex.remove(item['@id'])
            else:
                new_group.append(item)
                curr_group.append(item)

        dataset['datagroup'] = curr_group
        scidata['dataset'] = dataset
        self.meta['@graph']['scidata'] = scidata
        return new_group

    def scidatapackage(self, package):
        """Add a package of data where the datapoints are linked
            with the associated aspects and facets
        package = [{'aspects':{},'facets':{},'datapoint':{}},
            {'aspects':{},'facets':{},'datapoint':{}}]"""
        for packet in package:
            packet['facets'] = self.facets(packet['facets'])
            packet['aspects'] = self.aspects(packet['aspects'])
            atfacet = [a_dict["@id"] for a_dict in packet['facets']]
            ataspect = [a_dict["@id"] for a_dict in packet['aspects']]
            for dp in packet['dataset']:
                if atfacet:
                    dp.update({'facets#': atfacet})
                if ataspect:
                    dp.update({'aspects#': ataspect})
            self.datapoint(packet['dataset'])

    def sources(self, sources: list, replace=False) -> dict:
        """
        Add to or replace the source reference list
        :param sources - information about where the data came from
        :param replace - boolean to replace or not the existing data

        Add a list of sources with any of the available defined fields
        in the SciData context file: citation, reftype, url, doi
        Example
        SciDataObject.sources([
            {'citation': 'Chalk, S.J. SciData: a data model and
            ontology for semantic representation of scientific data.
            J Cheminform 8, 54 (2016)',
            'doi': https://doi.org/10.1186/s13321-016-0168-9'}])
        """
        srcs = []
        if not replace:
            srcs = self.meta['@graph']['sources']
        for x in sources:
            ld = {
                '@id': 'source/' + str(len(srcs) + 1) + '/',
                '@type': 'dc:source'
            }
            ld.update(x)
            srcs.append(ld)
        return self.meta['@graph']['sources']

    def rights(self, holder: str, license: str) -> dict:
        """
        Add the rights section to the file (max: 1 entry)
        :param holder - the entity that holds the license to this data
        :param license - the assigned license
        """
        rights = []
        if isinstance(holder, str) and isinstance(license, str):
            rights = [{
                '@id': 'rights/1/',
                '@type': 'dc:rights',
                'holder': holder,
                'license': license,
            }]
        self.meta['@graph']['rights'] = rights
        return self.meta['@graph']['rights']

    # private class functions
    def __addid(self, text: str) -> bool:
        """ adds entry to ids list if string contains ':' """
        if isinstance(text, str):
            if '://' in text:
                return False
            elif len(text.split(':')) > 1:
                return False
            elif ':' in text:
                self.ids(text)
                return True
        else:
            return False

    def __graphid(self, gid: str) -> bool:
        """
        Assigns the @id value within the @graph JSON object.
        Automatically set as the value of the '@base'
        """
        self.meta['@graph']['@id'] = gid
        return True

    def __addtoc(self):
        """ adds entries to the toc list """

        def tocdict(a):
            """ get the @type entry from a dictionary """
            for k, v in a.items():
                if k == '@type':
                    if isinstance(v, list):
                        self.meta['@graph']['toc'].extend(v)
                    else:
                        self.meta['@graph']['toc'].append(v)
                if isinstance(v, list):
                    toclist(v)
                if isinstance(v, dict):
                    tocdict(v)

        def toclist(a):
            """ process lists """
            for x in a:
                if isinstance(x, dict):
                    tocdict(x)
                if isinstance(x, list):
                    toclist(x)

        for key, value in self.meta['@graph'].items():
            if key == '@type':
                self.meta['@graph']['toc'].append(value)
            if isinstance(value, dict):
                tocdict(value)
            if isinstance(value, list):
                toclist(value)

        self.meta['@graph']['toc'] = sorted(set(self.meta['@graph']['toc']))
        return

    def __make_context(self) -> dict:
        """
        Recreates the context when something is added to contexts,
        namespaces or base. The method is called as part of
        the contexts, namespaces and base methods.
        """

        c = self.contexts
        n = self.nspaces
        b = self.baseurl
        self.meta["@context"] = c + [n, b]
        return self.meta["@context"]

    def __iterate_function(self, it, uid=False):

        if isinstance(it, str):
            self.__addid(it)
            return it
        prev_uid = uid

        # Set the category
        if '@id' in it:
            category = it['@id']
        elif 'descriptors' in it or 'identifiers' in it:
            category = 'compound'
        else:
            category = 'undefined'

        if prev_uid:
            uid = prev_uid + category + '/1/'
        else:
            uid = category + '/1/'

        def enumuid(uid):
            uidsplit = uid.rsplit('/', 2)
            uid = uidsplit[0] + '/' + str(int(uidsplit[1]) + 1) + '/'
            return uid

        while uid in self.uidindex:
            uid = enumuid(uid)
        self.uidindex.append(uid)

        temp: dict = {'@id': uid, '@type': 'sdo:' + category}

        for key, value in it.items():
            if key != '@id':

                if isinstance(value, list):
                    listuid = uid
                    for i, listentry in enumerate(value):
                        value[i] = self.__iterate_function(
                            listentry, listuid)
                    temp[key] = value

                elif isinstance(value, dict):
                    temp[key] = self.__iterate_function(
                        value, uid)

                else:
                    temp[key] = value
                    self.__addid(value)

        return temp

    @property
    def output(self) -> dict:
        """
        Generates Scidata JSON-LD File
        """
        today = datetime.today()
        self.meta['generatedAt'] = today.strftime("%m-%d-%y %H:%M:%S")

        # clean top level
        for key in list(self.meta['@graph']):
            if not self.meta['@graph'][key]:
                if key != 'toc':
                    del self.meta['@graph'][key]
        for key in list(self.meta['@graph']['scidata']):
            if not self.meta['@graph']['scidata'][key]:
                del self.meta['@graph']['scidata'][key]
        if self.meta['@graph']['scidata'].get('methodology'):
            if not self.meta['@graph']['scidata'].get(
                    'methodology',
                    {}).get(
                    'aspects',
                    False):
                del self.meta['@graph']['scidata']['methodology']
        if self.meta['@graph']['scidata'].get('system'):
            if not self.meta['@graph']['scidata'].get(
                    'system',
                    {}).get(
                    'facets',
                    False):
                del self.meta['@graph']['scidata']['system']
        if self.meta['@graph']['scidata'].get('dataset'):
            if not self.meta['@graph']['scidata'].get(
                    'dataset', {}).get('datapoint', False):
                if not self.meta['@graph']['scidata'].get(
                        'dataset', {}).get('dataseries', False):
                    del self.meta['@graph']['scidata']['dataset']
        self.__addtoc()

        return self.meta
