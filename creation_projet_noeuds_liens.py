# -*- coding: utf-8 -*-

import gns3fy
import json

def load_intent_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
    

server = gns3fy.Gns3Connector("http://localhost:3080")
lab = gns3fy.Project(name="test8_lab_avec_noeuds", connector=server)

lab.create()
print(f"Projet créé avec l'ID : {lab.project_id}")

#Maintenant que le projet existe, on le charge
lab.get()

#On lit le contenu de l'intent file (.json), qui nous est nécessaire pour créer les noeuds et liens
intent_file = "project.json"
intent_data = load_intent_file(intent_file)

# Pour créer les noeuds, on va parcourir tous les routeurs dans le json
for router in intent_data['routers']:
    router_node = gns3fy.Node(
        project_id=lab.project_id,
        connector=server,
        name=router['name'],
        #On utilise le template c7200 (Dynamips IOS router) pour ne pas avoir à configurer les propriétés manuellement
        template="c7200",
        #Pour des questions de lisibilité du projet créé, des coordonnées x et y sont associées à chaque routeur dans le json
        x=router['coord_x'],  # Coordonnée X depuis le JSON
        y=router['coord_y']   # Coordonnée Y depuis le JSON
        
        #Si on le fait manuellement, par exemple si on a oublié que l'attribut template existait...
        #node_type="dynamips",
        # compute_id="local", #local car on travaille sur notre machine
        # "image": "c7200-advipservicesk9-mz.152-4.S5.image", #image associée 
        # "ram": 512,  # Quantité de RAM en Mo
        # "nvram": 512,  # Taille de la mémoire NVRAM
        # "console_type": "telnet",  # Type de console
    )
    router_node.create()