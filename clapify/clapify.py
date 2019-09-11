import json

from redbot.core import commands, Config, checks
from redbot.core.utils import chat_formatting
import discord
from typing import Union, Optional


class Clapify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)

    @commands.command(autohelp=True)
    async def clapify(self, ctx, emoji: Optional[discord.Emoji], *, var: Union[int, str]):
        """Give me a string or a message ID!"""
        #
        if not emoji:
            emoji = "👏"

        if var:
            if not isinstance(var, str):
                channel = ctx.channel
                msg = await channel.fetch_message(var)
                var = msg.content

        pages = chat_formatting.pagify(var)

        clapified_pages = [x.replace(" ", " {} ".format(emoji)) for x in pages]

        await ctx.message.delete()
        
        for page in clapified_pages:
            await ctx.send(page)

    @commands.command(autohelp=True)
    async def testballs(self, ctx, butt:int):
        channel = ctx.channel
        msg = await channel.fetch_message(butt)
        msg = msg.content
        await ctx.send(msg)


