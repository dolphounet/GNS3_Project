def addressing_if(network, router, interface):
    pass 

def OSPF_if(network, router, interface):
    pass
    #return string avec les config protocol pour l'interface

def RIP_if(network, router, interface):
    pass

def RIP(network, router):
    config = "ipv6 router rip BeginRIP\n redistribute connected"
    return config

def OSPF(network, router):
    router-id = f"{network["routers"][router-1]["name"]}.{network["routers"][router-1]["name"]}.{network["routers"][router-1]["name"]}.{network["routers"][router-1]["name"]}"
    config = f"router ospf 10\n router-id {router-id}"
    return config

def BGP(network, router):
    config = f"router bgp {network["routers"][router-1]["name"]}\n no default ipv4-unicast\n "

def config_router(network, router, router_cfg):
    config = ""
    for interface in network["routers"][router-1]["interface"]:
        if interface[0] != []:
            config += f"interface {interface[1]}\n no ip address\n negotiation auto\n{addressing_if(network, router, interface)}{OSPF_if(network, router, interface)}{RIP_if(network, router, interface)}"
        else:
            config += f"interface {interface[1]}\n no ip address\n shutdown\n negotiation auto\n"

    if "RIP" in network["AS"][network["router"][router-1]["AS"]-1]["IGP"]:
        config += RIP(network, router)

    if "OSPF" in network["AS"][network["router"][router-1]["AS"]-1]["IGP"]:
        config += OSPF(network, router)

    return config
