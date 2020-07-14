#Play the lottery

import random
from datetime import datetime, timedelta

import config
import embedfromjson
import bot

def dtFormat(dt):
    s = dt.total_seconds()
    if not s:
        return "0s"

    m, s_ = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    d = str(int(d)) + "d " if d else ''
    h = str(int(h)) + "h " if h else ''
    m = str(int(m)) + "m " if m else ''
    s_ = str(int(s_)) + "s" if s_ else ''

    return (d + h + m + s_).strip()


def checkRateLimit(user, server):   #Check if a user is ratelimited
    try:
        lastUsed = server.rateList[user.id]    #Get last used date

        rateLimit = server.rateLimit
        if user.premium_since:
            #User is nitro booster
            rateLimit = rateLimit // 2

        dt = datetime.utcnow() - lastUsed   #Difference in time
        minutes = (dt.seconds % 3600) // 60     #minutes

        if minutes < rateLimit:  #Check if its less
            t = timedelta(minutes=rateLimit) - dt

            return dtFormat(t)
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
        return embedfromjson.rateLimited(user.id, dt);

    result = random.choices(params[0], cum_weights=params[1])[0]    #Choose outcome
    
    setRatelimit(user.id, server);     #Set new ratelimit
    
    if result == "lose":    #Player lost
        return embedfromjson.lose(user.id)
    else:                   #Player won
        metadata = { "server": server.name, "prize": result[0], "hostId": str(result[1]) }
        metadata["user"] = user.name

        return embedfromjson.win(metadata)