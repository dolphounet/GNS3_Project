import json
import os
from networkConfig import config_router

def readJson(file):
    Network_Intent = open(file)
    network = json.load(Network_Intent)
    Network_Intent.close
    return network

def writeCfg(filePath, config):
    with open(filePath, "w") as configFile:
        configFile.write(config)
    return

def placeBot(network,projectPath):
    #projectPath += "/project-files/dynamips"
    filesPath = {}

    for dirPath, dirs, files in os.walk(projectPath):
        for file in files:
            if file.endswith('.cfg'):
                filesPath[file] = os.path.join(dirPath, file)

    for router in network["routers"]:
        writeCfg(filesPath[f'i{router["ID"][0]}_startup-config.cfg'], config_router(network, router["ID"][0]))