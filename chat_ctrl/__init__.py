from .chat_ctrl import Chat_Ctrl


async def setup(bot):
    await bot.add_cog(Chat_Ctrl())
