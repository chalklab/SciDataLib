
=====
About
=====

A Python library for writing SciData_ JSON-LD_ files.

.. _SciData: http://stuchalk.github.io/scidata/
.. _JSON-LD: https://json-ld.org/

SciData and JSON-LD
-------------------

JSON-LD is a convenient (human-readable) encoding of Resource
Desctiption Framework (RDF) triples.  However, unlike traditional
relational databases (e.g., MySQL), the graph has no schema. This
is problematic as including data from different sources results
in a system with no common way to search across the data.  The
SciData framework is a structure for users to add data and its metadata
that are organized in the graph through the associated SciData ontology.

There are three main sections of the SciData framework:

* the methodology section (describing how the research was done)
* the system section (describing what the research studied and the conditions)
* the dataset section (the experimental data, plus any derived or supplemental
  data)

The methodology and system sections are generic and users can add any data
they need to contextualize the dataset.  However, in addition they must
provide a JSON-LD context file to semantically describe the data elements
included.  The dataset section has predefined data structures (dataseries,
datagroup, and datapoint) although other strudtures can be included
if needed.

Translating the content in JSON-LD.  Referencing the JSON-LD below:

*  '@context': provides resources that define the context (meaning) of
   data elements in the document (as a JSON array). It consists of
   three sections:

   - a list of one or more 'context' files
   - a JSON object containing one or more definitions of namespaces
     used in the document
   - a JSON object with one entry '@base' that defines the base URL
     to be prepended to all internal references (i.e. '@id' entries)
*  root level '@id': the 'name' of the file and where ingested into a
   graph database, the graph name
*  '@graph': the definition of content that will be represented as triples
   and identified by the graph name (this is therfore a 'quad')
*  '@id' under '@graph': the identifier for the graph.  The scidatalib
   code uses the '@base' to populate this, so they are consistent. As a result,
   all node identifiers '@id's in the document are globally unique because the
   '@base' is unique.

Example JSON-LD::

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
