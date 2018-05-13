# -*-coding:Utf-8 -*

import csv
import re

def defmodelesOc() :
    
    modeles = {}

    # modèle parenthèses
    modeles['(...en occitan...)'] = ["(\([^\)]*(en )?(occitan|gascon|limousin|languedocien)[^\)]*\))",1]
    # sous-modèle (en occitan ...) 
    modeles['(en occitan...)'] = ["\((en )?occitan( |:|, )([^\)]*)\)",3]
    # sous-modèle (... en occitan)
    modeles['(...en occitan)'] = ["\(([^\)]*) en occitan( marchois| vivaro-alpin| provençal| gascon| rouergat| languedocien| alpin| niçois| limousin| gavot| local| du Béarn)?[\)]*",1]
    #modeles['(...en occitan)'] = ["\(([^\)]*) en occitan( marchois| vivaro-alpin| provençal| gascon| rouergat| languedocien| alpin| niçois| limousin| gavot| local| du Béarn)?(,[\)]*)?\)",1]
    # sous-modèle (... en dialecte ...)
    modeles['(...en dialecte)'] = ["\(([^\)]*) en (marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot)[^\)]*\)",1]

    # modèle sans parenthèses
    # sous-modèle son nom ... 
    modeles['son nom en ...'] = ["on nom (en )?(marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot|occitan)( marchois| vivaro-alpin| provençal| gascon| rouergat| languedocien| alpin| niçois| limousin| gavot| local| du Béarn) est ([^,\.]*)(,|\.)",4]
    # sous-modèle se nomme ... 
    modeles['se nomme'] = ["(E|e)n (marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot|occitan)( marchois| vivaro-alpin| provençal| gascon| rouergat| languedocien| alpin| niçois| limousin| gavot| local| du Béarn), ((il|elle|le village|la ville) se nomme |on dit) (,|\.)",6]
   # sous-modèle en occitan ... 
    modeles['en occitan...'] = ["(,|et |)( )?en (marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot|occitan)( marchois| vivaro-alpin| provençal| gascon| rouergat| languedocien| alpin| niçois| limousin| gavot| local| du Béarn)?(: )?([^,\.]*)(,|\.)",6]
    # sous-modèle  ...en occitan
    modeles['...en occitan'] = ["(,|et|ou)( )?(« )?([^ ]*)( »)? en (marchois|vivaro-alpin|provençal|gascon|rouergat|languedocien|alpin|niçois|limousin|gavot|occitan)",4]
    
    return modeles  

def nettoienomOc(chaine):

    chaine = re.sub(" \[[^\]]*\]","",chaine)

    # suppression texte après nom
    chaine = re.sub("( selon la norme classique| en graphie classique).*","",chaine)
    chaine = re.sub(" prononcé.*","",chaine)
    chaine = re.sub(" qui signifie.*","",chaine)
    chaine = re.sub(" surnommé.*","",chaine)
    chaine = re.sub(" et ancienne graphie.*","",chaine)
    chaine = re.sub(" est une commune.*","",chaine)
   
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
    """ Programme principal."""
    
    ficentree = "abstractvillesOcDBpedia.csv"
    ficresultat = "listefiltreeOcDBpedia.csv"
    ficrejet = "rejets.csv"
    with open(ficrejet, 'w', newline='', encoding='utf-8') as csvrejet :
        spamwriterrejet = csv.writer(csvrejet,delimiter=',', quotechar='"')

        modeles =defmodelesOc()
    
        # récupération patron parenthèses
        regexparentheses = re.compile(modeles['(...en occitan...)'][0])


        #traitement du fichier d'entrée
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
  

                    trouve = regexparentheses.search(commentaire)
                    villeoc=""

                    # si mot occitan dans texte entre parenthèses
                    if trouve is not None :

                        souschaine = trouve.group(modeles['(...en occitan...)'][1])

                        # récupération sous-patrons
                        regex2 = re.compile(modeles['(...en occitan)'][0])
                        pos2 = modeles['(...en occitan)'][1]
                        regex3 = re.compile(modeles['(en occitan...)'][0])
                        pos3 = modeles['(en occitan...)'][1]
                        regex4 = re.compile(modeles['(...en dialecte)'][0])
                        pos4 = modeles['(...en dialecte)'][1]                      

                        #compilation des modèles
                        trouve2 = regex2.search(souschaine)
                        trouve3 = regex3.search(souschaine)
                        trouve4 = regex4.search(souschaine)

                        # parenthèse type (...en occitan)
                        if trouve2 is not None :
                            villeoc = nettoienomOc(trouve2.group(pos2))

                        # parenthèse type (en occitan ...)               
                        elif trouve3 is not None :
                            villeoc = nettoienomOc(trouve3.group(pos3))

                         # parenthèse type (... dialecte ...)
                        elif trouve4 is not None :
                            villeoc = nettoienomOc(trouve4.group(pos4))

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
                            
                    # si mot occitan pas entre parenthèses       
                    else :

                        # récupération sous-patrons
                        regex1 = re.compile(modeles['son nom en ...'][0])
                        pos1 = modeles['son nom en ...'][1]
                        regex2 = re.compile(modeles['en occitan...'][0])
                        pos2 = modeles['en occitan...'][1]
                        regex3 = re.compile(modeles['...en occitan'][0])
                        pos3 = modeles['...en occitan'][1]
                        regex4 = re.compile(modeles['se nomme'][0])
                        pos4 = modeles['se nomme'][1]

                        #compilation des modèles
                        trouve1 = regex1.search(commentaire)
                        trouve2 = regex2.search(commentaire)
                        trouve3 = regex3.search(commentaire)
                        trouve4 = regex4.search(commentaire)

                        # type  son nom est...
                        if trouve1 is not None :
                            villeoc = nettoienomOc(trouve1.group(pos1))
                             

                        # type  en occitan...
                        elif trouve2 is not None :
                            villeoc = nettoienomOc(trouve2.group(pos2))
                            
                        # type  se nomme
                        elif trouve4 is not None :
                            villeoc = nettoienomOc(trouve4.group(pos4))

                        #  type ...en occitan             
                        elif trouve3 is not None :
                            villeoc = nettoienomOc(trouve3.group(pos3))

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
