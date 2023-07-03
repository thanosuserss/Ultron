# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# UltronUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by Tgultron@Github.

# This file is part of: https://github.com/thanosuserss/Ultron
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/thanosuserss/Ultron/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import json
import os
import re

from telethon.events import CallbackQuery

from userbot import ultronub


@ultronub.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./userbot/secret.txt"):
        jsondata = json.load(open("./userbot/secret.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = userid + [ultronub.uid]
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
            else:
                reply_pop_up_alert = "why were you looking at this shit go away and do your own work, idiot"
        except KeyError:
            reply_pop_up_alert = "This message no longer exists in ultronub server"
    else:
        reply_pop_up_alert = "This message no longer exists "
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
