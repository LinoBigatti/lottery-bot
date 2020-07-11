#Play the lottery

import random
from datetime import datetime, timedelta

import config
import embedfromjson
import bot

def dtToArray(dt):
    return [dt.days, dt.seconds//3600, (dt.seconds//60)%60]

def checkRateLimit(user, server):   #Check if a user is ratelimited
    try:
        lastUsed = server.rateList[user]    #Get last used date
        dt = datetime.utcnow() - lastUsed   #Difference in time
        minutes = (dt.seconds % 3600) // 60     #minutes
        if minutes < server.rateLimit:  #Check if its less
            rateDelta = timedelta(seconds = server.rateLimit * 60)      #Generate the time left
            minutesLeft = (lastUsed + rateDelta) - datetime.utcnow()

            return dtToArray(minutesLeft)
        else:
            return -1
    except KeyError:
        return -1

def setRatelimit(user, server):
    server.rateList[user] = datetime.utcnow()
    server.save()

def play(params, user, server):
    dt = checkRateLimit(user, server)
    if dt != -1:    #Check if user is ratelimited
        return embedfromjson.rateLimited(user, dt);

    result = random.choices(params[0], cum_weights=params[1])[0]    #Choose outcome
    
    setRatelimit(user, server);     #Set new ratelimit
    
    if result == "lose":    #Player lost
        return embedfromjson.lose(user)
    else:                   #Player won
        metadata = { "server": server.name, "prize": result[0], "hostId": str(result[1]) }
        metadata["user"] = bot.bot.client.get_user(user).name

        return embedfromjson.win(metadata)