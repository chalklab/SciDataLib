"""pytest test class"""
from SciDataLib.SciData import SciData

sd = SciData('example')


def test_discipline():
    assert sd.discipline('chemistry') == 'chemistry'


def test_subdiscipline():
    assert sd.subdiscipline('physicalchemistry') == 'physicalchemistry'
