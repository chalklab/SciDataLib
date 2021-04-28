import pathlib
import pytest

from scidatalib.scidata import SciData
from scidatalib.io import jcamp, read
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
def citation():
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
    with open(hnmr_ethanol_file.absolute(), 'r') as fileobj:
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
    with open(infrared_ethanol_file.absolute(), 'r') as fileobj:
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
    with open(infrared_ethanol_file.absolute(), 'r') as fileobj:
        lines = fileobj.readlines()
        for i, line in enumerate(lines):
            if line.startswith("##XYDATA"):
                lines[i] = "##XYDATA=BAD_DATA_TYPE\n"

    # Read modified lines to the "bad type" tmp file
    with open(bad_file.absolute(), 'w') as fileobj:
        fileobj.writelines(lines)

    # Read in "bad file" for test
    with open(bad_file.absolute(), 'r') as fileobj:
        with pytest.raises(jcamp.UnsupportedDataTypeConfigException):
            jcamp._reader(fileobj)


def test_read_get_source_citation_section(citation):
    # Input dictionary to parse
    target = [
        f'{citation["$ref author"]} :',
        f'{citation["$ref title"]}.',
        f'{citation["$ref journal"]} ',
        f'{citation["$ref volume"]}',
        f'({citation["$ref date"]})',
        f'{citation["$ref page"]}',
    ]
    result = jcamp._read_get_graph_source_citation_section(citation)
    assert target == result


def test_reader_infrared_compressed(infrared_ethanol_compressed_file):
    with open(infrared_ethanol_compressed_file.absolute(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "$$ Begin of the data block"
    assert jcamp_dict.get('data type') == "INFRARED SPECTRUM"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(X++(Y..Y))'


def test_reader_infrared_compound(infrared_compound_file):
    with open(infrared_compound_file.absolute(), 'r') as fileobj:
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
    with open(infrared_multiline_file.absolute(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "multiline datasets test"
    assert jcamp_dict.get('data type') == "INFRARED SPECTRUM"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(X++(Y..Y))'


def test_reader_mass(mass_ethanol_file):
    with open(mass_ethanol_file.absolute(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "ethanol"
    assert jcamp_dict.get('data type') == "MASS SPECTRUM"
    assert jcamp_dict.get('data class') == "PEAK TABLE"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(XY..XY)'


def test_reader_neutron(neutron_emodine_file):
    with open(neutron_emodine_file.absolute(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "Emodine, C15H10O4"
    assert jcamp_dict.get('data type') == "INELASTIC NEUTRON SCATTERING"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(X++(Y..Y))'


def test_reader_raman(raman_tannic_acid_file):
    with open(raman_tannic_acid_file.absolute(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "tannic acid"
    assert jcamp_dict.get('data type') == "RAMAN SPECTRUM"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(XY..XY)'


def test_reader_uvvis(uvvis_toluene_file):
    with open(uvvis_toluene_file.absolute(), 'r') as fileobj:
        jcamp_dict = jcamp._reader(fileobj)
    xy_minmax_checker(jcamp_dict)

    assert jcamp_dict.get('title') == "Toluene"
    assert jcamp_dict.get('data type') == "UV/VIS SPECTRUM"
    assert jcamp_dict.get('molform') == "C7H8"
    assert jcamp_dict.get(jcamp._DATA_XY_TYPE_KEY) == '(XY..XY)'


def test_read_jcamp_function(raman_tannic_acid_file):
    scidata_obj = jcamp.read_jcamp(raman_tannic_acid_file)
    assert type(scidata_obj) == SciData


def test_read_jcamp(raman_tannic_acid_file):
    scidata_obj = read(raman_tannic_acid_file, ioformat="jcamp")
    assert type(scidata_obj) == SciData
