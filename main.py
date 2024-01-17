from filesIO import readJson
from IPattribution import attributeIP
from networkConfig import config_router



def main():

    # Récupération des informations du réseau
    network = readJson('Network_Intent.json')

    # Attribution des IP
    attributeIP(network)

    # Ecriture de la configuration avec telnet
    for router in network["routers"]:
        config_router(network, router["ID"][0])

if __name__ == "__main__":
    main()

