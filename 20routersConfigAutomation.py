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
    config.append("!")
    config.append("!")
    config.append("! Last configuration change at 11:22:51 UTC Wed Jan 22 2025")
    config.append("!")
    config.append("version 15.2")
    config.append("service timestamps debug datetime msec")
    config.append("service timestamps log datetime msec")
    config.append("!")
    config.append(f"hostname {router['name']}")  # Set hostname
    config.append("boot-start-marker")
    config.append("boot-end-marker")
    config.append("!")
    config.append("no aaa new-model")
    config.append("no ip icmp rate-limit unreachable")
    config.append("ip cef")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("no ip domain lookup")
    config.append("ipv6 unicast-routing")
    config.append("ipv6 cef")
    config.append("!")
    config.append("!")
    config.append("multilink bundle-name authenticated")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("ip tcp synwait-time 5")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("!")
    
    # loopback
    config.append("!")
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
    if "border_comm" in router:
        if "filtres" in router:
            for neighbor in router['bgp']['neighbors']:
                config.append(f" neighbor {neighbor['address']} activate")
                if neighbor['relationship'] == "iBGP":
                    config.append(f" neighbor {neighbor['address']} send-community both")
                if neighbor['relationship'] == "eBGP":
                    if neighbor['filtre'] is True:
                        config.append(f" neighbor {neighbor['address']} route-map comm in")
                        config.append(f" neighbor {neighbor['address']} route-map filtre out")
                    else:
                        config.append(f" neighbor {neighbor['address']} route-map comm in")         
        else:
            for neighbor in router['bgp']['neighbors']:
                config.append(f" neighbor {neighbor['address']} activate")
                if neighbor['relationship'] == "iBGP":
                    config.append(f" neighbor {neighbor['address']} send-community both")
                if neighbor['relationship'] == "eBGP":
                    config.append(f" neighbor {neighbor['address']} route-map comm in")
            
                
    else:
        for neighbor in router['bgp']['neighbors']:
            config.append(f" neighbor {neighbor['address']} activate")
            if router['as']=="1":
                if neighbor['send_community'] is True:
                    config.append(f" neighbor {neighbor['address']} send-community both") #chage variable name 

                
    config.append("exit-address-family")
    config.append("!")
    config.append("ip forward-protocol nd")
    config.append("!")
    config.append("ip bgp-community new-format")
    
    if "communities" in router:
        for community in router['communities']:
            config.append(f"ip community-list {community['community_name']} permit {community['permit']}")
        config.append("!")
    config.append("no ip http server")
    config.append("no ip http secure-server")
    config.append("!")
    config.append("!")
    if "border" in router:
        if router['igp']=='OSPF':
            config.append("ipv6 router ospf 1")
            config.append(f" router-id {router['bgp']['router_id']}")
            config.append(f" passive-interface {router['bgp']['border_interface']}")
            config.append(f" redistribute bgp {router['as']}")
            config.append("!")
        elif router['igp']=='RIP':
            config.append("ipv6 router rip RIP")
            config.append(" redistribute connected")
            config.append("!")
    else:
        if router['igp']=='OSPF':
            config.append("ipv6 router ospf 1")
            config.append(f" router-id {router['bgp']['router_id']}")
            config.append("!")
        if router['igp']=='RIP':
            config.append("ipv6 router rip RIP")
            config.append(" redistribute connected")
            config.append("!")
            
    if "filtres" in router:
        config.append(f"route-map filtre deny {router['filtres']['deny']}")
        config.append(f" match community {router['filtres']['match_comm']}")
        config.append("!")
        config.append("route-map filtre permit 30")
        config.append("!")
            
    if "border_comm" in router:
         config.append(f"route-map comm permit {router['border_comm']['permit']}")
         config.append(f" set local-preference {router['border_comm']['local_pref']}")
         config.append(f" set community {router['border_comm']['set_comm_add']} additive")
         config.append("!")

                
        
            
    config.append("!")
    config.append("!")
    config.append("!")
    config.append("control-plane")
    config.append("!")
    config.append("!")
    config.append("line con 0")
    config.append(" exec-timeout 0 0")
    config.append(" privilege level 15")
    config.append(" logging synchronous")
    config.append(" stopbits 1")
    config.append("line aux 0")
    config.append(" exec-timeout 0 0")
    config.append(" privilege level 15")
    config.append(" logging synchronous")
    config.append(" stopbits 1")
    config.append("line vty 0 4")
    config.append(" login")
    config.append("!")
    config.append("!")
    config.append("end")

   
    
    
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
    intent_file_path = "Network20routers.json"  # Update with your JSON file path
    output_directory = "configs"      # Directory to store the router configs
    main(intent_file_path, output_directory)
