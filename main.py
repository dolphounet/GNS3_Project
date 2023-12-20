from filesIO import read_from_json


def main():
    network = read_from_json('Network_intent.json')
    print(network["AS"])

if __name__ == "__main__":
    main()

