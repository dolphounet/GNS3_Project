from filesIO import readJson, writeCfg
from IPattribution import attributeIP
from networkConfig import config_router


def main():
    network = readJson('Network_Intent.json')
    attributeIP(network)
    #findAdjacency(network)
    print(network["AS"])
    writeCfg("config_R1", config_router(network, 4))
    
    for router in network["routers"]:
        print(router)

    #createLinks(network)

if __name__ == "__main__":
    main()

