from redbot.core import commands, Config, checks
import discord
import asyncio

class Screw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        gconf = self.config.guild(message.guild)

        if "screw" in message.content.lower() and message.author != self.bot.user:
            send_msg = "screw \n \nscrew"

            await message.channel.send(send_msg)

            asyncio.sleep(2)
