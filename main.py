from filesIO import read_from_json
from IPattribution import findAdjacency, createLinks


def main():
    network = read_from_json('Network_intent.json')
    for router in network["routers"]:
        print(router)

    findAdjacency(network)
    print(network["adjDic"])
    
    createLinks(network)

if __name__ == "__main__":
    main()

