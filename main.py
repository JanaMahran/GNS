# -*- coding: utf-8 -*-

import creation_projet_noeuds_liens
import creation_configs
import drag_and_drop_bot
import os

#Définition de tous les chemins dont on aura besoin :
INTENT_FILE = "project.json"  # Fichier contenant tout ce qu'on veut appliquer à nos routeurs
CONFIG_SOURCE_DIR = os.path.join(os.getcwd(), "config")  # Dossier où les fichiers .cfg sont générés
GNS3_PROJECTS_DIR = r"C:\Users\msoff\GNS3\projects"  # Dossier où GNS3 stocke ses projets

def main():
    print("Création du projet, des nœuds et des liens...")
    project_id, node_ids = creation_projet_noeuds_liens.create_project_and_nodes(INTENT_FILE)
    if project_id is None or not node_ids:
        print("Erreur lors de la création du projet ou des nœuds.")
        return
    
    print("Génération des fichiers de configuration des routeurs...")
    creation_configs.main(INTENT_FILE, CONFIG_SOURCE_DIR)

    print("Déplacement des fichiers de configuration via un drag and drop bot...")
    project_path = os.path.join(GNS3_PROJECTS_DIR, str(project_id))
    drag_and_drop_bot.drag_and_drop_configs(node_ids, CONFIG_SOURCE_DIR, project_path)

    print("Processus terminé avec succès !")

if __name__ == "__main__":
    main()
