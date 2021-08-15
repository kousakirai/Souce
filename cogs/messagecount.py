import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import increment

db = TinyDB('mescount.json')

money = TinyDB('money.json')

User = Query()


class count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add')
    async def add(self, ctx):
        if len(db.search(User.name == ctx.author.id)) > 0:
            await ctx.send('追加済みです')

        else:
            db.insert({'name': ctx.author.id, 'age': 0})
            await ctx.send('追加しました')

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        channel = self.bot.get_channel(818817278912626718)

        if not message.channel == channel:
            return

        if "h:" in message.content:
            return

        if '' in message.content:
            db.update(increment('age'), User.name == message.author.id)
            money.update(increment('money'), User.name == message.author.id)

            await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if db.search(User.name == member.id) == member.id:
            db.insert({'name': member.id, 'age': 0})

    @commands.command(name='dbtest')
    async def dbtest(self, ctx):
        l = db.all()
        l = discord.Embed(title='発言回数',
                          description=f'{l[0]["name"]}{l[0]["age"]}')
        await ctx.send(embed=l)

def setup(bot):
    return bot.add_cog(count(bot))
