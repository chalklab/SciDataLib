# SciDataLib

| Health | Releases |
|--------|----------|
| [![GitHub Actions](https://github.com/ChalkLab/SciDataLib/actions/workflows/actions.yml/badge.svg?branch=master)](https://github.com/ChalkLab/SciDataLib/actions/workflows/actions.yml) | [![PyPI version](https://badge.fury.io/py/SciDataLib.svg)](https://badge.fury.io/py/SciDataLib) |
| [![codecov](https://codecov.io/gh/ChalkLab/SciDataLib/branch/master/graph/badge.svg)](https://codecov.io/gh/ChalkLab/SciDataLib) | [![DOI](https://zenodo.org/badge/219040010.svg)](https://zenodo.org/badge/latestdoi/219040010) |

A Python library writing [SciData](http://stuchalk.github.io/scidata/) [JSON-LD](https://json-ld.org/) files.

# SciData and JSON-LD

JSON-LD is a convenient (human-readable) encoding of Resource
Desctiption Framework (RDF) triples.  However, unlike traditional
relational databases (e.g., MySQL), the graph has no schema. This
is problematic as including data from different sources results
in a system with no common way to search across the data.  The
SciData framework is a structure for users to add data and its metadata
that are organized in the graph through the associated SciData ontology.

There are three main sections of the SciData framework:
- the methodology section (describing how the research was done)
- the system section (describing what the research studied and the conditions)
- the dataset section (the experimental data, plus any derived or supplemental data)

The methodology and system sections are generic and users can add any data
they need to contextualize the dataset.  However, in addition they must
provide a JSON-LD context file to semantically describe the data elements
included.  The dataset section has predefined data structures (dataseries,
datagroup, and datapoint) although other strudtures can be included
if needed.

Translating the content in JSON-LD.  Referencing the JSON-LD below:
- '@context': provides resources that define the context (meaning) of 
  data elements in the document (as a JSON array). It consists of three sections:
    - a list of one or more 'context' files
    - a JSON object containing one or more definitions of namespaces
    used in the document
    - a JSON object with one entry '@base' that defines the base URL
    to be prepended to all internal references (i.e. '@id' entries)
- root level '@id': the 'name' of the file and where ingested into a
graph database, the graph name
- '@graph': the definition of content that will be represented as triples
and identified by the graph name (this is therfore a 'quad')
- '@id' under '@graph': the identifier for the graph.  The scidatalib
code uses the '@base' to populate this, so they are consistent. As a result,
  all node identifiers '@id's in the document are globally unique because the
  '@base' is unique.

```json
{
  "@context": [
    "https://stuchalk.github.io/scidata/contexts/scidata.jsonld",
    {
      "sci": "https://stuchalk.github.io/scidata/ontology/scidata.owl#"
    },
    {
      "@base": "https://my.research.edu/<uniqueid>/"
    }
  ],
  "@id": "file_identifier",
  "generatedAt": "<automatically added",
  "version": "1",
  "@graph": {
    "@id": "https://my.research.edu/<uniqueid>/",
    "@type": "sdo:scidataFramework",
    "uid": "<uniqueid>",
    "scidata": {
      "@type": "sdo:scientificData",
      "methodology": {
        "@id": "methodology/",
        "@type": "sdo:methodology",
        "aspects": []
      },
      "system": {
        "@id": "system/",
        "@type": "sdo:system",
        "facets": []
      },
      "dataset": {
        "@id": "dataset/",
        "@type": "sdo:dataset",
        "dataseries": [],
        "datagroup": [],
        "datapoint": []
      }
    }
  }
}
```


# Installation

### Using pip
```
pip install scidatalib
```

### Manual (from source)
Clone the repository either via:
 - HTTP:
```
git clone https://github.com/ChalkLab/SciDataLib.git
```
 - SSH:
```
git clone git@github.com:ChalkLab/SciDataLib.git
```

Create a virtual environment and activate to install the package in the isolated environment:
```
python -m venv <name of env>
source <env>/bin/activate
```

To [install the package from the local source tree into the environment](
https://packaging.python.org/tutorials/installing-packages/#installing-from-a-local-src-tree), run:
```
python -m pip install .
```

Or to do so in ["Development Mode"](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode), 
you can run:
```
python -m pip install -e .
```

To deactivate the virtual environment
```
deactivate
```

When finished, remove the virtual environment by deleting the directory:
```
rm -rf <name of env>
```

# Usage

SciDataLib consists of both a command line interface (CLI)
and a library for constructing and modifying SciData JSON-LD files

### Command Line Interface

The CLI tool is `scidatalib`.
You can use it to create SciData JSON-LD files
via specifying an output JSON-LD filename
and additional options to create the content of the file.

Example to create "bare" SciData JSON-LD file:
```
scidatalib output.jsonld
```

You can access the additional functionality via the `--help` option:
```
scidatalib --help
```

### SciDataLib library
After installation, import the `SciData` class to start creating SciData JSON-LD:
```python
from scidatalib.scidata import SciData
```

Example:
```python
from scidatalib.scidata import SciData
import json

uid = 'chalk:example:jsonld'
example = SciData(uid)

# context parameters
base = 'https://scidata.unf.edu/' + uid + '/'
example.base(base)

# print out the SciData JSON-LD for example
print(json.dumps(example.output, indent=2))
```

**Output**:
```json
{
  "@context": [
    "https://stuchalk.github.io/scidata/contexts/scidata.jsonld",
    {
      "sci": "https://stuchalk.github.io/scidata/ontology/scidata.owl#",
      "sub": "https://stuchalk.github.io/scidata/ontology/substance.owl#",
      "chm": "https://stuchalk.github.io/scidata/ontology/chemical.owl#",
      "w3i": "https://w3id.org/skgo/modsci#",
      "qudt": "http://qudt.org/vocab/unit/",
      "obo": "http://purl.obolibrary.org/obo/",
      "dc": "http://purl.org/dc/terms/",
      "xsd": "http://www.w3.org/2001/XMLSchema#"
    },
    {
      "@base": "https://scidata.unf.edu/chalk:example:jsonld/"
    }
  ],
  "@id": "",
  "generatedAt": "",
  "version": "",
  "@graph": {
    "@id": "",
    "@type": "sdo:scidataFramework",
    "uid": "chalk:example:jsonld",
    "scidata": {
      "@type": "sdo:scientificData",
      "discipline": "",
      "subdiscipline": "",
      "dataset": {
        "@id": "dataset/",
        "@type": "sdo:dataset"
      }
    }
  }
}
```

# Development

### Install using poetry
Install via [poetry](https://python-poetry.org/) with dev dependencies:
```
poetry install
```

Then, run commands via poetry:
```
poetry run python -c "import scidatalib"
```

### CLI

Run the CLI in using poetry via:
```
poetry install
poetry run scidatalib --help
```

### Tests / Linting

#### Flake8 linting
Run linting over the package with [flake8](https://flake8.pycqa.org/en/latest/) via:
```
poetry run flake8 --count
```

#### Pytest testing
Run tests using [pytest](https://docs.pytest.org/en/stable/):
```
poetry run pytest tests/
```

#### Code coverage

Get code coverage reporting using the [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) plugin:
```
poetry run pytest --cov=scidatalib --cov-report=term-missing tests/
```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# Links
* SciData Research Paper: [https://doi.org/10.1186/s13321-016-0168-9](https://doi.org/10.1186/s13321-016-0168-9)
* SciData Project Website: [http://stuchalk.github.io/scidata/](http://stuchalk.github.io/scidata/) 
* SciData Project GitHub Repository: [https://github.com/stuchalk/scidata](https://github.com/stuchalk/scidata)

# Licensing
[MIT](https://choosealicense.com/licenses/mit/)
