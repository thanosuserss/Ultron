# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# UltronUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2023-2023 by Tgultron@Github.

# This file is part of: https://github.com/thanosuserss/Ultron
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/thanosuserss/Ultron/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from userbot import ultronub

from ..core.managers import edit_or_reply
from ..helpers.utils import _format

plugin_category = "tools"


# yaml_format is ported from uniborg
@ultronub.cat_cmd(
    pattern="json$",
    command=("json", plugin_category),
    info={
        "header": "To get details of that message in json format.",
        "usage": "{tr}json reply to message",
    },
)
async def _(event):
    "To get details of that message in json format."
    catevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = catevent.stringify()
    await edit_or_reply(event, the_real_message, parse_mode=_format.parse_pre)


@ultronub.cat_cmd(
    pattern="yaml$",
    command=("yaml", plugin_category),
    info={
        "header": "To get details of that message in yaml format.",
        "usage": "{tr}yaml reply to message",
    },
)
async def _(event):
    "To get details of that message in yaml format."
    catevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = _format.yaml_format(catevent)
    await edit_or_reply(event, the_real_message, parse_mode=_format.parse_pre)
