#Config loading and handling

import json
from os import listdir
import datetime

token = ""
name = ""
prefix = ""
ownerList = []

servers = {}

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

class server:
    def __init__(self, params):
        self.id = params["id"]
        self.lotteryChannel = params["lotto-channel"]
        self.rateLimit = params["rate"]
        self.rateList = params["rate-list"]
        self.lottoParams = params["lotto-parameters"]

    def save(self):
        params = {}
        params["id"] = self.id
        params["lotto-channel"] = self.lotteryChannel
        params["rate"] = self.rateLimit
        params["rate-list"] = self.rateList
        params["lotto-parameters"] = self.lottoParams

        with open("data/servers/" + str(self.id) + ".json", "w") as f:
            json.dump(params, f, cls=DateTimeEncoder)

    def setRate(self, rate):
        daysIndex = rate.find('d')
        hoursIndex = rate.find('h')
        minutesIndex = rate.find('m')

        days = 0
        hours = 0
        minutes = 0

        if daysIndex != -1:
            days = int(rate[daysIndex - 2:daysIndex])
        if hoursIndex != -1:
            hours = int(rate[hoursIndex - 2:hoursIndex])
        if minutesIndex != -1:
            minutes = int(rate[minutesIndex - 2:minutesIndex])

        self.rateLimit = (days * 24 + hours) * 60 + minutes
        self.save()

        return "New rate limit: " + str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes. (Total minutes: " + str(self.rateLimit) + ")"

    def setChannel(self, channel):
        self.channel = channel
        self.save()

        return "Lottery set to use this channel."

    def addPrize(self, prize, weight):
        place = len(self.lottoParams[0]) - 1

        self.lottoParams[0].insert(place, prize)
        if place != 0:
            self.lottoParams[1].insert(place, int(weight) + self.lottoParams[1][place])
        else:
            self.lottoParams[1].insert(place, int(weight))

        self.save()
        print(self.lottoParams)

        return "Prize \"" + prize + "\" added with a probability of " + weight + "/1,000,000 at index " + str(place) + "." 


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