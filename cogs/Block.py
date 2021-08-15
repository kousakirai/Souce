import discord
from discord.ext import commands
import os
import aiofile
import json


class block(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = os.path.dirname(__file__) + "/txtfiles/Blockinglist.json"
        with open(self.path, "r") as f:
            content = f.read()
        self.content = json.loads(content)
        intents = discord.Intents.default()
        intents.members = True

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member):
        id = str(member.id)
        list = str(self.content)
        for i in list:
            if list in id:
                print("第三関門突破" + self.member.id)
                n = '\n'.join("あなたはブラックリストに登録されているためブロックされました。")
                await member.author.send(f"```{n}```")
                await member.kick(list)

    @commands.group(name="Block")
    async def Block(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('メインコマンドの後にサブコマンドが必要です。')

    @Block.command(name="add")
    async def add(self, ctx, *, message):
        self.content.append(message)
        async with aiofile.async_open(self.path, "w", encoding="utf_8") as f:
            await f.write(json.dumps(self.content))
        await ctx.send("Blockリストに追加しました。")

    @Block.command(name="remove", aliases=["delete", "del"])
    async def ng_remove(self, ctx, message):
        if not message in self.content:
            return await ctx.send("そのIDはリストにありません。")
        self.content.remove(message)
        async with aiofile.async_open(self.path, "w", encoding="utf_8") as f:
            await f.write(json.dumps(self.content))
        await ctx.send("完了。")

    @Block.command(name="list")
    async def ng_list(self, ctx):
        if ctx.author.id in [
                693025129806037003, 469067836690661377, 484655503675228171,
                756098405482364971, 820202188457508865, 663196515384295425
        ]:
            n = '\n'.join(self.content)
            await ctx.author.send(f"```{n}```")
            await ctx.message.add_reaction("✅")


def setup(bot):
    return bot.add_cog(block(bot))
