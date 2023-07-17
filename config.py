from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 10248430
    API_HASH = "42396a6ff14a569b9d59931643897d0d"
    # the name to display in your alive message
    ALIVE_NAME = "rishabh"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "postgres://agnnsppd:NOC_2Ax0Ha96AS1UoyHLw2HS-ioB5toh@satao.db.elephantsql.com/agnnsppd"
    # After cloning the repo and installing requirements do python3 stringsetup.py an fill that value with this
    STRING_SESSION = "1BVtsOIEBu7-pxyTR-itmeAzW_7A0y6TJzws3aC6utpOjLtElI5WNDO1PXt5ZG3IV0a2TbZEqibIuxWQHsh7rOV-JPwsPlVHHTR2hrLYR9WD8vkDxYM1QctELwMJ3Fx14BXW1SI3vQtVbNsunEdf9dUMg1lAMzqyBqcbxo0EGaUQ6qpMPPJReTaZ7QLlAWbJ201lKjklAxFGYEC63j05XDAPXtacoYxaaPVjbg0aPhEh-MumHevhUR_A8tw4HfGusLR-0OrZsaj9-Iv_AepIK4sF8pjqk9iVKDPKWciRT9CjIIgbtBscVVqhtKCjItEO6UMu7W37GAoQBtbn_65ai6OdPzAKllvA="
    # create a new bot in @botfather and fill the following vales with bottoken
    TG_BOT_TOKEN = "6036179027:AAHqPbt2Xm3ZAJOOvSV-hx4jx_flI2So0U0"
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -1001786908289
    # command handler
    COMMAND_HAND_LER = "."
    # command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
    # External plugins repo
    EXTERNAL_REPO = "https://github.com/Tgultron/CatPlugins"
    # if you need badcat plugins set "True"
    BADCAT = "False"
