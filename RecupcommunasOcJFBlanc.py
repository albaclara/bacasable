# -*-coding:Utf-8 -*

import csv
import re


def main():
    """ Programme principal."""
    
    ficentree = "communasOcFrJFBlanc.txt"
    ficresultat = "communasOcFrJFBlanc.csv"

    cp = []
    vila = []

    #traitement du fichier d'entrée
    with open(ficresultat, 'w', newline='', encoding='utf-8') as csvresult :
        spamwriter = csv.writer(csvresult,delimiter=',', quotechar='"')
        
        with open(ficentree, newline='', encoding='utf-8') as txtfile:
            
            temoincp = 0
            temoinnom = 0

            for ligne in txtfile.readlines():

                ligne = ligne.strip()
                if (ligne == "Còde de") or (ligne.startswith("La comunas d’Occitània")) :
                    temoincp = 1

                elif (temoincp == 1) :
                    if (ligne != "Nom oficial de la comuna") and (ligne !="comuna") :
                      print(ligne)
                      cp.append(ligne)
                    elif (ligne !="comuna")  :
                        temoincp = 0
                        temoinnom = 1
                elif  (temoinnom == 1) :
                    if ligne.startswith("La comunas d’Occitània") :
                        temoinnom = 0
                        temoincp = 1
                    else :
                        vila.append(ligne)


        for i in range(len(cp)):
            
            lignecsv = []
            lignecsv.append(cp[i])
            lignecsv.append(vila[i])
            print(lignecsv)
            spamwriter.writerow(lignecsv)

if __name__ == "__main__":

 
    main()
