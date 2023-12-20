import filesIO

def attributionIP(network):
    pass

def createMatAdj(network):

    N = len(network["routers"])
    adjMat = []

    for i in range(0,N):
        adjMat.append([])
        for j in range(0,N):
            adjMat[i].append(0)

    for router in network["routers"]:

        for interface in router["interface"]:

            for i in range(0,len(interface[0])):
                if interface[0][i] != []:
                    adjMat[router["name"]-1][interface[0][i]-1] = 1

    return adjMat