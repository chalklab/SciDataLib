"""pytest test class"""
from scidatalib.scidata import SciData

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
    new_nspaces = {'test': 'https://test.org/test#'}
    existing_nspaces.update(new_nspaces)
    assert sd.namespaces(new_nspaces) == existing_nspaces


def test_namespace_replace():
    new_nspaces = {'test': 'https://test.org/test#'}
    assert sd.namespaces(new_nspaces, True) == new_nspaces
#
#
# def test_add_base():
#     assert sd.add_base('chemistry') == 'chemistry'
#
#
# def test_make_context():
#     assert sd.make_context('chemistry') == 'chemistry'
#
#
# def test_doc_id():
#     assert sd.doc_id('chemistry') == 'chemistry'
#
#
# def test_generatedat():
#     assert sd.generatedat('chemistry') == 'chemistry'
#
#
# def test_version():
#     assert sd.version('chemistry') == 'chemistry'
#
#
# def test_graph_id():
#     assert sd.graph_id('chemistry') == 'chemistry'
#
# def test_graph_type():
#     assert sd.graph_type('chemistry') == 'chemistry'
#
#
# def test_graph_uid():
#     assert sd.graph_uid('chemistry') == 'chemistry'
#
#
# def test_author():
#     assert sd.author('chemistry') == 'chemistry'
#
#
# def test_title():
#     assert sd.title('chemistry') == 'chemistry'
#
#
# def test_description():
#     assert sd.description('chemistry') == 'chemistry'
#
#
# def test_publisher():
#     assert sd.publisher('chemistry') == 'chemistry'
#
#
# def test_graphversion():
#     assert sd.graphversion('chemistry') == 'chemistry'
#
#
# def test_keywords():
#     assert sd.keywords('chemistry') == 'chemistry'
#
#
# def test_add_keyword():
#     assert sd.add_keyword('chemistry') == 'chemistry'
#
#
# def test_starttime():
#     assert sd.starttime('chemistry') == 'chemistry'
#
#
# def test_permalink():
#     assert sd.permalink('chemistry') == 'chemistry'
#
#
# def test_related():
#     assert sd.related('chemistry') == 'chemistry'
#
#
# def test_add_related():
#     assert sd.add_related('chemistry') == 'chemistry'
#
#
# def test_ids():
#     assert sd.ids('chemistry') == 'chemistry'
#
#
# def test_add_ids():
#     assert sd.add_ids('chemistry') == 'chemistry'


def test_discipline():
    assert sd.discipline('chemistry') == 'chemistry'


def test_subdiscipline():
    assert sd.subdiscipline('physicalchemistry') == 'physicalchemistry'


def test_author():
    org = 'University of North Florida'
    orcid = '0000-0002-0703-7776'
    au = [{'name': 'Stuart Chalk', 'organization': org, 'orcid': orcid}]
    out = [{'@id': 'author/1/', '@type': 'dc:creator',
            'name': 'Stuart Chalk', 'organization': org, 'orcid': orcid}]
    assert sd.author(au) == out
#
#
# def test_aspects():
#     assert sd.aspects('chemistry') == 'chemistry'
#
#
# def test_facets():
#     assert sd.facets('chemistry') == 'chemistry'
#
#
# def test_datapoint():
#     assert sd.datapoint('chemistry') == 'chemistry'
#
#
# def test_datagroup():
#     assert sd.datagroup('chemistry') == 'chemistry'
#
#
# def test_source():
#     assert sd.source('chemistry') == 'chemistry'
#
#
# def test_add_source():
#     assert sd.add_source('chemistry') == 'chemistry'
#
#
# def test_rights():
#     assert sd.rights('chemistry') == 'chemistry'
#
#
# def test_add_rights():
#     assert sd.add_rights('chemistry') == 'chemistry'
#
#
# def test_toc():
#     assert sd.toc('chemistry') == 'chemistry'
