import json
import os


#notes prof 
#anoncer avec network statement 
#un sous reseau qui advertise tout: pour les advertisement
#ibgp dans tous les routeurs 


# Function to load the JSON file
def load_intent_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# pour generer la configuration d'un routeur 
def generate_router_config(router):
    config = []
    config.append(f"hostname {router['name']}")  # Set hostname

    # loopback
    for interface in router['interfaces']:
        if "Loopback" in interface['name']:
            config.append(f"interface {interface['name']}")
            config.append(" no ip address")
            config.append(f" ipv6 address {interface['address']}")
            if interface['protocol']:
                if interface['protocol'] == "ospf":
                    config.append(" ipv6 ospf 1 area 1")
                elif interface['protocol'] == "rip":
                    config.append(" ipv6 rip RIP enable")
            config.append("!")
            


    # physical interfaces
    for interface in router['interfaces']:
        # Check for both "GigabitEthernet" and "FastEthernet" in the interface name
        if any(keyword in interface['name'] for keyword in ("GigabitEthernet", "FastEthernet")):
            if interface['address'] is not False:
                config.append(f"interface {interface['name']}")
                config.append(" no ip address")
                config.append(" negotiation auto")
                config.append(f" ipv6 address {interface['address']}")
                config.append(" ipv6 enable")
                if interface['protocol']:
                    if interface['protocol'] == "ospf":
                        config.append(" ipv6 ospf 1 area 1")
                    elif interface['protocol'] == "rip":
                        config.append(" ipv6 rip RIP enable")
                config.append("!")  
            else:  # If 'address' is False
                config.append(f"interface {interface['name']}")
                config.append(" no ip address")
                config.append(" shutdown")
                config.append(" negotiation auto")
                config.append("!")  
        

    #bgp 
    
    config.append(f"router bgp {router['bgp']['local_as']}")
    config.append(f" bgp router-id {router['bgp']['router_id']}")
    config.append(" bgp log-neighbor-changes")
    config.append(" no bgp default ipv4-unicast")
    for neighbor in router['bgp']['neighbors']:
        config.append(f" neighbor {neighbor['address']} remote-as {neighbor['remote_as']}")
        if neighbor['relationship'] == "iBGP":
            config.append(f" neighbor {neighbor['address']} update-source Loopback0")
    config.append("!")
    
    config.append("address-family ipv4")
    config.append("exit-address-family")
    config.append("!")
    
    config.append("address-family ipv6") 
    if "border" in router:  
        if router['igp']=='RIP':
            config.append("redistribute rip RIP")
        elif router['igp']=='OSPF':
            config.append(" redistribute ospf 1")
        for border_entry in router["border"]:
            network_address = border_entry["network"]
            config.append(f" network {network_address}")
        for neighbor in router['bgp']['neighbors']:
            config.append(f" neighbor {neighbor['address']} activate")
        config.append("exit-address-family")
            
        
    

    
    
    return "\n".join(config)

# Function to save configuration to a file
def save_config(router_name, config, output_dir):
    os.makedirs(f"{output_dir}/{router_name}", exist_ok=True)
    file_path = f"{output_dir}/{router_name}/startup-config.cfg"
    with open(file_path, "w") as file:
        file.write(config)

# Main function
def main(intent_file, output_dir):
    # Load the JSON intent file
    intent_data = load_intent_file(intent_file)

    # Process each router in the JSON
    for router in intent_data['routers']:
        # Generate configuration
        config = generate_router_config(router)

        # Save the configuration to a .cfg file
        save_config(router['name'], config, output_dir)
        print(f"Configuration for {router['name']} saved!")

# Run the script
if __name__ == "__main__":
    intent_file_path = "project.json"  # Update with your JSON file path
    output_directory = "configs"      # Directory to store the router configs
    main(intent_file_path, output_directory)
