import discord
import json
import aiohttp
from discord.ext import commands


class Qrcode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def qrcreate(self, ctx, tt):
        embed = discord.Embed(title="QRCODE作成", description="しばらくお待ちください")
        await ctx.send(embed=embed)
        rjson={
          "token": "hatena",
          "text": tt
        }
        async with aiohttp.ClientSession() as session:
          async with session.post("https://qrcodeplus.dmssite.cf/api/create", data=rjson) as response:
            api=json.loads(await response.text())
            embed = discord.Embed(title="QRCODE作成")
            embed.set_image(url=api["url"])
            await ctx.send(embed=embed)


def setup(bot):
    return bot.add_cog(Qrcode(bot))
