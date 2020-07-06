import math
import time
from typing import Optional

# Red
import syllables
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.chat_formatting import humanize_list

# Standard Library
import json

# Red
from redbot.core import Config, bank, commands, checks
from redbot.core.data_manager import bundled_data_path

# Discord 
import discord

# Others
import asyncio
import datetime
import random


class OneWordStory(commands.Cog):
    """Make a story one word at a time! (or any other amount of words)"""

    def __init__(self,bot):
        self.tasks = []
        self.bot = bot
        self.config = Config.get_conf(self, 420420420, force_registration=True)
        self.path = bundled_data_path(self)
     
     
        ows_defaults = {'Cooldown': 3600,
                            'Counter': 0,
                            'Round_time': 100, # CHANGE ME to 100
                            'Start_time': 60, # Change me to 60
                            'Answer_time': 14,
                            'Max_words': 40,
                            'User_time_add': 10,
                            'Gallery_channel_id': None,
                            'Startup_lines':['General'],
                            'Word_count': 1
                            }

        
        self.config.register_guild(**ows_defaults)

    """Required to stop shit that's looping"""
    def cog_unload(self):
        for task in self.tasks:
            task.cancel()

    @commands.group(autohelp=True)
    async def ows(self, ctx):
        """Ows group command"""
        pass

    @checks.mod_or_permissions(administrator=True)
    @ows.group(autohelp=True)
    async def gallery(self, ctx):
        """Gallery settings"""
        pass

    @checks.mod_or_permissions(administrator=True)
    @ows.group(autohelp=True)
    async def settings(self, ctx):
        """General OWS settings"""
        pass

    @settings.group(autohelp=True)
    async def lines(self, ctx):
        """Pick which starting lines to use with your bot!"""
        pass

    @settings.command()
    async def counter_reset(self,ctx):
        """Resets the game counter! (the "One Word Story #xx" counter)"""
        self.gconf = self.config.guild(ctx.guild)
        await self.gconf.Word_count.set(0)

        await ctx.send("Counter reset to 0!")

    @checks.mod_or_permissions(administrator=True)
    @ows.command()
    async def rules(self, ctx):
        """How this game works!"""
        await ctx.send("**One Word Story!**\n"
                       "After a game has launched, type **ows** to join!"
                       "When it's your turn, continue the story with the specified number of words! \n"
                       "Type **Goodbye!** whenever to vote for ending the story before the timer is up!"
                       "*(The timer resets for each new word added.)* ")


    # TODO: Make ows start [optional word count] and make this function - wordcount - the default.
    @settings.command()
    async def wordcount(self, ctx, word_count:int):
        """Set how many words are allowed per prompt!"""
        """self.gconf = self.config.guild(ctx.guild)
        wordcount = await self.gconf.Word_count()
        await ctx.send("The current amount of allowed words are **{}**.\nWhat do you wish to set it to?".format(wordcount))
        pred = MessagePredicate.valid_int(ctx)
        await ctx.bot.wait_for('message', timeout=7, check=pred)
        number_choice = pred.result  # Minus one due to 0-indexed"""
        self.gconf = self.config.guild(ctx.guild)

        if word_count < 1:
            return await ctx.send("You can't have 0 words!")
        else:
            await self.gconf.Word_count.set(word_count)
            return await ctx.send("Word count set to **{}**!".format(word_count))


    @lines.command()
    async def add(self, ctx):
        """Add a set of preset starting lines."""
        await self.add_or_rem(ctx, True)

    @lines.command()
    async def rem(self, ctx):
        """Remove one of the active sets of starting lines."""
        await self.add_or_rem(ctx, False)

    """"@lines.command()
    async def curr(self, ctx):
        #The current enabled lines.
        #await self.add_or_rem(ctx, False)
        #await self.lines
        pass"""

    """"@ows.command()
    async def add_line(self, ctx):
        current_categories = await self.gconf.Startup_lines()"""


    async def get_default_lines(self, ctx):
        filepath = self.path / 'default_lines.json'
        with open(filepath) as json_file:
            return (json.load(json_file))

    # Add is True, remove is False.
    async def add_or_rem(self, ctx, add_or_rem_bool: bool):

        def format_category_list(category_list):
            return_string = ""
            for i, item in enumerate(category_list):
                return_string += "\n**{}**. {}".format(i + 1, item)
            return return_string

        self.gconf = self.config.guild(ctx.guild)
        current_categories = await self.gconf.Startup_lines()

        # Gets available lines.
        default_json_lines_dict = await self.get_default_lines(ctx)
        message_str = ("**Current startup lines**: ")

        if add_or_rem_bool:
            default_json_categories = list(default_json_lines_dict["Startup_lines"])
            available_categories = [category for category in default_json_categories if category not in current_categories]
            pick_category_list_string = format_category_list(available_categories)

            # At the writing of this code, "humanize_list()" crashes upon receiving an empty list.
            try:
                current_categories_humanized = humanize_list(current_categories)
            except IndexError:
                current_categories_humanized = ""

            message_str += ("{}\n**All available**: {}\n*Which one do you want to add?*".format(current_categories_humanized,pick_category_list_string))

        else:
            pick_category_list_string = format_category_list(current_categories)
            message_str += "\n{}\n*Which one do you want to remove?*".format(pick_category_list_string)


        await ctx.send(message_str)


        try:
            while True:
                pred = MessagePredicate.valid_int(ctx)
                await ctx.bot.wait_for('message', timeout=7, check=pred)
                number_choice = pred.result - 1  # Minus one due to 0-indexed
                try:

                    # add_index = default_json_categories.index(add_category)
                    async with self.gconf.Startup_lines() as startup_lines:
                        if add_or_rem_bool:
                            add_category = available_categories[number_choice]
                            startup_lines.append(add_category)
                            return await ctx.send("Category added!")
                        else:
                            rem_category = current_categories[number_choice]
                            startup_lines.remove(rem_category)
                            return await ctx.send("Category removed!")
                except IndexError:
                    await ctx.send("Incorrect number!")
        except asyncio.TimeoutError:
            await ctx.send("Timed out!")

    @gallery.command()
    async def set(self, ctx, new_gallery_channel: discord.TextChannel):
        """Set the gallery channel!"""
        """def channelcheck(msg):
                return ctx.author == msg.author and len(msg.channel_mentions) > 0

        await ctx.send("Tag the channel.")
        choice = await ctx.bot.wait_for('message',   
                                        timeout=5
                                        ,check=channelcheck)
        new_gallery_channel = choice.channel_mentions[0]"""

        # TODO
        # Add permission check for gallery.

        await self.config.guild(ctx.guild).set_raw("Gallery_channel_id", value=new_gallery_channel.id)
        await ctx.send("{} is the new One Word Story gallery!".format(new_gallery_channel.mention))

    @gallery.command()
    async def rem(self, ctx, rem_gallery_channel: discord.TextChannel):
        await self.config.guild(ctx.guild).set_raw("Gallery_channel_id", value=rem_gallery_channel.id)
        await ctx.send("Removed gallery channel. No gallery channel is set.s")

    @ows.command()
    async def haiku(self, ctx):
        """Start a game of haiku!"""

        await ctx.send("Welcome to the haiku games yeehaw")

        async def get_haiku_line(sylls) -> str:
            user_cd = 15
            while True:
                await ctx.send(f"Give me {sylls} syllables")
                message = await self.bot.wait_for('message',
                                                  timeout=user_cd, check=usercheck)
                cont = message.content
                act_sylls = syllables.estimate(cont)
                if sylls != act_sylls:
                    print("Wrong amount of sylls.")
                else:
                    return cont


        def usercheck(message):
            return message.author != self.bot.user and message.channel.id == ctx.channel.id

        choices = [[2, 3], [3, 4], [2, 3]]
        haiku = ""
        for bah in choices:
            random.shuffle(bah)
            for num in bah:
                haiku += await get_haiku_line(num) + ""

            haiku += "\n"

        await ctx.send("Check out this haiku, children:")
        await ctx.send(f"```\n{haiku}````")

    @ows.command()
    async def start(self, ctx, wordcount: Optional[int]):
        """Starts a game of One Word Story!"""

        # Will be used later for self-looping OWSes.
        #self.tasks.append(self.bot.loop.create_task(self.start_cont(ctx)))

        await self.start_cont(ctx, wordcount)


    async def start_cont(self, ctx, wordcountopt):
        """ows_values = {
                    "Games":{
                        "One Word Story":
                            {},
                        "Song":{
                            "Start": "It's time to make a song!"
                            }
                        }
                    }"""

        self.gconf = self.config.guild(ctx.guild)
        current_categories = await self.gconf.get_raw("Startup_lines")
        filepath = self.path / 'default_lines.json'
        startup_lines = list()
        global bonus_round_time
        bonus_round_time = 0

        global max_words_allowed
        if not wordcountopt:
            max_words_allowed = await self.gconf.Word_count()
        else:
            max_words_allowed = wordcountopt

        with open(filepath) as json_file:  
            data = json.load(json_file)

            for name, line_list in data["Startup_lines"].items():
                if name in current_categories:
                    startup_lines.extend(line_list)

            sad_lines = data["Sad_lines"]
        
        
        #game_name = random.choice(ows_values.keys())
        game_name = "One Word Story"

        # Counts the number of OWSes.
        try:
            counter = await self.config.guild(ctx.guild).get_raw(game_name,'Counter')
        except KeyError:
            counter = 0
            await self.config.guild(ctx.guild).set_raw(game_name, 'Counter', value = counter)

        def usercheck(message):
            return message.author != self.bot.user and message.channel.id == ctx.channel.id
        
        join_users = list()
        begin = datetime.datetime.now()
        current = begin
        # The time before it starts.
        start_time = await self.config.guild(ctx.guild).get_raw('Start_time')
        start_msg = await ctx.send("✎ **ONE WORD STORY TIME!** 📖\n"
                                   "*Words per user: **{user_words}***\n"
                                   "Beep boop, it's time to play **'One Word Story!'**\nType **ows** in the chat to join! We start in {start_time} seconds!\n"
                                    "*Type **Goodbye.** to end the story early.*"
                                   .format(start_time=start_time,user_words=max_words_allowed))
        
        delmsgs = []
        delmsgs.append(start_msg)

        global user_time_add
        user_time_add = await self.config.guild(ctx.guild).get_raw('User_time_add')

        # Adds users who type "ows" into a list.
        try:
            while True:
                current = datetime.datetime.now()
                message = await self.bot.wait_for('message',    
                                              timeout=(start_time - (current-begin).seconds),check=usercheck
                                              )

                # Checks if the bad boy needs to be added.
                (join_users, join_bool) = await self.ows_join_check(ctx, message, join_users)
                if join_bool:
                    bonus_round_time += user_time_add
                    await ctx.send("+{} 🕒 total seconds have been added to the game clock!".format(bonus_round_time))

                
        except asyncio.TimeoutError:
            pass

        # If the list is empty
        if not join_users:
            stop_line = random.choice(sad_lines)
            delmsg = await ctx.send(stop_line)
            delmsgs.append(delmsg)
            return 1, delmsgs

        # Let the One Word Story start!
        start_line = random.choice(startup_lines)
        await ctx.send("Alright, lets begin! The number of words per message is **{}**! \nI'll go first: \n**{}**".format(await self.gconf.Word_count(), start_line))
        await asyncio.sleep(3)
        start_line = start_line.strip(".")


        ###

        # Takes user input on a cycle.
        start_line, end_users  = await self.take_input(ctx, join_users, start_line, bonus_round_time)

        ###

        start_line += "."
        # A string with all the user's nicks.
        users_string = "**Creators**: "
        for user in end_users:
            users_string += user.display_name + ", "

        # Removes last two words.
        users_string = users_string[:-2]

        embed_string = start_line + "\n \n" + users_string

        counter += 1

        delmessage = await ctx.send("Let's see what we got here...")
        await asyncio.sleep(3)
        await delmessage.delete()

        embed = discord.Embed(
            colour= await ctx.embed_color(),
            title = "One Word Story #{}".format(counter),
            description = ('{}').format(embed_string)
            )

        # TODO
        # Check for permission to send/make embeds.

        # Sends the OWS in the current channel.
        await ctx.send(embed=embed)
        await self.config.guild(ctx.guild).set_raw(game_name, 'Counter', value = counter)

        # Post it to the gallery (if it exists). Else skip.
        try:
            gallery_channel_id = await self.config.guild(ctx.guild).Gallery_channel_id()

            if gallery_channel_id:
                gallery_channel = self.bot.get_channel(gallery_channel_id)
                await gallery_channel.send(embed=embed)
        except:
            pass

        # Saves the newest OWS.
        embed_dict = embed.to_dict()

        await self.save_ows_embed(ctx, end_users, embed_dict, counter, game_name)
        newdelmsg = await ctx.send("Round finished!")
        delmsgs.append(newdelmsg)
        return 1, delmsgs
            

    async def save_ows_embed(self, ctx, participants, embed_dict, counter, game_name):
        self.gconf = self.config.guild(ctx.guild)
        participants = [member.id for member in participants]
        await self.gconf.set_raw(game_name, counter, "Embed",value=embed_dict)
        await self.gconf.set_raw(game_name, counter, "Participants",value=participants)
        await self.gconf.set_raw(game_name, counter, "Timestamp",value=int(time.time()))

    """
    Checks if the message is user join worthy.
    """
    async def ows_join_check(self, ctx, message:discord.Message, join_users: list) -> (list, bool):
        if message.author not in join_users and message.content.lower()=="ows":
                join_users.append(message.author)
                await ctx.send("{} joined!".format(message.author.mention))
                return join_users, True
        else:
            return join_users, False

    async def take_input(self, ctx, join_users, start_line, bonus_round_time:int):
        """The function that actually takes the user input."""

        def usercheck(message):
            return message.author != self.bot.user and message.channel.id == ctx.channel.id

        begin = datetime.datetime.now()
        current = begin

        # COOLDOWN TIMEOUT
        global timeout_value
        timeout_value = await self.config.guild(ctx.guild).get_raw('Round_time')
        timeout_value += bonus_round_time
        # Adds time to the clock when users join.
        user_time_add = await self.config.guild(ctx.guild).get_raw('User_time_add')

        user_cd = await self.config.guild(ctx.guild).get_raw('Answer_time')
        user_cd += 3*max_words_allowed
        pick_users = join_users.copy()
        cd_users = list()
        maxwordcount = await self.config.guild(ctx.guild).get_raw('Max_words')
        wordcount = 0 # To be used as an additional display of information.
        wordlength = 32


        while True:
            
            # Picks a random user that's not "on cooldown", and if there are no available users, resets the "cooldown" of all the users.
            try:
                # Here in case more users join
                nr_goodbyes_required = (int(math.floor(len(join_users)) / 2)) + 1
                # Reset goodbyes
                curr_goodbyes = 0

                # Picks a random user.
                if not pick_users:
                    pick_users = join_users.copy()

                tempuser = random.choice(pick_users)
                pick_users.remove(tempuser)

                current = datetime.datetime.now()
                current=(timeout_value - (current-begin).seconds)

                # START OF WORD-ADDING
                maybe_s_string = ""

                # If the amount of words is over 1, add an s to "word(s)".
                if max_words_allowed > 1:
                    maybe_s_string = "s"
                wordmsg = await ctx.send(f"**Story so far**\n```{start_line}...```\nAlright {tempuser.mention}, give me at most **{max_words_allowed}** word{maybe_s_string}! *{current} seconds remaining...*")
                                         #.format(start_line=start_line, max_words_allowed=max_words_allowed, user_mention=tempuser.mention, current=current, maybe_s_string=maybe_s_string))
                
                
                # User timer is a set number, but if the overall cooldown is below the user timer, then that is the new timeout value.
                if current < user_cd: 
                    user_cd = current
                
                # Checks the input messages
                while True:
                    message = await self.bot.wait_for('message',
                                                  timeout=user_cd, check=usercheck)

                    content = message.content

                    if content.lower() == "goodbye.":
                        curr_goodbyes += 1
                        await ctx.send("**{}**/**{}** goodbyes!".format(curr_goodbyes, nr_goodbyes_required))
                        if curr_goodbyes >= nr_goodbyes_required:
                            return start_line, join_users

                    elif(message.author is tempuser):
                        content = message.content

                        # Splits word at spaces.
                        content_word_list = content.split()
                        # If the amount of words is less than max allowed
                        if not len(content_word_list) > max_words_allowed:
                            # Checks all words.
                            words_addition = list()
                            for i, word in enumerate(content_word_list):
                                if len(content) <= wordlength:
                                    if (word in ".,?!;:"):
                                        if i == 0:
                                            start_line.rstrip()
                                            start_line += word
                                        else:
                                            words_addition[i] += word
                                    else:
                                        word.strip(' ') # Needed, maybe?
                                        words_addition.append(word)
                                        wordcount += 1
                                
                                else:
                                    await ctx.send("Word too long!")
                                    break

                            start_line += " " + " ".join(words_addition)
                            break

                        else:
                            await ctx.send("Max {} word{} allowed!".format(max_words_allowed, maybe_s_string))
                    # Any other people typing
                    else:
                        (join_users, join_bool) = await self.ows_join_check(ctx, message, join_users)
                        if join_bool:
                            timeout_value += user_time_add

                    
            # Either stops the game or goes to the next user.
            except asyncio.TimeoutError:
                current = datetime.datetime.now()
                timer=(timeout_value - (current-begin).seconds)
                
                
                # IF TIMER
                if timer <= 0:
                    return start_line, join_users

                else:
                    await ctx.send("Time out! Next user!")




