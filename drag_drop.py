import os
import shutil

# pour remplacer routeurs configs en gns3
def replace_gns3_configs_with_ids(config_dir, gns3_project_dir):
    for router_name in os.listdir(config_dir):
        router_config_path = os.path.join(config_dir, router_name, "startup-config.cfg")

        # check si fichier config existe
        if not os.path.exists(router_config_path):
            print(f"No startup-config.cfg found for {router_name}. Skipping.")
            continue

        # Find the corresponding router config file in GNS3 by router ID
        #cherche router config file correspondant en GNS en utilisant le router ID
        router_id = extract_router_id(router_name)
        if router_id is None:
            print(f"Unable to extract router ID for {router_name}. Skipping.")
            continue

        # cherche GNS3 config file
        gns3_config_file = find_gns3_router_config_file(gns3_project_dir, router_id)

        if gns3_config_file:
            # remplace config file avec le nouveau
            shutil.copy(router_config_path, gns3_config_file)
            print(f"Replaced config for router {router_name} (ID {router_id}) in GNS3 project.")
        else:
            print(f"No config file found for router ID {router_id} in GNS3 project.")

#extracts router ID from the router name
def extract_router_id(router_name):
    # extraire partie numerique du nom du routeur
    for char in router_name:
        if char.isdigit():
            return int(''.join(filter(str.isdigit, router_name)))
    return None

# find the GNS3 router config file by ID
def find_gns3_router_config_file(gns3_project_dir, router_id):
    config_file_name = f"i{router_id}_startup-config.cfg"

    # Search for the file in the GNS3 project directory
    for root, dirs, files in os.walk(gns3_project_dir):
        if config_file_name in files:
            return os.path.join(root, config_file_name)
    return None

if __name__ == "__main__":
    generated_config_dir = "configs"  # dir where generated configs are stored
    gns3_project_directory = "projet_gns"  # GNS3 project path


    replace_gns3_configs_with_ids(generated_config_dir, gns3_project_directory)


