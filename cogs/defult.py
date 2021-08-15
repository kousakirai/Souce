import discord
from discord.ext import commands
import os
import keep_alive


class talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    カスタム返信実装予定のカテゴリ
    """

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if 'おうどん食べたい' in message.content:
            await message.channel.send("家の近くに丸亀製麺あるからそこ行こうぜ。")
        if '草' in message.content:
            await message.channel.send("wwwwwwwwwwwwwwwwwww")


def setup(bot):
    return bot.add_cog(talk(bot))
