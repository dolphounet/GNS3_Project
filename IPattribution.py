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

    
    
    return adjMat




def test():
    network = filesIO.read_from_json('Network_Intent.json')
    print(createMatAdj(network))
    return 0

test()