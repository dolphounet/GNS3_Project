import json

def read_from_json(file):
    Network_Intent = open(file)
    network = json.load(Network_Intent)
    Network_Intent.close
    return network

def write_to_cfg(file):
    pass
