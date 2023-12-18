""" example conversion of rruff file format """
from scidatalib.scidata import SciData
import json
import requests


def convert_rruff():
    """ load and process rruff file """
    f = open("../tests/data/rruff/raman_soddyite.rruff", "r")
    lines = f.read().splitlines()
    rruff, seriesx, seriesy = {}, [], []
    for line in lines:
        if line == '##END=' or line == '':
            pass
        elif line.find("##") != -1:
            line = line.replace("##", "")
            parts = line.split("=")
            rruff.update({parts[0].lower(): parts[1]})
        else:
            # datalines
            xy = line.split(", ")
            seriesx.append(xy[0])
            seriesy.append(xy[1])
    rruff.update({'series': {'x': seriesx, 'y': seriesy}})

    # initialize SciData object
    uid = 'ornl_rruff_' + rruff['rruffid']
    example2 = SciData(uid)

    """ METADATA "FINDING AID" SECTION """

    # add document base URL
    base = 'https://scidata.unf.edu/' + uid + '/'
    context = (
        'https://stuchalk.github.io',
        '/scidata',
        '/contexts',
        '/crg_substance.jsonld'
    )
    example2.context(context)
    example2.base(base)

    # named graph parameters
    example2.docid('rruff_' + rruff['rruffid'])  # Graph name
    example2.version('1')

    # inside @graph
    example2.title(rruff['names'] + ' rruff file')
    mm = {'name': rruff['source']}
    example2.author([mm])

    # add description
    example2.description(rruff['description'])

    # add publisher
    example2.publisher(rruff['locality'])

    # add permalink
    example2.permalink('https://' + rruff['url'])

    # add discipline and subdiscipline (plus namespace)
    example2.namespaces({'w3i': 'https://w3id.org/skgo/modsci#'})
    example2.discipline('w3i:Chemistry')
    example2.subdiscipline('w3i:MaterialsScience')

    """ METHODOLOGY SECTION """
    # methodology data goes into the aspects array in the JSON-LD file
    # for any field values that use namespaces add the namespaces separately
    # using .namespaces

    # add measurement
    aspects = []
    example2.namespaces({'obo': 'http://purl.obolibrary.org/obo/',
                        'qudt': 'https://qudt.org/vocab/unit/'})
    measurement = {
        '@id': 'measurement',
        'technique': 'Raman',
        'technique#': 'obo:CHMO_0000656',
        'settings': [
            {
                '@id': 'setting',
                'type': 'laser wavelength',
                'value': rruff['laser_wavelength'],
                'unit': 'nm',
                'unit#': 'qudt:NanoM'
            }
        ]}
    aspects.append(measurement)
    example2.aspects(aspects)

    """ SYSTEM SECTION """

    # add chemical substance
    facets = []
    name = 'uranyl silicate dihydrate'
    formula = rruff['ideal chemistry'].replace("_", "").replace("&#183;", ".")
    # chemical substance
    substance = {
        '@id': 'substance',
        'name': name,
        'formula': formula
    }
    meta = requests.get('https://opsin.ch.cam.ac.uk/opsin/' + name).json()  # get metadata from OPSIN
    ignore = ['status', 'message', 'cml', 'inchi']
    for key, value in meta.items():
        if key not in ignore:
            substance.update({key: value})
    facets.append(substance)

    # add minerals (named in title)
    mineral1 = {
        '@id': 'mineral',
        'name': 'malachite',
        'symbol': ['Mlc', 'Mal'],
        'dataurl': 'https://www.mindat.org/min-2550.html'
    }
    facets.append(mineral1)
    mineral2 = {
        '@id': 'mineral',
        'name': 'brochantite',
        'symbol': ['Bct', 'Bro'],
        'dataurl': 'https://www.mindat.org/min-779.html'
    }
    facets.append(mineral2)
    example2.facets(facets)

    """ DATASET SECTION """

    # dataset
    example2.namespaces(
        {'all': 'http://purl.allotrope.org/ontologies/result#'})
    seriesx = rruff['series']['x']
    seriesy = rruff['series']['y']
    series = {
        "@id": "dataseries",
        "label": "Raman Spectroscopy",
        "parameter": [
            {
                "@id": "parameter",
                "quantity": "wavenumber",
                "quantity#": "all:AFR_0001592",
                "units": "1/cm",
                "units#": "qudt:PER-CentiM",
                "datatype": "decimal",
                "data": seriesx
            },
            {
                "@id": "parameter",
                "quantity": "intensity",
                "datatype": "decimal",
                "data": seriesy
            }
        ]
    }
    example2.dataseries([series])

    # add source
    src = {'citation': 'RRUFF Project', 'url': 'https://rruff.info/R060361'}
    example2.sources([src])

    # add rights
    holder = (
        'Developed by The University of Arizona ',
        'and is the property of The Arizona Board of Regents ',
        'on behalf of The University of Arizona, Copyright (C) 2005'
    )
    lic = (
        'By accessing this database, ',
        'users consent to use this database and ',
        'software solely for informational purposes. ',
        'Selling, distributing, publishing, circulating, ',
        'or commercially exploiting the data in this database ',
        'without the express written permission of the owners ',
        'of the data is expressly prohibited. ',
        'Use of this database and software shall not convey any ',
        'ownership right, title or interest, '
        'nor any security or other interest in any '
        'intellectual property rights ',
        'relating to the database and software, ',
        'nor in any copy of any part of the database and software.'
    )
    example2.rights([{'holder': holder, 'license': lic}])

    print(json.dumps(example2.output, indent=4))
    exit()


convert_rruff()
