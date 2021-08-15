import discord
from discord.ext import commands


class my(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group()
    async def myc(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("サブコマンドが不正です。")

    @myc.command(name="create", aliases=["cre"])
    async def mychannel(self, ctx, ch_name):
        category = ctx.guild.get_channel(864057025185185802)
        await category.create_text_channel(name=ch_name)
        await ctx.reply(f"{ch_name}を作成しました。")
    #@myc.command(name="delete", aliase=["del"])
    #@commads.is_owner()
    #async def delete(self, ctx, ch_name):
        
def setup(bot):
    return bot.add_cog(my(bot))
