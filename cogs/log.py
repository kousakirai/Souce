import discord
from discord.ext import commands
from datetime import datetime
import pytz


class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%D %H:%M')
        embed = discord.Embed(title="メッセージ",
                              description=f"メッセージを取得しました。\n時刻(JST):{now}",
                              color=0x00ff00)
        embed.add_field(
            name="発言者",
            value=
            f"{message.author.mention}({message.author})\nID:{message.author.id}",
            inline=False)
        embed.add_field(
            name="チャンネル",
            value=
            f"{message.channel.mention}({message.channel.name})\nID:{message.channel.id}",
            inline=False)
        embed.add_field(name="メッセージ内容",
                        value="なし" if not message.content else message.content,
                        inline=False)
        await self.bot.get_channel(821245836163547176).send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.bot.get_user(payload.user_id).bot:
            return
        message = await self.bot.get_channel(payload.channel_id
                                             ).fetch_message(payload.message_id
                                                             )
        now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%D %H:%M')
        embed = discord.Embed(title="リアクション追加",
                              description=f"リアクションの追加を検知しました。\n時刻(JST):{now}",
                              color=0x00ffff)
        embed.add_field(
            name="発言者",
            value=
            f"{message.author.mention}({message.author})\nID:{message.author.id}",
            inline=False)
        embed.add_field(
            name="チャンネル",
            value=
            f"{message.channel.mention}({message.channel.name})\nID:{message.channel.id}",
            inline=False)
        embed.add_field(name="メッセージリンク", value=message.jump_url, inline=False)
        embed.add_field(name="リアクション", value=str(payload.emoji), inline=False)
        embed.add_field(
            name="リアクションを追加した人",
            value=
            f"{payload.member.mention}({payload.member})\nID:{payload.member.id}",
            inline=False)
        await self.bot.get_channel(821245836163547176).send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%D %H:%M:%S')
        embed = discord.Embed(title="メンバーの参加",
                              description=f"メンバーが参加しました。\n時刻(JST):{now}",
                              color=0x00ff88)
        embed.add_field(
            name="参加者",
            value=
            f"{member.mention}({member})\nID:{member.id}\n詳しくは`h:user info {member.id}`で確認してください。"
        )
        await self.bot.get_channel(821245836163547176).send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        embed = discord.Embed(title="招待リンク作成",
                              description="招待リンクが作成されました",
                              color=0x00ff88)
        embed.add_field(name="招待リンク",
                        value=f"https://discord.gg/{invite.code}")
        embed.add_field(
            name="作成者",
            value=f"ユーザー名:{invite.inviter} ユーザーID:{invite.inviter.id}")
        embed.add_field(name="期限",
                        value="期限なし" if str(invite.max_age) == "0" else
                        f"{invite.max_age // 60}分")
        embed.add_field(name="入れる回数",
                        value="無限" if str(invite.max_uses) == "0" else
                        f"{invite.max_uses}回")
        await self.bot.get_channel(821245836163547176).send(embed=embed)


def setup(bot):
    return bot.add_cog(log(bot))
