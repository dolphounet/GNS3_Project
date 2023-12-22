import filesIO

def attributionIP(network):
    pass

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
    visited = []

    linkCountAS = []
    for i in range(0,len(network["AS"])):
        linkCountAS.append(0)

    for routerID in network["adjDic"] :
        visited.append(routerID)

        for connectedRouter in network["adjDic"][routerID]:
            if (network["routers"][connectedRouter-1]["AS"] == network["routers"][routerID-1]["AS"]) and (connectedRouter not in visited):
                
                linkCountAS[network["routers"][routerID-1]["AS"]-1] += 1

    