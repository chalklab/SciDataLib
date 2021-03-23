import json
from scidatalib.cli import cli


def test_scidatalib_cli(tmp_path):
    filename = tmp_path / "output.jsonld"
    args = [filename.absolute().name]
    cli(args)

    with open(filename.absolute().name, 'r') as f:
        jsonld = json.load(f)

    assert '@context' in jsonld
