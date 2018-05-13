# -*-coding:Utf-8 -*
#RecupAbstractVillesOcDBpedia.py
# créé le: 10/02/2018
# par Eve Séguier
# The aim of this program is to get in dbpedia, label and comment of french towns where the word 'occitan' is found in the comment and to putb the result in the file 

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import csv

endpoint = "https://sophox.org/sophox/"

with open('abstractOSM.csv', 'w', newline='', encoding='utf-8') as csvfile :

    spamwriter = csv.writer(csvfile,delimiter=',', quotechar='"')	
    sparql = SPARQLWrapper(endpoint)

    querystring = """
prefix osmnode: <https://www.openstreetmap.org/node/>
prefix osmway: <https://www.openstreetmap.org/way/>
prefix osmrel: <https://www.openstreetmap.org/relation/>
prefix osmt: <https://wiki.openstreetmap.org/wiki/Key:>
prefix osmm: <https://www.openstreetmap.org/meta/>
prefix pageviews: <https://dumps.wikimedia.org/other/pageviews/>
SELECT
  ?id  ?loc
  (osmt:sport as ?tag_a1)  ('scuba_diving' as ?val_a1)
  (osmt:sport as ?tag_b1)  ('cliff_diving' as ?val_b1)
WHERE {
  ?id osmt:sport 'diving' .
  ?id osmm:loc ?loc .
}
LIMIT 10
"""

    sparql.setQuery(querystring)
    print('Recherche en cours, patience ...')
    sparql.setReturnFormat(JSON)
    resultats = sparql.query().convert()

    print(resultats)
 


