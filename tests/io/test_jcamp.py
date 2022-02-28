import numpy as np
import pathlib
import pytest
from typing import List

from scidatalib.scidata import SciData
from scidatalib.io import jcamp, read, write
from tests import TEST_DATA_DIR


@pytest.fixture
def hnmr_ethanol_file():
    """
    Hydrogen NMR JCAMP-DX file for ethanol
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/hnmr_spectra/ethanol_nmr.jdx  # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "hnmr_ethanol.jdx")
    return p


@pytest.fixture
def infrared_ethanol_file():
    """
    Infrared JCAMP-DX file for ethanol
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/infrared_spectra/ethanol.jdx  # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "infrared_ethanol.jdx")
    return p


@pytest.fixture
def infrared_ethanol_compressed_file():
    """
    Infrared JCAMP-DX file for ethanol using compression
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/infrared_spectra/ethanol2.jdx  # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "infrared_ethanol_compressed.jdx")
    return p


@pytest.fixture
def infrared_compound_file():
    """
    Infrared JCAMP-DX compound file
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/infrared_spectra/example_compound_file.jdx  # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "infrared_compound_file.jdx")
    return p


@pytest.fixture
def infrared_multiline_file():
    """
    Infrared JCAMP-DX multiline file
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/infrared_spectra/example_multiline_datasets.jdx  # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "infrared_multiline_datasets.jdx")
    return p


@pytest.fixture
def mass_ethanol_file():
    """
    Mass spectroscopy JCAMP-DX file
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/mass_spectra/ethanol_ms.jdx # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "mass_ethanol.jdx")
    return p


@pytest.fixture
def neutron_emodine_file():
    """
    Inelastic neutron spectroscopy JCAMP-DX file
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/neutron_scattering_spectra/emodine.jdx # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "neutron_emodine.jdx")
    return p


@pytest.fixture
def raman_tannic_acid_file():
    """
    Raman spectroscopy JCAMP-DX file
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/raman_spectra/tannic_acid.jdx # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "raman_tannic_acid.jdx")
    return p


@pytest.fixture
def uvvis_toluene_file():
    """
    UV-Visible spectroscopy JCAMP-DX file
    Retrieved on 1/12/2021 from:
        https://raw.githubusercontent.com/nzhagen/jcamp/master/data/uvvis_spectra/toluene.jdx # noqa: E501
    """
    p = pathlib.Path(TEST_DATA_DIR, "jcamp", "uvvis_toluene.jdx")
    return p


@pytest.fixture
def citation_dict():
    """
    Citation dict for testing using Alpha, Beta, Gamma paper
    """
    author = "Alpher, R. A.; Bethe, H.; Gamow, G."
    title = "The Origin of Chemical Elements"
    journal = "Phys. Rev."
    volume = "73"
    date = "1948"
    page = "803-804"

    citation_dict = {
        "$ref author": author,
        "$ref title": title,
        "$ref journal": journal,
        "$ref volume": volume,
        "$ref date": date,
        "$ref page": page,
    }
    return citation_dict


def remove_elements_from_list(
    old_list: List[str],
    skip_elements: List[str]
) -> List[str]:
    """
    Utility function for removing elements from a list

    :param old_list: List to remove elements from
    :param skip_elements: List with elements to remove from the list
    :return: New list with the elements removed
    """
    new_list = []
    for element in old_list:
        keep = True
        element_list = [x.strip() for x in element.split(',')]
        for key in skip_elements:
            for x in element_list:
                if key in x:
                    keep = False

        if keep:
            new_list.append(element)

    return new_list


def xy_minmax_checker(testdict):
    tol = 1e-4
    if testdict['x'] and 'minx' in testdict:
        assert isinstance(testdict['x'], list)
        assert isinstance(testdict['y'], list)
        assert len(testdict['x']) == len(testdict['y'])
        assert min(testdict['x']) == pytest.approx(testdict['minx'], tol)
        assert min(testdict['y']) == pytest.approx(testdict['miny'], tol)
        assert max(testdict['x']) == pytest.approx(testdict['maxx'], tol)
        assert max(testdict['y']) == pytest.approx(testdict['maxy'], tol)
    elif 'children' in testdict:
        for child in testdict['children']:
            if ('minx' in testdict):
                assert min(child['x']) == child['minx']
                assert min(child['y']) == child['miny']
                assert max(child['x']) == child['maxx']
                assert max(child['y']) == child['maxy']


# Tests

def test_reader_is_float():
    assert jcamp._reader_is_float('0.09')
    assert jcamp._reader_is_float(['0.09'])
    assert jcamp._reader_is_float(['0.09', '10.0', '10'])
    assert jcamp._reader_is_float(('0.09', '10.0', '10'))

    assert not jcamp._reader_is_float('cat')
    assert jcamp._reader_is_float(['cat']) == [False]
    assert jcamp._reader_is_float(['cat', 'x']) == [False, False]

    mylist = ['cat', 'x', '2', '=', 'cats']
    target = [False, False, True, False, False]
    assert jcamp._reader_is_float(mylist) == target

    with pytest.raises(TypeError):
        jcamp._reader_is_float(0.09)

    with pytest.raises(TypeError):
        jcamp._reader_is_float([0.09])

    with pytest.raises(ValueError):
        jcamp._reader_is_float([])


def test_read_num_dif_factory():
    # space character
    num, DIF = jcamp._read_num_dif_factory(' ', '')
    assert num == ''
    assert DIF is False

    # SQZ digits character
    num, DIF = jcamp._read_num_dif_factory('A', '')
    assert num == '+1'
    assert DIF is False

    # DIF digits character
    num, DIF = jcamp._read_num_dif_factory('n', '')
    assert num == '-5'
    assert DIF is True


def test_read_parse_dataset_line():
    target = [99.0, 98.0, 97.0, 96.0, 98.0, 93.0]
    line = "99 98 97 96 98 93"

    result = jcamp._read_parse_dataset_line(line, jcamp._DATA_FORMAT_XYYY)
    assert result == target

    result = jcamp._read_parse_dataset_line(line, jcamp._DATA_FORMAT_XYXY)
    assert result == target

    data_format = 'BAD FORMAT'
    with pytest.raises(jcamp.UnsupportedDataTypeConfigException):
        jcamp._read_parse_dataset_line(line, data_format)


def test_read_parse_dataset_duplicate_characters():
    assert jcamp._read_parse_dataset_duplicate_characters("9U") == "999"


def test_read_parse_dataset_line_single_x_multi_y():
    target = [99.0, 98.0, 97.0, 96.0, 98.0, 93.0]

    line = "99 98 97 96 98 93"
    assert jcamp._read_parse_dataset_line_single_x_multi_y(line) == target

    line = "99,98,97,96,98,93"
    assert jcamp._read_parse_dataset_line_single_x_multi_y(line) == target

    line = "99+98+97+96+98+93"
    assert jcamp._read_parse_dataset_line_single_x_multi_y(line) == target

    line = "99I8I7I6I8I3"
    assert jcamp._read_parse_dataset_line_single_x_multi_y(line) == target

    line = "99jjjKn"
    assert jcamp._read_parse_dataset_line_single_x_multi_y(line) == target

    line = "99jUKn"
    assert jcamp._read_parse_dataset_line_single_x_multi_y(line) == target

    line = "99 98 *"
    with pytest.raises(jcamp.UnknownCharacterException):
        jcamp._read_parse_dataset_line_single_x_multi_y(line)


def test_read_parse_header_line():
    line = ''
    in_dict = {}
    jcamp_dict, start, last_key = jcamp._read_parse_header_line(line, in_dict)
    jcamp_dict, start, last_key = jcamp._read_parse_header_line(line, in_dict)
    assert jcamp_dict == {}
    assert start is False
    assert last_key is None

    in_dict = {
        'title': "ETHANOL",
        'data type': "INFRARED SPECTRUM",
        'molform': "C2 H6 O"
    }
    jcamp_dict, start, last_key = jcamp._read_parse_header_line(line, in_dict)
    assert jcamp_dict == in_dict
    assert start is False
    assert last_key is None

    line = "##XUNITS= 1/CM"
    jcamp_dict, start, last_key = jcamp._read_parse_header_line(line, in_dict)
    in_dict.update({'xunits': '1/CM'})
    assert jcamp_dict == in_dict
    assert start is False
    assert last_key == 'xunits'


def test_reader_hnmr(hnmr_ethanol_file):
    with open(hnmr_ethanol_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert 'Ethanol' in jcamp_dict.get('title')
    assert jcamp_dict.get('data type') == "LINK"

    children = jcamp_dict.get('children')
    assert len(children) == jcamp_dict.get('blocks')

    atoms = children[0]
    assert 'atomlist' in atoms
    assert atoms.get('block_id') == 1

    assignments = children[1]
    assert assignments.get('block_id') == 2
    assert assignments.get('data type') == "NMR PEAK ASSIGNMENTS"
    assert assignments.get('data class') == "ASSIGNMENTS"

    peaks = children[2]
    assert peaks.get('block_id') == 3
    assert peaks.get('data type') == "NMR SPECTRUM"
    assert peaks.get('data class') == "PEAK TABLE"
    assert peaks.get(jcamp._DATA_XY_TYPE_KEY) == '(XY..XY)'

    xydata = children[3]
    assert xydata.get('block_id') == 4
    assert xydata.get('data type') == "NMR SPECTRUM"
    assert xydata.get('data class') == "XYDATA"
    assert xydata.get(jcamp._DATA_XY_TYPE_KEY) == '(X++(Y..Y))'


def test_reader_infrared(infrared_ethanol_file):
    with open(infrared_ethanol_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "ETHANOL"
    assert jcamp_dict.get('data type') == "INFRARED SPECTRUM"
    assert jcamp_dict.get('molform') == "C2 H6 O"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(X++(Y..Y))'


def test_reader_exception_bad_datatype(tmp_path, infrared_ethanol_file):
    # Create a "bad type" tmp file
    jcamp_dir = tmp_path / "jcamp"
    jcamp_dir.mkdir()
    bad_file = jcamp_dir / "bad_data_type.jdx"

    # Read input file lines and modify XYDATA file to "bad type"
    with open(infrared_ethanol_file.resolve(), 'r') as fileobj:
        lines = fileobj.readlines()
        for i, line in enumerate(lines):
            if line.startswith("##XYDATA"):
                lines[i] = "##XYDATA=BAD_DATA_TYPE\n"

    # Read modified lines to the "bad type" tmp file
    with open(bad_file.resolve(), 'w') as fileobj:
        fileobj.writelines(lines)

    # Read in "bad file" for test
    with open(bad_file.resolve(), 'r') as fileobj:
        with pytest.raises(jcamp.UnsupportedDataTypeConfigException):
            jcamp._reader(fileobj)


def test_read_get_graph_source_citation_section(citation_dict):
    target = [
        f'{citation_dict["$ref author"]} :',
        f'{citation_dict["$ref title"]}.',
        f'{citation_dict["$ref journal"]}',
        f'{citation_dict["$ref volume"]}',
        f'({citation_dict["$ref date"]})',
        f'{citation_dict["$ref page"]}',
    ]
    result = jcamp._read_get_graph_source_citation_section(citation_dict)
    assert target == result


def test_read_get_graph_source_section(citation_dict):
    # Citation
    abc_citation = {
        '@id': 'source/1',
        '@type': 'dc:source',
        'citation': (
            "Alpher, R. A.; Bethe, H.; Gamow, G. : "
            "The Origin of Chemical Elements. "
            "Phys. Rev. 73 (1948) 803-804"),
        'reftype': 'journal article',
        'doi': '',
        'url': ''
    }
    target = [abc_citation]
    result = jcamp._read_get_graph_source_section(citation_dict)
    assert target == result

    # Source reference
    citation_dict.update(
        {
            "source reference": (
                "R. C. Herman "
                "(who stubbornly refuses to change his name to Delter)")
        }
    )
    d_citation = {
        '@id': 'source/2',
        '@type': 'dc:source',
        'citation': f'{citation_dict["source reference"]}',
    }
    target.append(d_citation)
    result = jcamp._read_get_graph_source_section(citation_dict)
    assert target == result

    # NIST source
    citation_dict.update({"$nist source": "Source from NIST"})
    nist_source = f'NIST SOURCE: {citation_dict["$nist source"]}'
    nist_citation = {
        '@id': 'source/3',
        '@type': 'dc:source',
        'citation': f'{nist_source}',
    }
    target.append(nist_citation)
    result = jcamp._read_get_graph_source_section(citation_dict)
    assert target == result

    # NIST image
    citation_dict.pop("$nist source")

    citation_dict.update({"$nist image": "Image from NIST"})
    nist_image = f'NIST IMAGE: {citation_dict["$nist image"]}'
    nist_citation = {
        '@id': 'source/3',
        '@type': 'dc:source',
        'citation': f'{nist_image}',
    }
    target[-1] = nist_citation
    result = jcamp._read_get_graph_source_section(citation_dict)
    assert target == result

    # NIST source and image
    citation_dict.pop("$nist image")

    citation_dict.update({"$nist source": "Source from NIST"})
    citation_dict.update({"$nist image": "Image from NIST"})
    nist_image = f'NIST IMAGE: {citation_dict["$nist image"]}'
    nist_citation = {
        '@id': 'source/3',
        '@type': 'dc:source',
        'citation': f'{nist_source}, {nist_image}'
    }
    target[-1] = nist_citation
    result = jcamp._read_get_graph_source_section(citation_dict)
    assert target == result


def test_read_get_aspects_section():
    spectrometer = "DOW KBr FOREPRISM-GRATING"
    jcamp_dict = {
        "spectrometer/data system": spectrometer,
    }
    measurement = {
        "@id": "measurement/1",
        "@type": "sdo:measurement",
        "techniqueType": "cao:spectroscopy",
        "instrument": spectrometer,
    }
    target = [measurement]
    result = jcamp._read_get_aspects_section(jcamp_dict)
    assert target == result

    parameter = "GRATING CHANGED AT 5.0, 7.5, 15.0 MICRON"
    jcamp_dict.update({"instrument parameters": parameter})
    instrument_parameters = {
        "@id": "setting/1",
        "@type": "sdo:setting",
        "property": "instrument parameters",
        "value": {
            "@id": "setting/1/value",
            "number": parameter,
        }
    }
    settings = {"settings": [instrument_parameters]}
    measurement.update({"settings": [instrument_parameters]})
    target = [measurement]
    result = jcamp._read_get_aspects_section(jcamp_dict)
    assert target == result

    path_value = "5"
    path_unit = "CM"
    jcamp_dict.update({"path length": f'{path_value} {path_unit}'})
    path_length = {
        "@id": "setting/2",
        "@type": "sdo:setting",
        "quantity": "length",
        "property": "path length",
        "value": {
            "@id": "setting/2/value",
            "number": path_value,
            "unitref": "qudt:CentiM",
        }
    }
    settings = {"settings": [instrument_parameters, path_length]}
    measurement.update(settings)
    target = [measurement]
    result = jcamp._read_get_aspects_section(jcamp_dict)
    assert target == result

    resolution_value = "2"
    jcamp_dict.update({"resolution": f'{resolution_value}'})
    resolution = {
        "@id": "setting/3",
        "@type": "sdo:setting",
        "quantity": "resolution",
        "property": "resolution",
        "value": {
            "@id": "setting/3/value",
            "number": f'{resolution_value}',
        }
    }
    settings = {"settings": [instrument_parameters, path_length, resolution]}
    measurement.update(settings)
    target = [measurement]
    result = jcamp._read_get_aspects_section(jcamp_dict)
    assert target == result

    description = "TRANSMISSION"
    jcamp_dict.update({"sampling procedure": description})
    procedure = {
        "@id": "procedure/1",
        "@type": "sdo:procedure",
        "description": description,
    }
    target = [measurement, procedure]
    result = jcamp._read_get_aspects_section(jcamp_dict)
    assert target == result

    description = "DIGITIZED BY NIST FROM HARD COPY (FROM TWO SEGMENTS)"
    jcamp_dict.update({"data processing": description})
    processing = {
        "@id": "resource/1",
        "@type": "sdo:resource",
        "description": description,
    }
    target = [measurement, procedure, processing]
    result = jcamp._read_get_aspects_section(jcamp_dict)
    assert target == result


def test_read_get_facets_section():
    title = "ETHANOL"
    molform = "C2 H6 O"
    jcamp_dict = {
        "title": title,
        "molform": molform,
    }
    compound = {
        "@id": "compound/1",
        "@type": ["sdo:facet", "sdo:material"],
        "name": title,
        "formula": molform,
    }
    target = [compound]
    result = jcamp._read_get_facets_section(jcamp_dict)
    assert target == result

    casrn = "64-17-5"
    jcamp_dict.update({"cas registry no": casrn})
    compound.update({"casrn": casrn})
    target = [compound]
    result = jcamp._read_get_facets_section(jcamp_dict)
    assert target == result

    phase = "GAS"
    jcamp_dict.update({"state": phase})
    substance = {
        "@id": "substance/1",
        "@type": ["sdo:constituent"],
        "name": title,
        "phase": phase,
    }
    target = [compound, substance]
    result = jcamp._read_get_facets_section(jcamp_dict)
    assert target == result

    partial_pressure_value = "30"
    partial_pressure_unit = "mmHg"
    partial_pressure = f'{partial_pressure_value} {partial_pressure_unit}'
    jcamp_dict.update({"partial_pressure": partial_pressure})
    condition = {
        "@id": "condition/1",
        "@type": ["sdo:condition"],
        "quantity": "pressure",
        "property": "Partial pressure",
        "value": {
            "@id": "condition/1/value",
            "@type": "sdo:value",
            "number": partial_pressure_value,
            "unitref": "qudt:MilliM_HG",
        }
    }
    target = [compound, substance, condition]
    result = jcamp._read_get_facets_section(jcamp_dict)
    assert target == result


def test_read_get_dataseries_subsection():
    xset = [str(x) for x in np.arange(0., 10., 0.1)]
    yset = [str(y) for y in np.random.random(len(xset))]
    jcamp_dict = {
        "x": xset,
        "y": yset,
        "xunits": "1/CM",
    }
    result = jcamp._read_get_dataseries_subsection(jcamp_dict)

    result_x = result[0]["parameter"][0]["dataarray"]
    result_y = result[0]["parameter"][1]["dataarray"]
    result_xunit = result[0]["parameter"][0]["unitref"]

    assert list(xset) == list(result_x)
    assert list(yset) == list(result_y)
    assert "qudt:PER-CentiM" == result_xunit


def test_reader_infrared_compressed(infrared_ethanol_compressed_file):
    with open(infrared_ethanol_compressed_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "$$ Begin of the data block"
    assert jcamp_dict.get('data type') == "INFRARED SPECTRUM"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(X++(Y..Y))'


def test_reader_infrared_compound(infrared_compound_file):
    with open(infrared_compound_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == ""
    assert jcamp_dict.get('data type') == "LINK"

    children = jcamp_dict.get('children')
    assert len(children) == jcamp_dict.get('blocks')

    for child in children:
        assert child.get('data type') == "INFRARED SPECTRUM"
        assert child.get(jcamp._DATA_XY_TYPE_KEY) == '(XY..XY)'


def test_reader_infrared_multiline(infrared_multiline_file):
    with open(infrared_multiline_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "multiline datasets test"
    assert jcamp_dict.get('data type') == "INFRARED SPECTRUM"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(X++(Y..Y))'


def test_reader_mass(mass_ethanol_file):
    with open(mass_ethanol_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "ethanol"
    assert jcamp_dict.get('data type') == "MASS SPECTRUM"
    assert jcamp_dict.get('data class') == "PEAK TABLE"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(XY..XY)'


def test_reader_neutron(neutron_emodine_file):
    with open(neutron_emodine_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "Emodine, C15H10O4"
    assert jcamp_dict.get('data type') == "INELASTIC NEUTRON SCATTERING"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(X++(Y..Y))'


def test_reader_raman(raman_tannic_acid_file):
    with open(raman_tannic_acid_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "tannic acid"
    assert jcamp_dict.get('data type') == "RAMAN SPECTRUM"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(XY..XY)'


def test_reader_uvvis(uvvis_toluene_file):
    with open(uvvis_toluene_file.resolve(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "Toluene"
    assert jcamp_dict.get('data type') == "UV/VIS SPECTRUM"
    assert jcamp_dict.get('molform') == "C7H8"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(XY..XY)'


def test_read_jcamp_function(raman_tannic_acid_file):
    scidata_obj = jcamp.read_jcamp(raman_tannic_acid_file)
    assert type(scidata_obj) == SciData

    dataset = scidata_obj.output.get("@graph").get("scidata").get("dataset")
    dataseries = dataset.get("dataseries")[0]
    assert dataseries.get("@id") == "dataseries/1/"


def test_read_jcamp(raman_tannic_acid_file):
    scidata_obj = read(raman_tannic_acid_file, ioformat="jcamp")
    assert type(scidata_obj) == SciData


def test_write_jcamp_function(tmp_path, raman_tannic_acid_file):
    scidata = jcamp.read_jcamp(raman_tannic_acid_file.resolve())
    jcamp_dir = tmp_path / "jcamp"
    jcamp_dir.mkdir()
    filename = jcamp_dir / "raman_tannic_acid.jdx"

    jcamp.write_jcamp(filename.resolve(), scidata)

    result = filename.read_text().splitlines()
    target = raman_tannic_acid_file.read_text().splitlines()

    # List keys that io.jcamp.write_jcamp has yet to address
    skip_keys = [
        "##DATA TYPE",
        "##YUNITS",
    ]
    target = remove_elements_from_list(target, skip_keys)
    result = remove_elements_from_list(target, skip_keys)

    for result_element, target_element in zip(result, target):
        result_list = [x.strip() for x in result_element.split(',')]
        target_list = [x.strip() for x in target_element.split(',')]

        assert result_list == target_list


def test_write_jcamp(tmp_path, raman_tannic_acid_file):
    scidata = jcamp.read_jcamp(raman_tannic_acid_file.resolve())
    jcamp_dir = tmp_path / "jcamp"
    jcamp_dir.mkdir()
    filename = jcamp_dir / "raman_tannic_acid.jdx"

    write(filename.resolve(), scidata, ioformat="jcamp")

    result = filename.read_text().splitlines()
    target = raman_tannic_acid_file.read_text().splitlines()

    # List keys that io.jcamp.write_jcamp has yet to address
    skip_keys = [
        "##DATA TYPE",
        "##YUNITS",
    ]
    target = remove_elements_from_list(target, skip_keys)
    result = remove_elements_from_list(result, skip_keys)

    for result_element, target_element in zip(result, target):
        result_list = [x.strip() for x in result_element.split(',')]
        target_list = [x.strip() for x in target_element.split(',')]

        assert result_list == target_list
