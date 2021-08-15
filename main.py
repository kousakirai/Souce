print("Now loading...")
import textwrap
import discord
import os
import keep_alive
import feedparser
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandOnCooldown
from tinydb import TinyDB, Query
from Function.help import JapaneseHelpCommand
import async_google_trans_new
# 接続に必要なオブ

team_id = [
    739702692393517076, 693025129806037003, 757106917947605034,
    484655503675228171, 794491815125975092
]

class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        if user.id in team_id:
            return True
        return await super().is_owner(user)


prefix = "h?", "h:"
intents = discord.Intents.all()  # デフォルトのIntentsオブジェクトを生成
intents.typing = False

bot = MyBot(command_prefix=prefix,
            help_command=JapaneseHelpCommand(),
            intents=intents,
            case_insensitive=True)

db = TinyDB('money.json')

User = Query()

guild_ids = [774477394924666890]


bot.author_id = 757106917947605034

bot.load_extension("jishaku")

bot.load_extension("discord_debug")

bot.load_extension("adminonly.debug")

#cogの読み取り
for filename in os.listdir("cogs"):
    if not filename.startswith("_") and filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

#起動する際のイベント
@bot.event
async def on_ready():
  print(f"{bot.user.name}起動しました")
  channel = bot.get_channel(818817278912626718)
  await channel.send(
    "```疑問猫Bot再起動しました。起動時になにかエラーが起きた場合は制作者のkousakiraiにお伝え下さい。社畜のように働きます()```"
    )
  guild = bot.get_guild(774477394924666890)
  await bot.change_presence(activity=discord.Game(len(guild.members)))

keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))
