import telnetlib
import time


def writeLine(tn, line):
    tn.write(line.encode()+b"\r\n")
    time.sleep(0.1)

def border_router(network, router):
    for interface in network["routers"][router-1]["interface"]:
        if interface[0] != [] and network["routers"][interface[0][0]-1]["AS"] != network["routers"][router-1]["AS"]:
            return True
    return False

def belongs_to_subNet(network, router, subNet):
    return subNet in network["routers"][router-1]["subNets"]

def addressing_if(tn, interface):
    address = "".join(interface[2:])
    writeLine(tn, f"interface {interface[1]}")
    writeLine(tn, "ipv6 enable")
    writeLine(tn, f"ipv6 address {address}")


def passive_if(network, router):
    config = ""
    for interface in network["routers"][router-1]["interface"]:
        if interface[0] != [] and network["routers"][interface[0][0]-1]["AS"] != network["routers"][router-1]["AS"]:
            config += f" passive-interface {interface[1]}\n"
    return config

def OSPF_if(tn, network,interface):
    writeLine(tn, "ipv6 ospf 10 area 0")
    for interfaceType in network["Constants"]["Bandwith"]:
        if interfaceType in interface[1] and interfaceType != "Reference":
            writeLine(tn, f"bandwidth {network['Constants']['Bandwith'][interfaceType]}")

def OSPF(network, router):
    routerId = f"{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}"
    config = f"ipv6 router ospf 10\n router-id {routerId}\n"
    config += passive_if(network, router)
    config += f" auto-cost reference-bandwidth {network['Constants']['Bandwith']['Reference']}\n"
    config += "!\n"
    return config

def RIP_if(tn, network, router, interface):
    if interface[1] == "Loopback1" or network["routers"][interface[0][0]-1]["AS"] == network["routers"][router-1]["AS"]:
        writeLine(tn, "ipv6 rip BeginRIP enable")

def RIP():
    config = "ipv6 router rip BeginRIP\n redistribute connected\n!\n"
    return config

def BGP(network, router):
    routerId = f"{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}"
    config = f"router bgp {network['routers'][router-1]['AS']}\n no bgp default ipv4-unicast\n bgp router-id {routerId}\n"
    neighbor_addresses = []
    for rtr in network["routers"]:
        neighbor = rtr["ID"][0]
        if neighbor != router:
            if network["routers"][neighbor-1]["AS"] == network["routers"][router-1]["AS"]:
                for interface in network["routers"][neighbor-1]["interface"]:
                    if "Loopback" in interface[1]:
                        neighbor_address = interface[2]
                        break
                config += f" neighbor {neighbor_address} remote-as {network['routers'][neighbor-1]['AS']}\n"
                config += f" neighbor {neighbor_address} update-source Loopback1\n"
                neighbor_addresses.append(neighbor_address)
            elif neighbor in network["adjDic"][router]:
                for interface in network["routers"][neighbor-1]["interface"]:
                    if router in interface[0]:
                        neighbor_address = interface[2]
                        break
                config += f" neighbor {neighbor_address} remote-as {network['routers'][neighbor-1]['AS']}\n"
                neighbor_addresses.append(neighbor_address)

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
    port = network["routers"][routerID-1]["Port"]
    host = "localhost"
    tn = telnetlib.Telnet(host, port)
    writeLine(tn, "enable")
    writeLine(tn, "write erase") #To erase current configuration
    writeLine(tn, "") #To confirm the configuration deletion
    tn.read_until(b"Erase of nvram: complete") #Waiting for the deletion to finish
    writeLine(tn, "conf t")
    writeLine(tn, "ipv6 unicast-routing")
    for interface in network["routers"][routerID-1]["interface"]:
        if interface[0] != [] or "Loopback" in interface[1]:
            addressing_if(tn, interface)
            if "RIP" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
                RIP_if(tn, network, routerID, interface)

            if "OSPF" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
                OSPF_if(tn, network,interface)
            writeLine(tn, "no shutdown")
            writeLine(tn, "exit")
    tn.close()
    """
    config += BGP(network, routerID)

    if "RIP" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
        config += RIP()

    if "OSPF" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
        config += OSPF(network, routerID)

    config += "!\n!\n!\ncontrol-plane\n!\n!\nline con 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline aux 0\n exec-timeout 0 0\n privilege level 15\n logging synchronous\n stopbits 1\nline vty 0 4\n login\n!\n!\nend"
    
    return config
    """
