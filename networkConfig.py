def border_router(network, router):
    for interface in network["routers"][router-1]["interface"]:
        if interface[0] != [] and network["routers"][interface[0][0]-1]["AS"] != network["routers"][router-1]["AS"]:
            return True
    return False

def belongs_to_subNet(network, router, subNet):
    return subNet in network["routers"][router-1]["subNets"]

def addressing_if(interface):
    address = "".join(interface[2:])
    config = f" ipv6 address {address}\n"
    return config

def OSPF_if(network,interface):
    config = " ipv6 ospf 10 area 0\n"
    for interfaceType in network["Constants"]["Bandwith"]:
        if interfaceType in interface[1] and interfaceType != "Reference":
            config += f" bandwith {network['Constants']['Bandwith'][interfaceType]}\n"
    return config

def RIP_if(network, router, interface):
    config = ""
    if interface[1] == "Loopback1" or network["routers"][interface[0][0]-1]["AS"] == network["routers"][router-1]["AS"]:
        config += " ipv6 rip BeginRIP enable\n"
    return config

def RIP():
    config = "ipv6 router rip BeginRIP\n redistribute connected\n!\n"
    return config

def passive_if(network, router):
    config = ""
    for interface in network["routers"][router-1]["interface"]:
        if interface[0] != [] and network["routers"][interface[0][0]-1]["AS"] != network["routers"][router-1]["AS"]:
            config += f" passive-interface {interface[1]}\n"
    return config


def OSPF(network, router):
    routerId = f"{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}"
    config = f"router ospf 10\n router-id {routerId}\n"
    config += passive_if(network, router)
    config += f" auto-cost reference-bandwidth {network['Constants']['Bandwith']['Reference']}\n"
    config += "!\n"
    return config

def BGP(network, router):
    routerId = f"{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}"
    config = f"router bgp {network['routers'][router-1]['AS']}\n no default ipv4-unicast\n bgp router-id {routerId}\n"
    neighbor_addresses = []
    for neighbor in network["adjDic"][router]:
        if network["routers"][neighbor-1]["AS"] == network["routers"][router-1]["AS"]:
            for interface in network["routers"][neighbor-1]["interface"]:
                if "Loopback" in interface[1]:
                    neighbor_address = interface[2]
                    break
            config += f" neighbor {neighbor_address} remote-as {network['routers'][neighbor-1]['AS']}\n"
            config += f" neighbor {neighbor_address} update-source Loopback1\n"
            neighbor_addresses.append(neighbor_address)
        else:
            pass
    config += " !\n address-family ipv4\n exit-address-family\n !\n address-family ipv6 unicast\n"
    for neighbor_address in neighbor_addresses:
        config += f"  neighbor {neighbor_address} activate\n"
    if border_router(network, router):
        config += f"  network {''.join(network['AS'][network['routers'][router-1]['AS']-1]['networkIP'])}\n"
    else:
        for subNet in network["AS"][network["routers"][router-1]["AS"]-1]["subNets"]:
            if belongs_to_subNet(network, router, subNet):
                config += f"  network {''.join(subNet)}\n"
    
    if border_router(network, router):
        for subNet in network["InterAS"]["subNets"]:
            if belongs_to_subNet(network, router, subNet):
                config += f"  network {''.join(subNet)}\n"
        
    config += " exit-address-family\n"
    return config 

def config_router(network, routerID):
    config = f"!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostname {network['routers'][routerID-1]['ID'][1]}\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\nip tcp synwait-time 5\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n"
    for interface in network["routers"][routerID-1]["interface"]:
        if interface[0] != [] or "Loopback" in interface[1]:
            config += f"interface {interface[1]}\n no ip address\n ipv6 enable\n negotiation auto\n{addressing_if(interface)}"
        
            if "RIP" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
                config += RIP_if(network, routerID, interface)

            if "OSPF" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
                config += OSPF_if(network,interface)

            config += "!\n"
        else:
            config += f"interface {interface[1]}\n no ip address\n shutdown\n negotiation auto\n!\n"

    config += BGP(network, routerID)

    if "RIP" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
        config += RIP()

    if "OSPF" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
        config += OSPF(network, routerID)

    config += "!\n!\n!\ncontrol-plane\n!\n!\nline con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline vty 0 4\n login\n!\n!\nend"
    return config
