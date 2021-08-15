import discord
import json
from discord.ext import commands
from google_translate_py import AsyncTranslator
import async_google_trans_new

with open("data.json", mode="r") as f:
    data = json.load(f)


class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.channel.topic == ("h?trans"):
                g = async_google_trans_new.AsyncTranslator()
                if not (await g.detect(str(message.content))) == "ja":
                    t = "en"
                else:
                    t = "ja"
                result = await g.translate(str(message.content), t)
                embed = discord.Embed(title="google translate", color=0x00bfff)
                embed.add_field(name="before",
                                value=message.content,
                                inline=False)
                embed.add_field(name="after", value=result, inline=False)
                embed.set_footer(
                    text="Powered by googletranslate",
                    icon_url="https://ssl.gstatic.com/translate/favicon.ico")
                await message.channel.send(embed=embed)

    @commands.command()
    async def trans(self, ctx, *, word):
        g = async_google_trans_new.AsyncTranslator()
        if (await g.detect(word))[0] == "ja":
            t = "en"
        else:
            t = "ja"
        result = await g.translate(word, t)
        embed = discord.Embed(title="google translate", color=0x00bfff)
        embed.add_field(name="before", value=word, inline=False)
        embed.add_field(name="after", value=result, inline=False)
        embed.set_footer(
            text="Powered by googletranslate",
            icon_url="https://ssl.gstatic.com/translate/favicon.ico")
        await ctx.send(embed=embed)

    @commands.command()
    async def trans_lang(self, ctx, lang):
        data["trans"][ctx.author.id] = [lang]
        with open("data.json", mode="w") as f:
            json.dump(data, f, indent=4)
        await ctx.send("変更しました")

    @commands.command()
    async def trans2(self, ctx, lang, *, word):
        result = await AsyncTranslator().translate(word, "", lang)
        embed = discord.Embed(title="google translate", color=0x00bfff)
        embed.add_field(name="before", value=word, inline=False)
        embed.add_field(name="after", value=result, inline=False)
        embed.set_footer(text="Powered by googletranslate",icon_url="https://ssl.gstatic.com/translate/favicon.ico")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Translate(bot))
