"""pytest test class"""
import pytest
from scidatalib.scidata import SciData

sd = SciData('example')

@pytest.mark.skip
def test_context():
    assert sd.context(
        ['https://stuchalk.github.io/scidata/contexts/chembl.jsonld',
         'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']) == \
           ['https://stuchalk.github.io/scidata/contexts/chembl.jsonld',
            'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']


# def test_add_context():
#     assert sd.add_context('chemistry') == 'chemistry'
#
#
# def test_namespace():
#     assert sd.namespace('chemistry') == 'chemistry'
#
#
# def test_add_namespace():
#     assert sd.add_namespace('chemistry') == 'chemistry'
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
