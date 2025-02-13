# -*- coding: utf-8 -*-

import os
import shutil


def clear_directory(directory):
    """Fonction pour vider un répertoire et supprimer tous ses fichiers"""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
def extract_router_id(router_name):
    """Extrait le numéro du routeur depuis son nom (ex: 'R1' -> 1, 'Router12' -> 12)."""
    router_id_str = ""
    for char in router_name: #parcours du nom du routeur
        if char.isdigit():  # Si le caractère est un chiffre, on l'ajoute à la chaîne
            router_id_str += char
    
    # On convertit en entier si on a trouvé des chiffres, sinon renvoyer None
    if router_id_str:
        return int(router_id_str)  
    else :
        return None

def drag_and_drop_configs(node_ids, config_path, project_path):
    """
    Déplace les fichiers de configuration des routeurs vers leur répertoire correspondant dans le projet GNS3.
    Supprime ensuite le dossier temporaire des configurations si tout a été déplacé.
    
    :param node_ids: Dictionnaire {nom_routeur: node_id}
    :param config_path: Chemin du répertoire où sont stockées les configurations générées
    :param project_path: Chemin du répertoire du projet GNS3
    """
    moved_files = 0
    for router_name, node_id in node_ids.items():
        router_dir_in_config = os.path.join(config_path, router_name)  # Dossier R1, R2, etc., dans le répertoire config
        config_file_path = os.path.join(router_dir_in_config, "startup-config.cfg")  # Le fichier à déplacer
        
        if os.path.exists(config_file_path):
            router_dir_in_gns3 = os.path.join(project_path, "project-files", "dynamips", str(node_id),"configs")  # Répertoire du routeur dans GNS3

            if os.path.exists(router_dir_in_gns3):
                # On vide le répertoire du routeur dans GNS3 avant de déplacer le fichier, pour se débarasser de la config par défaut du routeur
                clear_directory(router_dir_in_gns3)
                
                # On renomme le fichier de configuration pour correspondre au format attendu par GNS3
                router_id = extract_router_id(router_name) #on récupère le numéro du routeur dans son nom
                new_config_file_name = f"i{router_id}_startup-config.cfg"
                new_config_file_path = os.path.join(router_dir_in_gns3, new_config_file_name)
                
                shutil.move(config_file_path, new_config_file_path)  # Déplace le fichier vers le répertoire du routeur
                print(f"Config de {router_name} déplacée avec succès dans le répertoire adapté !")
                moved_files += 1
            else:
                print(f"Le répertoire associé au routeur d'id {node_id} (de nom {router_name}) n'a pas été trouvé dans GNS3.")
        else:
            print(f"Aucune configuration trouvée pour {router_name} dans le dossier temporaire.")

    # Suppression du dossier temporaire config s'il est vide (en théorie si on a tout bien déplacé, il l'est)
    if moved_files > 0 and os.path.exists(config_path):
        shutil.rmtree(config_path)
        print(f"Dossier temporaire {config_path} supprimé.")




