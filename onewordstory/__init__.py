
from .onewordstory import OneWordStory
from redbot.core import commands

def setup(bot: commands.Bot):
    cog = OneWordStory(bot)
    bot.add_cog(cog)
    
 