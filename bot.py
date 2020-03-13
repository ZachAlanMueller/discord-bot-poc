import os
import random
import bisect

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


class WeightedChoice(object):
    def __init__(self, weights):
        self.totals = []
        self.weights = weights
        running_total = 0

        for w in weights:
            running_total += w[1]
            self.totals.append(running_total)

    def get(self):
        rnd = random.random() * self.totals[-1]
        i = bisect.bisect_right(self.totals, rnd)
        return self.weights[i][0]


maps = (
    ('Customs', 15), 
    ('Woods', 10), 
    ('Shoreline', 2), 
    ('Interchange', 20), 
    ('Reserve', 30), 
    ('Labs', 20)
)
times = (
    ('night', 10),
    ('day', 40)
)
playstyles = (
    ('chad it up!', 30),
    ('rat all that loot!', 10),
    ('snipe!', 10),
    ('be some thicc bois!', 30),
    ('take some thermals!', 10),
    ('do some quests!', 10),
    ('pistol whip some scavs!', 1),
    ('scav!', 5)
)
mapChoice = WeightedChoice(maps)
playstyleChoice = WeightedChoice(playstyles)
timeChoice = WeightedChoice(times)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        channel = message.channel
        await channel.send(msg)

    if message.content.startswith('!tarkov'):
        nextMap = mapChoice.get()
        nextTime = timeChoice.get()
        nextStyle = playstyleChoice.get()
        msg = ('Next you should go to '+nextMap + ' during the '+ nextTime + ' and '+ nextStyle).format(message)
        channel = message.channel
        await channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)