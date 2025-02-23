from .derpify import Derpify


async def setup(bot):
    await bot.add_cog(Derpify(bot))
