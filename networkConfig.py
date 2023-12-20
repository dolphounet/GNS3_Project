def addressing_if(network, router, interface):
    return 0 #string avec la commande à mettre dans la configuration de l'interface

def OSPF_if(network, router, interface):
    pass
    #return string avec les config protocol pour l'interface

def RIP_if(network, router, interface):
    pass

def config_router(network, router, router_cfg):
    config_if = ""
    for interface in network["routers"][router+1]["interface"]:
        if interface[0] != None:
            config_if += f"interface {interface[1]}\n{addressing_if(network, router, interface)}{OSPF_if(network, router, interface)}{RIP_if(network, router, interface)}"
        else:
            config_if += f"interface {interface[1]}\n no ip address\n shutdown\n negotiation auto\n"
    pass
