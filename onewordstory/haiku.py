import asyncio
import random

import syllables


async def _haiku(self, ctx):
    await ctx.send("Welcome to the haiku games yeehaw")
    user_cd = 30


    async def get_haiku_line(sylls) -> str:
        while True:
            await ctx.send(f"Give me {sylls} syllables")
            message = await self.bot.wait_for('message',
                                              timeout=user_cd, check=usercheck)
            cont = message.content
            act_sylls = syllables.estimate(cont)
            if sylls != act_sylls:
                await ctx.send("Wrong amount of syllables.")
            else:
                return cont


    def usercheck(message):
        return message.author != self.bot.user and message.channel.id == ctx.channel.id


    try:
        choices = [[2, 3], [3, 4], [2, 3]]
        haiku = ""
        for bah in choices:
            random.shuffle(bah)
            for num in bah:
                haiku += await get_haiku_line(num) + " "

            haiku += "\n"

        await ctx.send("And what's the name of this haiku?")
        message = await self.bot.wait_for('message',
                                          timeout=user_cd, check=usercheck)
        title = message.content

    except asyncio.TimeoutError:
        await ctx.send("Timed out, closing this battle.")

    await ctx.send(f"***~~{title}:~~***")
    await ctx.send(f"```\n{haiku}```")