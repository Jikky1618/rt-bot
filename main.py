"""RT Backend (C) 2020 RT-Team
LICENSE : ./LICENSE
README  : ./readme.md
"""

from os import listdir
from sys import argv
import ujson
import rtlib

from data import data, is_admin


# 設定ファイルの読み込み。
with open("token.secret", "r", encoding="utf-8_sig") as f:
    secret: dict = ujson.load(f)
TOKEN = secret["token"][argv[1]]


# その他設定をする。
prefixes = data["prefixes"][argv[1]]


# Backendのセットアップをする。
def on_init(bot):
    bot.data["mysql"] = rtlib.mysql.MySQLManager(
        loop=bot.loop, user=secret["mysql"]["user"],
        password=secret["mysql"]["password"], db="mysql",
        pool = True)

    # エクステンションを読み込む。
    bot.load_extension("jishaku")
    bot.load_extension("rtlib.libs.on_send")
    bot.load_extension("rtlib.componesy")
    bot.load_extension("rtlib.libs.on_full_reaction")
    bot.load_extension("rtlib.libs.on_command_add")
    bot.load_extension("rtlib.libs.dochelp")
    # cogsフォルダにあるエクステンションを読み込む。
    for path in listdir("cogs"):
        if path.endswith(".py"):
            bot.load_extension("cogs." + path[:-3])
        elif "." not in path and path != "__pycache__" and path[0] != ".":
            bot.load_extension("cogs." + path)


# テスト時は普通のBackendを本番はシャード版Backendを定義する。
args = (prefixes,)
kwargs = {
    "help_command": None,
    "on_init_bot": on_init
}
if argv[1] == "test":
    bot = rtlib.Backend(*args, **kwargs)
    bot.test = True
elif argv[1] == "production":
    bot = rtlib.AutoShardedBackend(*args, **kwargs)
    bot.test = False
bot.data = data
bot.colors = data["colors"]
bot.is_admin = is_admin


# jishakuの管理者かどうか確認するためのコルーチン関数を用意する。
async def _is_owner(user):
    return bot.is_admin(user.id)
bot.is_owner = _is_owner
del is_admin, _is_owner


bot.run(TOKEN, host="0.0.0.0", port=80)
