# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# UltronUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by Tgultron@Github.

# This file is part of: https://github.com/thanosuserss/Ultron
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/thanosuserss/Ultron/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import contextlib
import importlib
import sys
from pathlib import Path

from userbot import CMD_HELP, LOAD_PLUG

from ..Config import Config
from ..core import LOADED_CMDS, PLG_INFO
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..core.session import ultronub
from ..helpers.utils import _catutils, _format, install_pip, reply_id
from .decorators import admin_cmd, sudo_cmd

LOGS = logging.getLogger("UltronUserBot")


def load_module(shortname, plugin_path=None):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        load_module_sortner(shortname)
    else:
        if plugin_path is None:
            path = Path(f"userbot/plugins/{shortname}.py")
            name = f"userbot.plugins.{shortname}"
        else:
            path = Path((f"{plugin_path}/{shortname}.py"))
            name = f"{plugin_path}/{shortname}".replace("/", ".")
        checkplugins(path)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = ultronub
        mod.LOGS = LOGS
        mod.Config = Config
        mod._format = _format
        mod.sudo_cmd = sudo_cmd
        mod.CMD_HELP = CMD_HELP
        mod.reply_id = reply_id
        mod.admin_cmd = admin_cmd
        mod._catutils = _catutils
        mod.edit_delete = edit_delete
        mod.install_pip = install_pip
        mod.parse_pre = _format.parse_pre
        mod.edit_or_reply = edit_or_reply
        mod.tgbot = ultronub.tgbot
        mod.logger = logging.getLogger(shortname)
        mod.borg = ultronub
        spec.loader.exec_module(mod)
        # for imports
        sys.modules[f"userbot.plugins.{shortname}"] = mod
        LOGS.info(f"Successfully imported {shortname}")


def load_module_sortner(shortname):
    path = Path(f"userbot/plugins/{shortname}.py")
    checkplugins(path)
    name = f"userbot.plugins.{shortname}"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    LOGS.info(f"Successfully imported {shortname}")


def remove_plugin(shortname):
    try:
        cmd = []
        if shortname in PLG_INFO:
            cmd += PLG_INFO[shortname]
        else:
            cmd = [shortname]
        for cmdname in cmd:
            if cmdname in LOADED_CMDS:
                for i in LOADED_CMDS[cmdname]:
                    ultronub.remove_event_handler(i)
                del LOADED_CMDS[cmdname]
        return True
    except Exception as e:
        LOGS.error(e)
    with contextlib.suppress(BaseException):
        for i in LOAD_PLUG[shortname]:
            ultronub.remove_event_handler(i)
        del LOAD_PLUG[shortname]
    try:
        name = f"userbot.plugins.{shortname}"
        for i in reversed(range(len(ultronub._event_builders))):
            ev, cb = ultronub._event_builders[i]
            if cb.__module__ == name:
                del ultronub._event_builders[i]
    except BaseException as exc:
        raise ValueError from exc


def checkplugins(filename):
    with open(filename, "r") as f:
        filedata = f.read()
    filedata = filedata.replace("sendmessage", "send_message")
    filedata = filedata.replace("sendfile", "send_file")
    filedata = filedata.replace("editmessage", "edit_message")
    with open(filename, "w") as f:
        f.write(filedata)
