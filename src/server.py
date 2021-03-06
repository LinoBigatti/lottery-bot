#Server class

import json
import datetime
import pymongo

import log 

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["lottery"]
servers = db["servers"]

class DateTimeEncoder(json.JSONEncoder):    #Encode datetime objects
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

class server:       #Server configs
    def __init__(self, params):     #Create a new instance
        self.id = params["_id"]
        self.lotteryChannel = params["lotto-channel"]
        self.rateLimit = params["rate"]
        self.rateList = params["rate-list"]
        self.lottoParams = params["lotto-parameters"]
        self.name = params["name"]

    def save(self):     #Save this instance
        params = {}
        params["_id"] = str(self.id)
        params["name"] = self.name
        params["lotto-channel"] = self.lotteryChannel
        params["rate"] = self.rateLimit
        params["rate-list"] = self.rateList
        params["lotto-parameters"] = self.lottoParams
        
        try:
            servers.insert(params)
        except pymongo.errors.DuplicateKeyError:
            return 1

        log.success("Saved configuration for server " + str(self.id) + ".")

    def edit(self):     #Edit this instance
        params = {}
        params["_id"] = str(self.id)
        params["name"] = self.name
        params["lotto-channel"] = self.lotteryChannel
        params["rate"] = self.rateLimit
        params["rate-list"] = self.rateList
        params["lotto-parameters"] = self.lottoParams
        
        print(self.id)
        try:
            servers.update_one({"_id": str(self.id)}, {"$set": params})
        except pymongo.errors.DuplicateKeyError:
            return 1

        log.success("Edited configuration for server " + str(self.id) + ".")   

    def setRate(self, rate):    #Set ratelimit
        daysIndex = rate.find('d')
        hoursIndex = rate.find('h')
        minutesIndex = rate.find('m')

        days = 0
        hours = 0
        minutes = 0

        #Get time data
        if daysIndex != -1:
            days = int(rate[daysIndex - 2:daysIndex])
        if hoursIndex != -1:
            hours = int(rate[hoursIndex - 2:hoursIndex])
        if minutesIndex != -1:
            minutes = int(rate[minutesIndex - 2:minutesIndex])

        #Convert to minutes and save
        self.rateLimit = (days * 24 + hours) * 60 + minutes
        self.edit()

        log.info("New ratelimit for server " + str(self.id) + ": " + str(self.rateLimit) + " minutes.")
        return "New rate limit: " + str(days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes. (Total minutes: " + str(self.rateLimit) + ")"

    def setChannel(self, channel):  #Set the lottery channel
        self.lotteryChannel = channel
        self.edit()

        log.info("New lotto channel for server " + str(self.id) + ": " + str(self.lotteryChannel) + ".")
        return "Lottery set to use this channel."

    def addPrize(self, prize, weight):      #Add a new prize
        place = len(self.lottoParams[0]) - 1    #Get a place for it

        #Insert it
        self.lottoParams[0].insert(place, prize)
        if place != 0:
            self.lottoParams[1].insert(place, int(weight) + self.lottoParams[1][place - 1])
        else:
            self.lottoParams[1].insert(place, int(weight))

        self.edit()

        log.info("New prize added on server " + str(self.id) + ": " + prize[0] + ", hosted by " + prize[1] + ".")
        return "Prize \"" + prize[0] + "\" added with a probability of " + weight + "/1,000,000 at index " + str(place) + "." 

    def deletePrize(self, i_):  #Delete a prize
        i = int(i_)
        deleted = self.lottoParams[0].pop(i)
        self.lottoParams[1].pop(i)
        self.edit()

        log.info("Prize \"" + deleted[0] + "\" deleted on server " + str(self.id) + ".")
        return "Prize \"" + deleted[0] + "\" deleted."

    def listPrizes(self):       #Generate a list of prizes
        list_ = "Current prizes:\n"
        for i in range(len(self.lottoParams[0])):
            list_ += '\t"' + self.lottoParams[0][i][0] + '": '
            list_ += str(self.lottoParams[1][i]) + "/1,000,000 chance. Id: " + str(i)
            list_ += "\n"

        return list_

def find(guild):    #Find a server
    data = servers.find_one({"_id": str(guild.id)})

    if data:
        found = server(data)
        return found
    else:
        params = {"_id": str(guild.id), "name": guild.name, "lotto-channel": 0, "rate": 0, "rate-list": {}, "lotto-parameters": [["lose"], [1000000]]}
        tmpServer = server(params)
        tmpServer.save()

        log.info("New server: " + str(guild.id) + " (" + guild.name + ")")
        return tmpServer
