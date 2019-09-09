from redbot.core import commands, Config, checks
import datetime
import dateutil.parser
import discord
import asyncio

from redbot.core.utils.predicates import MessagePredicate


class Screw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        gconf = self.config.guild(message.guild)

        if "screw" in message.content:
            send_msg = "screw \n \nscrew"

            await message.channel.send(send_msg)
