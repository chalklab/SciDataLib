""" testing functions """
from scidatalib.scidata import SciData
import json


def scidata_nums():
    uid = 'ids'
    testy = SciData(uid)
    # add discipline and subdiscipline data
    src = {
        'citation': 'Example SciData JSON-LD file, Chalk Research Group',
        'url': 'https://stuchalk.github.io/scidata/examples/ph_min.jsonld',
        'stype': 'dataset',
        'otype#': 'sdo:dataset'
    }
    testy.sources([src])
    print(json.dumps(testy.output, indent=4, ensure_ascii=False))


scidata_nums()
