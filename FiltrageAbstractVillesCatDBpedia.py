# -*-coding:Utf-8 -*
# sortir compile de regex de la boucle !!!!!!!!!

import csv
import re

def defmodelesCat() :
    
    modeles = {}

    # modèle ville (nom occità)
    modeles['...(nom occità)'] = ["^(.*) \((nom |en francès i |en )?occità( modern| i francés)?(;| i|\))",1]
     

    # modèle occità dans parenthèses
    modeles['(...en occità...)'] = ["(\([^\)]*(en )?occità [^\)]*\))",1]
    # sous-modèle (en occità...)
    modeles['(en occità...)'] = ["\(en occità( |:|, )([^\)]*)\)",2]
    # sous-modèle (... en occità)
    modeles['(...en occità)'] = ["\(([^\)]*)(\[(^\])+\])? en occità( i francés)?[\)]*\)",1]

    # modèle sans parenthèses
    # sous-modèle son nom ... 
    modeles['son nom en ...'] = ["on nom (en )?(marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot|occitan)( marchois| vivaro-alpin| provençal| gascon| rouergat| languedocien| alpin| niçois| limousin| gavot| local| du Béarn) est ([^,\.]*)(,|\.)",4]
   # sous-modèle en occità ... 
    modeles['en occità...'] = ["(,|et |)( )?en (marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot|occitan)( marchois| vivaro-alpin| provençal| gascon| rouergat| languedocien| alpin| niçois| limousin| gavot| local| du Béarn)?(: )?([^,\.]*)(,|\.)",6]
    # sous-modèle  ...en occitan
    modeles['...en occità'] = ["^(.*) en occità",1]
    # sous-modèle se nomme ... 
    modeles['se nomme'] = ["(E|e)n (marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot|occità)( marchois| vivaro-alpin| provençal| gascon| rouergat| languedocien| alpin| niçois| limousin| gavot| local| du Béarn), ((il|elle|le village|la ville) se nomme |on dit) (,|\.)",6]
    
   
      
    return modeles  

def nettoienomCat(chaine):

    chaine = re.sub(" \[[^\]]*\]","",chaine)

    # suppression texte après nom
    chaine = re.sub(" és una vila.*","",chaine)
    chaine = re.sub(" (i )?en francès.*","",chaine)
   
    # suppression quand même nom pour occitan et autre langue
    modele = '(ou occitan |ou catalan |et en italien )'
    chaine = re.sub(modele,"",chaine)
 
    # suppression nom dialecte
    modele='(marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot)( |:|,)'
    chaine = re.sub(modele,"",chaine)

    # suppression texte entre parenthèses
    modele='\([^\)]*\)'
    chaine = re.sub(modele,"",chaine)

    # nettoyage final
    chaine = re.sub('^ ',"",chaine)
    chaine = chaine.replace(":","")
    chaine = re.sub("'","",chaine)
    chaine = re.sub('^ ',"",chaine)
    chaine = re.sub(",.*","",chaine)
    
    return chaine

def main():
    """Le programme principal."""
    
    ficentree = "abstractvillesCaDBpedia.csv"
    ficresultat = "listefiltreeCat.csv"
    ficrejet = "rejetsCat.csv"
    with open(ficrejet, 'w', newline='', encoding='utf-8') as csvrejet :
        spamwriterrejet = csv.writer(csvrejet,delimiter=',', quotechar='"')

        modeles =defmodelesCat()
        
        # récupération patron nom (nom occità)
        regex = re.compile(modeles['...(nom occità)'][0])
        pos = modeles['...(nom occità)'][1]

        # récupération patron parenthèses
        regexparentheses = re.compile(modeles['(...en occità...)'][0])
        posparentheses = modeles['(...en occità...)'][1]

        # traitement du fichier d'entrée
        with open(ficentree, newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
            with open(ficresultat, 'w', newline='', encoding='utf-8') as csvresult :
                spamwriter = csv.writer(csvresult,delimiter=',', quotechar='"')


                # lecture nom ville et commentaire récupérés de DBpédia
                for ligne in spamreader:

                    codeINSEE  = ligne[3]
                    
                    # normalisation des espaces
                    ville = re.sub("( )+"," ",ligne[0])
                    ville =  re.sub(" \(.*","",ville)
                    commentaire = re.sub("( )+"," ",ligne[1])


                    trouve = regex.search(commentaire)
                    villeoc=""

                    # cas nomville (nom occità)
                    if trouve is not None :

                        villeoc = nettoienomCat(trouve.group(pos))
                    
                    else  :
                        
                        trouve0 = regexparentheses.search(commentaire)

                        
                        # si mot occità et ville dans texte entre parenthèses
                        if trouve0 is not None :
                         
                            souschaine = trouve0.group(modeles['(...en occità...)'][1])

                            # récupération sous-patrons
                            regex2 = re.compile(modeles['(...en occità)'][0])
                            pos2 = modeles['(...en occità)'][1]
                            regex3 = re.compile(modeles['(en occità...)'][0])
                            pos3 = modeles['(en occità...)'][1]
                           

                            #compilation des modèles
                            trouve2 = regex2.search(souschaine)
                            trouve3 = regex3.search(souschaine)


                            # parenthèse type (...en occitaà)
                            if trouve2 is not None :
                                villeoc = nettoienomCat(trouve2.group(pos2))

                            # parenthèse type (en occità ...)               
                            elif trouve3 is not None :
                                villeoc = nettoienomCat(trouve3.group(pos3))

                            
                        # si nom ville pas entre parenthèses     
                        else :

                            # récupération sous-patrons
                            regex1 = re.compile(modeles['son nom en ...'][0])
                            pos1 = modeles['son nom en ...'][1]
                            regex2 = re.compile(modeles['en occità...'][0])
                            pos2 = modeles['en occità...'][1]
                            regex3 = re.compile(modeles['...en occità'][0])
                            pos3 = modeles['...en occità'][1]

                            #compilation des modèles
                            trouve1 = regex1.search(commentaire)
                            trouve2 = regex2.search(commentaire)
                            trouve3 = regex3.search(commentaire)

                            # type  son nom est...
                            if trouve1 is not None :
                                villeoc = nettoienomCat(trouve1.group(pos1))
                            
                            # type  en occitan...
                            elif trouve2 is not None :
                                villeoc = nettoienomCat(trouve2.group(pos2))

                            #  type ...en occitan             
                            elif trouve3 is not None :
                                villeoc = nettoienomCat(trouve3.group(pos3))

                    if villeoc != "" :                       
                        print(villeoc)
                        ligne = []
                        ligne.append(codeINSEE) 
                        ligne.append(ville)
                        ligne.append(villeoc)
                        spamwriter.writerow(ligne)
                            
                    else :
                        print(commentaire)

                        ligne = []
                        ligne.append(commentaire)
                        spamwriterrejet.writerow(ligne)
                            
                            


if __name__ == "__main__":
    main()

    
