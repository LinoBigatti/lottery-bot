#Config loading and handling

import json

from server import server
import log

token = ""
name = ""
prefix = ""
ownerList = []

with open("config.json", "r") as f:     #Load main config file
    raw = json.loads(f.read())
    token = raw["token"]
    name = raw["name"]
    prefix = raw["prefix"]
    owners = raw["owners"]

    log.success("Loaded main config.")
