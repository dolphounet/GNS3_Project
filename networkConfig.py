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


def passive_if(tn, network, router):
    for interface in network["routers"][router-1]["interface"]:
        if interface[0] != [] and network["routers"][interface[0][0]-1]["AS"] != network["routers"][router-1]["AS"]:
            writeLine(tn, f"passive-interface {interface[1]}")

def OSPF_if(tn, network,interface):
    writeLine(tn, "ipv6 ospf 10 area 0")
    for interfaceType in network["Constants"]["Bandwith"]:
        if interfaceType in interface[1] and interfaceType != "Reference":
            writeLine(tn, f"bandwidth {network['Constants']['Bandwith'][interfaceType]}")

def OSPF(tn, network, router):
    routerId = f"{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}"
    writeLine(tn, "ipv6 router ospf 10")
    writeLine(tn, f"router-id {routerId}")
    passive_if(tn, network, router)
    writeLine(tn, f"auto-cost reference-bandwidth {network['Constants']['Bandwith']['Reference']}")
    writeLine(tn, "exit")

def RIP_if(tn, network, router, interface):
    if interface[1] == "Loopback1" or network["routers"][interface[0][0]-1]["AS"] == network["routers"][router-1]["AS"]:
        writeLine(tn, "ipv6 rip BeginRIP enable")

def RIP(tn):
    writeLine(tn, "ipv6 router rip BeginRIP")
    writeLine(tn, "redistribute connected")
    writeLine(tn, "exit")

def BGP(tn, network, router):
    routerId = f"{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}.{network['routers'][router-1]['ID'][0]}"
    writeLine(tn, f"router bgp {network['routers'][router-1]['AS']}")
    writeLine(tn, "no bgp default ipv4-unicast")
    writeLine(tn, f"bgp router-id {routerId}")
    neighbor_addresses = []
    for rtr in network["routers"]:
        neighbor = rtr["ID"][0]
        if neighbor != router:
            if network["routers"][neighbor-1]["AS"] == network["routers"][router-1]["AS"]:
                for interface in network["routers"][neighbor-1]["interface"]:
                    if "Loopback" in interface[1]:
                        neighbor_address = interface[2]
                        break
                writeLine(tn, f"neighbor {neighbor_address} remote-as {network['routers'][neighbor-1]['AS']}")
                writeLine(tn, f"neighbor {neighbor_address} update-source Loopback1")
                neighbor_addresses.append(neighbor_address)
            elif neighbor in network["adjDic"][router]:
                for interface in network["routers"][neighbor-1]["interface"]:
                    if router in interface[0]:
                        neighbor_address = interface[2]
                        break
                writeLine(tn, f"neighbor {neighbor_address} remote-as {network['routers'][neighbor-1]['AS']}")
                neighbor_addresses.append(neighbor_address)

    writeLine(tn, "address-family ipv6 unicast")
    for neighbor_address in neighbor_addresses:
        writeLine(tn, f"neighbor {neighbor_address} activate")
    if border_router(network, router):
        writeLine(tn, f"network {''.join(network['AS'][network['routers'][router-1]['AS']-1]['networkIP'])}")
    else:
        for subNet in network["AS"][network["routers"][router-1]["AS"]-1]["subNets"]:
            if belongs_to_subNet(network, router, subNet):
                writeLine(tn, f"network {''.join(subNet)}")
    if border_router(network, router):
        for subNet in network["InterAS"]["subNets"]:
            if belongs_to_subNet(network, router, subNet):
                writeLine(tn, f"network {''.join(subNet)}")
        
    writeLine(tn, "exit-address-family")
    writeLine(tn, "exit") 

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

    BGP(tn, network, routerID)

    if "RIP" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
        RIP(tn)

    if "OSPF" in network["AS"][network["routers"][routerID-1]["AS"]-1]["IGP"]:
        OSPF(tn, network, routerID)
    writeLine(tn, "end")
    writeLine(tn, "write") #To write the configuration in order not to lose it the next time
    tn.read_until(b"[OK]") #Waiting for the writing to complete
    tn.close()
