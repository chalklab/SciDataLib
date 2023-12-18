"""file to create an example JSON-LD file"""
from scidatalib.scidata import SciData
import json


def create_scidata():
    # initialize SciData object
    uid = 'example'
    example = SciData(uid)

    """ METADATA "FINDING AID" SECTION """

    # context parameters
    base = 'https://scidata.unf.edu/' + uid + '/'
    context = 'https://stuchalk.github.io/scidata/contexts/scidata.jsonld'
    example.context(context)
    example.base(base)

    # named graph parameters
    example.docid('pH')
    example.version('1')

    # inside @graph
    example.title('pH of cyanide standard')
    sjc = {'name': 'Stuart Chalk',
           'organization': 'University of North Florida',
           'orcid': 'https://orcid.org/0000-0002-0703-7776'}
    example.author([sjc])

    # add description
    description = 'Determination of the pH of a 3 ppm cyanide solution'
    example.description(description)

    # add publisher
    publisher = (
        'Chalk Group, Department of Chemistry, University of North Florida'
    )
    example.publisher(publisher)

    # add permalink
    link = 'https://stuchalk.github.io/scidata/examples/ph_min.jsonld'
    example.permalink(link)

    # add namespaces (needed for values that point to ontological definitions of things)
    example.namespaces({'w3i': 'https://w3id.org/skgo/modsci#'})
    example.namespaces({'qudt': 'https://qudt.org/vocab/unit/'})
    example.namespaces({'obo': 'http://purl.obolibrary.org/obo/'})

    # add discipline and subdiscipline
    example.discipline('Chemistry')
    example.subdiscipline('w3i:Cheminformatics')

    """ METHODOLOGY SECTION """
    # methodology data goes into the aspects array in the JSON-LD file
    # for any field values that use namespaces add the namespaces separately
    # using .namespaces

    # add the type of methodology - experimental, computational, etc.
    example.evaluation('experimental')

    # add measurement
    measurement = {
        '@id': 'measurement',
        'scope': 'resource/1/',
        'technique': 'Potentiometry',
        'technique#': 'obo:OMIT_0005812'}
    value = {
        '@id': 'textvalue',
        'text': 'true'}
    settings = {
        '@id': 'setting',
        'category': 'instrument feature',
        'type': 'temperature compensation',
        'value': value}
    resource = {
        '@id': 'resource',
        'name': (
            'Accumet Liquid-Filled pH/ATC Epoxy Body Combination Electrode',
        ),
        'instrumentType': 'Temperature compensated pH electrode',
        'instrument#': 'obo:CHMO_0002344',
        'vendor': 'Fisher Scientific',
        'catalognumber': '13-620-530A',
        'settings': settings}
    procedure = {
        '@id': 'procedure',
        'description': (
            'The pH electrode was calibrated at ',
            'pH 7, pH 4, and pH 10 prior to measurement. ',
            'A portion of the solution was transferred to a beaker '
            'and the DI water washed electrode wash placed ',
            'in the solution and allowed to equilibrate ',
            'before the measurement was taken')
    }
    aspects = [measurement, resource, procedure]
    example.aspects(aspects)

    # add to system (data goes into the facets array)
    # for any field values using namespaces
    # makes sure to add them using .add_namespace
    inchi = 'InChI=1S/B4H4O9/c5-1-9-3(7)11-2(6)12-4(8,10-1)13-3/h5-8H/q-2',
    comp1 = {
        '@id': 'substance',
        'name': 'cyanide ion',
        'inchi': 'InChI=1S/CN/c1-2/q-1',
        'chebi': 'obo:CHEBI_17514'}
    comp2 = {
        '@id': 'substance',
        'name': 'phenolphthlin',
        'inchi': 'InChI=1S/C6H6O/c7-6-4-2-1-3-5-6/h1-5,7H',
        'chebi': 'obo:CHEBI_34915'}
    comp3 = {
        '@id': 'substance',
        'name': 'copper(II) ion',
        'inchi': 'InChI=1S/Cu/q+2',
        'chebi': 'obo:CHEBI_29036'}
    comp4 = {
        '@id': 'substance',
        'name': 'tetraborate ion',
        'inchi': inchi,
        'chebi': 'obo:CHEBI_38889'}
    comp5 = {
        '@id': 'substance',
        'name': 'ethanol',
        'inchi': 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3',
        'chebi': 'obo:CHEBI_16236'}
    comp6 = {
        '@id': 'substance',
        'name': 'water',
        'inchi': 'InChI=1S/H2O/h1H2',
        'chebi': 'obo:CHEBI_15377'}

    val1 = {'@id': 'value', 'number': 2.99, 'unit#': 'qudt:PPM'}
    val2 = {'@id': 'value', 'number': 100.0, 'unit#': 'qudt:MilliL'}
    val3 = {'@id': 'value', 'number': 22.8, 'unit#': 'qudt:DEG_C'}

    prp1 = {
        '@id': 'property',
        'quantitykind': 'mass of substance per volume',
        'quantity': 'Concentration (w/v)',
        'value': val1}
    prp2 = {
        '@id': 'property',
        'quantitykind': 'volume',
        'quantity': 'Volume of solution',
        'value': val2}
    example.namespaces(
        {"chm": "https://stuchalk.github.io/scidata/ontology/chemical.owl#"})
    con1 = {
        '@id': 'constituent',
        'source': 'substance/1/',
        'role#': 'chm:analyte',
        'properties': [prp1, prp2]
    }
    con2 = {
        '@id': 'constituent',
        'source': 'substance/2/',
        'role#': 'chm:reagent',
        'properties': [prp1, prp2]}
    con3 = {
        '@id': 'constituent',
        'source': 'substance/3/',
        'role#': 'chm:reagent'}
    con4 = {
        '@id': 'constituent',
        'source': 'substance/4/',
        'role#': 'chm:buffer'}
    con5 = {
        '@id': 'constituent',
        'source': 'substance/5/',
        'role#': 'chm:solvent'}
    con6 = {
        '@id': 'constituent',
        'source': 'substance/6/',
        'role#': 'chm:solvent'}
    cons = [con1, con2, con3, con4, con5, con6]

    example.namespaces(
        {'sub': 'https://stuchalk.github.io/scidata/ontology/substance.owl#',
         'gb': 'https://goldbook.iupac.org/'})
    sub1 = {
        '@id': 'substance',
        'title': '3 ppm cyanide standard solution',
        'aggregation#': 'sub:aq',
        'mixtype#': 'sub:homogeneousSolution',
        'phase#': 'sub:liquid',
        'constituents': cons,
        'properties': [prp2]}
    con1 = {
        '@id': 'condition',
        'source#': 'measurement/1/',
        'scope#': 'substance/1/',
        'quantitykind': 'temperature',
        'quantity': 'Ambient temperature',
        'quantity#': 'gb:T06321',
        'value': val3}
    facets = [comp1, comp2, comp3, comp4, comp5, comp6, sub1, con1]

    example.facets(facets)

    # add to dataset (goes into dataseries, datagroup, and/or datapoint
    dp1_datum1 = {
        "@id": "datum",
        "@type": "sdo:exptdata",
        "type": "IC50",
        "value": {
            "@id": "value",
            "relation": "=",
            "units": "uM",
            "value": "19.000000000000000000000000000000"
        }
    }

    dp1_datum2 = {
        "@id": "datum",
        "@type": "sdo:deriveddata",
        "value": {
            "@id": "value",
            "standard_relation": "=",
            "standard_value": "19000.000000000000000000000000000000",
            "standard_units": "nM",
            "standard_type": "IC50",
            "pchembl_value": "4.72",
            "unit#": ["obo:UO_0000065", "qudt:NanoMOL-PER-L"]
        }
    }

    dp1 = {
        "@id": "datapoint",
        "activity_id": 16464576,
        "assay": "CHEMBL3767769",
        "data": [dp1_datum1, dp1_datum2]
    }

    # Input datapoint 2
    text = "The solution was clear, no reagent precipitation was observed."
    dp2 = {
        "@id": "datapoint",
        "conditions": "Observation",
        "value": {
            "@id": "textvalue",
            "text": text,
            "textype": "plain",
            "language": "en-us"}}

    dps = [dp1, dp2]

    example.datapoint(dps)

    seriesx = [
        '107.9252',
        '108.4073',
        '108.8894',
        '109.3715',
        '109.8536',
        '110.3358',
        '110.8179',
        '111.3000',
        '111.7821']
    seriesy = [
        '831.4121',
        '833.1594',
        '839.9602',
        '848.9200',
        '855.5815',
        '860.6728',
        '862.4740',
        '859.3690',
        '851.6688']

    dataser1 = {"@id": "dataseries",
                "label": "Raman Spectrum",
                "parameter": [
                    {
                        "@id": "parameter",
                        "quantitykind": "Reciprocal length",
                        "quantity": "Wavenumber",
                        "units": "1/cm",
                        "datatype": "decimal",
                        "dataarray": seriesx
                    }, {
                        "@id": "parameter",
                        "quantitykind": "intensity",
                        "quantity": "intensity",
                        "datatype": "decimal",
                        "dataarray": seriesy
                    }
                ]
                }
    example.dataseries([dataser1])

    datagrp1 = {"@id": "datagroup",
                "label": "datagroup 1",
                "ids": ["datapoint/1/", "datapoint/2/"]}
    datagrp2 = {"@id": "datagroup",
                "label": "datagroup 2",
                "ids": ["datapoint/3/", "datapoint/4/"]}
    example.datagroup([datagrp1, datagrp2])

    # add source
    src = {'citation': 'Chalk Research Group',
           'url': 'https://stuchalk.github.io/scidata/examples/ph_min.jsonld'}
    example.sources([src])

    # add rights
    holder = (
        'Chalk Research Group, Department of Chemistry, Univ. of North Florida'
    )
    lic = 'https://creativecommons.org/licenses/by-nc-nd/4.0/'
    example.rights([{'holder': holder, 'license': lic}])

    packet = [{
        "aspects":
            [{"@id": "assay",
              "@type": "sdo:assay",
              "description": "Inhibition of human hERG by MK499 binding assay",
              "assay_organism": "Homo sapiens"}],
        "facets": [
            {"@id": "substance",
             "mw_freebase": "491.52",
             "full_molformula": "C26H26FN5O4",
             "#intlinks": [
                 {"@id": "identifier",
                  "standard_inchi_key":
                      "OINHUVBCKUJZAG-UHFFFAOYSA-N"}]},
            {"@id": "target",
             "@type": "sdo:target",
             "pref_name": "HERG",
             "tax_id": 9606,
             "organism": "Homo sapiens"}],
        "dataset": [
            {"@id": "datapoint",
             "@type": "sdo:datapoint",
             "data": [
                 {"@id": "datum",
                  "@type": "sdo:exptdata",
                  "type": "IC50",
                  "value":
                      "15.200000000000000000000000000000",
                  "units": "uM"}]}]}, {
        "aspects": [
            {"@id": "assay",
             "@type": "sdo:assay",
             "description": "Inhibition of human ERG "
                            "by MK499 binding assay",
             "assay_organism": "Homo sapiens"}],
        "facets": [
            {"@id": "substance",
             "mw_freebase": "491.52",
             "full_molformula": "C26H26FN5O4",
             "#intlinks": [
                 {"@id": "identifier",
                  "standard_inchi_key": "OINHUVBCKUJZAG-UHFFFAOYSA-N"}]},
            {"@id": "target",
             "@type": "sdo:target",
             "pref_name": "HERG",
             "tax_id": 9606,
             "organism": "Homo sapiens"}],
        "dataset": [
            {"@id": "datapoint",
             "@type": "sdo:datapoint",
             "empty_entry": "",
             "some_entry": "some",
             "data": [
                 {"@id": "datum",
                  "@type": "sdo:exptdata",
                  "type": "IC50",
                  "value":
                      "12.300000000000000000000000000000",
                  "units": "qudt:MicroM"}]}]}]

    example.scidatapackage(packet)

    # print(json.dumps(example.output, ensure_ascii=False))
    print(json.dumps(example.output, indent=4, ensure_ascii=False))


create_scidata()
