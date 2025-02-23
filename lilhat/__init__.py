from .lilhat import LilHat


async def setup(bot):
    await bot.add_cog(LilHat(bot))
