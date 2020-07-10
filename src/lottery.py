#Play the lottery

import random
import config
from datetime import datetime


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
        return "You lost"
    else:
        return result