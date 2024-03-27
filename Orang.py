import discord
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import random

from db import *

#----------------------------------------------------------------------

print("Current Working Directory:", os.getcwd())

uri = f"mongodb+srv://Munyin:Kelvinsam1@cluster0.bviirp8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())



#----------------------------------------------------------------------

@bot.command(name="Roll")
async def RollDice(ctx):

    roll = random.randint(1,6)
    await ctx.send(roll)


#-----------------------------------------------------------------

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



# -------------------------

bot.run("MTE3OTY5MzkzNzYzNjY5MjAyOA.GRIS8z.qem7u_G6XjDcTw8WhF2CuD-R1hb5VK8ldaLENk")