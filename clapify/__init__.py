from .clapify import Clapify


async def setup(bot):
    await bot.add_cog(Clapify(bot))
