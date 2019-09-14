# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway(yes, Internet). """

from datetime import datetime

import re
import os
import speedtest
import subprocess
from telethon import functions
from userbot import CMD_HELP
from userbot.events import register, errors_handler


@register(outgoing=True, pattern="^.speed$")
@errors_handler
async def speedtst(spd):
    """ For .speed command, use SpeedTest to check server speeds. """
    if not spd.text[0].isalpha() and spd.text[0] not in ("/", "#", "@", "!"):
        await spd.edit("`Running speed test . . .`")
        test = speedtest.Speedtest()

        test.get_best_server()
        test.download()
        test.upload()
        test.results.share()
        result = test.results.dict()

    await spd.edit("`"
                   "Started at "
                   f"{result['timestamp']} \n\n"
                   "Download "
                   f"{speed_convert(result['download'])} \n"
                   "Upload "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping "
                   f"{result['ping']} \n"
                   "ISP "
                   f"{result['client']['isp']}"
                   "`")


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.nearestdc$")
@errors_handler
async def neardc(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        """ For .nearestdc command, get the nearest datacenter information. """
        result = await event.client(functions.help.GetNearestDcRequest())
        await event.edit(f"Country : `{result.country}` \n"
                         f"Nearest Datacenter : `{result.nearest_dc}` \n"
                         f"This Datacenter : `{result.this_dc}`")


@register(outgoing=True, pattern="^.ping$")
@errors_handler
async def pingme(pong):
    """ FOr .pingme command, ping the userbot from any chat.  """
    if not pong.text[0].isalpha() and pong.text[0] not in ("/", "#", "@", "!"):
        #hostname = "1.1.1.1" #cloudfare's stable dns server
        #start = datetime.now()
        #response = os.system("ping -c 1 " + hostname)
        #end = datetime.now()
        #duration = (end - start).microseconds / 1000
        duration = 0
        out = subprocess.check_output("ping -c 1 1.1.1.1", shell=True).decode()
        listOut = out.splitlines()
        splitOut = listOut[1].split(' ')
        stringtocut = ""
        for line in splitOut:
            if(line.startswith('time=')):
                stringtocut=line
        newstr=stringtocut.split(' ')
        duration = float(newstr[1])
        await pong.edit("Ping speed: %sms" % (duration))


CMD_HELP.update(
    {"speed": ".speed\
    \nUsage: Does a speedtest and shows the results."})
CMD_HELP.update({
    "nearestdc":
    ".nearestdc\
    \nUsage: Finds the nearest datacenter from your server."
})
CMD_HELP.update({
    "ping":
    ".ping\
    \nUsage: Shows how long it takes to ping your bot."
})
