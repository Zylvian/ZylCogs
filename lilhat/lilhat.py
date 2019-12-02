import itertools
import json
import random

from redbot.core import commands, Config, checks
from redbot.core.utils import chat_formatting
import discord
from typing import Union, Optional


class LilHat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)

        with open('data/songs.json', 'r') as file:
            songs = json.load(file)

        self.all_lyrics = self._get_all_lyrics_list(songs)


    def _get_all_lyrics_list(self, songs):
        song_list = [song for song in songs.values()]
        massive_list = [lyric for lyric in song_list]
        un_nested_list = list(itertools.chain.from_iterable(massive_list))
        return un_nested_list

    @commands.command(autohelp=True)
    async def hat_me(self, ctx):
        random_lyric = random.choice(self.all_lyrics)
        await ctx.send(random_lyric)

