from iiif_prezi3 import Manifest, AnnotationPage, Annotation, ResourceItem, config
import json
import os
import arvestapi
from PIL import Image
from urllib.request import urlopen
from arvesttools.md_parser import recuperation, extraction_duration, extraction_colonne, extraction_metadonne, extraction_duration2, link_conversion


def md_to_manifest(markdown_folder, manifest_folder, mail, password) :

    ar = arvestapi.Arvest(mail, password)
    print(f"You are connecte as {ar.profile.name}")

    num_fichier = 25

    nbr = os.listdir(markdown_folder)
    md_count = 0
    for i in nbr :
        md_count += 1

    for i in range(1): 

        chemin = os.path.join(markdown_folder, f"Manifest_{num_fichier}.md")

        #Extraction des informations pour les Canvas

        Recuperation = recuperation(['## Canavses'],['@@@c'], chemin)
        link = extraction_colonne("Source", Recuperation)
        format = extraction_colonne("Format", Recuperation)
        durations = extraction_duration2(Recuperation, 2, 3, format)
        Base_info = recuperation(['## Manifest title '],['@@@t'], chemin)
        titre = extraction_metadonne("Title", Base_info)

        num = 0

        #Géneration du manifeste

        config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
        base_url = "http://127.0.0.1:5500"
        manifest = Manifest(id=f"{base_url}/manifest_{num_fichier}.json", label=titre)

        #Creation des Canvas 

        Recuperation.pop(0)


        for i in link:

            if format[num] == "video"  :
                canvas = manifest.make_canvas(id=f"{base_url}/canvas/{num}/")
                anno_body = ResourceItem(id=link[int(f"{num-1}")],
                                type="Video",
                                format="video/MPG")

                anno_page = AnnotationPage(id=f"{base_url}/canvas/page")
                anno = Annotation(id=f"{base_url}/canvas/page/annotation",
                            motivation="painting",
                            body=anno_body,
                            target=canvas.id)

                hwd = {"height": 113, "width": 200, "duration":durations[int(f"{num-1}")][2]}
                anno_body.set_hwd(**hwd)
                canvas.set_hwd(**hwd)

                anno_page.add_item(anno)
                canvas.add_item(anno_page)


            if format[num] == "image"  :

                img =Image.open(urlopen(i))
                widh_media, height_media = img.size

                if i.find("PNG") > 0 or i.find("png") > 0 :
                    format_image = "png"

                if i.find("jpg") > 0 or i.find("jpeg") > 0 :
                    format_image = "jpg"

                canvas = manifest.make_canvas(id=f"{base_url}/canvas{num}/p1", height=height_media, width=widh_media)
                anno_page = canvas.add_image(image_url = i,
                                                anno_page_id=f"{base_url}/page/p1/1",
                                                anno_id=f"{base_url}/annotation/p0001-image",
                                                format=f"image/{format_image}",
                                                height=widh_media,
                                                width=height_media
                                                )

            num = num + 1


        #Export manifest en .json 

        nom_manifest = f"manifest_essai{num_fichier}.json"
        manifest_path = os.path.join(manifest_folder, nom_manifest)
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest.dict(), f, ensure_ascii=False, indent=2)

                #Upload Arvest

        new_manifest = ar.add_manifest(path = manifest_path, update_id = True)
        new_manifest.update_title(titre)
        print(new_manifest.title)

        num_fichier = num_fichier +1 

        num = 0



        
def metadata_update(markdown_folder, manifest_folder, mail, password):

  ar = arvestapi.Arvest(mail, password)

  print("Update metadata...")

  #Ouverture du markdown

  num_fichier = 25
  nbr = os.listdir(markdown_folder)
  md_count = 0
  for i in nbr :
      md_count += 1

  for i in range(1): 

    chemin = os.path.join(markdown_folder, f"Manifest_{num_fichier}.md")
    
    Contenu_canvas = recuperation(['## Manifest metadata'],['@@@m'], chemin)
    Base_info = recuperation(['## Manifest title '],['@@@t'], chemin)
    Labels = extraction_colonne("Label", Contenu_canvas)
    Value = extraction_colonne("Value", Contenu_canvas)
    titre = extraction_metadonne("Title", Base_info)
    thumb = extraction_metadonne("thumbnail", Base_info)

    #Recuperation du manifest

    manifestes = ar.get_manifests()
    for item in manifestes:
      if item.title == titre:
        contenu = item.get_content()
        id = item.id
    manifeste = ar.get_manifest(id)

    url = contenu["items"][0]["items"][0]["items"][0]["body"]["id"]


    #Création des metadonnées

    metadonnee = []
    numo = 0

    for i in Labels: 
            dicto = {"label":f"{i}","value":f"{Value[numo]}"}
            metadonnee.append(dicto)
            numo += 1
    contenu["metadata"] = metadonnee


    #Creation du Thumbnail

    img = Image.open(urlopen(thumb))
    widh_media, height_media = img.size
    thumbnail = [
      {
        "id": f"{thumb}",
        "type": "Image",
        "format": "image/webp",
        "width": widh_media,
        "height": height_media
      }
      ]
    contenu["thumbnail"] = thumbnail


    #Export du manifest en .json

    nom_manifest = f"{titre}.json"

    #Update du manifeste

    manifeste.update_content(contenu)
    print("Metadata successfully updated !")

    num_fichier = num_fichier +1



def md_to_anotation(markdown_folder, manifest_folder, mail, password) :

      ar = arvestapi.Arvest(mail, password)

      num_fichier = 25
      nbr = os.listdir(markdown_folder)
      md_count = 0
      for i in nbr :
            md_count += 1
      md_count -= 1

      for i in range(1): 

            chemin = os.path.join(markdown_folder, f"Manifest_{num_fichier}.md")

            #Extraction des informations pour les Canvas------------------------------------------

            Recuperation_titres = recuperation(['## Manifest metadata'],['@@@m'], chemin)
            titre = extraction_metadonne("Title", Recuperation_titres)
            manifestes = ar.get_manifests()

            for item in manifestes:
                  if item.title == titre:
                        contenu = item.get_content()
                        #manifeste = item
                        ident = item.id

            manifeste = ar.get_manifest(ident)
            body = contenu["items"]

            #Extraction des informations pour les Canvas------------------------------------------

            Recuperation = recuperation(['## Text Annotations'],['@@@ta'], chemin)
            annot = extraction_colonne("Contenu", Recuperation)
            durations = extraction_duration(Recuperation, 2, 3)
            canva = extraction_colonne("Canvas", Recuperation)
            Recuperation_link = recuperation(['## Link Annotations'],['@@@la'], chemin)
            link = extraction_colonne("Manifest", Recuperation_link)
            content = extraction_colonne("Contenu", Recuperation_link)

            #Transformation des url en lien cliquable 

            http = "https:"
            link_conversion(http, annot)
            http = "http:"
            link_conversion(http, annot)


            #Creation d'une base d'annotation------------------------------------------

            base_url = manifeste.get_full_url()
            base_url = base_url.replace(".json","")

            canvas_id = contenu["items"][0]["id"]
            manifest = Manifest(id=f"{base_url}/manifest_essai2.json",
                    label={"en": ["Scott"]})

            num = 0

            # Detecteur d'annotation lien------------------------------------------

            def verifi(annotation):
                  resultat = False
                  for i in content :
                        if i == annotation :
                              resultat = True 
                  return resultat 
            num_par_canvas = []

            # Supression des doublons dans la liste des Canvas---------------------

            def anti_doublon(dicto, liste):
                  resultat = False
                  for i in liste :
                        if i == dicto :
                              resultat = True 
                  return resultat 

            for i in canva :
                  dicto = {"canvas":f"{i}","value": 0}
                  if anti_doublon(dicto, num_par_canvas) is False :
                    num_par_canvas.append(dicto)

            # Pour chaque annotation dans le markdown

            for i in annot : 
                
                  num = num +1

                  #Recuperation du numero et id du canvas
                  numero = canva[num-1]
                  canvas_id = (body[int(numero)-1]["id"])

                  # Compte si y a deja eu une annotation dans le canvas

                  num_par_canvas[int(numero)-1]["value"]  += 1

                  # Reset le canvas pour retirer des doublons

                  if num_par_canvas[int(numero)-1]["value"] == 1 : 
                    canvas = manifest.make_canvas_from_iiif(url="https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen",
                                        id=canvas_id)

                  # Detecte si le canvas est une image ou video 

                  typa = body[int(numero)-1]["items"][0]["items"][0]["body"]["type"]
                  if typa == "Video":
                       targeting = f"#t={durations[num-1][0]},{durations[num-1][1]}"
                  else :
                       targeting = ""

                  #Generation de l'anotation 

                  if verifi(i) is True :
                              wa = content.index(i)
                              anno = canvas.make_annotation(id=f"{base_url}/annotation/p{num}-comment/#{link[wa]}",
                                          motivation="commenting",
                                          body={"type": "TextualBody",
                                                "language": "en",
                                                "format": "text/plain",
                                                "value": f"{annot[num-1]}"},
                                          target=canvas_id + targeting,
                                          anno_page_id=f"{base_url}/page/p1/1")
                  else:
                               anno = canvas.make_annotation(id=f"{base_url}/annotation/p{num}-comment",
                                          motivation="commenting",
                                          body={"type": "TextualBody",
                                                "language": "en",
                                                "format": "text/plain",
                                                "value": f"{annot[num-1]}"},
                                          target=canvas_id + targeting,
                                          anno_page_id=f"{base_url}/page/p1/1")

                  rag = canvas.json(indent=2)
                  raga = json.loads(rag)


                  if num_par_canvas[int(numero)-1]["value"] == 1 :
                        contenu["items"][int(numero)-1]["annotations"] = raga["annotations"]
                  if num_par_canvas[int(numero)-1]["value"] > 1 : 
                        contenu["items"][int(numero)-1]["annotations"][0]["items"] = raga["annotations"][0]["items"]
                  
            #Upload sur Arvest

            manifeste.update_content(contenu)
            print(f"{titre} was successfuly annotated !" )
            