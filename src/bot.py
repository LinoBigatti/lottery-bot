#Bot class & basic async events

import config
import log
import lottery
import server as server_

import discord
import sys
import re

class main:
    def __init__(self, token, name, prefix):    #Init bot variables
        self.client = discord.Client()
        self.token = token
        self.name = name
        self.prefix = prefix
    
    def start(self):    #Run the bot
        self.client.run(self.token)

bot = main(config.token, config.name, config.prefix)  #Get a main bot instance

@bot.client.event
async def on_ready():   #Log when bot starts
    log.success("Started bot.")
    log.info("Bot info:")
    log.info(bot.client.user.name)
    log.info(bot.client.user.id)

@bot.client.event
async def on_message(message):  #Handle messages
    if message.author == bot.client.user:   #Do not reply to oneself
        return

    if message.author.id in config.owners and message.content == bot.prefix + "stop --instant": #High priority stop
        await message.channel.send("High priority stop requested. Stopping...")
        log.stop("Bot owner requested instant stop")
        sys.exit(0)

    if message.content.startswith(bot.prefix):    #Handle command
        log.info("Bot command called by " + message.author.name + ". Full command: " + message.content)
        
        server = config.servers[message.guild.id]
        rawCommand = message.content[len(bot.prefix):].lower()    #Take prefix out
        
        if (rawCommand == "lotto" or rawCommand == "lottery") and message.channel.id == server.lotteryChannel:    #Play the lottery
            await message.channel.send(embed=lottery.play(server.lottoParams, message.author.id, server))
        elif rawCommand.startswith("set "):
            if not message.author.permissions_in(message.channel).manage_guild: #User needs manage guild
                await message.channel.send("ERROR: You need to be server admin.")
                return

            variable = rawCommand[4:]
            if variable.startswith("channel"):
                await message.channel.send(server.setChannel(message.channel.id))
            elif variable.startswith("rate "):
                rate = variable[5:]

                await message.channel.send(server.setRate(rate))
            else:
                await message.channel.send("Unknown variable.")
        elif rawCommand.startswith("prize "):
            if not message.author.permissions_in(message.channel).manage_guild: #User needs manage guild
                await message.channel.send("ERROR: You need to be server admin.")
                return

            action = rawCommand[6:]
            if action.startswith("add "):
                params = action[4:]
                prize = re.findall(r'".+?"', params)
                weight, host = params[len(prize[0]) + 1:].split(' ')
                
                await message.channel.send(server.addPrize([prize[0][1:][:-1], host], weight))
            if action.startswith("delete "):
                i = action[7:]

                await message.channel.send(server.deletePrize(i))
            if action.startswith("list"):
                await message.channel.send(server.listPrizes())

@bot.client.event
async def on_guild_join(guild):
    params = {"id": guild.id, "name": guild.name, "lotto-channel": 0, "rate": 0, "rate-list": {}, "lotto-parameters": [["lose"], [1000000]]}
    tmpServer = server_.server(params)

    tmpServer.save()
    config.servers[guild.id] = tmpServer