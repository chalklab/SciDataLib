import json
from scidatalib.cli import cli


def test_scidatalib_cli(tmp_path):
    """Test for CLI 'bare' scidata jsonld"""
    output_dir = tmp_path / "scidatalib_cli"
    output_dir.mkdir()
    filename = output_dir / "output.jsonld"
    args = [str(filename.resolve())]
    cli(args)

    with open(filename.resolve(), 'r') as f:
        jsonld = json.load(f)

    assert '@context' in jsonld
    assert '@id' in jsonld
    assert 'generatedAt' in jsonld
    assert 'version' in jsonld
    assert '@graph' in jsonld

    graph = jsonld.get('@graph')
    assert '@type' in graph
    assert graph.get('@type') == 'sdo:scidataFramework'
    assert 'uid' in graph
    assert graph.get('uid') == 'example'
    assert 'scidata' in graph

    scidata = graph.get('scidata')
    assert '@type' in scidata
    assert scidata.get('@type') == 'sdo:scientificData'
    assert 'dataset' in scidata

    dataset = scidata.get('dataset')
    assert '@id' in dataset
    assert dataset.get('@id') == "dataset/"
    assert '@type' in dataset
    assert dataset.get('@type') == "sdo:dataset"


def test_scidatalib_cli_uid(tmp_path):
    """Test for CLI changing UID"""
    filename = tmp_path / "output.jsonld"
    uid = "new_example"
    args = [str(filename.resolve()), "--uid", uid]
    cli(args)

    with open(filename.resolve(), 'r') as f:
        jsonld = json.load(f)

    assert jsonld.get('@graph').get('uid') == uid


def test_scidatalib_cli_indent(tmp_path):
    """Test for CLI to change indent (basic check)"""
    filename = tmp_path / "output.jsonld"
    args = [str(filename.resolve()), "--indent", "1"]

    cli(args)

    with open(filename.resolve(), 'r') as f:
        jsonld = json.load(f)

    assert '@context' in jsonld
