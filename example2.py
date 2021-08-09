"""file to create an example JSON-LD file"""
from scidatalib.scidata import SciData
import json
import pandas as pd

uid = 'example'
example = SciData(uid)

# context parameters
example.context(
    ['https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
)
example.context(
    'https://stuchalk.github.io/scidata/contexts/scidata2.jsonld', True)
base = 'https://scidata.unf.edu/' + uid + '/'
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
example.description(
    ('Determination of the pH of a 3 ppm cyanide solution '
     'after complete reaction'))
example.publisher(
    'Chalk Group, Department of Chemistry, University of North Florida')
example.permalink('https://stuchalk.github.io/scidata/examples/ph_min.jsonld')

# add to scidata discipline and subdiscipline
example.namespaces({'w3i': 'https://w3id.org/skgo/modsci#'})
example.discipline('w3i:Chemistry')
example.subdiscipline('w3i:ChemicalInformatics')

# add to methodology (data goes into the aspects array)
# for any field values using namespaces
# makes sure to add them using .add_namespace
example.evaluation('experimental')
measurement = {
    '@id': 'measurement',
    'scope': 'resource/1/',
    'technique': 'Potentiometry',
    'techniqueref': 'obo:OMIT_0005812'}
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
    'instrument': 'obo:CHMO_0002344',
    'instrumentType': 'Temperature compensated pH electrode',
    'name': 'Accumet Liquid-Filled pH/ATC Epoxy Body Combination Electrode',
    'vendor': 'Fisher Scientific',
    'catalognumber': '13-620-530A',
    'settings': settings}
procedure = {
    '@id': 'procedure',
    'description': (
        'The pH electrode was calibrated at pH 7, pH 4, and pH 10 prior to '
        'measurement. A portion of the solution was transferred to a beaker '
        'and the DI water washed electrode wash placed in the solution and '
        'allowed to equilibrate before the measurement was taken'
    )}
aspects = [measurement, resource, procedure]
example.aspects(aspects)

# add to system (data goes into the facets array)
# for any field values using namespaces
# makes sure to add them using .add_namespace
comp1 = {
    '@id': 'compound',
    'name': 'cyanide ion',
    'inchi': 'InChI=1S/CN/c1-2/q-1',
    'chebi': 'obo:CHEBI_17514'}
comp2 = {
    '@id': 'compound',
    'name': 'phenolphthlin',
    'inchi': 'InChI=1S/C6H6O/c7-6-4-2-1-3-5-6/h1-5,7H',
    'chebi': 'obo:CHEBI_34915'}
comp3 = {
    '@id': 'compound',
    'name': 'copper(II) ion',
    'inchi': 'InChI=1S/Cu/q+2',
    'chebi': 'obo:CHEBI_29036'}
comp4 = {
    '@id': 'compound',
    'name': 'tetraborate ion',
    'inchi': 'InChI=1S/B4H4O9/c5-1-9-3(7)11-2(6)12-4(8,10-1)13-3/h5-8H/q-2',
    'chebi': 'obo:CHEBI_38889'}
comp5 = {
    '@id': 'compound',
    'name': 'ethanol',
    'inchi': 'InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3',
    'chebi': 'obo:CHEBI_16236'}
comp6 = {
    '@id': 'compound',
    'name': 'water',
    'inchi': 'InChI=1S/H2O/h1H2',
    'chebi': 'obo:CHEBI_15377'}

val1 = {'@id': 'value', 'number': 2.99, 'unitref': 'qudt:PPM'}
val2 = {'@id': 'value', 'number': 100.0, 'unitref': 'qudt:MilliL'}
val3 = {'@id': 'value', 'number': 22.8, 'unitref': 'qudt:DEG_C'}

prp1 = {
    '@id': 'property',
    'quantity': 'mass of substance per volume',
    'property': 'Concentration (w/v)',
    'value': val1}
prp2 = {
    '@id': 'property',
    'quantity': 'volume',
    'property': 'Volume of solution',
    'value': val2}
example.namespaces(
    {"chm": "https://stuchalk.github.io/scidata/ontology/chemical.owl#"})
con1 = {
    '@id': 'constituent',
    'source': 'compound/1/',
    'role': 'chm:analyte',
    'properties': [prp1]}
con2 = {
    '@id': 'constituent',
    'source': 'compound/2/',
    'role': 'chm:reagent'}
con3 = {
    '@id': 'constituent',
    'source': 'compound/3/',
    'role': 'chm:reagent'}
con4 = {
    '@id': 'constituent',
    'source': 'compound/4/',
    'role': 'chm:buffer'}
con5 = {
    '@id': 'constituent',
    'source': 'compound/5/',
    'role': 'chm:solvent'}
con6 = {
    '@id': 'constituent',
    'source': 'compound/6/',
    'role': 'chm:solvent'}
cons = [con1, con2, con3, con4, con5, con6]

example.namespaces(
    {'sub': 'https://stuchalk.github.io/scidata/ontology/substance.owl#',
     'gb': 'https://goldbook.iupac.org/'})
sub1 = {
    '@id': 'substance',
    'title': '3 ppm cyanide standard solution',
    'aggregation': 'sub:aq',
    'mixtype': 'sub:homogeneousSolution',
    'phase': 'sub:liquid',
    'constituents': cons,
    'properties': [prp2]}
con1 = {
    '@id': 'condition',
    'source': 'measurement/1/',
    'scope': 'substance/1/',
    'quantity': 'temperature',
    'property': 'Ambient temperature',
    'propertyref': 'gb:T06321',
    'value': val3}
facets = [comp1, comp2, comp3, comp4, comp5, comp6, sub1, con1]

example.facets(facets)

# add to dataset (goes into dataseries, datagroup, and/or datapoint
val4 = {'@id': 'value', 'number': 10.03}
val5 = {
    '@id': 'textvalue',
    'text': 'The solution was clear, no reagent precipitation was observed.',
    'textype': 'plain', 'language': 'en-us'}
pnt1 = {
    '@id': 'datapoint',
    'quantity': 'gb:P04524',
    'conditions': 'condition/1/',
    'value': val4}
pnt2 = {
    '@id': 'datapoint',
    'annotation': 'gb:P04524',
    'conditions': 'Observation',
    'value': val5}

dps = [pnt1, pnt2]

dp1_datum1 = {
    "@id": "datum",
    "@type": "sdo:exptdata",
    "type": "IC50",
    "value": {
        "@id": "value",
        "@type": "sdo:value",
        "relation": "=",
        "units": "uM",
        "value": "19.000000000000000000000000000000"
    }
}

dp1_datum2 = {
    "@id": "datum",
    "@type": "sdo:deriveddata",
    "value": {
        "standard_relation": "=",
        "@id": "value",
        "@type": "sdo:value",
        "standard_value": "19000.000000000000000000000000000000",
        "standard_units": "nM",
        "standard_type": "IC50",
        "pchembl_value": "4.72",
        "uo_units": "obo:UO_0000065",
        "qudt_units": "qudt:NanoMOL-PER-L"
    }
}

dp1_datum3 = {
    "@id": "datum",
    "@type": "sdo:None",
    "value": {
        "standard_flag": "1",
        "@id": "value",
        "@type": "sdo:value",
        "activity_id": "16464576"
    }
}

dp1 = {
    "@id": "datapoint",
    "@type": "sdo:datapoint",
    "activity_id": 16464576,
    "assay": "CHEMBL3767769",
    "data": [dp1_datum1, dp1_datum2, dp1_datum3]
}

# Input datapoint 2
dp2 = {
    "@id": "datapoint",
    "annotation": "gb:P04524",
    "conditions": "Observation",
    "value": {
        "@id": "textvalue",
        "text":
            "The solution was clear, no reagent precipitation was observed.",
        "textype": "plain",
        "language": "en-us"
    }
}

dps = [dp1, dp2]
example.datapoint(dps)


spectrax = [
    '107.9252',
    '108.4073',
    '108.8894',
    '109.3715',
    '109.8536',
    '110.3358',
    '110.8179',
    '111.3000',
    '111.7821']
spectray = [
    '831.4121',
    '833.1594',
    '839.9602',
    '848.9200',
    '855.5815',
    '860.6728',
    '862.4740',
    '859.3690',
    '851.6688']
ser1_input = {'spectra_x': spectrax, 'spectra_y': spectray}
ser1_dataframe = pd.DataFrame(ser1_input)
ser1_dataframe_str = pd.DataFrame(ser1_input).applymap(str)
ser1_dict_str = ser1_dataframe_str.reset_index().to_dict(orient='list')
del ser1_dict_str['index']

dataser1 = {
    '@id': 'dataseries',
    'annotation': 'gb:P04524',
    'conditions': 'Spectra'}

for k, v in ser1_dict_str.items():
    dataser1.update({k: v})

example.dataseries([dataser1])

# example.datagroup(
#     [{"@id": "datagroup", "@type": "sdo:datagroup",
#       "datapoints": ["datapoint"]}])

# add source
src = {'citation': 'Chalk Research Group',
       'url': 'https://stuchalk.github.io/scidata/examples/ph_min.jsonld'}
example.sources([src])

# add rights
holder = ', '.join([
    'Chalk Research Group',
    'Department of Chemistry',
    'University of North Florida'])
lic = 'https://creativecommons.org/licenses/by-nc-nd/4.0/'
example.rights(holder, lic)

print(json.dumps(example.output, indent=4, ensure_ascii=False))
