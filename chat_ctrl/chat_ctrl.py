from redbot.core import commands, Config, checks
import discord
import asyncio

defaults = {"Only_Image_Channels": [],  
            } 

class Chat_Ctrl(commands.Cog):

    
    def __init__(self):
        self.database = Config.get_conf(self, identifier=420420420, force_registration=True)
        self.database.register_guild(**defaults)

    @commands.Cog.listener()
    async def on_message(self, message):
        async with self.database.guild(message.guild).Only_Image_Channels() as only_image_channels:
            if message.channel.id in only_image_channels:
                if len(message.attachments)<1:
                    await message.delete()
        

    async def add_img_only_channel(self, ctx, input_channel:discord.TextChannel=None):

        # If nothing, add current channel
        # If an ID, add that ID IF it exists.
        # If a name, check if it exists and add it.
        # If not, send an error message.

        async with self.database.guild(ctx.guild).Only_Image_Channels() as only_image_channels:


            # If no additional input was given.
            if input_channel is None:
                input_channel = ctx.channel

            if input_channel.id not in only_image_channels:
                    only_image_channels.append(input_channel.id)
                    await ctx.send("Added the specified channel!")
            else:
                await ctx.send("This channel has already been added!")

    @checks.mod_or_permissions(administrator=True)
    @commands.command()
    async def img_only(self, ctx):
        """Configure channels where only images are allowed."""

        try:

            def channelcheck(msg):
                return ctx.author == msg.author and len(msg.channel_mentions) > 0

            choice = await self.get_int_choice(ctx, "What do you want to do?\n1. List all image only channels.\n2. Add a new image only channel.")
        
            # Adds a new channel
            if choice == 2:
                choice = await self.get_int_choice(ctx, "This or another channel?\n1. This.\n2. Another.")

                if choice == 1:
                    await self.add_img_only_channel(ctx)
                if choice == 2:
                    await ctx.send("Tag the channel.")
                    choice = await ctx.bot.wait_for('message',   
                                                    timeout=5
                                                    ,check=channelcheck)
                    await self.add_img_only_channel(ctx, choice.channel_mentions[0])

            # Lists image only channel
            elif choice == 1:
                async with self.database.guild(ctx.guild).Only_Image_Channels() as only_image_channels:
                    await ctx.send(only_image_channels)
            else:
                await ctx.send("Incorrect option!")

        except asyncio.TimeoutError:
            await ctx.send("Timed out!")

    async def get_int_choice(self, ctx, out_msg):

        await ctx.send(out_msg)

        def intcheck(message):
                return message.content.isdigit() and message.author==ctx.author

        choice = await ctx.bot.wait_for('message',    
                                                timeout=5,
                                                check=intcheck
                                                )
        return int(choice.content)

    async def list_img_only_channels(self, ctx):
        await ctx.send("Balls 2!")