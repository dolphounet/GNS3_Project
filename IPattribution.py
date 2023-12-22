import filesIO

def findAdjacency(network):
    adjDic = {}

    for router in network["routers"]:
        adjDic[router["ID"][0]]=[]

        for interface in router["interface"]:
            for i in range(0,len(interface[0])):
                if interface[0][i] != []:
                    adjDic[router["ID"][0]].append(interface[0][i])

    network["adjDic"] = adjDic

    return

def createLinks(network):

    ASlinks = []
    for i in range(0,len(network["AS"])):
        ASlinks.append({ "Count":0, "Links":[] })
        network["AS"][i]["subNets"] = []

    visited = []
    for routerID in network["adjDic"] :
        visited.append(routerID)
        for connectedRouter in network["adjDic"][routerID]:
            if (network["routers"][connectedRouter-1]["AS"] == network["routers"][routerID-1]["AS"]) and (connectedRouter not in visited):
                ASlinks[network["routers"][routerID-1]["AS"]-1]["Count"] += 1
                ASlinks[network["routers"][routerID-1]["AS"]-1]["Links"].append([routerID,connectedRouter])

    for j in range(0,len(ASlinks)):
        for k in range(0,ASlinks[j]["Count"]):
            Subnet = network["AS"][j]["networkIP"][0]
            network["AS"][j]["subNets"].append([Subnet[:len(Subnet)-1] + str(k+1) + "::",network["AS"][j]["networkIP"][1]])

    return ASlinks

def attributeIP(network):

    findAdjacency(network)
    ASlinks = createLinks(network)

    return
    