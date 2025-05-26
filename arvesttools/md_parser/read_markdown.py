import os
import csv

racine = os.getcwd()

def recuperation(debut, fin, chemin):
    ma_liste = []
    numdebut = 0
    numfin = 0
    num_recolte = 0

    f = open(chemin, encoding='utf-8')
    csv_read = csv.reader(f)
    for ligne in csv_read: 
        numdebut = numdebut + 1
        if ligne == debut:
            break
    f.close()

    f = open(chemin, encoding='utf-8')
    csv_read = csv.reader(f)
    for ligne in csv_read: 
        numfin = numfin + 1
        if ligne == fin:
            break
    f.close()

    f = open(chemin, encoding='utf-8')
    csv_read = csv.reader(f)
    for ligne in csv_read: 
        num_recolte = num_recolte + 1
        if num_recolte > numdebut and num_recolte < numfin:
            ma_liste.append(ligne)
    f.close()

    sortie = []

    for line in ma_liste:
        i = str(line).split("|")
        sortie.append(i)

    return sortie 

def extraction_colonne(colonne, recuperation):
    num_ligne = 0
    resultat = []
    for liste in recuperation:
        num_ligne = num_ligne + 1
        for item in liste :
            if item == colonne:
                wa = liste.index(colonne)
        if num_ligne > 2 :
            texte = liste[int(f"{wa}")]
            if texte.find("\', \'") > 0 :
                  virgule = texte.find("\', \'")
                  cible = texte[virgule:virgule+4]
                  texte = texte.replace(cible,",")
            resultat.append(texte)
    return resultat


def extraction_data(colonne, url, recuperation):
    for liste in recuperation:
        for item in liste :
            if item == colonne:
                wa = liste.index(colonne)
            if item == url: 
                resultat = (liste[int(f"{wa}")])
    return resultat

def sec_convert(time):
    i = str(time).split(":")
    h = int(i[0]) * 3600
    m = int(i[1]) * 60
    s = int(i[2])
    resultat = h + m + s 
    return resultat

def extraction_duration(recuperation, start, end):
    num_ligne = 0
    resultat = []
    for liste in recuperation:
        num_ligne = num_ligne + 1
        if num_ligne > 2 :
            #Extraction des timecode de la signe en seconde
            timers = []
            timer1 = sec_convert(liste[start])
            timers.append(timer1)
            timer2 = sec_convert(liste[end])
            timers.append(timer2)
            duration = timer2 - timer1
            timers.append(duration)
            resultat.append(timers)
    return resultat


def extraction_metadonne(target, recuperation):
  for liste in recuperation:
    for item in liste :
      if item == target:
            wa = liste.index(target) + 1
            resultat = liste[int(f"{wa}")]
            if resultat.find("\', \'") > 0:
                  virgule = resultat.find("\', \'")
                  cible = resultat[virgule:virgule+4]
                  resultat = resultat.replace(cible,",")
  return resultat

def extraction_duration2(recuperation, start, end, format):
    num_ligne = 0
    resultat = []
    numa = 0
    for liste in recuperation:
        num_ligne = num_ligne + 1
        if num_ligne > 2 and format[numa] == "video":
            #Extraction des timecode de la ligne en seconde
            timers = []
            timer1 = sec_convert(liste[start])
            timers.append(timer1)
            timer2 = sec_convert(liste[end])
            timers.append(timer2)
            duration = timer2 - timer1
            timers.append(duration)
            resultat.append(timers)
            numa +=1
    return resultat


def link_conversion(http, annot) :
    for i in annot :
        if i.find(http) > 0 :
            wa = annot.index(i)
            a = i.index(http)
            b = len(i)
            url1 = (i[a:b])
            if url1.find(" ") > 0:
                j = url1.index(" ")
                url2 = (url1[0:j])
                url3 = f"<a href=\"{url2}\">🔗</a>"
                y = i.replace(url1,url3)
                annot[wa] = y
            else :
                url2 = f"<a href=\"{url1}\">🔗</a>"
                y = i.replace(url1,url2)
                annot[wa] = y