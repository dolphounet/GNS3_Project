import json

def readJson(file):
    Network_Intent = open(file)
    network = json.load(Network_Intent)
    Network_Intent.close
    return network

def writeCfg(file, config):
    with open(file, "w") as configFile:
        configFile.write(config)
    return
