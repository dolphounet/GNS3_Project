def addressing_if(network, router, interface):
    address = "".join(interface[2:])
    config = f" ipv6 address {address}\n"
    return config

def OSPF_if(network, router, interface):
    config = " ipv6 ospf 10 area 1\n"
    return config
    #return string avec les config protocol pour l'interface

def RIP_if(network, router, interface):
    config = " ipv6 rip BeginRIP enable\n"
    return config

def RIP(network, router):
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
    for subNet in network["AS"][network["routers"][router-1]["AS"]-1]["subNets"]:
        config += f"  network {''.join(subNet)}\n"
    config += " exit-address-family\n"
    return config 

def config_router(network, router):
    config = f"!\n!\n!\n!\n\n!\n! Last configuration change at 16:58:26 UTC Tue Dec 19 2023\n!\nversion 15.2\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\n!\nhostname {network['routers'][router-1]['ID'][1]}\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nno aaa new-model\nno ip icmp rate-limit unreachable\nip cef\n!\n!\n!\n!\n!\n!\nno ip domain lookup\nipv6 unicast-routing\nipv6 cef\n!\n!\nmultilink bundle-name authenticated\n!\n!\n!\n!\n!\n!\n!\n!\n!\nip tcp synwait-time 5\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n"
    for interface in network["routers"][router-1]["interface"]:
        if interface[0] != [] or "Loopback" in interface[1]:
            config += f"interface {interface[1]}\n no ip address\n ipv6 enable\n negotiation auto\n{addressing_if(network, router, interface)}"
        
            if "RIP" in network["AS"][network["routers"][router-1]["AS"]-1]["IGP"]:
                config += RIP_if(network, router, interface[1])

            if "OSPF" in network["AS"][network["routers"][router-1]["AS"]-1]["IGP"]:
                config += OSPF_if(network, router, interface[1])

            config += "!\n"
        else:
            config += f"interface {interface[1]}\n no ip address\n shutdown\n negotiation auto\n!\n"

    if "RIP" in network["AS"][network["routers"][router-1]["AS"]-1]["IGP"]:
        config += RIP(network, router)

    if "OSPF" in network["AS"][network["routers"][router-1]["AS"]-1]["IGP"]:
        config += OSPF(network, router)

    config += BGP(network, router)

    return config
