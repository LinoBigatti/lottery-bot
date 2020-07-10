#Config loading and handling

import json
from os import listdir

from server import server

token = ""
name = ""
prefix = ""
ownerList = []

servers = {}

with open("config.json", "r") as f:
    raw = json.loads(f.read())
    token = raw["token"]
    name = raw["name"]
    prefix = raw["prefix"]
    owners = raw["owners"]

for file in listdir("data/servers"):
    if file != ".nodelete":
        with open("data/servers/" + file, "r") as f:
            raw = json.loads(f.read())
            tempServer = server(raw)
            servers[tempServer.id] = tempServer