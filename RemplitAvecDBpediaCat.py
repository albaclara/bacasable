# -*-coding:Utf-8 -*

import csv
import re

def main():
    """ Programme principal."""
    
    ficentree2 = "topo_dbpediaCat.csv" 
    ficentree1 = "Toponimia.csv"
    ficresultat = "listeTopoCatDBpedia.csv"
    ficrejet1 = "rejetsToponimiaCat.csv"
    ficrejet2 = "rejetsDBpediaCat.csv"

    dicoville = {}
    dbpediaville = {}
    
    try :
        rejet1 = open(ficrejet1, 'w', newline='', encoding='utf-8') 
        spamwriterrejet1 = csv.writer(rejet1,delimiter=',', quotechar='"')

        try :
            rejet2 = open(ficrejet2, 'w', newline='', encoding='utf-8')  
            spamwriterrejet2 = csv.writer(rejet2,delimiter=',', quotechar='"')

            try :
                resultat = open(ficresultat, 'w', newline='', encoding='utf-8') 
                spamwriterresultat = csv.writer(resultat,delimiter=',', quotechar='"')

                try :
                    entree1 = open(ficentree1, 'r', newline='', encoding='utf-8')
                    spamreader1 = csv.reader(entree1, delimiter=',', quotechar='"')

                    try :
                        entree2 = open(ficentree2, 'r', newline='', encoding='utf-8')
                        spamreader2 = csv.reader(entree2, delimiter=',', quotechar='"')

                        # lecture liste communes DBpedia et rangement dans dictionnaire dbpediaville
                        for ligne in spamreader2 :
                            dbpediaville[ligne[0]] = ligne[2]
                        print("Nombre de toponymes dans DBPedia :"+str(len(dbpediaville)))

                        # lecture donnees Toponimia  et rangement dans dictionnaire dicoville
                        cpttrouve = 0
                        
                        for ligne in spamreader1 :
                            if ligne[0] != "CP" :
                                cp = ligne[0]
                                ville = ligne[1]
                                dicoville[cp] = ville
                                ligneresult = []
                                ligneresult.append(cp)
                                ligneresult.append(ville)

                                # si code commune existe dans DBpedia on rajoute à la ligne le nom Oc
                                if cp  in dbpediaville :
   
                                    ligneresult.append(dbpediaville[cp])
                                    cpttrouve += 1
                                  
                                # si code commune n'existe pas dans DBpedia on envoie dans fichier rejet DBpédia
                                else :
                                    spamwriterrejet2.writerow(ligneresult)

                                spamwriterresultat.writerow(ligneresult)
                            
                        print("Nombre de toponymes dans Toponimia :"+str(len(dicoville)))
                        print("Nombre de toponymes de DBPedia Cat trouvés dans Toponimia :"+str(cpttrouve))

                        # recherche villes dans DBpedia et pas dans Toponimia
                        cpttrouve = 0

                        for ligne in dbpediaville.items() :

                            # si code commune existe dans DBpedia et pas dans Toponimia on envoie dans fichier rejet Toponimia
                            if ligne[0] not in dicoville :
                                ligneresult = []
                                ligneresult.append(ligne[0])
                                ligneresult.append(ligne[1])
                                spamwriterrejet1.writerow(ligneresult)
                                cpttrouve += 1
                        print("Nombre de toponymes de DBPedia Cat non trouvés dans Toponimia :"+str(cpttrouve))
                               
                    except IOError :
                        print("fichier entree2 non trouvé")
                except IOError :
                    print("fichier entree1 non trouvé")         
            except NameError :
                print("ficresultat non défini")
        except NameError :
            print("ficrejet2 non défini")
    except NameError :
        print("ficrejet1 non défini")
        
    entree1.close()
    entree2.close()
    resultat.close()
    rejet1.close()
    rejet2.close()
                            

if __name__ == "__main__":
    main()
