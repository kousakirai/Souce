import sys
import os
import discord
from discord.ext import commands
from tinydb import TinyDB, Query

db = TinyDB('mescount.json')

User = Query()


class debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="debug")
    async def debug(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('メインコマンドの後にサブコマンドが必要です()')

    @debug.command(name="reload2", aliases=["r2"])
    async def reload2(self, ctx, name):
        role = ctx.guild.get_role(813389100815351869)
        if ctx.author.guild_permissions.administrator or role in ctx.author.roles:
            try:
                self.bot.reload_extension(f"adminonly.{name}")
            except Exception as e:
                await ctx.send('**エラー**' + '\n'.join(e.args))
            else:
                await ctx.send(f"adminonly.{name}のリロードに成功しました")
        else:
            await ctx.send("あなたには権限がありません()")

    @debug.command(name="reloads", aliases=["re"])
    async def reload1(self, ctx, name):
        role = ctx.guild.get_role(813389100815351869)
        if ctx.author.guild_permissions.administrator or role in ctx.author.roles:
            try:
                self.bot.reload_extension(f"cogs.{name}")
            except Exception as e:
                await ctx.send('**エラー**' + '\n'.join(e.args))
            else:
                await ctx.send(f"cogs.{name}のリロードに成功しました")
        else:
            await ctx.send("あなたには権限がありません")

    @debug.command(name="reboot")
    async def reboot(self, ctx):
        role = ctx.guild.get_role(813389100815351869)
        if ctx.author.guild_permissions.administrator or role in ctx.author.roles:
            await ctx.send("Botを再起動します。")
            await self.bot.change_presence(
                activity=discord.Game(name="rebooting now...", type=1))
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            await ctx.send("あなたには権限がありません")

    @debug.command(name="shutdown")
    async def shutdown(self, ctx):
        role = ctx.guild.get_role(813389100815351869)
        if ctx.author.guild_permissions.administrator or role in ctx.author.roles:
            await ctx.send("シャットダウンします")
            await self.bot.logout()

    @commands.command(name="reload", aliases=["re"])
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if cog:
            try:
                self.bot.reload_extension("cogs." + cog)
            except commands.errors.ExtensionNotLoaded:
                self.bot.load_extension("cogs." + cog)
            except commands.errors.NoEntryPointError:
                pass
            return await ctx.message.add_reaction("✅")
            for o in os.listdir(os.path.dirname(os.path.abspath(__file__))):
                try:
                    if not o.endswith(".py"):
                        continue
                    self.bot.reload_extension(
                        "cogs." + os.path.splitext(os.path.basename(o))[0])
                except commands.errors.ExtensionNotLoaded:
                    self.bot.load_extension(
                        "cogs." + os.path.splitext(os.path.basename(o))[0])
                except commands.errors.NoEntryPointError:
                    pass
        await ctx.message.add_reaction("✅")

    @debug.command(name='test')
    async def _test(self, ctx):
        if db.search(User.name == ctx.author.id) == ctx.author.id:
            a = db.search(User.name == ctx.author.id)
            print(a[0]['name'], a[0]['age'])


def setup(bot):
    return bot.add_cog(debug(bot))
