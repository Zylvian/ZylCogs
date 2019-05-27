from redbot.core import commands, Config, checks
import datetime
import dateutil.parser
import discord
import asyncio

from redbot.core.utils.predicates import MessagePredicate

defaults = {"toggled": False,
            "msg_format": "Season 4 will premiere in **{}** days!"}


class Countdown_Tagger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)
        #self.premiere_date = "2019-11-01T00:00:00+0100"
        self.config.register_guild(**defaults)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        gconf = self.config.guild(message.guild)
        toggled = await gconf.toggled()

        if toggled:
            if message.guild.me.mentioned_in(message):

                msg_format = await gconf.msg_format()
                premiere_time = await gconf.premiere_date()

                if premiere_time is None:
                    return

                premiere_time = dateutil.parser.parse(self.premiere_date).replace(tzinfo=None)
                curr_time = datetime.datetime.now().replace(tzinfo=None)
                days_til_something = (premiere_time - curr_time).days

                send_msg = msg_format.format(days_til_something)

                if days_til_something <= 0:
                    send_msg = "Season 4 has already premiered!"

                await message.channel.send(send_msg)

    @checks.mod_or_permissions(administrator=True)
    @commands.group(autohelp=True)
    async def cd_tag(self, ctx):
        """Ows group command"""
        pass

    @cd_tag.command()
    async def date(self, ctx):
        """Set the date of your countdown!"""
        gconf = self.config.guild(ctx.guild)

        await ctx.send("Post your date in this format: **DAY MONTH YEAR**\n"
                       'I.e *17 04 1980* ')

        usercheck = MessagePredicate.same_context(ctx)

        try:
            message = await self.bot.wait_for('message',
                                          timeout=15, check=usercheck)

            new_date = dateutil.parser.parse(message.content)

            await ctx.send("Is this the correct date?\n{} (y/n)".format(new_date))

            message = await self.bot.wait_for('message',
                                              timeout=15, check=usercheck) # type: discord.Message

            if message.content == "y":
                await gconf.premiere_date.set(str(new_date))
                await ctx.send("Saved!")
            else:
                await ctx.send("Stopping.")

        except asyncio.TimeoutError:
            await ctx.send("Timed out!")



    @cd_tag.command()
    async def on(self, ctx):
        """Toggle your cooldown tagger on!"""
        gconf = self.config.guild(ctx.guild)
        await gconf.toggled.set(True)

    @cd_tag.command()
    async def off(self, ctx):
        """Toggle your cooldown tagger off!"""
        gconf = self.config.guild(ctx.guild)
        await gconf.toggled.set(False)
