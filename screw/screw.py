from redbot.core import commands, Config, checks
import discord
import asyncio
import random

class Screw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=420420420, force_registration=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        gconf = self.config.guild(message.guild)

        if "screw" in message.content.lower() and message.author != self.bot.user:
            send_msg = self.roll_hook()

            await message.channel.send(send_msg)

            await asyncio.sleep(2)


    def roll_hook(self):

        chance = 8

        roll = random.randint(0, 100)

        if roll <= chance:
            line = random.choice(self.get_lyrics().split('\n'))
            return line

        else:
            return "screw \n \nscrew"


    def get_lyrics(self):
        return """Ahh, Uh P-Mo bump babu
This is the story of Captain Hook
A young Swede that liked to cook up rhymes
In the bathroom all alone
Singing hooky hooky gibberish into his phone
There's no need to steal from Marvin Gaye (no!)
When the hottest hooks are public domain
'Cause if Foster Sylvers's got a misdemeanor
I'll Madoff with a felony explicit or clean
Or whatever you need to bleep in the mix
I still make hits that don't even rhyme
That aren't even in time
[Hook: Baby Theo (Bootsy Collins)]
I'm Captain Hook (I'm so catchy)
I'm Captain Hook (I'm so catchy)
I'm Captain Hook (I'm catchy baby)
I'm Captain Hook (I'm so catchy)
[Verse 2: Baby Theo (Bootsy Collins) Mushy Krongold]
Through my veins, the chorus is coursin'
Mainstream and delicious like Boursin (yeah)
Franchise the verse in a spin-off (spin-off)
I'll climb Mount Cleverest on a Wim Hof (yeah)
I'll make your mother proud of you the family unit
I'll make your mother proud of you the family unit
I slow down when others go faster
Forget the writing, I own the master
(Gold futures trade) Take delivery
('Cause on a bank run, I got stability)
Learn somethin', edutainment
Focus on your breath, I'm a brain mint
[Hook: Baby Theo (Bootsy Collins)]
I'm Captain Hook (I'm so catchy)
I'm Captain Hook (So catchy)
I'm Captain Hook (I am so catchy)
I'm Captain Hook (Well uh)
[Breakdown: Baby Theo (Bootsy Collins)]
Oh wow
Wow
(Aye Joe, let it go)
Bed-wetter, go-getter
Just another J rappin'
GitHub bootstrappin'
Bed-wetter, go-getter
This is my life, this is my story
Bed-wetter, go-getter
Just another J rappin'
GitHub bootstrappin'
Bed-wetter, go-getter
This is my life, this is my story
I'm Captain Hook (I'm so catchy)
I'm Captain Hook He's very talented
I'm Captain Hook (So catchy baby)
I'm Captain Hook (Can you catch me now)
I'm Captain Hook He's very talented
I'm Captain Hook He's very talented
I'm Captain Hook (He's Captain Hook)
I'm Captain Hook
Break it down to the kinderlach, to the kinderlach
Ya buh buh buh buh bub
To the kinderlach
I'm Captain Hook
And I'm P-Mo baby"""
