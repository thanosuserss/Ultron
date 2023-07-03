# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# UltronUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2023-2023 by Tgultron@Github.

# This file is part of: https://github.com/thanosuserss/Ultron
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/thanosuserss/Ultron/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import contextlib
import sys

import userbot
from userbot import BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from .Config import Config
from .core.logger import logging
from .core.session import ultronub
from .utils import (
    add_bot_to_logger_group,
    install_externalrepo,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("UltronUserBot")

LOGS.info(userbot.__copyright__)
LOGS.info(f"Licensed under the terms of the {userbot.__license__}")

cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("Starting Userbot")
    ultronub.loop.run_until_complete(setup_bot())
    LOGS.info("TG Bot Startup Completed")
except Exception as e:
    LOGS.error(f"{e}")
    sys.exit()


async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    LOGS.info(
        "============================================================================"
    )
    LOGS.info("||               Yay your userbot is officially working.!!!")
    LOGS.info(
        f"||   Congratulation, now type {cmdhr}alive to see message if ultronub is live"
    )
    LOGS.info("||   If you need assistance, head to https://t.me/thanosprosss")
    LOGS.info(
        "============================================================================"
    )
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return


async def externalrepo():
    string = "<b>Your external repo plugins have imported.<b>\n\n"
    if Config.EXTERNAL_REPO:
        data = await install_externalrepo(
            Config.EXTERNAL_REPO, Config.EXTERNAL_REPOBRANCH, "xtraplugins"
        )
        string += f"<b>➜ Repo:  </b><a href='{data[0]}'><b>{data[1]}</b></a>\n<b>     • Imported Plugins:</b>  <code>{data[2]}</code>\n<b>     • Failed to Import:</b>  <code>{', '.join(data[3])}</code>\n\n"
    if Config.BADCAT:
        data = await install_externalrepo(
            Config.BADCAT_REPO, Config.BADCAT_REPOBRANCH, "badcatext"
        )
        string += f"<b>➜ Repo:  </b><a href='{data[0]}'><b>{data[1]}</b></a>\n<b>     • Imported Plugins:</b>  <code>{data[2]}</code>\n<b>     • Failed to Import:</b>  <code>{', '.join(data[3])}</code>\n\n"
    if Config.VCMODE:
        data = await install_externalrepo(Config.VC_REPO, Config.VC_REPOBRANCH, "catvc")
        string += f"<b>➜ Repo:  </b><a href='{data[0]}'><b>{data[1]}</b></a>\n<b>     • Imported Plugins:</b>  <code>{data[2]}</code>\n<b>     • Failed to Import:</b>  <code>{', '.join(data[3])}</code>\n\n"
    if "Imported Plugins" in string:
        await ultronub.tgbot.send_message(BOTLOG_CHATID, string, parse_mode="html")


ultronub.loop.run_until_complete(startup_process())

ultronub.loop.run_until_complete(externalrepo())

if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        ultronub.run_until_disconnected()
else:
    ultronub.disconnect()
