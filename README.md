# SciDataLib
Python library for development of [SciData](http://stuchalk.github.io/scidata/) [JSON-LD](https://json-ld.org/) files

# Installation

### Using pip
*coming soon*!!!

### Manual (from source)
Clone the repository either via:
 - HTTP:
```
git clone git@github.com:ChalkLab/SciDataLib.git
```
 - SSH:
```
git clone https://github.com/ChalkLab/SciDataLib.git
```

Create a virtual environment and activate to install the package in the isolated environment:
```
python -m venv <name of env>
source <env>/bin/activate
```

To [install the package from the local source tree into the environment](https://packaging.python.org/tutorials/installing-packages/#installing-from-a-local-src-tree), run:
```
python -m pip install .
```

Or to do so in ["Development Mode"](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode), you can run:
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
After installation, import the `SciData` class to start creating SciData JSON-LD:
```python
from SciDataLib.SciData import SciData
```

Example:
```python
from SciDataLib.SciData import SciData
import json

uid = 'chalk:example:jsonld'
example = SciData(uid)

# context parameters
base = 'https://scidata.unf.edu/' + uid + '/'
example.add_base(base)

# print out the SciData JSON-LD for example
print(json.dumps(example.output, indent=2))
```

**Output**:
```python
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
poetry run python -c "import SciDataLib"
```

### Tests / Linting

#### Flake8 linting
Run linting over the package with [flake8](https://flake8.pycqa.org/en/latest/) via:
```
poetry run flake8 SciDataLib/ tests/
```

#### Pytest testing
Run tests using [pytest](https://docs.pytest.org/en/stable/):
```
poetry run pytest tests/
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