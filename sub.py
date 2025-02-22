"""りつたん！ (C) 2020 RT-Team
LICENSE : ./LICENSE
README  : ./readme.md
"""

desc = """りつたん - (C) 2021 RT-Team
少女起動中..."""
print(desc)

from discord.ext import commands
import discord

# routeは無効にする。
commands.Cog.route = lambda *args, **kwargs: lambda *args, **kwargs: (args, kwargs)

from aiohttp import ClientSession
from sys import argv
import ujson
import rtlib

from data import data, is_admin, RTCHAN_COLORS


with open("token.secret", "r", encoding="utf-8_sig") as f:
    secret = ujson.load(f)
TOKEN = secret["token"]["sub"]


prefixes = data["prefixes"]["sub"]


def setup(bot):
    bot.admins = data["admins"]

    @bot.listen()
    async def on_close(loop):
        await bot.session.close()
        del bot.mysql

    bot.mysql = bot.data["mysql"] = rtlib.mysql.MySQLManager(
        loop=bot.loop, user=secret["mysql"]["user"],
        host="146.59.153.178" if argv[1] == "production" else "localhost",
        password=secret["mysql"]["password"], db="mysql",
        pool = True, minsize=1, maxsize=30, autocommit=True)

    rtlib.setup(bot)
    bot.load_extension("jishaku")

    bot._loaded = False

    @bot.event
    async def on_ready():
        if not bot._loaded:
            bot.session = ClientSession(loop=bot.loop)
            for name in ("cogs.tts", "cogs.music", "cogs._sub", "cogs.language"):
                bot.load_extension(name)
            bot.dispatch("full_ready")
            bot._loaded = True
            print("少女絶賛稼働中！")


intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.guild_typing = False
intents.dm_typing = False
args = (prefixes,)
kwargs = {
    "help_command": None,
    "intents": intents
}
bot = commands.Bot(
    command_prefix=data["prefixes"]["sub"], **kwargs
)
bot.test = argv[1] != "production"


bot.data = data
bot.colors = RTCHAN_COLORS
bot.is_admin = is_admin


async def _is_owner(user):
    return bot.is_admin(user.id)
bot.is_owner = _is_owner
del is_admin, _is_owner


setup(bot)


bot.run(TOKEN)
