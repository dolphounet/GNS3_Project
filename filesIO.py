import json

def read_from_json(file):
    Network_Intent = open('Network_Intent.json')
    data = json.load(Network_Intent)
    AS = data[AS]
    routers = data[routers]
    Network_Intent.close
    return (AS, routers)

def write_to_cfg(file):
    pass
