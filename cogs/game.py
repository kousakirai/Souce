from discord.ext import commands
import discord
import random
import json

with open("data.json", mode="r") as f:
    data = json.load(f)


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def game(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('メインコマンドの後にサブコマンドが必要です。')

    @game.command()
    async def atk(self, ctx, user_id):
        if ctx.author.id in data["game"]:
            if user_id in data["game"]:
                damage = random.choice(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                       13, 14, 15, 16, 17, 18, 19, 20)
                damage2 = random.choice(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                        13, 14, 15, 16, 17, 18, 19, 20)
                data["game"][ctx.author.id] - damage2
                data["game"][user_id] - damage
                with open("data.json", mode="w") as f:
                    json.dump(data, f, indent=4)
def setup(bot):
    return bot.add_cog(Greetings(bot))