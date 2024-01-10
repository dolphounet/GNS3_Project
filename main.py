from filesIO import readJson, writeCfg
from IPattribution import attributeIP
from networkConfig import config_router


def main():

    # Récupération des informations du réseau
    network = readJson('Network_Intent.json')

    # Attribution des IP
    attributeIP(network)

    #print(network)
    
    # Ecriture des fichiers config
    for router in network["routers"]:
        writeCfg(f'i{router["ID"][0]}_startup-config.cfg', config_router(network, router["ID"][0]))


if __name__ == "__main__":
    main()

