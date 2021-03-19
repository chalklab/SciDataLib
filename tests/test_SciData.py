"""pytest test class"""
from SciDataLib.SciData import SciData

sd = SciData('example')


def test_context():
    assert sd.context(['https://stuchalk.github.io/scidata/contexts/chembl.jsonld',
                       'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']) == \
            ['https://stuchalk.github.io/scidata/contexts/chembl.jsonld',
                'https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
#
#
# def add_context(self, context: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def namespace(self, namespace: dict) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def add_namespace(self, namespace: dict) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def add_base(self, base: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def make_context(self) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def doc_id(self, i: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def generatedat(self, i: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def version(self, i: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def graph_id(self, i: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
# def graph_type(self, i: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def graph_uid(self, i: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def author(self, author: list) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def title(self, title: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def description(self, description: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def publisher(self, publisher: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def graphversion(self, version: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def keywords(self, keywords: str or list) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def add_keyword(self, keyword: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def starttime(self, st: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def permalink(self, link: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def related(self, related: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def add_related(self, related: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def ids(self, ids: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def add_ids(self, ids: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'


def test_discipline():
    assert sd.discipline('chemistry') == 'chemistry'


def test_subdiscipline():
    assert sd.subdiscipline('physicalchemistry') == 'physicalchemistry'
#
#
# def aspects(self, aspects: list) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def facets(self, facets: list) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def datapoint(self, points: list) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def datagroup(self, datagroup: list) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def source(self, source: list) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def add_source(self, source: list) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def rights(self, holder: str, license: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def add_rights(self, holder: str, license: str) -> dict:
#     assert sd.discipline('chemistry') == 'chemistry'
#
#
# def toc(self):
#     assert sd.discipline('chemistry') == 'chemistry'
