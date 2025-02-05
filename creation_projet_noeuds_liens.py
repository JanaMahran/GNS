# -*- coding: utf-8 -*-

import gns3fy
import json

def load_intent_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
   
def create_project_and_nodes(intent_file):

    server = gns3fy.Gns3Connector("http://localhost:3080")
    lab = gns3fy.Project(name="projet_gns", connector=server)
    
    lab.create()
    print(f"Projet créé avec l'ID : {lab.project_id}")
    
    #Maintenant que le projet existe, on le charge
    lab.get()
    
    #On lit le contenu de l'intent file (.json), qui nous est nécessaire pour créer les noeuds et liens
    intent_data = load_intent_file(intent_file)
    
    #initialisation d'un dictionnaire qui contiendra l'association entre les noms de nos routeurs et leur id dans gns3fy
    node_ids = {}
    
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
        )
        router_node.create() #on crée le noeud
        
        #La suite est utile pour la création des liens
        router_node.get()  # Récupère les informations mises à jour, y compris node_id
        node_ids[router['name']] = router_node.node_id  # Associe le nom au node_id
        print(f"Nœud créé : {router['name']} avec ID : {router_node.node_id}")
        
    #Création des liens en reparcourant la liste des liens dans le json
    for lien in intent_data['liens']:
        source_name = lien['source']['name']
        dest_name = lien['destination']['name']
        source_adapter = lien['source']['adapter']
        source_port = lien['source']['port']
        dest_adapter = lien['destination']['adapter']
        dest_port = lien['destination']['port']
        link = gns3fy.Link(
            project_id=lab.project_id,
            connector=server,
            nodes = [
                {"node_id": node_ids[source_name], "adapter_number": source_adapter, "port_number": source_port},
                {"node_id": node_ids[dest_name], "adapter_number": dest_adapter, "port_number": dest_port}
                ]
            )
        link.create() #création du lien une fois qu'on a bien toutes les infos
        print(f"Lien créé : {source_name} ({source_adapter}/{source_port}) -> {dest_name} ({dest_adapter}/{dest_port})")
    return lab.project_id, node_ids