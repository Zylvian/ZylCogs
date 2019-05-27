from redbot.core import commands, Config, checks
import datetime
import dateutil.parser
import discord
import asyncio

from redbot.core.utils.predicates import MessagePredicate

defaults = {"toggled": False,
            "custom_msg":"Season 4 will premiere in",
            "msg_format": "{} **{}** days!",
            "premiere_date": None}


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

        print("Toggled:" + str(toggled))

        if toggled:
            if message.guild.me.mentioned_in(message):

                send_msg = await self.get_send_msg(self, gconf)

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

        await ctx.send("**Post your date in this format:** ***DAY MONTH YEAR***\n"
                       '*I.e* `17 04 1980` ')

        usercheck = MessagePredicate.same_context(ctx)

        try:
            message = await self.bot.wait_for('message',
                                          timeout=15, check=usercheck)

            new_date = dateutil.parser.parse(message.content)

            await ctx.send("**Is this the correct date?**\n{}\n(y/n)".format(new_date.strftime("%d %m %y")))

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
        await ctx.send("Toggled the cooldown tagger on!")

    @cd_tag.command()
    async def off(self, ctx):
        """Toggle your cooldown tagger off!"""
        gconf = self.config.guild(ctx.guild)
        await gconf.toggled.set(False)
        await ctx.send("Toggled the cooldown tagger off!")

    @cd_tag.command()
    async def message(self, ctx):
        """Set the response message!"""
        gconf = self.config.guild(ctx.guild)
        await ctx.send("**Set your message:**\nFormat: * _________ x days!*")

        usercheck = MessagePredicate.same_context(ctx)

        try:
            message = await self.bot.wait_for('message',
                                          timeout=15, check=usercheck)

            send_msg = await self.get_send_msg(self, gconf)
            await ctx.send('Message set!\n"{}'.format(send_msg))

        except asyncio.TimeoutError:
            await ctx.send("Timed out!")



    async def get_send_msg(self, gconf):

        custom_msg = await gconf.msg_format()
        msg_format = await gconf.msg_format()
        premiere_date = await gconf.premiere_date()

        if premiere_date is None:
            return

        premiere_date = dateutil.parser.parse(premiere_date).replace(tzinfo=None)
        curr_time = datetime.datetime.now().replace(tzinfo=None)
        days_til_something = (premiere_date - curr_time).days

        send_msg = msg_format.format(custom_msg, days_til_something)

        if days_til_something <= 0:
            send_msg = "Season 4 has already premiered!"