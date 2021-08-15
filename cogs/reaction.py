import discord
from discord.ext import commands


class role_add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:  # BOTアカウントは無視する
            return

        if payload.channel_id != 828936225897054218:  # 特定のチャンネル以外でリアクションした場合は無視する
            return

        if str(payload.emoji.name) == "<:sonota:774505088123011073>":  # 特定の絵文字
            await payload.member.add_roles(
                payload.member.guild.get_role(123456789123)  # ロールID
            )

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if guild is None or member is None:  # サーバーやメンバー情報が読めなかったら無視
            return

        if member.bot:  # BOTアカウントは無視する
            return

        if payload.channel_id != 123456789123:  # 特定のチャンネル以外でリアクションを解除した場合は無視する
            return

        if payload.emoji.name == "👍":  # 特定の絵文字
            await payload.member.remove_roles(
                payload.member.guild.get_role(123456789123)  # ロールID
            )


def setup(bot):
    return bot.add_cog(role_add(bot))
