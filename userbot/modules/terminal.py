# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
#
# Eval command has been removed, module renamed terminal
""" Userbot module for executing code and terminal commands from Telegram. """

import asyncio
from getpass import getuser
from os import remove
from sys import executable

from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID
from userbot.events import register, errors_handler

@register(outgoing=True, pattern=r"^.exec(?: |$)([\s\S]*)")
@errors_handler
async def run(run_q):
    """ For .exec command, which executes the dynamically created program """
    if not run_q.text[0].isalpha() and run_q.text[0] not in ("/", "#", "@",
                                                             "!"):
        code = run_q.pattern_match.group(1)

        if run_q.is_channel and not run_q.is_group:
            await run_q.edit("`Exec isn't permitted on channels!`")
            return

        if not code:
            await run_q.edit("``` At least a variable is required to \
execute. Use .help exec for an example.```")
            return

        if code in ("userbot.session", "config.env"):
            await run_q.edit("`That's a dangerous operation! Not Permitted!`")
            return

        if len(code.splitlines()) <= 5:
            codepre = code
        else:
            clines = code.splitlines()
            codepre = clines[0] + "\n" + clines[1] + "\n" + clines[2] + \
                "\n" + clines[3] + "..."

        command = "".join(f"\n {l}" for l in code.split("\n.strip()"))
        process = await asyncio.create_subprocess_exec(
            executable,
            '-c',
            command.strip(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if result:
            if len(result) > 4096:
                file = open("output.txt", "w+")
                file.write(result)
                file.close()
                await run_q.client.send_file(
                    run_q.chat_id,
                    "output.txt",
                    reply_to=run_q.id,
                    caption="`Output too large, sending as file`",
                )
                remove("output.txt")
                return
            await run_q.edit("**Query: **\n`"
                             f"{codepre}"
                             "`\n**Result: **\n`"
                             f"{result}"
                             "`")
        else:
            await run_q.edit("**Query: **\n`"
                             f"{codepre}"
                             "`\n**Result: **\n`No Result Returned/False`")

        if BOTLOG:
            await run_q.client.send_message(
                BOTLOG_CHATID,
                "Exec query " + codepre + " was executed successfully")


@register(outgoing=True, pattern="^.term(?: |$)(.*)")
@errors_handler
async def terminal_runner(term):
    """ For .term command, runs bash commands and scripts on your server. """
    if not term.text[0].isalpha() and term.text[0] not in ("/", "#", "@", "!"):
        curruser = getuser()
        command = term.pattern_match.group(1)
        try:
            from os import geteuid
            uid = geteuid()
        except ImportError:
            uid = "This ain't it chief!"

        if term.is_channel and not term.is_group:
            await term.edit("`Term commands aren't permitted on channels!`")
            return

        if not command:
            await term.edit("``` Give a command or use .help term for \
                an example.```")
            return

        if command in ("userbot.session", "config.env"):
            await term.edit("`That's a dangerous operation! Not Permitted!`")
            return

        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if len(result) > 4096:
            output = open("output.txt", "w+")
            output.write(result)
            output.close()
            await term.client.send_file(
                term.chat_id,
                "output.txt",
                reply_to=term.id,
                caption="`Output too large, sending as file`",
            )
            remove("output.txt")
            return

        if uid is 0:
            await term.edit("`" f"{curruser}:~# {command}" f"\n{result}" "`")
        else:
            await term.edit("`" f"{curruser}:~$ {command}" f"\n{result}" "`")

        if BOTLOG:
            await term.client.send_message(
                BOTLOG_CHATID,
                "Terminal Command " + command + " was executed sucessfully",
            )

CMD_HELP.update(
    {"exec": ".exec print('hello')\nUsage: Execute small python scripts."})
CMD_HELP.update(
    {"term": ".term ls\nUsage: Run bash commands and scripts on your server."})