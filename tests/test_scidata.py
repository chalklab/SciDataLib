"""pytest test class for scidata.py"""
from scidatalib.scidata import SciData
from datetime import datetime

sd = SciData('example')


def test_context():
    existing_contexts = sd.contexts
    new_contexts = [
        'https://stuchalk.github.io/scidata/contexts/chembl.jsonld',
        'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
    out_contexts = list(set(existing_contexts + new_contexts))
    assert sd.context(new_contexts) == out_contexts


def test_context_replace():
    new_contexts = [
        'https://stuchalk.github.io/scidata/contexts/chembl.jsonld',
        'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
    assert sd.context(new_contexts, True) == list(set(new_contexts))


def test_context_replace_string():
    new_contexts = 'https://stuchalk.github.io/scidata/contexts/chembl.jsonld'
    assert sd.context(new_contexts, True) == [new_contexts]


def test_namespace():
    existing_nspaces = sd.nspaces
    new_nspaces = {'dna': 'https://en.wikipedia.org/wiki/Douglas_Adams#'}
    existing_nspaces.update(new_nspaces)
    assert sd.namespaces(new_nspaces) == existing_nspaces


def test_namespace_replace():
    new_nspaces = {'dna': 'https://en.wikipedia.org/wiki/Douglas_Adams#'}
    assert sd.namespaces(new_nspaces, True) == new_nspaces


def test_base():
    base = 'https://douglasadams.com/'
    assert sd.base(base) == {'@base': base}


def test_doc_id():
    assert sd.docid('example1') == 'example1'


def test_version():
    assert sd.version('1') == '1'
    assert sd.version(2) == '1'


def test_graph_uid():
    assert sd.graph_uid('<uniqueid>') == '<uniqueid>'


def test_author():
    org = 'Whooshing Deadline Productions'
    orcid = '0042-0042-0042-0042'
    name = 'Douglas Adams'
    au = [{'name': name, 'organization': org, 'orcid': orcid}]
    out = [{'@id': 'author/1/', '@type': 'dc:creator',
            'name': name, 'organization': org, 'orcid': orcid}]
    assert sd.author(au) == out


def test_title():
    title = 'The Hitchhiker\'s Guide to the Galaxy'
    assert sd.title(title) == title


def test_description():
    desc = 'Mostly harmless'
    assert sd.description(desc) == desc


def test_publisher():
    pub = 'Megadodo Publications'
    assert sd.publisher(pub) == pub


def test_graphversion():
    version = "Guide Mark II"
    assert sd.graphversion(version) == version


def test_keywords():
    key1 = 'Don\'t panic'
    key2 = 'Infinite improbability drive'
    key3 = 'Bowl of petunias'
    sd.keywords(key1)
    sd.keywords(key2)
    keys = [key1, key2, key3]
    keys.sort()
    assert sd.keywords(key3) == keys


def test_starttime():
    now = datetime.now()
    timestr = now.strftime("%d/%m/%Y %H:%M:%S")
    assert sd.starttime(timestr) == timestr


def test_permalink():
    url = 'https://en.wikipedia.org/wiki/Douglas_Adams'
    assert sd.permalink(url) == url


def test_related():
    url = 'https://hitchhikers.fandom.com/'
    assert sd.related(url) == [url]


def test_ids():
    sd.namespaces({'hhgttg': 'https://hitchhikers.fandom.com/wiki/'})
    id42 = 'hhgttg:42'
    assert sd.ids(id42) == [id42]


def test_discipline():
    sd.namespaces({'w3i': 'https://w3id.org/skgo/modsci#'})
    disc = 'w3i:ScienceFiction'
    assert sd.discipline(disc) == disc


def test_subdiscipline():
    sd.namespaces({'w3i': 'https://w3id.org/skgo/modsci#'})
    subdisc = 'w3i:ScienceHumor'
    assert sd.subdiscipline(subdisc) == subdisc


def test_evaluation():
    evaln = 'probability'
    assert sd.subdiscipline(evaln) == evaln


def test_aspects():
    sd.namespaces({'obo': 'http://purl.obolibrary.org/obo/'})
    meas = {
        '@id': 'measurement',
        'scope': 'resource/1/',
        'technique': 'Potentiometry',
        'techniqueref': 'obo:OMIT_0005812'}
    out = {
        '@id': 'measurement/1/',
        '@type': 'sdo:measurement',
        'scope': 'resource/1/',
        'technique': 'Potentiometry',
        'techniqueref': 'obo:OMIT_0005812'}
    assert sd.aspects([meas]) == [out]


def test_facets():
    sd.namespaces({'obo': 'http://purl.obolibrary.org/obo/'})
    compd = {
        '@id': 'compound',
        'name': 'cyanide ion',
        'inchi': 'InChI=1S/CN/c1-2/q-1',
        'chebi': 'obo:CHEBI_17514'
    }
    out = {
        '@id': 'compound/1/',
        "@type": 'sdo:compound',
        'name': 'cyanide ion',
        'inchi': 'InChI=1S/CN/c1-2/q-1',
        'chebi': 'obo:CHEBI_17514'
    }
    assert sd.facets([compd]) == [out]


def test_scope():
    scope = 'solarsystem/1/'
    assert sd.scope(scope) == scope


def test_datapoint():
    sd.namespaces({'gb': 'https://goldbook.iupac.org/terms/view/'})
    val = {'@id': 'numericvalue', 'number': 10.03}
    pnt = {
        '@id': 'datapoint',
        'quantity': 'gb:P04524',
        'conditions': 'condition/1/',
        'value': val
    }
    out = {
        '@id': 'datapoint/1/',
        '@type': 'sdo:datapoint',
        'quantity': 'gb:P04524',
        'conditions': 'condition/1/',
        'value': {
            '@id': 'datapoint/1/numericvalue/1/',
            '@type': 'sdo:numericvalue',
            'number': 10.03
        }
    }
    assert sd.datapoint([pnt]) == [out]


def test_datagroup():
    sd.namespaces(
        {
            'gb': 'https://goldbook.iupac.org/terms/view/',
            'qudt': 'http://qudt.org/vocab/unit/'
        }
    )
    atid = 'numericvalue'
    val1 = {'@id': atid, 'number': 0.99913, 'unitref': 'qudt:GM-PER-MilliL'}
    val2 = {'@id': atid, 'number': 0.99823, 'unitref': 'qudt:GM-PER-MilliL'}
    val3 = {'@id': atid, 'number': 0.99707, 'unitref': 'qudt:GM-PER-MilliL'}
    pnt1 = {
        '@id': 'datapoint',
        'quantity': 'gb:D01590',
        'conditions': 'condition/1/',
        'value': val1
    }
    pnt2 = {
        '@id': 'datapoint',
        'quantity': 'gb:D01590',
        'conditions': 'condition/2/',
        'value': val2
    }
    pnt3 = {
        '@id': 'datapoint',
        'quantity': 'gb:D01590',
        'conditions': 'condition/3/',
        'value': val3
    }
    grp = {
        '@id': 'datagroup',
        'source': 'chemicalsystem/1/',
        'datapoints': [pnt1, pnt2, pnt3]
    }
    # datapoint indexes start at 2 because of the
    # datapoint added in the datapoint test above
    out = {
        "@id": "datagroup/1/",
        "@type": "sdo:datagroup",
        "source": "chemicalsystem/1/",
        "datapoints": [
            "datapoint/2/",
            "datapoint/3/",
            "datapoint/4/"
            ]
        }
    assert sd.datagroup([grp]) == [out]


def test_source():
    cite = 'The Meaning of Liff, Douglas Adams and John Lloyd, ' \
           'ISBN 0-330-28121-6, 1983'
    url = 'https://en.wikipedia.org/wiki/The_Meaning_of_Liff'
    src = [{'citation': cite, 'url': url}]
    out = [{"@id": "source/1/", "@type": "dc:source",
            "citation": cite, "url": url}]
    assert sd.sources(src) == out


def test_rights():
    holder = 'Megadodo Productions'
    licurl = 'https://creativecommons.org/licenses/by/4.0/'
    lic = 'Creative Commons, Attribution 4.0 Galactic (CC BY 4.0) ' + licurl
    out = [{"@id": "rights/1/", "@type": "dc:rights",
            "holder": holder, "license": lic}]
    assert sd.rights(holder, lic) == out
