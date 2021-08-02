"""pytest test class for scidata.py"""
import copy
from scidatalib.scidata import SciData
from datetime import datetime
import pytest


@pytest.fixture
def sd():
    return SciData('example')


def test_context(sd):
    existing_contexts = sd.contexts
    new_contexts = [
        'https://stuchalk.github.io/scidata/contexts/chembl.jsonld',
        'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
    out_contexts = list(set(existing_contexts + new_contexts))
    assert sd.context(new_contexts) == out_contexts


def test_context_replace(sd):
    new_contexts = [
        'https://stuchalk.github.io/scidata/contexts/chembl.jsonld',
        'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
    assert sd.context(new_contexts, True) == list(set(new_contexts))


def test_context_replace_string(sd):
    new_contexts = 'https://stuchalk.github.io/scidata/contexts/chembl.jsonld'
    assert sd.context(new_contexts, True) == [new_contexts]


def test_namespace(sd):
    existing_nspaces = sd.nspaces
    new_nspaces = {'dna': 'https://en.wikipedia.org/wiki/Douglas_Adams#'}
    existing_nspaces.update(new_nspaces)
    assert sd.namespaces(new_nspaces) == existing_nspaces


def test_namespace_replace(sd):
    new_nspaces = {'dna': 'https://en.wikipedia.org/wiki/Douglas_Adams#'}
    assert sd.namespaces(new_nspaces, True) == new_nspaces


def test_base(sd):
    base = 'https://douglasadams.com/'
    assert sd.base(base) == {'@base': base}


def test_doc_id(sd):
    assert sd.docid('example1') == 'example1'


def test_version(sd):
    assert sd.version('1') == '1'
    assert sd.version(2) == '1'


def test_graph_uid(sd):
    assert sd.graph_uid('<uniqueid>') == '<uniqueid>'


def test_author(sd):
    org = 'Whooshing Deadline Productions'
    orcid = '0042-0042-0042-0042'
    name = 'Douglas Adams'
    au = [{'name': name, 'organization': org, 'orcid': orcid}]
    out = [{'@id': 'author/1/', '@type': 'dc:creator',
            'name': name, 'organization': org, 'orcid': orcid}]
    assert sd.author(au) == out


def test_title(sd):
    title = 'The Hitchhiker\'s Guide to the Galaxy'
    assert sd.title(title) == title


def test_description(sd):
    desc = 'Mostly harmless'
    assert sd.description(desc) == desc


def test_publisher(sd):
    pub = 'Megadodo Publications'
    assert sd.publisher(pub) == pub


def test_graphversion(sd):
    version = "Guide Mark II"
    assert sd.graphversion(version) == version


def test_keywords(sd):
    key1 = 'Don\'t panic'
    key2 = 'Infinite improbability drive'
    key3 = 'Bowl of petunias'
    sd.keywords(key1)
    sd.keywords(key2)
    keys = sorted([key1, key2, key3])
    assert sd.keywords(key3) == keys


def test_starttime(sd):
    now = datetime.now()
    timestr = now.strftime("%d/%m/%Y %H:%M:%S")
    assert sd.starttime(timestr) == timestr
    assert sd.meta.get("@graph").get("starttime") == timestr


def test_permalink(sd):
    url = 'https://en.wikipedia.org/wiki/Douglas_Adams'
    assert sd.permalink(url) == url


def test_related(sd):
    url = 'https://hitchhikers.fandom.com/'
    assert sd.related(url) == [url]


def test_ids(sd):
    sd.namespaces({'hhgttg': 'https://hitchhikers.fandom.com/wiki/'})
    id42 = 'hhgttg:42'
    assert sd.ids(id42) == [id42]


def test_discipline(sd):
    sd.namespaces({'w3i': 'https://w3id.org/skgo/modsci#'})
    disc = 'w3i:ScienceFiction'
    assert sd.discipline(disc) == disc


def test_subdiscipline(sd):
    sd.namespaces({'w3i': 'https://w3id.org/skgo/modsci#'})
    subdisc = 'w3i:ScienceHumor'
    assert sd.subdiscipline(subdisc) == subdisc


def test_evaluation(sd):
    evaln = 'probability'
    assert sd.subdiscipline(evaln) == evaln


def test_aspects(sd):
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


def test_facets(sd):
    sd.namespaces({'obo': 'http://purl.obolibrary.org/obo/',
        "sdo": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"})
    compd = {
        "@id": "substance",
        "title": "3 ppm cyanide standard solution",
        "aggregation": "sub:aq",
        "mixtype": "sub:homogeneousSolution",
        "phase": "sub:liquid",
        "constituents": [
            {
                "@id": "constituent",
                "source": "compound/1/",
                "role": "chm:analyte",
                "properties": [
                    {
                        "@id": "property",
                        "quantity": "mass of substance per volume",
                        "property": "Concentration (w/v)",
                        "value": {
                            "@id": "value",
                            "number": 2.99,
                            "unitref": "qudt:PPM"
                        }
                    },
                    {
                        "@id": "property",
                        "quantity": "volume",
                        "property": "Volume of solution",
                        "value": {
                            "@id": "value",
                            "number": 100.0,
                            "unitref": "qudt:MilliL"
                        }
                    }
                ]
            },
            {
                "@id": "constituent",
                "source": "compound/2/",
                "role": "chm:reagent",
                "properties": [
                    {
                        "@id": "property",
                        "quantity": "mass of substance per volume",
                        "property": "Concentration (w/v)",
                        "value": {
                            "@id": "value",
                            "number": 2.99,
                            "unitref": "qudt:PPM"
                        }
                    },
                    {
                        "@id": "property",
                        "quantity": "volume",
                        "property": "Volume of solution",
                        "value": {
                            "@id": "value",
                            "number": 100.0,
                            "unitref": "qudt:MilliL"
                        }
                    }
                ]
            }
        ],
        "properties": [
            {
                "@id": "property",
                "quantity": "volume",
                "property": "Volume of solution",
                "value": {
                    "@id": "value",
                    "number": 100.0,
                    "unitref": "qudt:MilliL"
                }
            }
        ]
    }
    out = {"@id": "substance/1/",
           "@type": "sdo:substance",
           "title": "3 ppm cyanide standard solution",
           "aggregation": "sub:aq",
           "mixtype": "sub:homogeneousSolution",
           "phase": "sub:liquid",
           "constituents": [{"@id": "substance/1/constituent/1/",
                             "@type": "sdo:constituent",
                             "source": "compound/1/",
                             "role": "chm:analyte",
                             "properties": [{"@id": "substance/1/constituent/1/property/1/",
                                             "@type": "sdo:property",
                                             "quantity": "mass of substance per volume",
                                             "property": "Concentration (w/v)",
                                             "value": {"@id": "substance/1/constituent/1/property/1/value/1/",
                                                       "@type": "sdo:value",
                                                       "number": 2.99,
                                                       "unitref": "qudt:PPM"}},
                                            {"@id": "substance/1/constituent/1/property/2/",
                                             "@type": "sdo:property",
                                             "quantity": "volume",
                                             "property": "Volume of solution",
                                             "value": {"@id": "substance/1/constituent/1/property/2/value/1/",
                                                       "@type": "sdo:value",
                                                       "number": 100.0,
                                                       "unitref": "qudt:MilliL"}}]},
                            {"@id": "substance/1/constituent/2/",
                             "@type": "sdo:constituent",
                             "source": "compound/2/",
                             "role": "chm:reagent",
                             "properties": [{"@id": "substance/1/constituent/2/property/1/",
                                             "@type": "sdo:property",
                                             "quantity": "mass of substance per volume",
                                             "property": "Concentration (w/v)",
                                             "value": {"@id": "substance/1/constituent/2/property/1/value/1/",
                                                       "@type": "sdo:value",
                                                       "number": 2.99,
                                                       "unitref": "qudt:PPM"}},
                                            {"@id": "substance/1/constituent/2/property/2/",
                                             "@type": "sdo:property",
                                             "quantity": "volume",
                                             "property": "Volume of solution",
                                             "value": {"@id": "substance/1/constituent/2/property/2/value/1/",
                                                       "@type": "sdo:value",
                                                       "number": 100.0,
                                                       "unitref": "qudt:MilliL"}}]}],
           "properties": [{"@id": "substance/1/property/1/",
                           "@type": "sdo:property",
                           "quantity": "volume",
                           "property": "Volume of solution",
                           "value": {"@id": "substance/1/property/1/value/1/",
                                     "@type": "sdo:value",
                                     "number": 100.0,
                                     "unitref": "qudt:MilliL"}}]}
    assert sd.facets([compd]) == [out]


def test_scope(sd):
    scope = 'solarsystem/1/'
    assert sd.scope(scope) == scope


def test_datapoint(sd):
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


def test_datapoint_nested(sd):
    """Test multiple, nested datum in datapoints for correct enumeration"""
    sd.namespaces({'gb': 'https://goldbook.iupac.org/terms/view/'})

    # Input datapoint 1
    dp1_datum1 = {
        "@id": "datum",
        "@type": "sdo:exptdata",
        "type": "IC50",
        "value": {
            "@id": "value",
            "@type": "sdo:value",
            "relation": "=",
            "units": "uM",
            "value": "19.000000000000000000000000000000"
        }
    }

    dp1_datum2 = {
        "@id": "datum",
        "@type": "sdo:deriveddata",
        "value": {
            "standard_relation": "=",
            "@id": "value",
            "@type": "sdo:value",
            "standard_value": "19000.000000000000000000000000000000",
            "standard_units": "nM",
            "standard_type": "IC50",
            "pchembl_value": "4.72",
            "uo_units": "obo:UO_0000065",
            "qudt_units": "qudt:NanoMOL-PER-L"
        }
    }

    dp1_datum3 = {
        "@id": "datum",
        "@type": "sdo:None",
        "value": {
            "standard_flag": "1",
            "@id": "value",
            "@type": "sdo:value",
            "activity_id": "16464576"
        }
    }

    dp1 = {
        "@id": "datapoint",
        "@type": "sdo:datapoint",
        "activity_id": 16464576,
        "assay": "CHEMBL3767769",
        "data": [dp1_datum1, dp1_datum2, dp1_datum3]
    }

    # Input datapoint 2
    dp2 = {
        "@id": "datapoint",
        "@type": "sdo:datapoint",
        "annotation": "gb:P04524",
        "conditions": "Observation",
        "value": {
            "@id": "textvalue",
            "@type": "sdo:textvalue",
            "text":
                "The solution was clear, no reagent precipitation was observed.",  # noqa
            "textype": "plain",
            "language": "en-us"
        }
    }

    # Create target output datapoints
    out_dp1 = copy.deepcopy(dp1)

    out_dp1["@id"] = "datapoint/1/"

    out_dp1_datum1 = out_dp1["data"][0]
    out_dp1_datum1["@id"] = "datapoint/1/datum/1/"
    out_dp1_datum1["value"]["@id"] = "datapoint/1/datum/1/value/1/"

    out_dp1_datum2 = out_dp1["data"][1]
    out_dp1_datum2["@id"] = "datapoint/1/datum/2/"
    out_dp1_datum2["value"]["@id"] = "datapoint/1/datum/2/value/1/"

    out_dp1_datum3 = out_dp1["data"][2]
    out_dp1_datum3["@id"] = "datapoint/1/datum/3/"
    out_dp1_datum3["value"]["@id"] = "datapoint/1/datum/3/value/1/"

    out_dp2 = copy.deepcopy(dp2)

    out_dp2["@id"] = "datapoint/2/"
    out_dp2["value"]["@id"] = "datapoint/2/textvalue/1/"

    assert sd.datapoint([dp1, dp2]) == [out_dp1, out_dp2]


def test_datagroup_with_datapoints(sd):
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
    out = {
        "@id": "datagroup/1/",
        "@type": "sdo:datagroup",
        "source": "chemicalsystem/1/",
        "datapoints": [
            "datapoint/1/",
            "datapoint/2/",
            "datapoint/3/"
        ]
    }
    assert sd.datagroup([grp]) == [out]


def test_datagroup_with_attributes(sd):
    sd.namespaces(
        {
            'gb': 'https://goldbook.iupac.org/terms/view/',
            'qudt': 'http://qudt.org/vocab/unit/'
        }
    )

    # Create an X data vector
    datax = [0.1 * i for i in range(10)]

    # Setup attributes of the X data
    atid = 'numericvalue'
    val1 = {'@id': atid, 'number': min(datax), 'unitref': 'qudt:PER-CentiM'}
    val2 = {'@id': atid, 'number': max(datax), 'unitref': 'qudt:PER-CentiM'}
    val3 = {'@id': atid, 'number': len(datax), 'unitref': 'qudt:PER-CentiM'}
    pnt1 = {
        '@id': 'attribute',
        'quantity': 'gb:W06659',
        'value': val1
    }
    pnt2 = {
        '@id': 'attribute',
        'quantity': 'gb:W06659',
        'value': val2
    }
    pnt3 = {
        '@id': 'attribute',
        'quantity': 'gb:W06659',
        'value': val3
    }
    grp = {
        '@id': 'datagroup',
        'attribute': [pnt1, pnt2, pnt3]
    }
    out = {
        "@id": "datagroup/1/",
        "@type": "sdo:datagroup",
        "attribute": [
            "attribute/1/",
            "attribute/2/",
            "attribute/3/"
        ]
    }
    result = sd.datagroup([grp])
    assert result == [out]


def test_source(sd):
    cite = 'The Meaning of Liff, Douglas Adams and John Lloyd, ' \
           'ISBN 0-330-28121-6, 1983'
    url = 'https://en.wikipedia.org/wiki/The_Meaning_of_Liff'
    src = [{'citation': cite, 'url': url}]
    out = [{"@id": "source/1/", "@type": "dc:source",
            "citation": cite, "url": url}]
    assert sd.sources(src) == out


def test_rights(sd):
    holder = 'Megadodo Productions'
    licurl = 'https://creativecommons.org/licenses/by/4.0/'
    lic = 'Creative Commons, Attribution 4.0 Galactic (CC BY 4.0) ' + licurl
    out = [{"@id": "rights/1/", "@type": "dc:rights",
            "holder": holder, "license": lic}]
    assert sd.rights(holder, lic) == out
