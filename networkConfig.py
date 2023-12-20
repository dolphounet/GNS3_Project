def addressing_if(network, router, interface):
    pass 

def OSPF_if(network, router, interface):
    pass
    #return string avec les config protocol pour l'interface

def RIP_if(network, router, interface):
    pass

def RIP(network, router):
    pass

def OSPF(network, router):
    pass

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
