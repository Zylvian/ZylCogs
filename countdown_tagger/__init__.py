
from redbot.core import commands
from .countdown_tagger import Countdown_Tagger

def setup(bot: commands.Bot):

    cog = Countdown_Tagger(bot)
    bot.add_cog(cog)