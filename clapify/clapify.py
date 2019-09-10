from redbot.core import commands, Config, checks
import discord
from typing import Union, Optional


class Clapify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)

    @commands.command(autohelp=True)
    async def clapify(self, ctx, *, var: Union[discord.Message, str]):
        """Give me a string or a message ID!"""
        #emoji: Optional[discord.Emoji],
        #if not emoji:
        emoji = "👏"

        if not isinstance(var, str):
            var = var.content

        clapified_str = var.replace(" ", " {} ".format(emoji))

        await ctx.send(clapified_str)


