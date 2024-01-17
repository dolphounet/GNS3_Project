from filesIO import readJson, placeBot,writeCfg,config_router
from IPattribution import attributeIP



def main():

    # Path to GNS3 project
    # path = "/home/maxence/GNS3/projects/ProjetGNSDEOUFMALADE14ROUTEURS"
    path = "C:\Doc_User\Projets\Programming\GNS3_Local"

    # Récupération des informations du réseau
    network = readJson('Network_Intent.json')

    for elem in network["AS"]:
        print(elem)

    # Attribution des IP
    attributeIP(network)

    # Ecriture des fichiers config
    placeBot(network,path)
    '''
    for router in network["routers"]:
        writeCfg(f'output/i{router["ID"][0]}_startup-config.cfg', config_router(network, router["ID"][0]))
    '''
    for elem in network["InterAS"]:
        print(f'{elem} : {network["InterAS"][elem]}')
    
    
    

if __name__ == "__main__":
    main()

