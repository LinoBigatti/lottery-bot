#Play the lottery

import random
from datetime import datetime

import config
import embedfromjson
import bot

def checkRateLimit(user, server):   #Check if a user is ratelimited
    try:
        lastUsed = server.rateList[user]    #Get last used date
        dt = datetime.utcnow() - lastUsed   #Difference in time
        minutes = (dt.seconds % 3600) // 60     #minutes
        if minutes < server.rateLimit:  #Check if its less
            return True
        else:
            return False
    except KeyError:
        return False

def setRatelimit(user, server):
    server.rateList[user] = datetime.utcnow()
    server.save()

def play(params, user, server):
    if checkRateLimit(user, server):    #Check if user is ratelimited
        return embedfromjson.rateLimited(user);

    result = random.choices(params[0], cum_weights=params[1])[0]    #Choose outcome
    
    setRatelimit(user, server);     #Set new ratelimit

    print(result)
    if result == "lose":    #Player lost
        return embedfromjson.lose(user)
    else:                   #Player won
        metadata = { "server": server.name, "prize": result[0], "hostId": str(result[1]) }
        metadata["user"] = bot.bot.client.get_user(user).name

        return embedfromjson.win(metadata)