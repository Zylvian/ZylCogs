import asyncio
import itertools
import json
import random

from redbot.core import commands, Config, checks
from redbot.core.data_manager import bundled_data_path, cog_data_path
from redbot.core.utils.predicates import MessagePredicate


from . import hat_song_download


class LilHat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)
        ###
        #self.path = bundled_data_path(self)
        self.path = cog_data_path(self)
        ##

        try:
            self.all_lyrics = self.load_lyrics()
        except FileNotFoundError:
            self.all_lyrics = []


    @commands.command(autohelp=True)
    async def hat_me(self, ctx):

        if self.all_lyrics:
            random_lyric = random.choice(self.all_lyrics)
            formatted_lyrics = self.format_lyrics(random_lyric)
            await ctx.send(formatted_lyrics)
        else:
            await ctx.send("Songs haven't been downloaded!")

    def format_lyrics(self, lyric):
        return "```\"{}\"\n-Lil Hat```".format(lyric)

    ###

    @commands.command(autohelp=True)
    async def update_hat(self, ctx):
        await self.download_songs(ctx)

    async def download_songs(self, ctx):
        botmsg = await ctx.send("Post Genius API token:")

        usercheck = MessagePredicate.same_context(ctx)

        try:
            msg = await self.bot.wait_for('message',
                                          timeout=15, check=usercheck)
        except asyncio.TimeoutError:
            await ctx.send("Timed out!")

        token = msg.content
        await msg.delete()
        await botmsg.delete()

        try:
            await ctx.send("Downloading songs...")
            hat_song_download.downloader(token, self.path)
            await ctx.send("Songs downloaded!")

            self.all_lyrics = self.load_lyrics()

        except ValueError as e:
            await ctx.send("Token invalid.")
            return

    @commands.command(autohelp=True)
    async def songs(self, ctx):
        songs = self.load_songs()
        title_string = "**Current songs:**\n"
        title_list = [title for title in songs.keys()]
        for title in title_list:
            title_string += "*{}*\n".format(title)


        await ctx.send(title_string)

    def load_songs(self):
        filepath = self.path / 'songs.json'
        with open(filepath) as json_file:
            return json.load(json_file)

    def load_lyrics(self):
        songs = self.load_songs()
        return self._get_all_lyrics_list(songs)


    def _get_all_lyrics_list(self, songs):
        song_list = [song for song in songs.values()]
        massive_list = [lyric for lyric in song_list]
        un_nested_list = list(itertools.chain.from_iterable(massive_list))
        return un_nested_list
