# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# UltronUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by Tgultron@Github.

# This file is part of: https://github.com/thanosuserss/Ultron
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/thanosuserss/Ultron/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import glob
import os
import sys
import urllib.request
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils

from userbot import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from ..Config import Config
from ..core.logger import logging
from ..core.session import ultronub
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup

ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("ultronubStartUP")
cmdhr = Config.COMMAND_HAND_LER

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]


async def setup_bot():
    """
    To set up bot for userbot
    """
    try:
        await ultronub.connect()
        config = await ultronub(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == ultronub.session.server_address:
                if ultronub.session.dc_id != option.id:
                    LOGS.warning(
                        f"Fixed DC ID in session from {ultronub.session.dc_id}"
                        f" to {option.id}"
                    )
                ultronub.session.set_dc(option.id, option.ip_address, option.port)
                ultronub.session.save()
                break
        bot_details = await ultronub.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await ultronub.start(bot_token=Config.TG_BOT_USERNAME)
        ultronub.me = await ultronub.get_me()
        ultronub.uid = ultronub.tgbot.uid = utils.get_peer_id(ultronub.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(ultronub.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {e}")
        sys.exit()


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            Config.ultronubLOGO = await ultronub.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/d1724e41554cefcb22b8f.jpg",
                caption="**Your UltronUserBot has been started successfully.**",
                buttons=[(Button.url("Support", "https://t.me/thanosprosss"),)],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await ultronub.check_testcases()
            message = await ultronub.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**Ok Bot is Back and Alive.**"
            await ultronub.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await ultronub.send_message(
                    msg_details[0],
                    f"{cmdhr}ping",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await ultronub.tgbot.get_me()
    try:
        await ultronub(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await ultronub(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def load_plugins(folder, extfolder=None):
    """
    To load plugins from the mentioned folder
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"userbot/{folder}/*.py"
        plugin_path = f"userbot/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                os.remove(Path(f"{plugin_path}/{shortname}.py"))
                LOGS.info(
                    f"unable to load {shortname} because of error {e}\nBase Folder {plugin_path}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        return success, failure


async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    flag = False
    if BOTLOG:
        try:
            entity = await ultronub.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if (
                    entity.default_banned_rights
                    and entity.default_banned_rights.send_messages
                ) or not entity.admin_rights.post_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
                if (
                    entity.default_banned_rights
                    and entity.default_banned_rights.invite_users
                ) or not entity.admin_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PRIVATE_GROUP_BOT_API_ID."
                    )
        except ValueError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID cannot be found. Make sure it's correct."
            )
        except TypeError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID is unsupported. Make sure it's correct."
            )
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        descript = "Don't delete this group or change to group(If you change group all your previous snips, welcome will be lost.)"
        _, groupid = await create_supergroup(
            "UltronUserBot BotLog Group", ultronub, Config.TG_BOT_USERNAME, descript
        )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        LOGS.info(
            "Private Group for PRIVATE_GROUP_BOT_API_ID is created successfully and added to vars."
        )
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await ultronub.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if (
                    entity.default_banned_rights
                    and entity.default_banned_rights.send_messages
                ) or not entity.admin_rights.post_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified PM_LOGGER_GROUP_ID."
                    )
                if (
                    entity.default_banned_rights
                    and entity.default_banned_rights.invite_users
                ) or not entity.admin_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified PM_LOGGER_GROUP_ID."
                    )
        except ValueError:
            LOGS.error("PM_LOGGER_GROUP_ID cannot be found. Make sure it's correct.")
        except TypeError:
            LOGS.error("PM_LOGGER_GROUP_ID is unsupported. Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the PM_LOGGER_GROUP_ID.\n"
                + str(e)
            )
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "userbot"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)


async def install_externalrepo(repo, branch, cfolder):
    CATREPO = repo
    rpath = os.path.join(cfolder, "requirements.txt")
    if CATBRANCH := branch:
        repourl = os.path.join(CATREPO, f"tree/{CATBRANCH}")
        gcmd = f"git clone -b {CATBRANCH} {CATREPO} {cfolder}"
        errtext = f"There is no branch with name `{CATBRANCH}` in your external repo {CATREPO}. Recheck branch name and correct it in vars(`EXTERNAL_REPO_BRANCH`)"
    else:
        repourl = CATREPO
        gcmd = f"git clone {CATREPO} {cfolder}"
        errtext = f"The link({CATREPO}) you provided for `EXTERNAL_REPO` in vars is invalid. please recheck that link"
    response = urllib.request.urlopen(repourl)
    if response.code != 200:
        LOGS.error(errtext)
        return await ultronub.tgbot.send_message(BOTLOG_CHATID, errtext)
    await runcmd(gcmd)
    if not os.path.exists(cfolder):
        LOGS.error(
            "There was a problem in cloning the external repo. please recheck external repo link"
        )
        return await ultronub.tgbot.send_message(
            BOTLOG_CHATID,
            "There was a problem in cloning the external repo. please recheck external repo link",
        )
    if os.path.exists(rpath):
        await runcmd(f"pip3 install --no-cache-dir -r {rpath}")
    success, failure = await load_plugins(folder="userbot", extfolder=cfolder)
    return repourl, cfolder, success, failure
