#Play the lottery

import random
from datetime import datetime

import config
import embedfromjson
import bot

def checkRateLimit(user, server):
    try:
        lastUsed = server.rateList[user]
        dt = datetime.utcnow() - lastUsed
        minutes = (dt.seconds % 3600) // 60
        if minutes < server.rateLimit:
            return True
        else:
            return False
    except KeyError:
        return False

def setRatelimit(user, server):
    server.rateList[user] = datetime.utcnow()
    server.save()

def play(params, user, server):
    if checkRateLimit(user, server):
        return "Ratelimited."

    result = random.choices(params[0], cum_weights=params[1])[0]
    
    setRatelimit(user, server);

    if result == "lose":
        return embedfromjson.lose(user)
    else:
        metadata = { "server": server.name, "prize": result[0], "hostId": str(result[1]) }
        metadata["user"] = bot.bot.client.get_user(user).name
        return embedfromjson.win(metadata)