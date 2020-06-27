from tg_userbot import bot, CMD_HELP
from tg_userbot.events import register
from tg_userbot.modules.libs.get_id import get_id
import os.path
from os import path
import os

@register(outgoing=True, pattern="^\.save(?: |$)(\w+)(.*)")
async def save(event):
    name = event.pattern_match.group(1)
    text = event.pattern_match.group(2).lstrip()
    textx = await event.get_reply_message()
    npath = "notes/" + name + ".txt"
    if not os.path.isdir("notes/"):
        os.makedirs("notes/")
    if path.exists(npath):
        await event.edit(f"Note `{name}` already exists.")
    f=open(npath,"w+")
    if text:
        f.write(text)
        await event.edit(f"Successfully saved note `{name}`.\n"+
                       f"Type `.note {name}` to get it.")
    if textx:
    	f.write(textx.message)
    	await event.edit(f"Successfully saved note `{name}`.\n"+
                       f"Type `.note {name}` to get it.")

@register(outgoing=True, pattern="^\.note (.*)")
async def note(event):
    name = event.pattern_match.group(1)
    npath = "notes/" + name + ".txt"
    if not path.exists(npath):
        await event.edit(f"Note `{name}` doesn't exist.\n"+
                           f"Type `.save {name} <text> to create the note.")
    f=open(npath,"r+")
    await event.edit(f.read())

@register(outgoing=True, pattern="^\.notes")
async def notes(mention):
    reply = "You have these notes:\n\n"
    allnotes = os.listdir("notes/")
    if not allnotes:
        reply = "You have no notes!"
    else:
        for n in allnotes:
            reply = reply + f"- {n.split('.')[0]}\n"
        reply = reply + "\nGet any of these notes by typing `.note <notename>`"
    await mention.edit(reply)