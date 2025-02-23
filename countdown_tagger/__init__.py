from redbot.core import commands
from .countdown_tagger import Countdown_Tagger


async def setup(bot: commands.Bot):
    cog = Countdown_Tagger(bot)
    await bot.add_cog(cog)
