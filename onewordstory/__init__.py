
from .onewordstory import OneWordStory
from redbot.core import commands

async def setup(bot: commands.Bot):
    cog = OneWordStory(bot)
    await bot.add_cog(cog)
    
 