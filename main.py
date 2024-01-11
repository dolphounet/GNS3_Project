from filesIO import readJson, placeBot
from IPattribution import attributeIP



def main():

    # Récupération des informations du réseau
    network = readJson('Network_Intent.json')

    # Attribution des IP
    attributeIP(network)

    # Ecriture des fichiers config
    placeBot(network,input("Input a file path : "))

if __name__ == "__main__":
    main()

