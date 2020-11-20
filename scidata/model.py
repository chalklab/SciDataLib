""" This module contains the Scidata class used in generating Scidata JSON-LD documents """
from collections import defaultdict
from itertools import count
import json



def denester(q, r):
    """ denester function """
    denestered = {}

    def denest(x, y):
        """ denest function """
        denested = {}
        if type(y) is dict:
            for a, b in y.items():
                if type(b) is dict:
                    denest(a, b)
                elif type(b) is list:
                    for c in b:
                        denest(a, c)

                else:
                    if b not in ['null', None]:
                        denested.update({str(a): str(b)})

            if denested:
                denestered.update({str(x): denested})
    denest(q, r)
    return denestered

def is_number(n):
    """Function used for determining datatype"""

    try:
        float(n)
    except ValueError:
        return False
    return True


def find_sigfigs(x):
    """Function used for determining significant figures"""
    x = x.lower()
    if 'e' in x:
        mystr = x.split('e')
        return len((mystr[0])) - 1
    else:
        n = ('%.*e' % (8, abs(float(x)))).split('e')
        if '.' in x:
            s = x.replace('.', '')
            length = len(s) - len(s.rstrip('0'))
            n[0] = n[0].rstrip('0') + ''.join(['0' for num in range(length)])
        else:
            n[0] = n[0].rstrip('0')
    return find_sigfigs('e'.join(n))


class SciData:
    """This class generates the Scidata JSON-LD document"""

    def __init__(self, uid: str):
        """Initialize the instance using a unique id"""

        self.meta['@graph']['uid'] = uid

    meta = {
        "@context": [],
        "@id": "",
        "generatedAt": "",
        "version": "",
        "@graph": {
            "@id": "",
            "@type": "",
            "sourcecode": "",
            "datasetname": "",
            "uid": "",
            "title": "",
            "author": [],
            "description": "",
            "publisher": "",
            "version": "",
            "keywords": [],
            "dateTime": "",
            "permalink": "",
            "related": [],
            "toc": [],
            "ids": [],
            "scidata": {
                "@id": "scidata",
                "@type": "sci:scientificData",
                "discipline": "",
                "subdiscipline": "",
                "methodology": {
                    "aspects": []},
                "system": {
                    "facets": []},
                "dataset": {
                    "datagroup": [],
                    "datapoint": []
                },
            },
            "sources": [],
            "rights": []
        }
    }

    contexts = []
    nspaces = {}
    bass = {}

    def context(self, context: list) -> dict:
        """Make or replace the external context files"""
        self.contexts = []
        self.contexts = context
        self.make_context()
        return self.meta

    def add_context(self, context: str) -> dict:
        """Add to the external context files"""

        self.contexts.append(context)
        self.make_context()
        return self.meta

    def namespace(self, namespace: dict) -> dict:
        """Make or replace the namespace"""

        self.nspaces = namespace
        self.make_context()
        return self.meta

    def add_namespace(self, namespace: dict) -> dict:
        """Add to the namespace"""

        self.nspaces.update(namespace)
        self.make_context()
        return self.meta

    def base(self, base: dict) -> dict:
        """Make or replace the base"""

        if base == "":
            self.bass = {"@base": "http://BASE.jsonld"}
            self.make_context()
        else:
            self.bass = base
        return self.meta

    def make_context(self) -> dict:
        """Recreate the context when something is added to contexts, nspaces or base"""

        c = self.contexts
        n = self.nspaces
        b = self.bass
        con = c + [n, b]
        self.meta["@context"] = con
        return self.meta

    def doc_id(self, i: str) -> dict:
        """Make or replace the document id"""

        self.meta['@id'] = i
        return self.meta

    def graph_id(self, i: str) -> dict:
        """Make or replace the graph id"""

        self.meta['@graph']['@id'] = i
        return self.meta

    def graph_type(self, i: str) -> dict:
        """Make or replace the graph type"""

        self.meta['@graph']['@type'] = i
        return self.meta

    def graph_uid(self, i: str) -> dict:
        """Make or replace the unique id for the graph"""

        self.meta['@graph']['uid'] = i
        return self.meta

    def sourcecode(self, i: str) -> dict:
        """Make or replace the sourcecode for the graph"""

        self.meta['@graph']['sourcecode'] = i
        return self.meta

    def datasetname(self, i: str) -> dict:
        """Make or replace the sourcecode for the graph"""

        self.meta['@graph']['datasetname'] = i
        return self.meta

    def generatedAt(self, i: str) -> dict:
        """Make or replace the sourcecode for the graph"""

        self.meta['generatedAt'] = i
        return self.meta

    def version(self, i: str) -> dict:
        """Make or replace the sourcecode for the graph"""

        self.meta['version'] = i
        return self.meta

    def author(self, author: list) -> dict:
        """Make or replace the author"""

        a = []
        if isinstance(author, list):
            for c, au in enumerate(author):
                auth = {'@id': ('author/' + str(c + 1) + '/')}
                t = {'@type': 'dc:author'}
                auth.update(t)
                auth.update(au)
                a.append(auth)
            self.meta['@graph']['author'] = a
        return self.meta

    def title(self, title: str) -> dict:
        """Make or replace document title"""

        self.meta['@graph']['title'] = title
        return self.meta

    def description(self, description: str) -> dict:
        """Make or replace document description"""

        self.meta['@graph']['description'] = description
        return self.meta

    def publisher(self, publisher: str) -> dict:
        """Make or replace document publisher"""

        self.meta['@graph']['publisher'] = publisher
        return self.meta

    def graphversion(self, version: str) -> dict:
        """Make or replace the document version"""

        self.meta['@graph']['version'] = version
        return self.meta

    def keywords(self, keywords: str or list) -> dict:
        """Make or replace the keywords of the instance"""

        keys = self.meta['@graph']['keywords']
        if isinstance(keywords, str):
            keys = []
            keys.append(keywords)
        elif isinstance(keywords, list):
            keys = keywords
        keys.sort()
        self.meta['@graph']['keywords'] = keys
        return self.meta

    def add_keyword(self, keyword: str) -> dict:
        """Add keyword(s)"""

        keys = self.meta['@graph']['keywords']
        if isinstance(keyword, str) and keyword not in keys:
            keys.append(keyword)
        elif isinstance(keyword, list):
            for k in keyword:
                if k not in keys:
                    keys.append(k)
        return self.meta

    def dateTime(self) -> dict:
        """initiate the date time"""

        self.meta['@graph']['dateTime'] = "datetime from GraphDB"
        return self.meta

    def permalink(self, link: str) -> dict:
        """Make or replace the document permanent link"""

        self.meta['@graph']['permalink'] = link
        return self.meta

    def related(self, related: str) -> dict:
        """Make or replace the related URIs (adds to array)"""

        self.meta['@graph']['related'] = related
        return self.meta

    def add_related(self, related: str) -> dict:
        """Make or replace the related URIs (adds to array)"""

        self.meta['@graph']['related'].append(related)
        return self.meta

    def ids(self, ids: str) -> dict:
        """Make or replace the ids (adds to array)"""

        self.meta['@graph']['ids'] = sorted(set(ids))
        return self.meta

    def add_ids(self, ids: str) -> dict:
        """Make or replace the ids (adds to array)"""

        self.meta['@graph']['ids'].append(ids)
        self.meta['@graph']['ids'] = sorted(set(ids))
        return self.meta

    def discipline(self, disc: str) -> dict:
        """Make or replace discipline"""

        self.meta['@graph']['scidata']['discipline'] = disc
        return self.meta

    def subdiscipline(self, subdisc: str) -> dict:
        """Make or replace subdiscipline"""

        self.meta['@graph']['scidata']['subdiscipline'] = subdisc
        return self.meta

    def aspects(self, aspects: list) -> dict:
        """Make or replace the aspects of the instance"""

        s = self.meta['@graph']['scidata']['methodology']
        if "@id" not in s:
            self.meta['@graph']['scidata']['methodology']['@id'] = "methodology/"
        if "@type" not in s:
            self.meta['@graph']['scidata']['methodology']['@type'] = "sci:methodology"
        if "datapoint" not in s:
            self.meta['@graph']['scidata']['methodology']['aspects'] = []
        count_index = defaultdict(lambda: count(1))
        prefix = ['']
        data = []

        def iterateaspects(it):
            """ iterateaspects function """
            if '@id' in it:
                category = prefix[-1] + it['@id']
                categoryx = it['@id']
            else:
                category = 'undefined'
                categoryx = 'undefined'
            index = next(count_index[category])
            it['@id'] = '{category}/{index}/'.format(category=category, index=index)
            it['@type'] = 'sci:{category}'.format(category=categoryx)
            for x in it.values():
                if isinstance(x, list):
                    for y in x:
                        prefix.append(it['@id'])
                        iterateaspects(y)
                if isinstance(x, dict):
                    prefix.append(it['@id'])
                    iterateaspects(x)
        for item in aspects:
            iterateaspects(item)
            prefix = ['']
            self.meta['@graph']['scidata']['methodology']['aspects'].append(item)

        return self.meta

    def facets(self, facets: list) -> dict:
        """Make or replace the facets of the instance"""

        s = self.meta['@graph']['scidata']['system']
        if "@id" not in s:
            self.meta['@graph']['scidata']['system']['@id'] = "system/"
        if "@type" not in s:
            self.meta['@graph']['scidata']['system']['@type'] = "sci:system"
        if "datapoint" not in s:
            self.meta['@graph']['scidata']['system']['facets'] = []
        count_index = defaultdict(lambda: count(1))
        prefix = ['']
        data = []

        def iteratefacets(it):
            """ iteratefacets function """
            if '@id' in it:
                category = prefix[-1] + it['@id']
                categoryx = it['@id']
            else:
                category = 'undefined'
                categoryx = 'undefined'
            index = next(count_index[category])
            it['@id'] = '{category}/{index}/'.format(category=category, index=index)
            it['@type'] = 'sci:{category}'.format(category=categoryx)
            for x in it.values():
                if isinstance(x, list):
                    for y in x:
                        prefix.append(it['@id'])
                        iteratefacets(y)
                if isinstance(x, dict):
                    prefix.append(it['@id'])
                    iteratefacets(x)
        for item in facets:
            iteratefacets(item)
            prefix = ['']
            self.meta['@graph']['scidata']['system']['facets'].append(item)
        return self.meta

    def datapoint(self, datapoint: list) -> dict:
        """ create or replace the datapoint """

        s = self.meta['@graph']['scidata']['dataset']
        if "@id" not in s:
            self.meta['@graph']['scidata']['dataset']['@id'] = "dataset/1/"
        if "@type" not in s:
            self.meta['@graph']['scidata']['dataset']['@type'] = "sci:dataset"
        if "datapoint" not in s:
            self.meta['@graph']['scidata']['dataset']['datapoint'] = []
        count_index = defaultdict(lambda: count(1))
        prefix = ['']
        data = []

        def iteratedatapoint(it):
            """ iteratedatapoint function """
            category = prefix[-1] + it['@id']
            index = next(count_index[category])
            it['@id'] = '{category}/{index}/'.format(category=category, index=index)
            for x in it.values():
                if isinstance(x, list):
                    for y in x:
                        prefix.append(it['@id'])
                        iteratedatapoint(y)
                if isinstance(x, dict):
                    prefix.append(it['@id'])
                    iteratedatapoint(x)
        for item in datapoint:
            iteratedatapoint(item)
            prefix = ['']
            data.append(item)
            self.meta['@graph']['scidata']['dataset']['datapoint'] = data
        return self.meta

    def datagroup(self, datagroup: list) -> dict:
        """ create or replace the datagroup """
        count_index = defaultdict(lambda: count(1))
        data = []

        def iteratedatagroup(it):
            """ iteratedatagroup function """
            category = it['@id']
            index = next(count_index[category])
            it['@id'] = '{category}/{index}/'.format(category=category, index=index)
            pointlist = []
            for x in it['datapoints']:
                category = x
                index = next(count_index[category])
                pointlist.append('{category}/{index}/'.format(category=category, index=index))
            it['datapoints'] = pointlist
        for item in datagroup:
            iteratedatagroup(item)
            data.append(item)
            self.meta['@graph']['scidata']['dataset']['datagroup'] = data
        return self.meta

    # rewritten by SJC 081219
    '''def add_source(self, source):
        srcs = self.meta['@graph']['sources']
        ld = {
            '@id': 'source/' + str(len(srcs) + 1) + '/',
            '@type': 'dc:source'
        }
        src = dict(ld, *source)
        srcs.append(src)
        self.meta['@graph']['sources'] = srcs
        return self.meta'''

    def source(self, source: list) -> dict:
        """Make or replace the source"""

        srcs = []
        for x in source:
            ld = {
                '@id': 'source/' + str(len(srcs) + 1) + '/',
                '@type': 'dc:source'
            }
            ld.update(x)
            srcs.append(ld)
        self.meta['@graph']['sources'] = srcs
        return self.meta

    def add_source(self, source: list) -> dict:
        """ add to the sources list"""

        srcs = self.meta['@graph']['sources']
        for x in source:
            ld = {
                '@id': 'source/' + str(len(srcs) + 1) + '/',
                '@type': 'dc:source'
            }
            ld.update(x)
            srcs.append(ld)
        self.meta['@graph']['sources'] = srcs
        return self.meta

    def rights(self, r: str, s: str) -> dict:
        """ create or replace the rights """

        right = []
        right.append({
            '@id': 'rights/' + str(len(right) + 1) + '/',
            '@type': 'dc:rights',
            'license': r,
            'holder': s,
        })
        self.meta['@graph']['rights'] = right
        return self.meta

    def add_rights(self, r: str, s: str) -> dict:
        """ add to the rights list """

        rights = self.meta['@graph']['rights']
        rights.append({
            '@id': 'rights/' + str(len(self.meta['@graph']['rights']) + 1) + '/',
            '@type': 'dc:rights',
            'license': r,
            'holder': s,
        })
        return self.meta

    def toc(self):
        """ toc function """
        def tocdict(a):
            """ tocdict function """
            for key, value in a.items():
                if key == '@type':
                    self.meta['@graph']['toc'].append(value)
                if isinstance(value, list):
                    toclist(value)
                if isinstance(value, dict):
                    tocdict(value)

        def toclist(a):
            """ toclist function """
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
        return self.meta

    @property
    def output(self) -> dict:
        """Generates Scidata JSON-LD File"""

        empty = []
        for key, value in self.meta['@graph'].items():
            if isinstance(value, str) and value == "":
                empty.append(key)
            elif isinstance(value, list) and value == []:
                empty.append(key)
        for key, value in self.meta['@graph']['scidata'].items():
            if isinstance(value, dict):
                for v in value.values():
                    if not v:
                        empty.append(key)
        for e in empty:
            if e in self.meta['@graph']['scidata'].keys():
                self.meta['@graph']['scidata'].pop(e)
            elif e in self.meta['@graph'].keys():
                self.meta['@graph'].pop(e)
        temp = json.dumps(self.meta, indent=4, ensure_ascii=False)
        # print(temp)

        print('complete')
        return self.meta
