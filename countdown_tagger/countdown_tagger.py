from redbot.core import commands, Config, checks
import datetime
import dateutil.parser
import discord
import asyncio

#defaults = {"Only_Image_Channels": [],
         #   }


class Countdown_Tagger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.database = Config.get_conf(self, identifier=420420420, force_registration=True)
        self.premiere_date = "2019-11-01T00:00:00+0100"
        #self.database.register_guild(**defaults)


    async def on_message(self, message: discord.Message):
        #if self.bot.user.mentioned_in(message):
        if message.guild.me.mentioned_in(message):
            await message.channel.send("cehck me out")
            premiere_time = dateutil.parser.parse(self.premiere_date).replace(tzinfo=None)
            curr_time = datetime.datetime.now().replace(tzinfo=None)
            days_til_premiere = (premiere_time-curr_time).days

            send_msg = "Season 4 will premiere in **{}** days!".format(days_til_premiere)

            #if days_til_premiere <= 0:
            #    send_msg = "Season 4 has already premiered!"

            await message.channel.send(send_msg)

        #if message.author.id == 233669548673335296:
        #    await message.channel.send("ayo")

    @checks.mod_or_permissions(administrator=True)
    @commands.command()
    async def testman(self, ctx):
        await ctx.send("yeah I exist")
