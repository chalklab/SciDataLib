import numpy as np
from typing import TextIO

from scidatalib.scidata import SciData
from scidatalib.io import jcamp


_SCIDATA_UID = "scidata:rruff:jsonld"


def read_rruff(filename: str) -> dict:
    """
    Reader for RRUFF database files to SciData object
    RRUFF file format is a modified version of JCAMP, so re-use jcamp module

    :param filename: Filename to read from for RRUFF files
    :return: SciData object read in from RRUFF file
    """
    with open(filename, "r") as fileobj:
        rruff_dict = _reader(fileobj)
    scidata = _read_translate_rruff_to_scidata(rruff_dict)
    return scidata


def write_rruff(filename: str, scidata: SciData):
    """
    Writer for SciData object to RRUFF files.
    RRUFF URL:  https://rruff.info/
    :param filename: Filename for RRUFF file
    :param scidata: SciData object to write out
    """
    _write_rruff_header_section(filename, scidata, mode='w')
    jcamp._write_jcamp_data_section(
        filename,
        scidata,
        mode='a',
        precision=8,
        trim=8
    )

    with open(filename, 'a') as fileobj:
        fileobj.write('##END=\n')


def _reader(filehandle: TextIO) -> dict:
    """
    File reader for  RRUFF file format

    :param filehandle: RRUFF file to read from
    :return: Dictionary parsed from RRUFF file
    """
    rruff_dict = {}
    y = []
    x = []
    for line in filehandle:
        # Skip blank or comment lines
        if not line.strip():
            continue
        if line.startswith("$$"):
            continue

        rruff_dict, _, _ = jcamp._read_parse_header_line(line, rruff_dict)

        if not line.startswith("##"):
            datavals = jcamp._read_parse_dataset_line(
                line,
                jcamp._DATA_FORMAT_XYXY)
            x.extend(datavals[0::2])
            y.extend(datavals[1::2])

    x = np.array([float(xval) for xval in x])
    y = np.array([float(yval) for yval in y])

    if ("xfactor" in rruff_dict):
        x = x * rruff_dict["xfactor"]
    if ("yfactor" in rruff_dict):
        y = y * rruff_dict["yfactor"]

    rruff_dict['x'] = x
    rruff_dict['y'] = y
    return rruff_dict


def _read_get_aspects_section(rruff_dict: dict) -> dict:
    """
    Extract and translate from the RRUFF dictionary the SciData JSON-LD
    'aspects' sub-ection of the 'methodology' section

    :param rruff_dict: RRUFF dictionary to extract aspects section from
    :return: The 'aspects' section of SciData JSON-LD methodology
    """
    aspects = []

    # Measurement
    measurement = {
        "@id": "measurement/1/",
        "@type": "cao:CAO_000152",
        "techniqueType": "obo:CHMO_0000228",
        "technique": "obo:CHMO_0000656",
        "instrumentType": "raman spectrometer",
        "instrument": "Unknown",
    }

    # Settings for measurement
    settings = []
    if "laser_wavelength" in rruff_dict:
        wavelength = {
            "@id": "setting/1",
            "@type": "sdo:setting",
            "quantity": "wavelength",
            "property": "Laser Wavelength",
            "value": {
                "@id": "setting/1/value/",
                "number": rruff_dict.get("laser_wavelength"),
                "unitstr": "qudt:NanoM",
            }
        }
        settings.append(wavelength)

    measurement.update({"settings": settings})

    aspects.append(measurement)
    return aspects


def _read_get_facets_section(rruff_dict: dict) -> dict:
    """
    Extract and translate from the RRUFF dictionary the SciData JSON-LD
    'facets' sub-section of the 'system' section

    :param rruff_dict: RRUFF dictionary to extract facets section from
    :return: The 'facets' section of SciData JSON-LD from translation
    """

    facets = []
    material = {
        "@id": "material",
        "@type": "sdo:material",
        "name": rruff_dict.get("names", ""),
        "materialType": rruff_dict.get("ideal chemistry", ""),
    }
    facets.append(material)
    return facets


def _read_translate_rruff_to_scidata(rruff_dict: dict) -> dict:
    """
    Main translation of RRUFF to SciData object

    :param rruff_dict: RRUFF dictionary extracted from read
    :return: SciData object from translation
    """
    scidata = SciData(_SCIDATA_UID)

    # Add champ namespace for aspect techniqueType
    cao = {"cao": "http://champ-project.org/images/ontology/cao.owl#"}
    scidata.namespaces(cao)

    # Title
    scidata.title(rruff_dict.get("names", ""))
    scidata.publisher(rruff_dict.get("owner", ""))

    # Description
    description_keywords = [
        "description",
        "locality",
        "status",
    ]
    description = jcamp._read_get_description(rruff_dict, description_keywords)
    scidata.description(description)

    # UID
    rruff_dict.update({"rruffid": f'rruff:{rruff_dict.get("rruffid")}'})
    scidata.graph_uid(rruff_dict.get('rruffid'))

    # Authors
    authors = []
    author_keywords = ["source"]
    for author_keyword in author_keywords:
        if author_keyword in rruff_dict:
            authors.append({
                "@id": "author/{}".format(len(authors) + 1),
                "@type": "dc:creator",
                "name": rruff_dict[author_keyword]
            })
    scidata.author(authors)

    # Sources / references
    sources = []
    sources.append({
        "@id": "source/1/",
        "@type": "dc:source",
        "citation": "Highlights in Mineralogical Crystallography 2015 1-30",
        "reftype": "journal article",
        "doi": "10.1515/9783110417104-003",
        "url": "https://doi.org/10.1515/9783110417104-003"
    })

    if "url" in rruff_dict:
        sources.append({
                "@id": f"source/{len(sources) + 1}",
                "@type": "dc:source",
                "citation": "RRUFF project database entry",
                "url": f'https://{rruff_dict.get("url")}',
            })
    scidata.sources(sources)

    # Discipline and sub-discipline
    scidata.discipline("w3i:Chemistry")
    scidata.subdiscipline("w3i:AnalyticalChemistry")

    # Methodology - aspects
    scidata.aspects(_read_get_aspects_section(rruff_dict))

    # System - facets
    scidata.facets(_read_get_facets_section(rruff_dict))

    # Dataset
    scidata.scope("material")
    datagroup = jcamp._read_get_datagroup_subsection(rruff_dict)
    scidata.datagroup([datagroup])

    # TODO: add the dataseries
    #   Issue: https://github.com/ChalkLab/SciDataLib/issues/43

    return scidata


def _write_get_ideal_chemistry(scidata: SciData) -> str:
    """
    Extract ideal chemistry from SciData object

    :param scidata: SciData object
    :return: The ideal chemistry if exists in SciData object, None otherwise
    """
    chemistry = None
    graph = scidata.output.get("@graph")
    system = graph.get('scidata').get('system')
    for facet in system.get('facets'):
        if facet.get('@id').startswith('material'):
            chemistry = facet.get('materialType')
    return chemistry


def _write_get_laser_wavelength(scidata: SciData) -> str:
    """
    Extract laser wavelength from SciData object

    :param scidata: SciData object
    :return: The laser wavelength if exists in SciData object, None otherwise
    """
    laser_wavelength = None
    graph = scidata.output.get("@graph")
    methodology = graph.get('scidata').get('methodology')
    for aspect in methodology.get('aspects'):
        if aspect.get('@id').startswith('measurement'):
            settings = aspect.get('settings')
            for setting in settings:
                prop = setting.get('property').lower()
                if prop.startswith('laser wavelength'):
                    laser_wavelength = setting.get('value').get('number')
    return laser_wavelength


def _write_get_rruff_url(scidata: SciData) -> str:
    """
    Extract RRUFF URL from SciData object

    :param scidata: SciData object
    :return: The RRUFF URL if exists in SciData object, None otherwise
    """
    url = None
    graph = scidata.output.get("@graph")
    sources = graph.get('sources')
    for source in sources:
        if source.get('url').startswith('https://rruff.info'):
            url = source.get('url').strip('https://')
    return url


def _write_get_header_section(scidata: SciData) -> str:
    """
    Get the header lines section for RRUFF file from SciData object

    :param scidata: SciData object
    :return: List of lines to write for the RRUFF header section
    """
    lines = []

    graph = scidata.output.get("@graph")
    lines.append(f'##NAMES={graph.get("title")}')

    rruffid = graph.get("uid").strip("rruff:")
    lines.append(f'##RRUFFID={rruffid}')

    description = graph.get("description")

    chemistry = _write_get_ideal_chemistry(scidata)
    if chemistry:
        lines.append(f'##IDEAL CHEMISTRY={chemistry}')

    locality = jcamp._write_extract_description_section(
        description,
        "LOCALITY")
    if locality:
        lines.append(f'##LOCALITY={locality}')

    publisher = graph.get("publisher")
    lines.append(f'##OWNER={publisher}')

    author = graph.get('authors')[0]["name"]
    lines.append(f'##SOURCE={author}')

    rruff_description = jcamp._write_extract_description_section(
        description,
        "DESCRIPTION")
    if rruff_description:
        lines.append(f'##DESCRIPTION={rruff_description}')

    status = jcamp._write_extract_description_section(description, "STATUS")
    if status:
        lines.append(f'##STATUS={status}')

    laser_wavelength = _write_get_laser_wavelength(scidata)
    if laser_wavelength:
        lines.append(f'##LASER_WAVELENGTH={laser_wavelength}')

    url = _write_get_rruff_url(scidata)
    if url:
        lines.append(f'##URL={url}')

    return '\n'.join(lines) + '\n'


def _write_rruff_header_section(
    filename: str, scidata: SciData, mode: str = 'w'
):
    """
    Writes RRUFF file header to filename using the SciData object.
    Can optionally change the mode of how to open the file.

    :param filename: Name of the RRUFF file to write
    :param scidata: SciData object to write as RRUFF file
    :param mode: File mode. Default is 'w'.
    """
    lines = _write_get_header_section(scidata)
    with open(filename, mode) as fileobj:
        for line in lines:
            fileobj.write(line)
