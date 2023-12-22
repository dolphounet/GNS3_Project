from filesIO import readJson, writeCfg
from IPattribution import attributeIP
from networkConfig import config_router


def main():
    network = readJson('Network_Intent.json')
    attributeIP(network)
    #findAdjacency(network)
    print(network["AS"])
    writeCfg("config_R1", config_router(network, 5))
    
    #createLinks(network)

if __name__ == "__main__":
    main()

