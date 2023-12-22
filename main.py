from filesIO import read_from_json
from IPattribution import createMatAdj


def main():
    network = read_from_json('Network_intent.json')
    #print(network["AS"])
    createMatAdj(network)
    print(network["adjDic"])

if __name__ == "__main__":
    main()

