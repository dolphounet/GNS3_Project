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


def createLinks(network):
    # Crée les dictionnaires contenants les liens, le nb de liens et la liste des routeurs concernés

    ASlinks = []
    for i in range(0,len(network["AS"])):
        ASlinks.append({ "Count":0, "Links":[],"RouterList":[] })
        network["AS"][i]["subNets"] = []

    InterASlinks = { "Count":0, "Links": {}}
    network["InterAS"]["subNets"] = []

    visited = []
    for routerID in network["adjDic"] :
        visited.append(routerID)
        for connectedRouter in network["adjDic"][routerID]:
            if (network["routers"][connectedRouter-1]["AS"] == network["routers"][routerID-1]["AS"]) and (connectedRouter not in visited):
                ASlinks[network["routers"][routerID-1]["AS"]-1]["Count"] += 1
                ASlinks[network["routers"][routerID-1]["AS"]-1]["Links"].append([routerID,connectedRouter])
            elif connectedRouter not in visited :
                InterASlinks["Count"] += 1
                InterASlinks["Links"][(routerID,connectedRouter)] = None

    # Gestion des addresses des routeurs interAS

    for l in range(0,InterASlinks["Count"]):
        Subnet = network["InterAS"]["networkIP"][0]
        network["InterAS"]["subNets"].append([Subnet[:len(Subnet)-1] + str(l+1) + "::","/"+str(int(network["InterAS"]["networkIP"][1][1:])+16)])

    # Gestion des addresses des routeurs des AS

    for j in range(0,len(ASlinks)):
        for k in range(0,ASlinks[j]["Count"]):
            Subnet = network["AS"][j]["networkIP"][0]
            network["AS"][j]["subNets"].append([Subnet[:len(Subnet)-1] + str(k+1) + "::","/"+str(int(network["AS"][j]["networkIP"][1][1:])+16)])
    
    for router in network["routers"]:
        ASlinks[router["AS"]-1]["RouterList"].append(router["ID"][0])
        router["subNets"]=[]

    # Appliquer les adresses de loopback

    for i in range(0,len(ASlinks)):

        loopbackNetIP = network["AS"][i]["loopbackNetworkIP"][0]
        loopbackRouterAdd = 1

        for routerID in ASlinks[i]["RouterList"]:
            network["routers"][routerID-1]["interface"].append([[],"Loopback1", loopbackNetIP[:len(loopbackNetIP)-1] + str(loopbackRouterAdd) + "::","/128"])
            loopbackRouterAdd += 1

    return ASlinks,InterASlinks

def attributeIP(network):

    findAdjacency(network)
    ASlinks,InterASlinks = createLinks(network)

    # Gestion pour un AS
    for i in range(0,len(ASlinks)):
        for j in range(0,len(ASlinks[i]["Links"])):
            currentNet = network["AS"][i]["subNets"][j][0]
            (ID1,ID2) = ASlinks[i]["Links"][j]

            for interface in network["routers"][ID1-1]["interface"]:
                if interface[0] == [ID2] :
                    interface.append(currentNet+"1")
                    interface.append(network["AS"][i]["subNets"][j][1])
                    network["routers"][ID1-1]["subNets"].append([currentNet,network["AS"][i]["subNets"][j][1]])
                    
            for interface in network["routers"][ID2-1]["interface"]:
                if interface[0] == [ID1] :
                    interface.append(currentNet+"2")
                    interface.append(network["AS"][i]["subNets"][j][1])
                    network["routers"][ID2-1]["subNets"].append([currentNet,network["AS"][i]["subNets"][j][1]])

    # Gestion pour les InterAS
    for k in range(0,len(InterASlinks["Links"])):
        currentNet = network["InterAS"]["subNets"][k][0]
        ID1,ID2 = list(InterASlinks["Links"].keys())[k]
        InterASlinks["Links"][(ID1,ID2)] = ([currentNet+"1",network["InterAS"]["subNets"][k][1]],[currentNet+"2",network["InterAS"]["subNets"][k][1]])

        for interface in network["routers"][ID1-1]["interface"]:
            if interface[0] == [ID2] :
                interface.append(currentNet+"1")
                interface.append(network["InterAS"]["subNets"][k][1])
                network["routers"][ID1-1]["subNets"].append([currentNet,network["InterAS"]["subNets"][k][1]])         
                    
        for interface in network["routers"][ID2-1]["interface"]:
            if interface[0] == [ID1] :
                interface.append(currentNet+"2")
                interface.append(network["InterAS"]["subNets"][k][1])
                network["routers"][ID2-1]["subNets"].append([currentNet,network["InterAS"]["subNets"][k][1]])

    network["InterAS"]["InterASlinks"] = InterASlinks
    
