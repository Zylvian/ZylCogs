# Discord 
import discord
from redbot.core import commands
import random
import time
import unicodedata
import asyncio
import uuid
import datetime
import heapq
import lavalink
import math
import re
import time

# Red
from redbot.core import Config, bank, commands, checks
from redbot.core.data_manager import bundled_data_path


# Standard Library
import asyncio
import csv
import logging
import random
import textwrap
import uuid
from bisect import bisect
from copy import deepcopy
from itertools import zip_longest


# Red
from redbot.core import Config, bank, commands, checks

# Discord 
import discord
#from discord.ext import commands

# Others
import asyncio
import datetime
import random


class OneWordStory(commands.Cog):


    def __init__(self,bot):
        self.bot = bot
        self.config = Config.get_conf(self, 420420420, force_registration=True)
        
     
     
        ows_defaults = {'Cooldown': 3600,
                            'Counter': 0,
                            'Round_time': 1, # CHANGE ME to 100
                            'Start_time': 5, # Change me to 60
                            'Answer_time': 14,
                            'Max_words': 40,
                            'User_time_add': 20,
                            'Gallery_channel_id': None
                            }
                            
        # If releasing, make sure to change the channel ID. Can be an available command with e.g set_channel
        
        self.config.register_guild(**ows_defaults)

    @commands.group(autohelp=True)
    async def ows(self, ctx):
        """Ows group command"""
        pass

    @ows.command()
    async def counter_reset(self,ctx):
        """Resets the game counter!"""
        async with self.config.guild(ctx.guild).Counter() as counter:
            counter = 0
            await ctx.send("Counter reset to " + counter)

    @ows.group(autohelp=True)
    async def gallery(self, ctx):
        """Gallery settings"""
        pass
    
    @gallery.command()
    async def set_channel(self, ctx):
        """Set the gallery channel!"""
        def channelcheck(msg):
                return ctx.author == msg.author and len(msg.channel_mentions) > 0

        await ctx.send("Tag the channel.")
        choice = await ctx.bot.wait_for('message',   
                                        timeout=5
                                        ,check=channelcheck)
        new_gallery_channel = choice.channel_mentions[0]
        await self.config.guild(ctx.guild).set_raw("Gallery_channel_id", value=new_gallery_channel.id)
        await ctx.send("{} is the new One Word Story gallery!".format(new_gallery_channel.mention))
 
    @ows.command()
    async def start(self, ctx):
        """Starts a game of One Word Story!"""

        ows_values = {
                    "Games":{
                        "One Word Story":
                            {},
                        "Song":{
                            "Start": "It's time to make a song!"
                            }
                        }
                    }
    
        startup_lines = ["Did you hear of the...", "There once was a...", '"Morty, we gotta...',
                        "The old man from...","Somebody once told me...", "The universe is...",
                        "The fact of the matter is...", "Did you know that...", "Fyre makes soap out of...",
                        "The FBI doesnt know yet but...", "After a long talk my roommates and I decided that...",
                        "My father used to always say...",  "Your mother is...",
                        "Have you ever wondered about...", "Sorry I was late boss, I...", "Mom, it's not what it looks like. I was just...",
                        "One thing that people dont understand is...", "As a licensed professional I think that...",
                        "\"What are you doing?\" Don't worry I was just...", "When you look at it from a technical standpoint...", 
                        "Did you know that its illegal to...", "I watch Rick and Morty because..."]
        sad_lines = ["Oh. Well, I uh, I had better things to do anyways! Like uh, do things, and stuff! *By myself...*", "Hello? Nobody? No...?",
                     "Play with me, damnit! I refuse to go back to the butter-passing factory!", "Oh nobody? Bah, I guess you are all busy." \
                     " Or sick. Or dead. *Hopefully dead...*","**ECHO**,**echo**, echo, *echo*...",
                     "What music do I listen to? Good question, human who is actually my friend and actually exists. Thanks"\
                     " for not leaving me hanging here!  \n\n :'("]
        
        #game_name = random.choice(ows_values.keys())
        game_name = "One Word Story"

        # Counts the number of OWSes.
        try:
            counter = await self.config.guild(ctx.guild).get_raw(game_name,'Counter')
        except KeyError:
            counter = 1
            await self.config.guild(ctx.guild).set_raw(game_name, 'Counter', value = counter)

        def usercheck(message):
            return message.author != self.bot.user and message.channel.id == ctx.channel.id
        
        join_users = list()
        begin = datetime.datetime.now()
        current = begin
        # The time before it starts.
        start_time = await self.config.guild(ctx.guild).get_raw('Start_time')
        start_msg = await ctx.send("✎ **ONE WORD STORY TIME!** 📖\nBeep boop, it's time to play 'One Word Story!' Type **ows** in the chat to join! We start in {} seconds!".format(start_time))
        
        delmsgs = []
        delmsgs.append(start_msg)

        user_time_add = await self.config.guild(ctx.guild).get_raw('User_time_add')

        # Adds users who type "ows" into a list.
        try:
            while True:
                current = datetime.datetime.now()
                message = await self.bot.wait_for('message',    
                                              timeout=(start_time - (current-begin).seconds),check=usercheck
                                              )
                if message.author not in join_users and message.content.lower() == 'ows' and message.author != self.bot.user:
                    join_users.append(message.author)
                    await ctx.send("{} joined! {} seconds added to the game clock!".format(message.author.mention, user_time_add))
                
                # await message.delete()
                
        except asyncio.TimeoutError:
            pass
        
        if not join_users:
            stop_line = random.choice(sad_lines)
            delmsg = await ctx.send(stop_line)
            delmsgs.append(delmsg)
            return 1, delmsgs
            # return random.randint(30, 120)
            
        # Let the One WOrd Story start!
        join_users_copy = join_users.copy()
        start_line = random.choice(startup_lines)
        await ctx.send("Alright, lets begin! I'll go first: \n**{}**".format(start_line))
        await asyncio.sleep(3)
        start_line = start_line.strip(".")
        #start_line = start_line.strip('"')
        
        # Takes user input on a cycle.
        start_line = await self.take_input(ctx, join_users, start_line)

        start_line += "."
        # A string with all the user's nicks.
        users_string = "**Creators**: "
        for user in join_users_copy:
            users_string += user.display_name + ", "

        # Removes last two words.
        users_string = users_string[:-2]

        embed_string = start_line + "\n \n" + users_string
            
        counter += 1
        delmessage = await ctx.send("Let's see what we got here...")
        await asyncio.sleep(3)
        await delmessage.delete()

        embed = discord.Embed(
            colour=ctx.guild.me.top_role.colour,
            title = "One Word Story #{}".format(counter),
            description = ('{}').format(embed_string)
            )
        
        # FIX THIS
        # Sends the OWS in the current channel.
        await ctx.send(embed=embed)
        await self.config.guild(ctx.guild).set_raw(game_name, 'Counter', value = counter)

        # Post it to the gallery.
        gallery_channel_id = await self.config.guild(ctx.guild).Gallery_channel_id()

        if gallery_channel_id:
            gallery_channel = self.bot.get_channel(gallery_channel_id)
            await gallery_channel.send(embed=embed)
        # Saves the newest OWS.
        embed_dict = embed.to_dict()

        await self.save_ows_embed(ctx, join_users_copy, embed_dict, counter, game_name)
        newdelmsg = await ctx.send("Round finished!")
        delmsgs.append(newdelmsg)
        return 1, delmsgs
            

    async def save_ows_embed(self, ctx, participants, embed_dict, counter, game_name):
        self.gconf = self.config.guild(ctx.guild)
        participants = [member.id for member in participants]
        await self.gconf.set_raw(game_name, counter, "Embed",value=embed_dict)
        await self.gconf.set_raw(game_name, counter, "Participants",value=participants)
        await self.gconf.set_raw(game_name, counter, "Timestamp",value=int(time.time()))



    async def take_input(self, ctx, join_users, start_line):

        def usercheck(message):
            return message.author != self.bot.user and message.channel.id == ctx.channel.id

        begin = datetime.datetime.now()
        current = begin
        # COOLDOWN TIMEOUT WHATEVER
        timeout_value = await self.config.guild(ctx.guild).get_raw('Round_time')
        # Adds time to the clock when users join.
        user_time_add = await self.config.guild(ctx.guild).get_raw('User_time_add')
        timeout_value += user_time_add*len(join_users)
        user_cd = await self.config.guild(ctx.guild).get_raw('Answer_time')
        all_users = join_users[:] # Optionally join_users.copy()
        cd_users = list()
        maxwordcount = await self.config.guild(ctx.guild).get_raw('Max_words')
        wordcount = 0

        while True:
            
            # Picks a random user that's not "on cooldown", and if there are no available users, resets the "cooldown" of all the users.
            try:
                
                wordlength = 22
                # Picks a random user.
                tempuser = None
                while(True):
                    try:
                        tempuser = random.choice(join_users)
                        cd_users.append(tempuser)
                        join_users.remove(tempuser)
                        break
                    
                    except IndexError:
                        join_users = cd_users
                        cd_users = list()
                        tempuser = random.choice(join_users)
                   
                current = datetime.datetime.now()
                current=(timeout_value - (current-begin).seconds)

                # START OF WORD-ADDING
                wordmsg = await ctx.send("*{}*...\nAlright {}, give me a word! *{} seconds remaining...*".format(start_line, tempuser.mention, current))
                
                

                # User timer is a set number, but if the overall cooldown is below the user timer, then that is the new timeout value.
                if current < user_cd: 
                    user_cd = current
                
                while True:
                    message = await self.bot.wait_for('message',
                                                  timeout=user_cd, check=usercheck)
                                                        
                    if(message.author is tempuser):
                        content = message.content
                        if not len(content.split())>1:
                            if len(content) <= wordlength:
                                content.strip(' ')
                                start_line += " " + content
                                wordcount += 1
                                break
                                
                            else:
                                await ctx.send("Word too long!")
                        else:
                            await ctx.send("Only one word!")
                    
            # Either stops the game or goes to the next user.
            except asyncio.TimeoutError:
                current = datetime.datetime.now()
                timer=(timeout_value - (current-begin).seconds)
                
                
                # IF TIMER
                if timer <= 0:
                    return start_line

                else:
                    await ctx.send("Time out! Next user!")
                    #cd_users.append(tempuser)
                    """if usercheck(message):
                        cd_users.append(message.author)"""

    
