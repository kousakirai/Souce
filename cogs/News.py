from discord.ext import commands
import feedparser
from discord.ext import tasks
import json


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks = [self.get_news.start()]

    def news_get(self):
        no_news_flg = 1
        news_list = []
        site_name_list = []
        site_name_list.append('日テレ')
        site_name_list.append('sankei')
        site_name_list.append('yahoo')

        rss_url_list = []
        rss_url_list.append(
            'https://www.news24.jp/rss/index.rdf')  #AUTOMATONのRSS-URL
        rss_url_list.append(
            'https://www.sankeibiz.jp/rss/news/flash.xml')  #GameSparkのRSS-URL
        rss_url_list.append(
            ''
        )  #4GamerのRSS-URL

        #各ログのファイルパス
        log_path_list = []
        log_path_list.append(
            'cogs/Newslogs/asahi_log.txt')  #AUTOMATONのlogファイルパス
        log_path_list.append(
            'cogs/Newslogs/sankei_log.txt')  #GameSparkのlogファイルパス
        log_path_list.append('cogs/Newslogs/yahoo_log.txt')  #4Gamerのlogファイルパス
        for path in log_path_list:
            with open(path, "r") as f:
                old_news_url = f.read()
            print('前回取得したニュースURL: ' + old_news_url)
        for path2 in rss_url_list:
            d = feedparser.parse(path2)
        for entry in d.entries:
            if old_news_url == entry.link:
                print("最新のニュースは以上です。")
                break
            no_news_flg = 0
            print(entry.title, entry.link)
            news_list.append(entry.title + '\r\n' + entry.link)

        if no_news_flg == 0:
            try:
                for news1 in news_list:
                    with open(path, mode='w') as f:
                        f.write(json.dumps(news1))
            except IndexError:
                print('正常にニュースを取得できませんでした。')
                print('次のサイトのRSSフィード等を再度確認してください: ' + site_name_list)
        else:
            news_list.append('最新のニュースはありません')
            returnlist = []
            for i in news_list:
                returnlist.append(i)
        return returnlist

    @commands.command(name="News")
    async def testnews(self, ctx):
        guild = self.bot.get_guild(774477394924666890)
        channel = guild.get_channel(774486601710436392)  #発言チャンネルを指定
        news_list = self.news_get()
        #ニュースをチャットに送信
        for news in news_list:
            await channel.send(news)

    @tasks.loop(hours=2)
    async def get_news(self):
        await self.bot.wait_until_ready()
        news_list = self.news_get()
        #ニュースをチャットに送信
        for news in news_list:
            guild = self.bot.get_guild(774477394924666890)
            channel = guild.get_channel(774486601710436392)
            await channel.send(news)

    def cog_unload(self):
        for t in self.tasks:
            t.cancel()


def setup(bot):
    return bot.add_cog(News(bot))
