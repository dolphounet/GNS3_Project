def addressing_if(network, router, interface):
    for interf in network["router"][router-1]["interface"]:
        if interf[1] == interface:
            address = "".join(interf[2])
    config = f" ipv6 address {address}\n"
    return config

def OSPF_if(network, router, interface):
    config = " ipv6 ospf 10 area 1\n"
    return config
    #return string avec les config protocol pour l'interface

def RIP_if(network, router, interface):
    config = " ipv6 rip BeginRIP enable\n"
    pass

def RIP(network, router):
    config = "ipv6 router rip BeginRIP\n redistribute connected\n!\n"
    return config

def OSPF(network, router):
    router-id = f"{network["routers"][router-1]["name"][0]}.{network["routers"][router-1]["name"][0]}.{network["routers"][router-1]["name"][0]}.{network["routers"][router-1]["name"][0]}"
    config = f"router ospf 10\n router-id {router-id}\n!\n"
    return config

def BGP(network, router):
    eBGP = False
    router-id = f"{network["routers"][router-1]["name"][0]}.{network["routers"][router-1]["name"][0]}.{network["routers"][router-1]["name"][0]}.{network["routers"][router-1]["name"][0]}"
    config = f"router bgp {network["routers"][router-1]["name"]}\n no default ipv4-unicast\n bgp router-id {router-id}\n"
    neighbor_addresses = []
    for neighbor in network["adjDic"][router]:
        if network["routers"][neighbor-1]["AS"] == network["routers"][router-1]["AS"]:
            for interface in network["routers"][neighbor-1]["interface"]:
                if "Loopback" in interface[1]:
                    neighbor_address = interface[2][0]
                    break
            config += f" neighbor {neighbor_address} remote-as {network["routers"][neighbor-1]["AS"]}\n"
            config += f" neighbor {neighbor_address} update-source Loopback1\n"
            neighbor_addresses.append(neighbor_address)
        else:
            pass
    config += " address-family ipv6 unicast\n"
    for neighbor_address in neighbor_addresses:
        config += f"  neighbor {neighbor_address} activate\n"
        for subNet in network["AS"][network["routers"][router-1]["AS"]-1]["subNet"]:
            config += f"  network {"".join(subNet)}\n"


def config_router(network, router, router_cfg):
    config = ""
    for interface in network["routers"][router-1]["interface"]:
        if interface[0] != []:
            config += f"interface {interface[1]}\n no ip address\n negotiation auto\n{addressing_if(network, router, interface)}"
        
            if "RIP" in network["AS"][network["router"][router-1]["AS"]-1]["IGP"]:
                config += RIP_if(network, router)

            if "OSPF" in network["AS"][network["router"][router-1]["AS"]-1]["IGP"]:
                config += OSPF_if(network, router)

            config += "!\n"
        else:
            config += f"interface {interface[1]}\n no ip address\n shutdown\n negotiation auto\n!\n"

    if "RIP" in network["AS"][network["router"][router-1]["AS"]-1]["IGP"]:
        config += RIP(network, router)

    if "OSPF" in network["AS"][network["router"][router-1]["AS"]-1]["IGP"]:
        config += OSPF(network, router)

    return config
