import json

from redbot.core import commands, Config, checks
from redbot.core.utils import chat_formatting
import discord
from typing import Union, Optional


class Derpify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)

    @commands.command(autohelp=True)
    async def derpify(self, ctx,  *, var: Union[int, str]):
        """Give me a string or a message ID!"""
        #
        user_name = ctx.author.display_name


        if var:
            if not isinstance(var, str):
                channel = ctx.channel
                msg = await channel.fetch_message(var)
                var = msg.content


        derpyfied_str = self._string_derp(var)
        derpyfied_pages = list(chat_formatting.pagify(derpyfied_str))
        derpyfied_pages[-1] += ("\n*(derpyfied by {})*".format(user_name))


        await ctx.message.delete()

        for page in derpyfied_pages:
            await ctx.send(page)

    def _string_derp(self, stringy):
        r_string = ""
        for i, letter in enumerate(stringy):
            if (letter == ' '):
                i = i - 1
            elif (i % 2 != 0):
                letter = letter.upper()
            else:
                letter = letter.lower()

            r_string += letter

        return r_string


