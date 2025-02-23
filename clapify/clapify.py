import json

import discord
from redbot.core import commands, Config, app_commands
from redbot.core.utils import chat_formatting
from typing import Union, Optional


class Clapify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)

    @commands.bot_has_permissions(manage_messages=True)
    @commands.command()
    async def clapify(self, ctx, emoji: Optional[discord.Emoji], *, message_id_or_string: Union[int, str]):
        """Give me a string or a message ID!"""
        #
        user_name = ctx.author.display_name

        if not emoji:
            emoji = "👏"

        if message_id_or_string:
            if not isinstance(message_id_or_string, str):
                channel = ctx.channel
                msg = await channel.fetch_message(message_id_or_string)
                message_id_or_string = msg.content

        clapified_str = message_id_or_string.replace(" ", " {} ".format(emoji))
        clapified_pages = list(chat_formatting.pagify(clapified_str))
        clapified_pages[-1] += ("\n*(clapified by {})*".format(user_name))

        await ctx.message.delete()

        for page in clapified_pages:
            await ctx.send(page)

    @commands.command(autohelp=True)
    async def testballs(self, ctx, butt: int):
        channel = ctx.channel
        msg = await channel.fetch_message(butt)
        msg = msg.content
        await ctx.send(msg)
