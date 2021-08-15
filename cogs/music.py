import asyncio
from discord.ext import commands
import discord
import youtube_dl
from discord.utils import get
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address':
    '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)


class Music(commands.Cog):
    """
    音楽機能のカテゴリです。
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('サブコマンドが不正です。')

    @music.command()
    async def join(self, ctx):

        if not ctx.message.author.voice:
            await ctx.send("あなたはボイスチャンネルに接続していません。")
            return
        else:
            channel = ctx.message.author.voice.channel
            self.queue = {}
            await ctx.send(f'``{channel}``に接続しました。')

        await channel.connect()

    @music.command()
    async def clear_queue(self, ctx):
        '''キューを空にします。'''
        self.queue.clear()
        user = ctx.message.author.mention
        await ctx.send(f"{user}がキューを空にしました。")
    @music.command()
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user = ctx.message.author.mention
        await voice_client.disconnect()
        await ctx.send(f'{user}がbotをボイスチャットから切断させました。')

    async def play_only(self, ctx):
            urls = self.d[0]
            player = await YTDLSource.from_url(urls, loop=self.bot.loop)
            embed=discord.Embed(title="音楽キューシステム",description=f"キューリストに追加されました。" ,color=0xff0000)
            embed.add_field(name="音楽名",value=f"{urls}",inline=False)
            async with ctx.typing():    
                await ctx.send(embed=embed)
                return ctx.guild.voice_client.play(player, after=lambda _:self.bot.loop.create_task(self.play_end(ctx)))
    
    async def play_end(self, ctx):
            self.d.popleft()
            if len(self.d) == 0:
                return await ctx.send("キューの中身が空になりました。再生を終了します。")
            else:
                await ctx.send("次の曲を再生します。")
                return self.play_only(ctx)
    
    @music.command()
    async def play(self, ctx,*,message):
        # youtubeから音楽をダウンロードする
        self.d.append(message)
        if len(self.d) == 0:
            await self.play_only(ctx)
    
    @music.command()
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        voice.pause()

        user = ctx.message.author.mention
        await ctx.send(f"<:pause_button:>{user}再生を中断しました。")
    @music.command()
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        voice.resume()

        user = ctx.message.author.mention
        await ctx.send(f"<:arrow_forward:>{user}再生を再開しました。")

    @music.command()
    async def view_queue(self, ctx):

        if len(self.queue) < 1:
            await ctx.send("キューは空です。")
        else:
            await ctx.send(f'現在再生中{self.queue}')

    @music.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("ボイスチャンネルに接続していません。")
        if volume <100:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send("音量を{}%に変更しました。".format(volume))
        else:
            await ctx.send("音量が指定できるのは100までです。")

def setup(bot):
    return bot.add_cog(Music(bot))
