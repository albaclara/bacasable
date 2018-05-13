# -*-coding:Utf-8 -*

import csv
import re

def litDico(fic) :
    
    dico = {}

    with open(fic, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for ligne in spamreader:
            dico[ligne[0]] = 1
    return dico  

def main():
    """Le programme principal."""
    
    ficentree1 = "dicoVillesDBpedia.csv"
    ficentree2 = "abstractvillescadbpedia.csv"
    ficresultat = "compareOcCat.csv"

    dicoVilles = litDico(ficentree1)  

    with open(ficentree2, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        with open(ficresultat, 'w', newline='', encoding='utf-8') as csvresult :
            spamwriter = csv.writer(csvresult,delimiter=',', quotechar='"')

            # lecture villes 
            for ligne in spamreader:
                
                # normalisation forme
                ville = re.sub("( )+"," ",ligne[0])
                ville =  re.sub(" \(.*","",ville)
                
                trouve = 1
                
                if not ville in dicoVilles :                      
                    trouve = 0                    
                print(ville)
                ligne = []
                ligne.append(ville)
                ligne.append(trouve)
                spamwriter.writerow(ligne)


if __name__ == "__main__":
    main()
