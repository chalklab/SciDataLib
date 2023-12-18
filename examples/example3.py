"""file to create an example JSON-LD file"""
from scidatalib.scidata import SciData
import json

uid = 'example'
example = SciData(uid)


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
    'inchi': 'InChI=1S/B4H4O9/c5-1-9-3(7)11-2(6)12-4(8,10-1)13-3/h5-8H/q-2',
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

con1 = {
    '@id': 'constituent/1/',
    'source': 'substance/1/',
    'role': 'chm:analyte',
    'quantities': [{
        '@id': 'quantity/1/',
        'quantitykind': 'mass of substance per volume',
        'quantity': 'Concentration (w/v)',
        'value': {
            '@id': 'value', 'number': 2.99, 'unitref': 'qudt:PPM'}
    }, {
        '@id': 'quantity/2/',
        'quantitykind': 'volume',
        'quantity': 'Volume of solution',
        'value': {
            '@id': 'value', 'number': 100.0, 'unitref': 'qudt:MilliL'}
    }]
}
con2 = {
    '@id': 'constituent/2/',
    'source': 'substance/2/',
    'role': 'chm:reagent',
    'properties': [{
        '@id': 'quantity/1/',
        'quantitykind': 'mass of substance per volume',
        'quantity': 'Concentration (w/v)',
        'value': {
            '@id': 'value', 'number': 2.99, 'unitref': 'qudt:PPM'}
    }, {
        '@id': 'quantity/2/',
        'quantitykind': 'volume',
        'quantity': 'Volume of solution',
        'value': {
            '@id': 'value', 'number': 100.0, 'unitref': 'qudt:MilliL'}
    }]}
con3 = {
    '@id': 'constituent/3/',
    'source': 'substance/3/',
    'role': 'chm:reagent'}
con4 = {
    '@id': 'constituent/4/',
    'source': 'substance/4/',
    'role': 'chm:buffer'}
con5 = {
    '@id': 'constituent/5/',
    'source': 'substance/5/',
    'role': 'chm:solvent'}
con6 = {
    '@id': 'constituent/6/',
    'source': 'substance/6/',
    'role': 'chm:solvent'}
cons = [con1, con2, con3, con4, con5, con6]


sub1 = {
    '@id': 'substance',
    'title': '3 ppm cyanide standard solution',
    'aggregation#': 'sub:aq',
    'mixtype#': 'sub:homogeneousSolution',
    'phase#': 'sub:liquid',
    'constituents': cons,
    'properties': [{
        '@id': 'quantity/1/',
        'quantitykind': 'mass of substance per volume',
        'quantity': 'Concentration (w/v)',
        'value': {
            '@id': 'value', 'number': 4, 'unitref': 'qudt:PPM'}
    }, {
        '@id': 'quantity/2/',
        'quantitykind': 'volume',
        'quantity': 'Volume of solution',
        'value': {
            '@id': 'value', 'number': 250.0, 'unitref': 'qudt:MilliL'}
    }]}
con1 = {
    '@id': 'condition/1/',
    'source': 'measurement/1/',
    'scope': 'substance/1/',
    'quantitykind': 'temperature',
    'quantity': 'Ambient temperature',
    'quantity#': 'gb:T06321',
    'value': '100.0'}
facets = [comp1, comp2, comp3, comp4, comp5, comp6, sub1, con1]
example.facets(facets)

print(json.dumps(example.output, indent=4, ensure_ascii=False))
