""" JCAMP-DX module for reading / writing to SciData objects

Original author for JCAMP reader code:
    Nathan Hagen, 2013, https://github.com/nzhagen/jcamp
Modified by:
    Marshall McDonnell, 2021

Original copyright
==================
Copyright (c) 2013 Nathan Hagen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
import numpy as np
import re
from typing import List, Tuple

from scidatalib.scidata import SciData

_DATA_FORMAT_XYXY = '(XY..XY)'
_DATA_FORMAT_XYYY = '(X++(Y..Y))'
_DATA_FORMATS = (_DATA_FORMAT_XYXY, _DATA_FORMAT_XYYY)
_DATA_TYPE_KEY = "data type"
_DATA_XY_TYPE_KEY = "xy data type"
_DATA_XY_TYPES = ('xydata', 'xypoints', 'peak table')
_DATA_LINK = "link"
_DESCRIPTION_KEY_SPLIT_CHAR = ";"
_CHILDREN = "children"
_XUNIT_MAP = {
    "1/CM": "qudt:PER-CentiM",
}
_PRESSURE_UNIT_MAP = {
    "mmHg": "qudt:MilliM_HG",
}
_LENGTH_UNIT_MAP = {
    "cm": "qudt:CentiM",
}
_SCIDATA_UID = "scidata:jcamp:jsonld"


class UnknownCharacterException(Exception):
    """Exception for unknown character in line of JCAMP-DX file"""


class UnsupportedDataTypeConfigException(Exception):
    """Exception for an unsupported data type configuration for parsing"""


class MultiHeaderKeyException(Exception):
    """Exception for finding multiple header keys in a single line"""


# Compression encoding dictionaries for JCAMP
# Reference found on following site under "Compression Table"
#   - http://wwwchem.uwimona.edu.jm/software/jcampdx.html

# Represents the value with a preceding space (compresses whitespace)
SQZ_digits = {
    '@': '+0',
    'A': '+1',
    'B': '+2',
    'C': '+3',
    'D': '+4',
    'E': '+5',
    'F': '+6',
    'G': '+7',
    'H': '+8',
    'I': '+9',
    'a': '-1',
    'b': '-2',
    'c': '-3',
    'd': '-4',
    'e': '-5',
    'f': '-6',
    'g': '-7',
    'h': '-8',
    'i': '-9',
    '+': '+',  # For PAC
    '-': '-',  # For PAC
    ',': ' ',  # For CSV
}

# Difference agaisnt previous character
DIF_digits = {
    '%': 0,
    'J': 1,
    'K': 2,
    'L': 3,
    'M': 4,
    'N': 5,
    'O': 6,
    'P': 7,
    'Q': 8,
    'R': 9,
    'j': -1,
    'k': -2,
    'l': -3,
    'm': -4,
    'n': -5,
    'o': -6,
    'p': -7,
    'q': -8,
    'r': -9,
}

# Duplicates the previous character by value
DUP_digits = {
    'S': 1,
    'T': 2,
    'U': 3,
    'V': 4,
    'W': 5,
    'X': 6,
    'Y': 7,
    'Z': 8,
    's': 9,
}


def read_jcamp(filename: str) -> SciData:
    """
    Reader for JCAMP-DX files to SciData object
    JCAMP-DX is Joint Committee on Atomic and Molecular Physical Data eXchange
    JCAMP-DX URL:  http://jcamp-dx.org/

    :param filename: Filename to read from for JCAMP-DX files
    :return: SciData object
    """
    # Extract jcamp file data
    with open(filename, 'r') as fileobj:
        jcamp_dict = _reader(fileobj)
    scidata_obj = _read_translate_jcamp_to_scidata(jcamp_dict)
    return scidata_obj


def write_jcamp(filename: str, scidata: SciData):
    """
    Writer for SciData object to JCAMP-DX files.
    JCAMP-DX is Joint Committee on Atomic and Molecular Physical Data eXchange
    JCAMP-DX URL:  http://jcamp-dx.org/

    :param filename: Filename for JCAMP-DX file
    :param scidata: SciData object to write out
    """
    _write_jcamp_header_section(filename, scidata, mode='w')
    _write_jcamp_data_section(filename, scidata, mode='a')
    with open(filename, 'a') as fileobj:
        fileobj.write('##END=\n')


def _reader_is_float(strings: List[str]) -> bool:
    '''
    Test if a string, or list of strings, contains a numeric value(s).

    :param strings: The string or list of strings to test.
    :return: Single boolean or list of boolean values indicating whether
        each input can be converted into float.
    :raises TypeError: If passing a list and elements are not strings or
        single element is not a string
    :raises ValueError: If passing empty list
    '''
    if isinstance(strings, tuple) or isinstance(strings, list):
        if not all(isinstance(i, str) for i in strings):
            raise TypeError("Input {} not a list of strings".format(strings))

        if not strings:
            raise ValueError('Input {} empty'.format(strings))

        bool_list = list(True for i in range(0, len(strings)))
        for i in range(0, len(strings)):
            try:
                float(strings[i])
            except ValueError:
                bool_list[i] = False
        return bool_list

    else:
        if not isinstance(strings, str):
            raise TypeError("Input '%s' is not a string" % (strings))

        try:
            float(strings)
            return True
        except ValueError:
            return False


def _read_parse_dataset_duplicate_characters(line: str) -> str:
    """
    Parse duplicate character compression for a line (i.e. DUP characters).
    Valid DUP characters are: [S, T, U, V, W, X, Y, Z]

    Example: Repeat 9 character 3 times with 'U'
        "9U" == "999"

    Reference found on following site under "Compression Table"
        - http://wwwchem.uwimona.edu.jm/software/jcampdx.html

    :param line: Line in JCAMP-DX file with duplicate characters (DUP)
    :return: Processed line with duplicates added in
    """
    new_line = ""
    for i, char in enumerate(line):
        if (char in DUP_digits):
            # Get number of duplicates to multiply by
            # NOTE: subtract one since we will already have one character from
            #       the original one we are duplicating from.
            nduplicates = DUP_digits[char] - 1
            new_line += line[i-1] * nduplicates
        else:
            new_line += char
    return "".join(new_line)


def _read_num_dif_factory(char: str, line: str) -> Tuple[str, bool]:
    """
    Helper utility factory function to
    :func:`_read_parse_dataset_line_single_x_multi_y` to use the current
    character to give the next numeric value  and flag if we are processing
    using DIF compression.

    :param char: Character we are currently processing.
    :param line: Line we are processing, used for raising exception.
    :return: Tuple of updated values for numeric character (char)
        and DIF flag (bool). Example: ('+1', False)
    :raises UnkownCharacterException: If we find a character that is neither
            a valid compression character or number.
    """
    if char == ' ':
        num = ''
        DIF = False

    elif char in SQZ_digits:
        num = SQZ_digits[char]
        DIF = False

    elif char in DIF_digits:
        num = str(DIF_digits[char])
        DIF = True

    else:
        msg = f"Unknown character {char} encountered in line {line}"
        raise UnknownCharacterException(msg)

    return (num, DIF)


def _read_parse_dataset_line_single_x_multi_y(line: str) -> List[float]:
    """
    Parse a JCAMP data line when using the format '(X++(Y..Y))',
    where we have one X column and multiple Y columns on one line.
    Handles decoding JCAMP compression encoding.

    Reference found on following site under "Compression Table"
        - http://wwwchem.uwimona.edu.jm/software/jcampdx.html

    :param line: Line from JCAMP for data of '(X++(Y..Y))' format
    :return: List of float values for the line
    :raises UnkownCharacterException: If we find a character that is neither
        a valid compression character or number.
    """
    # process the duplicate characters (DUP_digits)
    DUP_set = set(DUP_digits)
    if any(char in DUP_set for char in line):
        line = _read_parse_dataset_duplicate_characters(line)

    DIF = False
    num = ''
    values = []
    for char in line:
        if char.isdigit() or char == '.':
            num += char
            continue

        if num:
            value = float(num)
            if DIF:
                value = float(num) + values[-1]
            values.append(value)

        num, DIF = _read_num_dif_factory(char, line)

    if num:
        value = float(num)
        if DIF:
            value = float(num) + values[-1]
        values.append(value)
    return values


def _read_parse_dataset_line(line: str, data_format: str) -> List[float]:
    """
    Parse a data line of the JCAMP-DX file format for the given data format.
    Handles decoding JCAMP compression encoding.

    Reference found on following site under "Compression Table"
        - http://wwwchem.uwimona.edu.jm/software/jcampdx.html

    :param line: Line in JCAMP-DX file to parse
    :param data_format: Format of data. Choices: ['(XY..XY)', '(X++(Y..Y))']

    :return: List of float values for the line
    """
    if data_format not in _DATA_FORMATS:
        msg = f'Data format {data_format} not supported type: {_DATA_FORMATS}'
        raise UnsupportedDataTypeConfigException(msg)

    if data_format == _DATA_FORMAT_XYXY:
        values = [float(v.strip()) for v in re.split(r"[,;\s]", line) if v]

    if data_format == _DATA_FORMAT_XYYY:
        line = ' '.join(line.split())
        values = _read_parse_dataset_line_single_x_multi_y(line)

    return values


def _read_parse_header(line: str, datastart: bool) -> Tuple[dict, bool]:
    """
    Parse the header line, returning a dictionary for the key-value found
    and if we are starting into the data section.

    :param line: Line to parse as a JCAMP header
    :param datastart: Current boolean flag for if we are in a data section

    :return: Tuple of a header dictionary and datastart boolean.
        Dictionary with header keys found.
        Will mostly return a single key-value pair but
        for some will return multiple pairs

        Example: A compound file will return the extra
            {'children': []} pair when detected.

        Boolean for datastart is updated flag if we are inside a data section
    """
    header_dict = {}

    if line.startswith('##'):
        # Get key-value from header line
        line = line.strip('##')
        (key, value) = line.split('=', 1)
        key = key.strip().lower()
        value = value.strip()

        # Convert 'datatype' key -> _DATA_TYPE_KEY
        if key == 'datatype' or key == 'data type':
            key = _DATA_TYPE_KEY

        # Detect compound files.
        # See table XI in http://www.jcamp-dx.org/protocols/dxir01.pdf
        if (key == _DATA_TYPE_KEY) and (value.lower() == _DATA_LINK):
            header_dict[_CHILDREN] = []

        # Put key-value into JCAMP header dictionary for output
        if value.isdigit():
            header_dict[key] = int(value)
        elif _reader_is_float(value):
            header_dict[key] = float(value)
        else:
            header_dict[key] = value

        # Figure out if we are starting a new data entry
        if (key in _DATA_XY_TYPES):
            datastart = True
            header_dict[_DATA_XY_TYPE_KEY] = value
        elif (key == 'end'):
            datastart = True
        elif datastart:
            datastart = False

    return header_dict, datastart


def _read_parse_header_line(
    line: str, jcamp_dict: dict, datastart: bool = False, last_key: str = None
) -> Tuple[dict, bool, str]:
    """
    Parse the JCAMP header line and update the output JCAMP dictionary.

    :param line: Header line to parse
    :param jcamp_dict: Dictionary currently holding the JCAMP-DX file info
    :param datastart: Boolean that is True if we are inside a data section,
        False if not
    :param last_key: String to store the last key we parsed from the header

    :return: Tuple of the modified JCAMP dictionary, the updated flag for if
        in a data section and the last key entered used for updating a
        multiline comment in the header.

    :raises MultiHeaderKeyException: If multiple header keys parsed
    """
    output_dict = dict(jcamp_dict)
    header_dict, datastart = _read_parse_header(line, datastart)

    # Get the header key, stripping 'children' key if it is a compound file
    remove_keys = (_CHILDREN, _DATA_XY_TYPE_KEY)
    keys = [k for k in header_dict.keys() if k not in remove_keys]
    if len(keys) > 1:
        msg = f'Found multiple header keys: {keys}'
        raise MultiHeaderKeyException(msg)

    # Check if this is a multiline entry in the header
    is_multiline = last_key and not line.startswith('##') and not datastart
    if is_multiline:
        output_dict[last_key] += '\n{}'.format(line.strip())

    # Just do normal update of jcamp w/ header if not multiline
    elif header_dict:
        output_dict.update(header_dict)
        last_key = keys[0]

    return output_dict, datastart, last_key


def _read_post_process_data_xy(
    jcamp_dict: dict,
    x: List[float],
    y: List[float],
    xstart: List[float],
    xnum: List[int]
) -> Tuple[List[float], List[float]]:
    """
    Utility function for _reader to format the XY data in a
    post-process manner after we parse out this data from the file.

    :param jcamp_dict: JCAMP dictionary parsed from file
    :param x: X-axis data
    :param y: Y-axis data
    :param xstart: Starting X-axis values for multi-datasets
    :param xnum: Number of starting X-axis value for multi-datasets
    :return: Post-processed XY data
    """
    if jcamp_dict.get(_DATA_XY_TYPE_KEY) == _DATA_FORMAT_XYYY:
        xstart.append(jcamp_dict['lastx'])
        x = np.array([])
        for n in range(len(xnum)-1):
            dx = (xstart[n+1] - xstart[n]) / xnum[n]
            x = np.append(x, xstart[n]+(dx*np.arange(xnum[n])))

        if (xnum[len(xnum)-1] > 1):
            numerator = (jcamp_dict['lastx'] - xstart[len(xnum)-1])
            denominator = (xnum[len(xnum)-1] - 1.0)
            dx = numerator / denominator

            xnext = xstart[len(xnum)-1]+(dx*np.arange(xnum[len(xnum)-1]))
            x = np.append(x, xnext)
        else:
            x = np.append(x, jcamp_dict['lastx'])

        y = np.array([float(yval) for yval in y])

    else:
        x = np.array([float(xval) for xval in x])
        y = np.array([float(yval) for yval in y])

    if ('xfactor' in jcamp_dict):
        x = x * jcamp_dict['xfactor']
    if ('yfactor' in jcamp_dict):
        y = y * jcamp_dict['yfactor']

    return x, y


def _reader(filehandle: str) -> dict:
    """
    File reader for JCAMP-DX file format

    :param filehandle: JCAMP-DX file to read from
    :return: Dictionary parsed from JCAMP-DX file
    """
    jcamp_dict = dict()
    xstart = []
    xnum = []
    y = []
    x = []
    datastart = False
    in_compound_block = False
    compound_block_contents = []
    last_key = None
    for line in filehandle:
        # Skip blank or comment lines
        if not line.strip():
            continue
        if line.startswith('$$'):
            continue

        # ===================================
        # Detect the start of a compound block
        is_compound = _CHILDREN in jcamp_dict
        if is_compound and line.upper().startswith('##TITLE'):
            in_compound_block = True
            compound_block_contents = [line]
            continue

        # If we are reading a compound block, collect lines into an array to be
        # processed by a recursive call this this function.
        if in_compound_block:
            compound_block_contents.append(line)

            # Detect the end of the compound block.
            if line.upper().startswith('##END'):
                # Process the entire block and put it into the children array.
                jcamp_dict[_CHILDREN].append(_reader(compound_block_contents))
                in_compound_block = False
                compound_block_contents = []
            continue

        # ===================================
        # Parse header line
        jcamp_dict, datastart, last_key = _read_parse_header_line(
            line,
            jcamp_dict,
            datastart=datastart,
            last_key=last_key)

        if datastart and not line.startswith('##'):
            if jcamp_dict.get(_DATA_XY_TYPE_KEY) == _DATA_FORMAT_XYYY:
                datavals = _read_parse_dataset_line(line, _DATA_FORMAT_XYYY)
                xstart.append(float(datavals[0]))
                xnum.append(len(datavals) - 1)
                y.extend([float(f) for f in datavals[1:]])

            elif jcamp_dict.get(_DATA_XY_TYPE_KEY) == _DATA_FORMAT_XYXY:
                datavals = _read_parse_dataset_line(line, _DATA_FORMAT_XYXY)
                x.extend(datavals[0::2])
                y.extend(datavals[1::2])

            else:
                msg = f"Unable to parse data: {jcamp_dict[_DATA_XY_TYPE_KEY]}"
                raise UnsupportedDataTypeConfigException(msg)

    # ===================================
    x, y = _read_post_process_data_xy(jcamp_dict, x, y, xstart, xnum)
    jcamp_dict['x'] = list(x)
    jcamp_dict['y'] = list(y)

    return jcamp_dict


def _read_get_description(jcamp_dict: dict, keywords: List[str]) -> str:
    """
    Utility function to create a description string from the JCAMP
    dictionary

    :param jcamp_dict: JCAMP-DX dictionary extracted from read
    :return: String for the description for SciData object
    """
    description_lines = []
    for key in keywords:
        if key in jcamp_dict:
            value = jcamp_dict.get(key)
            description_lines.append(f'{key.upper()}: {value}')

    return _DESCRIPTION_KEY_SPLIT_CHAR.join(description_lines)


def _read_get_graph_source_citation_section(jcamp_dict: dict) -> List[str]:
    """
    Extract and translate from the JCAMP-DX dictionary the SciData JSON-LD
    citations in the 'sources' section from the '@graph' scection.

    :param jcamp_dict: JCAMP-DX dictionary to extract citations from
    :return: List for citation from SciData JSON-LD
    """
    citation = []
    if "$ref author" in jcamp_dict:
        citation.append(f'{jcamp_dict["$ref author"]} :')
    if "$ref title" in jcamp_dict:
        citation.append(f'{jcamp_dict["$ref title"]}.')
    if "$ref journal" in jcamp_dict:
        citation.append(f'{jcamp_dict["$ref journal"]}')
    if "$ref volume" in jcamp_dict:
        citation.append(f'{jcamp_dict["$ref volume"]}')
    if "$ref date" in jcamp_dict:
        citation.append(f'({jcamp_dict["$ref date"]})')
    if "$ref page" in jcamp_dict:
        citation.append(f'{jcamp_dict["$ref page"]}')
    return citation


def _read_get_graph_source_section(jcamp_dict: dict) -> List[dict]:
    """
    Extract and translate from the JCAMP-DX dictionary the SciData JSON-LD
    'sources' section from the '@graph' scection.

    :param jcamp_dict: JCAMP-DX dictionary to extract sources section from
    :return: List for 'sources' section of SciData JSON-LD from translation
    """
    sources = []

    citation = _read_get_graph_source_citation_section(jcamp_dict)
    if citation:
        sources.append({
            "@id": f'source/{len(sources) + 1}',
            "@type": "dc:source",
            "citation": ' '.join(citation),
            "reftype": "journal article",
            "doi": "",
            "url": ""
        })

    if "source reference" in jcamp_dict:
        sources.append({
            "@id": f'source/{len(sources) + 1}',
            "@type": "dc:source",
            "citation": jcamp_dict.get("source reference"),
        })

    if "$nist source" in jcamp_dict or "$nist image" in jcamp_dict:

        nist_citation = []

        if "$nist source" in jcamp_dict:
            nist_source = f'NIST SOURCE: {jcamp_dict.get("$nist source")}'
            nist_citation.append(nist_source)

        if "$nist image" in jcamp_dict:
            nist_image = f'NIST IMAGE: {jcamp_dict.get("$nist image")}'
            nist_citation.append(nist_image)

        nist_string = ', '.join(nist_citation)
        sources.append({
            "@id": f'source/{len(sources) + 1}',
            "@type": "dc:source",
            "citation": nist_string,
        })

    return sources


def _read_get_aspects_section(jcamp_dict: dict) -> dict:
    """
    Extract and translate from the JCAMP-DX dictionary the SciData JSON-LD
    'aspects' sub-ection of the 'methodology' section

    :param jcamp_dict: JCAMP-DX dictionary to extract aspects section from
    :return: The 'aspects' section of SciData JSON-LD methodology
    """
    measurement = {}
    if "spectrometer/data system" in jcamp_dict:
        measurement = {
            "@id": "measurement/1",
            "@type": "sdo:measurement",
            "techniqueType": "cao:spectroscopy",
            "instrument":  f'{jcamp_dict.get("spectrometer/data system")}',
        }

    settings = []
    if "instrument parameters" in jcamp_dict:
        settings.append({
            "@id": f'setting/{len(settings) + 1}',
            "@type": "sdo:setting",
            "property": "instrument parameters",
            "value": {
                "@id": f'setting/{len(settings) + 1}/value',
                "number": jcamp_dict.get("instrument parameters"),
            }
        })

    if "path length" in jcamp_dict:
        pl_value = jcamp_dict.get("path length").split(" ")[0]
        pl_unit = jcamp_dict.get("path length").split(" ")[1]
        pl_unitref = _LENGTH_UNIT_MAP.get(pl_unit.lower())
        settings.append({
            "@id": f'setting/{len(settings) + 1}',
            "@type": "sdo:setting",
            "quantity": "length",
            "property": "path length",
            "value": {
                "@id": f'setting/{len(settings) + 1}/value',
                "number": pl_value,
                "unitref": pl_unitref,
            }
        })

    if "resolution" in jcamp_dict:
        settings.append({
            "@id": f'setting/{len(settings) + 1}',
            "@type": "sdo:setting",
            "quantity": "resolution",
            "property": "resolution",
            "value": {
                "@id": f'setting/{len(settings) + 1}/value',
                "number": jcamp_dict.get("resolution"),
            }
        })

    if settings:
        measurement["settings"] = settings

    aspects = []
    if measurement:
        aspects.append(measurement)
    if "sampling procedure" in jcamp_dict:
        sampling_procedure = {
            "@id": "procedure/1",
            "@type": "sdo:procedure",
            "description": jcamp_dict.get("sampling procedure")
        }
        aspects.append(sampling_procedure)
    if "data processing" in jcamp_dict:
        data_processing_procedure = {
            "@id": "resource/1",
            "@type": "sdo:resource",
            "description": jcamp_dict.get("data processing")
        }
        aspects.append(data_processing_procedure)

    return aspects


def _read_get_facets_section(jcamp_dict: dict) -> dict:
    """
    Extract and translate from the JCAMP-DX dictionary the SciData JSON-LD
    'facets' sub-section of the 'system' section

    :param jcamp_dict: JCAMP-DX dictionary to extract facets section from
    :return: The 'facets' section of SciData JSON-LD from translation
    """
    facets = []

    compound_dict = {}
    if "molform" in jcamp_dict or "cas registry no" in jcamp_dict:
        compound_dict = {
            "@id": "compound/1",
            "@type": ["sdo:facet", "sdo:material"],
            "name": jcamp_dict.get("title", "")
        }
        if "molform" in jcamp_dict:
            compound_dict.update({"formula": jcamp_dict.get("molform")})
        if "cas registry no" in jcamp_dict:
            compound_dict.update({"casrn": jcamp_dict.get("cas registry no")})
        facets.append(compound_dict)

    substances_dict = {}
    if "state" in jcamp_dict:
        substances_dict = {
            "@id": "substance/1",
            "@type": ["sdo:constituent"],
            "name": jcamp_dict.get("title", ""),
            "phase": jcamp_dict.get("state", "")
        }
        facets.append(substances_dict)

    if "partial_pressure" in jcamp_dict:
        pp_value = jcamp_dict.get("partial_pressure").split(" ")[0]
        pp_unit = jcamp_dict.get("partial_pressure").split(" ")[1]
        pp_unitref = _PRESSURE_UNIT_MAP.get(pp_unit)
        condition_dict = {
            "@id": "condition/1",
            "@type": ["sdo:condition"],
            "quantity": "pressure",
            "property": "Partial pressure",
            "value": {
                "@id": "condition/1/value",
                "@type": "sdo:value",
                "number": pp_value,
                "unitref": pp_unitref
            }
        }

        facets.append(condition_dict)

    return facets


def _read_get_datagroup_subsection(jcamp_dict: dict) -> List[dict]:
    """
    Extract and translate from the JCAMP-DX dictionary the SciData JSON-LD
    'dataset' section's datagroup

    :param jcamp_dict: JCAMP-DX dictionary to extract
        dataset section's datagroup from
    :return: The 'dataset' section's datagroup of
        SciData JSON-LD from translation
    """
    # Convert from JCAMP units -> SciData JSON-LD unitref
    xunits = jcamp_dict.get("xunits", "")
    xunitref = _XUNIT_MAP.get(xunits, "")
    yunitref = jcamp_dict.get("yunits", "")

    # Values for attributes
    atid = 'numericvalue'
    x = jcamp_dict['x']

    count = {'@id': atid, 'number': str(len(x)), 'unitref': xunitref}

    xfirst = {'@id': atid, 'number': str(x[0]), 'unitref': xunitref}
    xlast = {'@id': atid, 'number': str(x[-1]), 'unitref': xunitref}
    xmin = {'@id': atid, 'number': str(min(x)), 'unitref': xunitref}
    xmax = {'@id': atid, 'number': str(max(x)), 'unitref': xunitref}
    xfactor = {
        '@id': atid,
        'number': str(jcamp_dict.get("xfactor", "1")),
        'unitref': xunitref
    }

    y = jcamp_dict['y']
    yfirst = {'@id': atid, 'number': str(y[0]), 'unitref': yunitref}
    ylast = {'@id': atid, 'number': str(y[-1]), 'unitref': yunitref}
    ymin = {'@id': atid, 'number': str(min(y)), 'unitref': yunitref}
    ymax = {'@id': atid, 'number': str(max(y)), 'unitref': yunitref}
    yfactor = {
        '@id': atid,
        'number': str(jcamp_dict.get("yfactor", "1")),
        'unitref': yunitref
    }

    # Attributes
    attr_count = {
        "@id": "attribute",
        "quantity": "count",
        "property": "Number of Data Points",
        "value": count,
    }
    attr_xfirst = {
        "@id": "attribute",
        "property": "First X-axis Value",
        "value": xfirst,
    }
    attr_xlast = {
        "@id": "attribute",
        "property": "Last X-axis Value",
        "value": xlast,
    }
    attr_xmin = {
        "@id": "attribute",
        "property": "Minimum X-axis Value",
        "value": xmin,
    }
    attr_xmax = {
        "@id": "attribute",
        "property": "Maximum X-axis Value",
        "value": xmax,
    }
    attr_xfactor = {
        "@id": "attribute",
        "property": "X-axis Scaling Factor",
        "value": xfactor,
    }

    attr_yfirst = {
        "@id": "attribute",
        "property": "First Y-axis Value",
        "value": yfirst,
    }
    attr_ylast = {
        "@id": "attribute",
        "property": "Last Y-axis Value",
        "value": ylast,
    }
    attr_ymin = {
        "@id": "attribute",
        "property": "Minimum Y-axis Value",
        "value": ymin,
    }
    attr_ymax = {
        "@id": "attribute",
        "property": "Maximum X-axis Value",
        "value": ymax,
    }
    attr_yfactor = {
        "@id": "attribute",
        "property": "Y-axis Scaling Factor",
        "value": yfactor,
    }

    # Create data group
    datagroup = {
        "@id": "datagroup/1",
        "type": "sdo:datagroup",
        "attribute": [
            attr_count,
            attr_xfirst,
            attr_xlast,
            attr_xmin,
            attr_xmax,
            attr_xfactor,
            attr_yfirst,
            attr_ylast,
            attr_ymin,
            attr_ymax,
            attr_yfactor,
        ]
    }
    return datagroup


# TODO: add the dataseries
#   Issue: https://github.com/ChalkLab/SciDataLib/issues/43
def _read_get_dataseries_subsection(jcamp_dict: dict) -> List[dict]:
    """
    Extract and translate from the JCAMP-DX dictionary the SciData JSON-LD
    'dataset' section's dataseries

    :param jcamp_dict: JCAMP-DX dictionary to extract dataset section's
        dataseries from
    :return: The 'dataset' section's dataseries of SciData
    """
    xunits = jcamp_dict.get("xunits", "")
    xunitref = _XUNIT_MAP.get(xunits)

    dataseries = [
        {
            "@id": "dataseries/1/",
            "@type": "sdo:independent",
            "label": "Wave Numbers (cm^-1)",
            "axis": "x-axis",
            "parameter": {
                "@id": "dataseries/1/parameter/",
                "@type": "sdo:parameter",
                "quantity": "wavenumbers",
                "property": "Wave Numbers",
                "valuearray": {
                    "@id": "dataseries/1/parameter/valuearray/",
                    "@type": "sdo:valuearray",
                    "datatype": "decimal",
                    "numberarray": jcamp_dict['x'],
                    "unitref": xunitref,
                }
            }
        },
        {
            "@id": "dataseries/2/",
            "@type": "sdo:dependent",
            "label": "Intensity (Arbitrary Units)",
            "axis": "y-axis",
            "parameter": {
                "@id": "dataseries/2/parameter/",
                "@type": "sdo:parameter",
                "quantity": "intensity",
                "property": "Intensity",
                "valuearray": {
                    "@id": "dataseries/2/parameter/valuearray/",
                    "@type": "sdo:valuearray",
                    "datatype": "decimal",
                    "numberarray": jcamp_dict['y']
                }
            }
        }
    ]

    return dataseries


def _read_translate_jcamp_to_scidata(jcamp_dict: dict) -> SciData:
    """
    Main translation of JCAMP-DX to SciData JSON-LD

    :param jcamp_dict: JCAMP-DX dictionary extracted from read
    :return: SciData object from translation
    """
    scidata = SciData(_SCIDATA_UID)

    # Add champ namespace for aspect techniqueType
    cao = {"cao": "http://champ-project.org/images/ontology/cao.owl#"}
    scidata.namespaces(cao)

    # Title and publisher
    scidata.title(jcamp_dict.get("title", ""))
    scidata.publisher(jcamp_dict.get("origin", ""))

    # Date and time
    today_date = datetime.today().strftime("%m-%d-%y")
    today_time = datetime.today().strftime("%H:%M:%S")
    jcamp_date = jcamp_dict.get("date", today_date)
    jcamp_time = jcamp_dict.get("time", today_time)
    scidata.starttime(f'{jcamp_date} {jcamp_time}')

    # Description
    description_keywords = [
        "jcamp-dx",
        "class",
        "cas registry no",
        "sample description",
        "xydata"
    ]
    description = _read_get_description(jcamp_dict, description_keywords)
    scidata.description(description)

    # Authors
    authors = []
    author_keywords = ["owner", "$ref author"]
    for author_keyword in author_keywords:
        if author_keyword in jcamp_dict:
            authors.append({
                "@id": "author/{}".format(len(authors) + 1),
                "@type": "dc:creator",
                "name": jcamp_dict[author_keyword]
            })
    scidata.author(authors)

    # Sources / references
    sources = _read_get_graph_source_section(jcamp_dict)
    if sources:
        scidata.sources(sources)

    # Discipline and sub-discipline
    scidata.discipline("w3i:Chemistry")
    scidata.subdiscipline("w3i:AnalyticalChemistry")

    # Methodology - aspects
    scidata.aspects(_read_get_aspects_section(jcamp_dict))

    # System - facets
    scidata.facets(_read_get_facets_section(jcamp_dict))

    # Dataset
    scidata.scope("material/1")
    datagroup = _read_get_datagroup_subsection(jcamp_dict)
    scidata.datagroup([datagroup])

    # TODO: add the dataseries
    #   Issue: https://github.com/ChalkLab/SciDataLib/issues/43

    return scidata


def _write_extract_description_section(description: str, key: str) -> str:
    """
    Given a description string of the form "KEY1: VALUE1, KEY2: VALUE2, ..."
    extract the KEY that matches input key and extract the VALUE

    :param desc: The description of form "KEY1: VALUE1, KEY2: VALUE2, ..."
    :param key: The key used to extract value from the description
    :return: String of the VALUE extracted from description for the key
        provided. None is returned if key is not in the description.
    """
    desc_list = description.split(_DESCRIPTION_KEY_SPLIT_CHAR)
    results = [x for x in desc_list if x.strip().startswith(key)]
    if not results:
        return None
    element = results[0]
    value = element.split(':')[1].strip()
    return value


def _write_add_header_lines_general(scidata: SciData) -> List[str]:
    """
    Get the general graph header lines from the SciData object
    used to write the JCAMP-DX header lines

    :param scidata: SciData object to write as JCAMP-DX file
    :return: List of header lines to write to the JCAMP-DX file
    """
    graph = scidata.output.get("@graph")
    description = graph.get("description", "")
    jcamp_dx = _write_extract_description_section(description, "JCAMP-DX")
    lines = []
    lines.append(f'##JCAMP-DX={jcamp_dx}')
    if "property" in graph["scidata"]:
        lines.append(f'##DATA TYPE={graph["scidata"]["property"][0]}')
    if "publisher" in graph:
        lines.append(f'##ORIGIN={graph["publisher"]}')
    if "authors" in graph:
        lines.append(f'##OWNER={graph["authors"][0]["name"]}')

    date_and_time = None
    if "starttime" in graph:
        date_and_time = graph.get("starttime").split(" ")
    elif "generatedAt" in scidata.output:
        date_and_time = scidata.output.get("generatedAt").split(" ")

    if date_and_time:
        date = date_and_time[0].strip()
        lines.append(f'##DATE={date}')

    if len(date_and_time) > 1:
        time = date_and_time[1].strip()
        lines.append(f'##TIME={time}')

    the_class = _write_extract_description_section(description, "CLASS")
    if the_class:
        lines.append(f'##CLASS={the_class}')

    sources = graph.get("sources")
    if sources:
        citation = graph.get("sources")[0]["citation"]
        lines.append(f'##SOURCE REFERENCE={citation}')

        for source in sources:
            nist_description = source.get("citation", "")
            if nist_description.startswith("NIST"):
                nist_source = _write_extract_description_section(
                    nist_description,
                    "NIST SOURCE")
                lines.append(f'##$NIST SOURCE={nist_source}')

                nist_image = _write_extract_description_section(
                    nist_description,
                    "NIST IMAGE")
                lines.append(f'##$NIST IMAGE={nist_image}')

    return '\n'.join(lines)


def _write_add_header_lines_methodology(scidata: SciData) -> List[str]:
    """
    Get the methodology header lines from the SciData object
    used to write the JCAMP-DX header lines

    :param scidata: SciData object to write as JCAMP-DX file
    :return: List of header lines to write to the JCAMP-DX file
    """
    lines = []
    graph = scidata.output.get("@graph")
    methodology = graph.get("scidata").get("methodology")

    # Aspects
    aspects = methodology.get("aspects")
    measurement = ""
    for aspect in aspects:
        if aspect.get("@id").startswith("procedure"):
            lines.append(f'##SAMPLING PROCEDURE={aspect["description"]}')

        if aspect.get("@id").startswith("resource"):
            lines.append(f'##DATA PROCESSING={aspect["description"]}')

        if aspect.get("@id").startswith("measurement"):
            measurement = aspect
            instrument = measurement.get("instrument")
            lines.append(f'##SPECTROMETER/DATA SYSTEM={instrument}')

    # Settings
    settings = measurement.get("settings", "")
    for setting in settings:
        if setting.get("property").startswith("instrument parameters"):
            parameters = setting["value"]["number"]
            lines.append(f'##INSTRUMENT PARAMETERS={parameters}')
        if setting.get("property").startswith("path length"):
            reverse_length_map = {v: k for k, v in _LENGTH_UNIT_MAP.items()}
            scidata_path_unit = settings[1]["value"]["unitref"]
            jcamp_path_unit = reverse_length_map[scidata_path_unit]
            path_length = f'{settings[1]["value"]["number"]} '
            path_length += f'{jcamp_path_unit.upper()}'
            lines.append(f'##PATH LENGTH={path_length}')
        if setting.get("property").startswith("resolution"):
            resolution = setting["value"]["number"]
            lines.append(f'##RESOLUTION={resolution}')

    return '\n'.join(lines)


def _write_add_header_lines_system(scidata: SciData) -> List[str]:
    """
    Get the system header lines from the SciData object
    used to write the JCAMP-DX header lines

    :param scidata: SciData object to write as JCAMP-DX file
    :return: List of header lines to write to the JCAMP-DX file
    """
    lines = []
    graph = scidata.output.get("@graph")
    system = graph.get("scidata").get("system", False)

    # Facets
    if system:
        facets = system.get("facets", False)
        if facets:
            for facet in facets:
                if facet.get("@id").startswith("compound"):
                    if "casrn" in facet:
                        lines.append(f'##CAS REGISTRY NO={facet["casrn"]}')

                    if "formula" in facet:
                        lines.append(f'##MOLFORM={facet["formula"]}')

                if facet.get("@id").startswith("substance"):
                    if "phase" in facet:
                        lines.append(f'##STATE={facet["phase"]}')

                if facet.get("@id").startswith("condition"):
                    items = _PRESSURE_UNIT_MAP.items()
                    reverse_pressure_map = {v: k for k, v in items}
                    scidata_punit = facet["value"]["unitref"]
                    jcamp_punit = reverse_pressure_map[scidata_punit]
                    partial_pressure = f'{facet["value"]["number"]} '
                    partial_pressure += f'{jcamp_punit}'
                    lines.append(f'##PARTIAL_PRESSURE={partial_pressure}')

    return '\n'.join(lines)


def _write_add_header_lines_dataset(scidata: SciData) -> List[str]:
    """
    Get the dataset header lines from the SciData object
    used to write the JCAMP-DX header lines

    :param scidata: SciData object to write as JCAMP-DX file

    :return: List of header lines to write to the JCAMP-DX file
    """
    lines = []

    graph = scidata.output.get("@graph")
    dataset = graph.get("scidata").get("dataset", False)

    if dataset:
        attributes = dataset.get("attribute", False)

        reverse_xunit_map = {v: k for k, v in _XUNIT_MAP.items()}
        scidata_xunits = attributes[0]["value"]["unitref"]
        xunits = reverse_xunit_map[scidata_xunits]

        scidata_yunits = attributes[0]["value"]["unitref"]
        yunits = scidata_yunits

        npoints = attributes[0]["value"]["number"]

        first_x = attributes[1]["value"]["number"]
        last_x = attributes[2]["value"]["number"]
        min_x = attributes[3]["value"]["number"]
        max_x = attributes[4]["value"]["number"]
        xfactor = attributes[5]["value"]["number"]

        first_y = attributes[6]["value"]["number"]
        # last_y = attributes[7]["value"]["number"]
        min_y = attributes[8]["value"]["number"]
        max_y = attributes[9]["value"]["number"]
        yfactor = attributes[10]["value"]["number"]
        yunits = attributes[5]["value"]["unitref"]
        delta_x = (float(last_x) - float(first_x)) / (float(npoints) - 1)

        lines.append(f'##XUNITS={xunits}')
        lines.append(f'##YUNITS={yunits}')
        lines.append(f'##XFACTOR={xfactor}')
        lines.append(f'##YFACTOR={yfactor}')
        lines.append(f'##DELTAX={delta_x:.6f}')
        lines.append(f'##FIRSTX={first_x}')
        lines.append(f'##LASTX={last_x}')
        lines.append(f'##FIRSTY={first_y}')
        lines.append(f'##MAXX={max_x}')
        lines.append(f'##MINX={min_x}')
        lines.append(f'##MAXY={max_y}')
        lines.append(f'##MINY={min_y}')
        lines.append(f'##NPOINTS={npoints}')

        description = graph.get("description")
        xydata = _write_extract_description_section(description, "XYDATA")
        lines.append(f'##XYDATA={xydata}')

    return '\n'.join(lines)


def _write_jcamp_header_section(
    filename: str, scidata: SciData, mode: str = 'w'
):
    """
    Writes header of the JCAMP-DX file for given SciData object
    to the filename provided. Default mode is to overwrite the file.

    :param filename: String name of file to write JCAMP header
    :param scidata: SciData object to extract header info
    :param mode: File mode to use (i.e. 'w' for overwrite, 'a' for append, ...)
    """
    lines = []

    graph = scidata.output.get("@graph")
    lines.append(f'##TITLE={graph.get("title")}')

    headers = [
        _write_add_header_lines_general(scidata),
        _write_add_header_lines_methodology(scidata),
        _write_add_header_lines_system(scidata),
        _write_add_header_lines_dataset(scidata),
    ]
    for header in headers:
        if header:
            lines.append(header)
    lines = '\n'.join(lines) + '\n'

    with open(filename, mode) as fileobj:
        for line in lines:
            fileobj.write(line)


def _write_jcamp_data_section(
    filename: str,
    scidata: SciData,
    mode: str = 'w',
    precision: int = 3,
    trim: int = None,
):
    """
    Writes dataset section of the JCAMP-DX file for given SciData object
    to the filename provided. Default mode is to overwrite the file.

    :param filename: String name of file to write JCAMP header
    :param scidata: SciData object to extract dataset info
    :param mode: File mode to use (i.e. 'w' for overwrite, 'a' for append, ...)
    :param precision: Floating point number for formatting the output data
    """
    pass
    # TODO: add the dataseries
    #   Issue: https://github.com/ChalkLab/SciDataLib/issues/43
    '''
    graph = scidata.output.get("@graph")
    dataset = graph.get("scidata").get("dataset")
    dataseries = dataset.get("dataseries")
    with open(filename, mode) as fileobj:
        xdata = []
        ydata = []
        for data in dataseries:
            if data.get("axis") == "x-axis":
                xdata = data["parameter"]["valuearray"]["numberarray"]
            if data.get("axis") == "y-axis":
                ydata = data["parameter"]["valuearray"]["numberarray"]

        for x, y in zip(xdata, ydata):
            line = f' {x:.{precision}f},   {y:.{precision}f}'
            if trim:
                xline = f'{x:.{precision}f}'[0:trim]
                yline = f'{y:.{precision}f}'[0:trim]
                line = f' {xline},   {yline}'
            fileobj.write(f'{line}\n')
    '''
