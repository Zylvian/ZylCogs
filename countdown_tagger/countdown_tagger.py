from redbot.core import commands, Config, checks
import datetime
import dateutil.parser
import discord
import asyncio

from redbot.core.utils.predicates import MessagePredicate

defaults = {"toggled": False,
            "custom_msg": "Season 4 will premiere in",
            "msg_format": "{} **{}** days!",
            "premiere_date": None}


class Countdown_Tagger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)
        # self.premiere_date = "2019-11-01T00:00:00+0100"
        self.config.register_guild(**defaults)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        gconf = self.config.guild(message.guild)
        toggled = await gconf.toggled()

        if toggled:
            if message.guild.me.mentioned_in(message):
                send_msg = await self.get_send_msg(gconf)

                await message.channel.send(send_msg)

    @checks.mod_or_permissions(administrator=True)
    @commands.group(autohelp=True)
    async def cd_tag(self, ctx):
        """Cooldown Tagger group command!
        The current date is `{}`!""".format(await self.config.guild(ctx.guild).premiere_date())
        pass

    @cd_tag.command()
    async def date(self, ctx):
        """Set the date of your countdown!"""
        gconf = self.config.guild(ctx.guild)

        await ctx.send("**Post your date in this format:**\n`DAY MONTH YEAR`\n"
                       '*I.e 17 04 1980* ')

        usercheck = MessagePredicate.same_context(ctx)

        try:

            while True:
                message = await self.bot.wait_for('message',
                                                  timeout=15, check=usercheck)

                try:
                    new_date = dateutil.parser.parse(message.content, dayfirst=True)
                except ValueError as e:
                    await ctx.send("Incorrect date format! Try again:")
                days_until_something = self.get_days_until_date(new_date)
                if days_until_something <=0:
                    await ctx.send("This date has already passed! Try again:")
                else:
                    break

            await ctx.send("**Is this the correct date?**\n`{}`\n*(y/n)*".format(new_date.strftime("%d %m %y")))

            message = await self.bot.wait_for('message',
                                              timeout=15, check=usercheck)  # type: discord.Message

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


        await ctx.send('**Set your message:**\n*Format: "_________ x days!*"')

        usercheck = MessagePredicate.same_context(ctx)

        try:

            message = await self.bot.wait_for('message',
                                              timeout=15, check=usercheck)

            send_msg = await self.get_send_msg(gconf)
            await ctx.send('Message set!\n"{}'.format(send_msg))

        except asyncio.TimeoutError:
            await ctx.send("Timed out!")

    async def get_send_msg(self, gconf):

        premiere_date_str = await gconf.premiere_date()
        premiere_date = dateutil.parser.parse(premiere_date_str).replace(tzinfo=None)
        custom_msg = await gconf.custom_msg()
        msg_format = await gconf.msg_format()

        days_til_something = self.get_days_until_date(premiere_date)

        send_msg = msg_format.format(custom_msg, days_til_something)

        if days_til_something <= 0:
            send_msg = "*{}* has already passed!".format(premiere_date.strftime("%d %B, %Y"))

        return send_msg

    def get_days_until_date(self, premiere_date: datetime.datetime):

        curr_time = datetime.datetime.now().replace(tzinfo=None)
        days_til_something = (premiere_date - curr_time).days

        return days_til_something
