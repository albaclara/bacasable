# -*-coding:Utf-8 -*

import csv
import re

def nettoienomOc(chaine):

    chaine = re.sub(" \[[^\]]*\]","",chaine)

    # suppression texte après nom
    chaine = re.sub("( selon la norme classique| en graphie classique).*","",chaine)
    chaine = re.sub(" prononcé.*","",chaine)
    chaine = re.sub(" qui signifie.*","",chaine)
    chaine = re.sub(" surnommé.*","",chaine)
    chaine = re.sub(" et ancienne graphie.*","",chaine)
    chaine = re.sub(" est une commune.*","",chaine)
    chaine = re.sub("(\()?( )?qui signifie.*","",chaine)
    chaine = re.sub("(\()?( )?prononcer.*","",chaine)
   
    # suppression quand même nom pour occitan et autre langue
    modele = '(ou occitan |ou catalan |et en italien )'
    chaine = re.sub(modele,"",chaine)
 
    # suppression nom dialecte
    modele='(marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot)( |:|,)'
    chaine = re.sub(modele,"",chaine)

    # nettoyage final
    chaine = re.sub('^ ',"",chaine)
    chaine = chaine.replace(":","")
    chaine = re.sub("'","",chaine)
    chaine = re.sub('^ ',"",chaine)
    chaine = re.sub(",.*","",chaine)
    
    return chaine

def main(modeleteste, position_a_sauver, typemod):
    """ Programme principal."""
    
    ficentree = "abstractvillesOcDBpedia.csv"
    ficresultat = "resulttest.csv"
    ficrejet = "rejets.csv"
    
    with open(ficrejet, 'w', newline='', encoding='utf-8') as csvrejet :
        spamwriterrejet = csv.writer(csvrejet,delimiter=',', quotechar='"')
        modeleparenthese =     modelesparenthese = "(\([^\)]*(en )?(occitan|gascon|limousin|languedocien)[^\)]*\))"   

        # choix des patrons de sélection
        regexparentheses = re.compile(modeleparenthese)
        regexteste = re.compile(modeleteste)


        #traitement du fichier d'entrée
        with open(ficentree, newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
            with open(ficresultat, 'w', newline='', encoding='utf-8') as csvresult :
                spamwriter = csv.writer(csvresult,delimiter=',', quotechar='"')

                # lecture nom ville et commentaire récupérés de DBpédia
                for ligne in spamreader:
                
                    # normalisation des espaces
                    ville = re.sub("( )+"," ",ligne[0])
                    ville =  re.sub(" \(.*","",ville)
                    commentaire = re.sub("( )+"," ",ligne[1])

                    trouveparentheses = regexparentheses.search(commentaire)
                    villeoc=""

                    # si mot occitan pas dans texte entre parenthèses
                    if trouveparentheses is None :
                        
                        trouve = regexteste.search(commentaire)
                        
                        if trouve is not None :

                            #villeoc = nettoienomOc(trouve.group(position_a_sauver))
                            villeoc= nettoienomOc(trouve.group(position_a_sauver))

                        if villeoc != "" :                       

                            ligne = []
                            ligne.append(ville)
                            ligne.append(villeoc)
                            print(villeoc)
                            spamwriter.writerow(ligne)
                        else :
                            # print(commentaire)

                            ligne = []
                            ligne.append(commentaire)
                            spamwriterrejet.writerow(ligne)


if __name__ == "__main__":

    modeleteste = "(,|et |ou )( )?en (marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot|occitan) (: )?([^,\.]*)(,|\.)"
    position_a_sauver = 3
    typemod = 0 # modele hors parenthèses
    main(modeleteste,position_a_sauver,typemod)
