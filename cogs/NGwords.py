import discord
from discord.ext import commands
import os
import aiofile
import json
import datetime


class NGs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = os.path.dirname(__file__) + "/txtfiles/NGwords.json"
        with open(self.path, "r") as f:
            content = f.read()
        self.content = json.loads(content)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 821725199069085706:
            return
        for word in self.content:
            msg = message.content.lower()
            if word in msg:
                if message.content.startswith("h?NGwords remove "): return
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention},NGワードを発言したためメッセージを削除しました。",
                    delete_after=4.0)
                embed = discord.Embed(
                    title="NGワード削除ログ",
                    description=
                    f"NGワードの削除が行われました。\n時刻：{datetime.datetime.now()} + 9時間",
                    color=0xff0000)
                embed.add_field(
                    name="対象者",
                    value=
                    f"{message.author.mention}({message.author})\nID:{message.author.id}",
                    inline=False)
                embed.add_field(
                    name="チャンネル",
                    value=
                    f"{message.channel.mention}({message.channel.name})\nID:{message.channel.id}",
                    inline=False)
                embed.add_field(name="メッセージ内容",
                                value=message.content.replace(
                                    word, f"||{word}||"),
                                inline=False)
                await self.bot.get_channel(822112963535568936).send(embed=embed
                                                                    )
                break

    @commands.group(aliases=["ng", "ngwords"])
    async def NGword(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('メインコマンドの後にサブコマンドが必要です。')

    @NGword.command(name="add")
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, *, message):
        msg = message.lower()
        self.content.append(msg)
        async with aiofile.async_open(self.path, "w", encoding="utf_8") as f:
            await f.write(json.dumps(self.content))
        await ctx.send("NGリストに追加しました。")

    @NGword.command(name="remove", aliases=["delete", "del"])
    @commands.has_permissions(manage_messages=True)
    async def ng_remove(self, ctx, message):
        if not message in self.content:
            return await ctx.send("その言葉はリストにありません。")
        msg = message.lower()
        self.content.remove(msg)
        async with aiofile.async_open(self.path, "w", encoding="utf_8") as f:
            await f.write(json.dumps(self.content))
        await ctx.send("完了。")

    @NGword.command(name="list")
    @commands.has_permissions(manage_messages=True)
    async def ng_list(self, ctx):
        n = '\n'.join(self.content)
        await ctx.author.send(f"```{n}```")
        await ctx.message.add_reaction("✅")


def setup(bot):
    return bot.add_cog(NGs(bot))
