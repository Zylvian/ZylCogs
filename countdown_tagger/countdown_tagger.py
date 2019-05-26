from redbot.core import commands, Config, checks
import discord
import asyncio

#defaults = {"Only_Image_Channels": [],
         #   }


class Countdown_Tagger(commands.Cog):

    def __init__(self):
        self.database = Config.get_conf(self, identifier=420420420, force_registration=True)
        #self.database.register_guild(**defaults)

    """async def on_message(self, message):
        async with self.database.guild(message.guild).Only_Image_Channels() as only_image_channels:
            if message.channel.id in only_image_channels:
                if len(message.attachments) < 1:
                    await message.delete()"""

    async def on_message(self, message):
        if message.author.id == 233669548673335296:
            message.channel.send("ayo")

