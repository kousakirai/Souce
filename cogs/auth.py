import discord
import random, string
from discord.ext import commands
import json
import requests

with open("auth.json", mode="r") as f:
    data = json.load(f)


def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def auth(self, ctx):
        code = randomname(15)
        data["auth"][code] = [ctx.author.id]
        with open("auth.json", mode="w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(
            title="web認証システム",
            description=
            f"認証するにはこの[url](https://www.hatenabot.cf/captcha?id={code})に入ってください",
            color=0xff0000)

        await ctx.author.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        code = randomname(15)
        data["auth"][code] = [member.id]
        with open("auth.json", mode="w") as f:
            json.dump(data, f, indent=4)
        embed = discord.Embed(
            title="web認証システム",
            description=
            f"認証url:https://Yi-Wen-Mao-BotGai.hatenanyanbots.repl.co/captcha?id={code}",
            color=0xff0000)
        dm = await member.create_dm()
        await dm.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 855991168981401631:
            await message.add_reaction("🔄")
            auth = json.loads(message.content)
            role = message.guild.get_role(819828678208782336)
            member = message.guild.get_member(int(auth["user_id"][0]))
            await member.add_roles(role)
            channel = self.bot.get_channel(855991936488964133)
            embed = discord.Embed(title="web認証",description=member.id)
            c=await channel.send(embed=embed)
            await c.add_reaction("✅")
            dm = await member.create_dm()
            await dm.send("認証成功")
            await message.remove_reaction("🔄", self.bot.user)
            await message.add_reaction("✅")


def setup(bot):
    return bot.add_cog(Auth(bot))
