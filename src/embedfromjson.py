#Build an embed from JSON data

import datetime
import discord
import re
import json


def lose(ping):  #Do a winning embed
    raw = {}

    with open("data/embeds/losing.json", "r") as f:
        raw = json.loads(f.read())

    raw["description"] = re.sub(r'{user}', "<@" + str(ping) + ">", raw["description"])

    embed = discord.Embed(\
        description = raw["description"],\
        type = "rich",\
        timestamp = datetime.datetime.now(),\
        color = raw["color"])

    return embed;

def win(metadata):  #Do a winning embed
    raw = {}
    
    with open("data/embeds/winning.json", "r") as f:
        raw = json.loads(f.read())

    raw["author"]["name"] = re.sub(r'{user}', metadata["user"], raw["author"]["name"])
    raw["footer"]["text"] = re.sub(r'{server}', metadata["server"], raw["footer"]["text"])  
    raw["description"] = re.sub(r'{prize}', metadata["prize"], raw["description"])
    raw["description"] = re.sub(r'{host}',"<@" + metadata["hostId"] + ">", raw["description"])

    embed = discord.Embed(\
        description = raw["description"],\
        type = "rich",\
        timestamp = datetime.datetime.now(),\
        color = raw["color"])
    embed.set_footer(\
        text = raw["footer"]["text"],\
        icon_url = raw["footer"]["icon_url"])
    embed.set_author(\
        name = raw["author"]["name"],\
        icon_url = raw["author"]["icon_url"])
    embed.set_image(url = raw["image"])

    return embed;