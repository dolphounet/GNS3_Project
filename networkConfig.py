def border_router(network, router):
    for interface in network["routers"][router-1]["interface"]:
        if interface["neighbor"] != [] and network["routers"][interface["neighbor"][0]-1]["AS"] != network["routers"][router-1]["AS"]:
            return True
    return False

def belongs_to_subNet(network, router, subNet):
    return subNet in network["routers"][router-1]["subNets"]

def addressing_if(interface):
    config = ""
    address = "".join(interface["address"])
    config += f" ipv6 address {address}\n"
    return config

def passive_if(network, router):
    config = ""
    for interface in network["routers"][router-1]["interface"]:
        if interface["neighbor"] != [] and network["routers"][interface["neighbor"][0]-1]["AS"] != network["routers"][router-1]["AS"]:
            config += f" passive-interface {interface['name']}\n"
    return config

def OSPF_if(network,interface):
    config = " ipv6 ospf 10 area 0\n"
    for interfaceType in network["Constants"]["Bandwith"]:
        if interfaceType in interface['name'] and interfaceType != "Reference":
            config += f" bandwidth {network['Constants']['Bandwith'][interfaceType]}\n"
            if interface['metricOSPF'] != "":
                config += f" ipv6 ospf cost " + interface['metricOSPF'] + "\n"
    return config

def OSPF(network, router):
    routerId = f"{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}"
    config = f"ipv6 router ospf 10\n router-id {routerId}\n"
    config += passive_if(network, router)
    config += f" auto-cost reference-bandwidth {network['Constants']['Bandwith']['Reference']}\n"
    config += "!\n"
    return config

def RIP_if(network, router, interface):
    config = ""
    if interface['name'] == "Loopback1" or network["routers"][interface["neighbor"][0]-1]["AS"] == network["routers"][router-1]["AS"]:
        config += " ipv6 rip BeginRIP enable\n"
    return config

def RIP():
    config = "ipv6 router rip BeginRIP\n redistribute connected\n!\n"
    return config

def BGP(network, router):
    """
    Ca s'applique pour le routeur d'ID router
    """
    routerId = f"{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}"
    neighbor_addresses = {"iBGP" : [], "eBGP" : []}

    config = f"router bgp {network['routers'][router-1]['AS']}\n no bgp default ipv4-unicast\n bgp router-id {routerId}\n"
    
    for rtr in network["routers"]:
        neighbor = rtr["ID"][0]
        if neighbor != router:

            # iBGP
            if network["routers"][neighbor-1]["AS"] == network["routers"][router-1]["AS"]:
                for interface in network["routers"][neighbor-1]["interface"]:
                    if "Loopback" in interface["name"]:
                        neighbor_address = interface["address"][0]
                        break
                config += f" neighbor {neighbor_address} remote-as {network['routers'][neighbor-1]['AS']}\n"
                config += f" neighbor {neighbor_address} update-source Loopback1\n"
                neighbor_addresses["iBGP"].append((neighbor_address,neighbor))

            # eBGP
            elif neighbor in network["adjDic"][router]:
                for interface in network["routers"][neighbor-1]["interface"]:
                    if router in interface["neighbor"]:
                        neighbor_address = interface["address"][0]
                        break
                config += f" neighbor {neighbor_address} remote-as {network['routers'][neighbor-1]['AS']}\n"
                neighbor_addresses["eBGP"].append((neighbor_address,neighbor))

    # Config de l'address-family en ipv6
    config += " !\n address-family ipv4\n exit-address-family\n !\n address-family ipv6 unicast\n"

    once = False
    # iBGP
    for (neighbor_address,neighborID) in neighbor_addresses["iBGP"]:
        config += f"  neighbor {neighbor_address} activate\n"
        config += f"  neighbor {neighbor_address} send-community\n"
        if not once :
            # Rejoindre son sous réseau
            for subNet in network["AS"][network["routers"][router-1]["AS"]-1]["subNets"]:
                if belongs_to_subNet(network, router, subNet):
                    config += f"  network {''.join(subNet)} route-map {network['routers'][router-1]['AS']}_Client_in\n"
            once = True

    # eBGP
    for (neighbor_address,neighborID) in neighbor_addresses["eBGP"]:
        config += f"  neighbor {neighbor_address} activate\n"
        config += BGP_Border(network, router,neighbor_address,neighborID)
        if not once :
            # Rejoindre son sous réseau
            for subNet in network["InterAS"]["subNets"]:
                if belongs_to_subNet(network, router, subNet):
                    config += f"  network {''.join(subNet)} route-map {network['routers'][router-1]['AS']}_Client_in\n"
            config += f"  network {network['AS'][network['routers'][router-1]['AS']-1]['networkIP'][0]}{network['AS'][network['routers'][router-1]['AS']-1]['networkIP'][1]}\n"
            once = True

    
    config += " exit-address-family\n!\n"

    config += BGP_CommunityLists(network,router)
    config += BGP_Routemap(network,router)

    return config 

def BGP_Border(network,router,neighbor_address,neighborID):

    # Application des route-map
    neighborType = network["AS"][network["routers"][router-1]["AS"]-1]["relations"][str(network["routers"][neighborID-1]["AS"])]
    config = f"  neighbor {neighbor_address} route-map {network['routers'][router-1]['AS']}_{neighborType}_in in\n"
    # Route-map out
    config += f"  neighbor {neighbor_address} route-map {network['routers'][router-1]['AS']}_{neighborType}_out out\n"

    return config

def BGP_CommunityLists(network,router):
    config = f"ipv6 route {network['AS'][network['routers'][router-1]['AS']-1]['networkIP'][0]}{network['AS'][network['routers'][router-1]['AS']-1]['networkIP'][1]} Null0\n"
    config += f"ip bgp-community new-format\n!\n"

    for relation in network["Constants"]["LocPref"]:
        if relation != "Client" :
            config += f"ip community-list {network['Constants']['LocPref'][relation]} permit {network['routers'][router-1]['AS']}:{network['Constants']['LocPref']['Client']}\n"
            config += f"ip community-list {network['Constants']['LocPref'][relation]} deny {network['routers'][router-1]['AS']}:{network['Constants']['LocPref']['Peer']}\n"
            config += f"ip community-list {network['Constants']['LocPref'][relation]} deny {network['routers'][router-1]['AS']}:{network['Constants']['LocPref']['Provider']}\n!\n"

        elif relation == "Client" :
            config += f"ip community-list {network['Constants']['LocPref'][relation]} permit {network['routers'][router-1]['AS']}:{network['Constants']['LocPref']['Client']}\n"
            config += f"ip community-list {network['Constants']['LocPref'][relation]} permit {network['routers'][router-1]['AS']}:{network['Constants']['LocPref']['Peer']}\n"
            config += f"ip community-list {network['Constants']['LocPref'][relation]} permit {network['routers'][router-1]['AS']}:{network['Constants']['LocPref']['Provider']}\n!\n"

    return config

def BGP_Routemap(network,router):
    config = ""
    
    # In route-map
    for relation in network["Constants"]["LocPref"]:
        config += f"route-map {network['routers'][router-1]['AS']}_{relation}_in permit {int(network['Constants']['LocPref'][relation]/10)}\n"
        config += f" set local-preference {network['Constants']['LocPref'][relation]}\n"
        config += f" set community {network['routers'][router-1]['AS']}:{network['Constants']['LocPref'][relation]}\n!\n"
    
    # Out route-map
    for relation in network["Constants"]["LocPref"] :
        config += f"route-map {network['routers'][router-1]['AS']}_{relation}_out permit {int(network['Constants']['LocPref'][relation]/10)}\n"
        config += f" match community {network['Constants']['LocPref'][relation]}\n!\n"


    return config




def config_router(network, routerID):
    config = f"!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostname {network['routers'][routerID-1]['ID'][1]}\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\nip tcp synwait-time 5\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n"
    for interface in network["routers"][routerID-1]["interface"]:
        if interface["neighbor"] != [] or "Loopback" in interface["name"]:
            if "Loopback" in interface["name"]:
                config += f"interface {interface['name']}\n no ip address\n ipv6 enable\n{addressing_if(interface)}"
            elif "Fast" in interface["name"]:
                config += f"interface {interface['name']}\n no ip address\n duplex full\n ipv6 enable\n{addressing_if(interface)}"

            else:
                config += f"interface {interface['name']}\n no ip address\n ipv6 enable\n{addressing_if(interface)}"

            if "RIP" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
                config += RIP_if(network, routerID, interface)

            if "OSPF" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
                config += OSPF_if(network,interface)

            config += "!\n"
        else:
            config += f"interface {interface['name']}\n no ip address\n shutdown\n!\n"

    config += BGP(network, routerID)
    

    if "RIP" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
        config += RIP()

    if "OSPF" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
        config += OSPF(network, routerID)

    config += "!\n!\n!\ncontrol-plane\n!\n!\nline con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline vty 0 4\n login\n!\n!\nend"
    return config
