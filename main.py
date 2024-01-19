from filesIO import readJson, placeBot,writeCfg,config_router
from IPattribution import attributeIP



def main():

    # Path to GNS3 project
    # path = "/home/maxence/GNS3/projects/ProjetGNSDEOUFMALADE14ROUTEURS"
    path = "C:\Doc_User\Projets\Programming\GNS3_Local\projetCommunities"

    # Récupération des informations du réseau
    network = readJson('Network_Intent.json')
    
    # Attribution des IP
    attributeIP(network)

    # Ecriture des fichiers config
    placeBot(network,path)

    for elem in network["InterAS"]["InterASlinks"]["Links"]:
        print(f'{elem} : {network["InterAS"]["InterASlinks"]["Links"][elem]}')

if __name__ == "__main__":
    main()

