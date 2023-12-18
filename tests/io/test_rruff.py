import pathlib
import pytest

from scidatalib.io import rruff
from tests import TEST_DATA_DIR


@pytest.fixture
def raman_soddyite_file():
    """
    Raman RRUFF file for Soddyite for wavelength 780 nm
    Retrieved on 1/12/2021 from:
        https://rruff.info/tmp_rruff/Soddyite__R060361__Broad_Scan__780__0__unoriented__Raman_Data_RAW__21504.rruff  # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "rruff", "raman_soddyite.rruff")
    return p


def test_read_rruff(raman_soddyite_file):
    scidata = rruff.read_rruff(raman_soddyite_file.resolve())

    # Top-level section
    graph = scidata.output.get("@graph")
    assert graph["title"] == "Soddyite"
    assert graph["uid"] == "rruff:R060361"

    assert len(graph["authors"]) == 1
    assert graph["authors"][0]["name"] == "Michael Scott"

    assert len(graph["sources"]) == 2
    assert graph["sources"][0]["@type"] == "dc:source"
    assert "Mineralogical" in graph["sources"][0]["citation"]
    assert graph["sources"][0]["reftype"] == "journal article"
    assert graph["sources"][0]["doi"] == "10.1515/9783110417104-003"

    assert graph["sources"][1]["@type"] == "dc:source"
    assert "RRUFF" in graph["sources"][1]["citation"]
    assert graph["sources"][1]["url"] == "https://rruff.info/R060361"

    assert graph["scidata"]["discipline#"] == "w3i:Chemistry"
    assert graph["scidata"]["subdiscipline#"] == "w3i:AnalyticalChemistry"

    # Check description has all the keywords from RRUFF file
    description = graph.get("description")
    for rruff_keyword in ["DESCRIPTION", "LOCALITY", "STATUS"]:
        assert rruff_keyword in description

    # Check that the DESCRIPTION from RRUFF file is copied over
    for description_keyword in ["pyramidal", "malachite", "brochantite"]:
        assert description_keyword in description

    # Check that the LOCALITY from RRUFF file is copied over
    for locality_keyword in ["Musonoi", "Kolwezi", "Shaba", "Zaire"]:
        assert locality_keyword in description

    # Check that the STATUS from RRUFF file is copied over
    for status_keyword in ["identification", "single-crystal", "X-ray"]:
        assert status_keyword in description

    # Methodology
    methodology = graph["scidata"]["methodology"]
    assert methodology["@id"] == 'methodology/'
    assert methodology["@type"] == 'sdo:methodology'
    assert len(methodology["aspects"]) == 1
    aspects = methodology["aspects"]
    assert len(aspects[0]["settings"]) == 1
    assert aspects[0]["settings"][0]["value"]["number"] == 780

    # System
    system = graph["scidata"]["system"]
    assert system["@id"] == 'system/'
    assert system["@type"] == 'sdo:system'
    assert len(system["facets"]) == 1
    facet = system["facets"][0]
    assert facet["@id"] == "material/1/"
    assert facet["@type"] == "sdo:material"
    assert facet["materialType"] == "(UO_2_)_2_SiO_4_&#183;2H_2_O"
    assert facet["name"] == "Soddyite"


def test_write_rruff(tmp_path, raman_soddyite_file):
    scidata = rruff.read_rruff(raman_soddyite_file.absolute())
    rruff_dir = tmp_path / "rruff"
    rruff_dir.mkdir()
    filename = rruff_dir / "raman_soddyite.rruff"

    rruff.write_rruff(filename.resolve(), scidata)

    result = filename.read_text().splitlines()
    target = raman_soddyite_file.read_text().splitlines()

    for result_element, target_element in zip(result, target):
        result_list = [x.strip() for x in result_element.split(',')]
        target_list = [x.strip() for x in target_element.split(',')]

        assert result_list == target_list
