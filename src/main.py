#Main startup file

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

from bot import *
import log

import discord

save = False

if len(sys.argv) <= 3 and len(sys.argv) > 1: #Bot called with arguments
    if sys.argv[1] == "--help":    #Display help message
        print("Lottery bot by Lino Bigatti.")
        print("Use: python3 -B src/main.py [options]")
        print("options:")
        print("    --help/-h       displays this message")
        print("    --silent/-s       logs on silent mode")
        print("    --save/-S       save to a secondary log file")
        exit()
    else:
        if sys.argv[1] in ("-s", "--silent"):   #Log silently
            log.silent = True
        elif sys.argv[1] in ("-S", "--save"):   #Save to a secondary log file
            save = True
        elif sys.argv[1] in ("-sS", "-Ss"):     #Do both
            log.silent = True
            save = True
        else:   #Not a valid option
            print("Unrecognized option: " + sys.argv[1] + ". Please use --help")
            exit()

        if len(sys.argv) == 3:
            if sys.argv[2] in ("-s", "--silent"):   #Log silently
                log.silent = True
            elif sys.argv[2] in ("-S", "--save"):   #Save to a secondary log file
                save = True
            else:   #Not a valid option
                print("Unrecognized option: " + sys.argv[2] + ". Please use --help")
                exit()

elif len(sys.argv) > 1:    #Too many arguments
    print("Too many arguments. Please use --help")
    exit()

log.start(save) #Start logging
bot.start() #epic complexity