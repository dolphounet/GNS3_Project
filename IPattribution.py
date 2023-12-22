import filesIO

def attributionIP(network):
    pass

def createMatAdj(network):

    N = len(network["routers"])
    adjDic = {}

    for router in network["routers"]:
        adjDic[str(router["ID"][0])]=[]

        for interface in router["interface"]:
            for i in range(0,len(interface[0])):
                if interface[0][i] != []:
                    adjDic[str(router["ID"][0])].append(interface[0][i])

    network["adjDic"] = adjDic
