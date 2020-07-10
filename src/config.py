#Config loading and handling

import json
from os import listdir

from server import server
import log

token = ""
name = ""
prefix = ""
ownerList = []

servers = {}

with open("config.json", "r") as f:     #Load main config file
    raw = json.loads(f.read())
    token = raw["token"]
    name = raw["name"]
    prefix = raw["prefix"]
    owners = raw["owners"]

    log.success("Loaded main config.")


for file in listdir("data/servers"):    #Load server specific configs
    if file != ".nodelete":     #File is useful
        with open("data/servers/" + file, "r") as f:
            raw = json.loads(f.read())
            tempServer = server(raw)
            servers[tempServer.id] = tempServer

            log.success("Loaded config for server " + str(tempServer.id) + ".")