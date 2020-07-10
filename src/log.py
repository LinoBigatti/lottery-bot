#Log events

#Log format: [HH:MM:SS] [Log type] {message}
#Log files: latest.log, (optional) log-YYYY-MM-DD.log, (optional) console

from datetime import datetime
import json
import os
from colorama import Fore, Style

savePath = ""     #Path to second save file
silent = False     #Set to true for silent console

def start(save):    #Set up logging
    if os.path.isdir("logs/"):    #Check for logs directory
        pass
    else:                         #If it doesnt exist, make it
        os.makedirs("logs/") 

    open("logs/latest.log", "w+")    #Create latest.log file

    if save:    #If we need to save a second file
        global savePath
        date = datetime.now().date()    #Get the date

        #Open a file with format log-YYYY-MM-DD.log and set it as the secondary save path
        open("logs/log-" + str(date.year) + \
                     "-" + str(date.month) + \
                     "-" + str(date.day) + ".log", "w+")
        savePath = "logs/log-" + str(date.year) + \
                     "-" + str(date.month) + \
                     "-" + str(date.day) + ".log"


def log(text, logType, color):    #Log something
    time = datetime.now().time()    #Get the current time
    formatTime = str(time.hour) + ":" + str(time.minute) + ":" + str(time.second)    #Format the time as HH:MM:SS
    
    with open("logs/latest.log", "a") as f:    #Save in latest.log
        f.write("[" + formatTime + "] " + logType + text + "\n")

    if savePath != "":    #Save to secondary log file
        with open(savePath, "a") as f:
            f.write("[" + formatTime + "] " + logType + text + "\n")

    if not silent:    #Log to console
        print(Fore.RED + "[" + Fore.BLUE + formatTime + Fore.RED + "] "\
                       + color + logType + text)

def success(text):    #Log a success
    log(str(text), "[SUCCESS] ", Fore.GREEN)

def info(text):        #Log information
    log(str(text), "[INFO] ", Fore.BLUE)

def warning(text):    #Log warnings
    log(str(text), "[WARNING] ", Fore.YELLOW)

def error(text):
    log(str(text), "[ERROR] ", Fore.RED)

def stop(reason):            #Log a stop
    log("Bot stoping. Reason: " + reason, "", Fore.RED)