"""file to create an example JSON-LD file"""
from SciDataLib.scidata import SciData
import json

uid = 'chalk:example:jsonld'
example = SciData(uid)

# context parameters
example.context(
            ['https://stuchalk.github.io/scidata/contexts/scidata.jsonld']
        )
example.context(
    'https://stuchalk.github.io/scidata/contexts/scidata2.jsonld', True)
base = 'https://scidata.unf.edu/' + uid + '/'
example.add_base(base)

# named graph parameters
example.doc_id('example1')
example.generatedat('')
example.version('1')

# inside @graph
example.graph_id(base)
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
example.namespace({'test': 'https://test.org/test#'})
example.discipline('w3i:Chemistry')
example.subdiscipline('w3i:ChemicalInformatics')

# add to methodology (data goes into the aspects array)
# for any field values using namespaces
# makes sure to add them using .add_namespace
measurement = {
    '@id': 'measurement',
    'scope': 'resource/1/',
    'techniqueType': 'obo:OMIT_0005812',
    'technique': 'obo:NCIT_C142343'}
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
example.namespace({'gb': 'https://goldbook.iupac.org/'})
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
example.datapoint([pnt1, pnt2])

# add source
src = {'citation': 'Chalk Research Group',
       'url': 'https://stuchalk.github.io/scidata/examples/ph_min.jsonld'}
example.source([src])

# add rights
holder = ','.join([
    'Chalk Research Group',
    'Department of Chemistry',
    'University of North Florida'])
license = 'https://creativecommons.org/licenses/by-nc-nd/4.0/'
example.rights(holder, license)

print(json.dumps(example.output, indent=4, ensure_ascii=False))
