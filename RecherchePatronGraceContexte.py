# -*-coding:Utf-8 -*

import csv

listeville = "abstractvillesocdbpedia.csv"
ficresultat = "patron.csv"
margegauche =int(input("Nb car à gauche:"))
margedroite = int(input("Nb car à droite:"))+7

with open(listeville, newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    with open(ficresultat, 'w', newline='', encoding='utf-8') as csvresult :

        spamwriter = csv.writer(csvresult,delimiter=',', quotechar='"')	
        for ligne in spamreader:
            commentaire = ligne[1]
            position = commentaire.find("occitan")

            if (position != -1)  and (position-margegauche >=0) and (position+margedroite <= len(commentaire)-1) :
                print("--"+commentaire[position-margegauche:position]+"-- / occitan /--"+commentaire[position+7:position+margedroite]+"--")
                ligne = []
                ligne.append(commentaire[position-margegauche:position])
                ligne.append(commentaire[position+7:position+margedroite])
                spamwriter.writerow(ligne)