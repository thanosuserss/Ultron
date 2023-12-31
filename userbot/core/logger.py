# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# UltronUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2023-2023 by Tgultron@Github.

# This file is part of: https://github.com/thanosuserss/Ultron
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/thanosuserss/Ultron/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import logging

logging.basicConfig(
    format="[%(levelname)s- %(asctime)s]- %(name)s- %(message)s",
    handlers=[logging.FileHandler("ultronub.log"), logging.StreamHandler()],
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

logging.getLogger("telethon.client.updates").setLevel(logging.WARNING)
logging.getLogger("telethon.network").setLevel(logging.WARNING)
