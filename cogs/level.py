import discord
import json
from motor import motor_asyncio as motor
from discord.ext import commands

with open("data.json", mode="r") as f:
    data = json.load(f)

levels = data["level"]
password="W3KpCKMb4nLXIw34"
dbclient = motor.AsyncIOMotorClient(f"mongodb+srv://hatenabot:{password}@cluster0.ykp78.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", port=8080)
db2 = dbclient["myFirstDatabase"]
db = db2.level
log={}

class lv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group()
    async def level(self, ctx):
      if ctx.invoked_subcommand is None:
        await ctx.send("サブコマンドが要ります")
        
    @level.command()
    async def check(self, ctx):
      if not str(ctx.author.id) in data["level"]:
        await ctx.send("まだカウントされていません")
      else:
        lev = data["level"][str(ctx.author.id)]["level"]
        embed = discord.Embed(title="レベリング機能",description=f"あなたのレベルは{lev}です。",color=0xff0000)
        embed.set_author(name=ctx.author,icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        
    @level.command()
    @commands.has_permissions(administrator=True)
    async def block(self, ctx):
      data["level_block"].append(ctx.channel.id)
      with open("data.json", mode="w") as f:
        json.dump(data, f, indent=4)
      await ctx.send("レベル機能を無効にしました")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data["level"][member.id] = {}
        data["level"][member.id]["level"] = 1
        data["level"][member.id]["exp"] = 0
        with open("data.json", mode="w") as f:
            json.dump(data, f, indent=4)
     
    """       
    @commands.Cog.listener(name="on_message")
    async def level(self, message):
      level=await db.find_one({
        "userid": message.author.id
      })
      if level is None:
        await db.insert_one({
          "userid": message.author.id,
          "exp": 0,
          "lv": 1
        })
      else:
        exp=level["exp"]
        lv=level["level"]
        jn={
          "userid": message.author.id,
          "exp": int(exp)+1,
          "level": int(lv)
        }
        await db.replace_one({
          "userid": message.author.id
        }, jn)
        level = await db.find_one({
        "userid": message.author.id
        })
        lv=level["level"]
        if int(level["exp"]) >= int(lv)*3:
          await db.replace_one({
            "userid": message.author.id
          }, {
            "userid": message.author.id,
            "exp": int(level["exp"]),
            "level": int(level["level"])+1
          })
          await message.channel.send(f"Lv.{lv+1}に上がりました")"""
          

def setup(bot):
  bot.add_cog(lv(bot))
