# -*-coding:Utf-8 -*
#RecupAbstractVillesOcDBpedia.py
# créé le: 10/02/2018
# par Eve Séguier
# The aim of this program is to get in dbpedia, label and comment of french towns where the word 'occitan' is found in the comment and to putb the result in the file 

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import csv

endpoint = "http://fr.dbpedia.org/sparql"

with open('abstractvillesOcDBpedia.csv', 'w', newline='', encoding='utf-8') as csvfile :

    spamwriter = csv.writer(csvfile,delimiter=',', quotechar='"')	
    sparql = SPARQLWrapper(endpoint)

    querystring = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX db-owl: <http://dbpedia.org/ontology/>
SELECT  ?ville ?label ?comment ?code
WHERE {
    ?ville db-owl:country <http://fr.dbpedia.org/resource/France> ;
        db-owl:inseeCode ?code;
        rdf:type db-owl:Settlement ;
	rdfs:comment ?comment  ;
        rdfs:label ?label 

FILTER regex(?comment,".*occitan.*")
FILTER langmatches(lang(?label),"fr")
FILTER langmatches(lang(?comment),"fr")
}
"""

    sparql.setQuery(querystring)
    print('Recherche en cours, patience ...')
    sparql.setReturnFormat(JSON)
    resultats = sparql.query().convert()

    for result in resultats["results"]["bindings"]:

       lignesortie = []

       lignesortie.append(result["label"]["value"])
       lignesortie.append(result["comment"]["value"])
       lignesortie.append(result["ville"]["value"])
       lignesortie.append(result["code"]["value"])

       spamwriter.writerow(lignesortie)


