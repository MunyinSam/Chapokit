import discord
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import time

#-----------------------------------------------------------------
print("Current Working Directory:", os.getcwd())

uri = f"mongodb+srv://Munyin:Kelvinsam1@cluster0.bviirp8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())


#-----------------------------------------------------------------
# Commands

user_timers = {}

@bot.command(name="ใช้")
async def start_timer(ctx):
    if ctx.channel.id == 1212294270254448690:
        user_timers[ctx.author.id] = time.time()
        await ctx.send(f"{ctx.author}, your timer has started!")

@bot.command(name="เลิก")
async def stop_timer(ctx):
    if ctx.channel.id == 1212294270254448690:

        if ctx.author.id in user_timers:
            users_time = user_timers[ctx.author.id]
            elapsed_time = time.time() - users_time
            del user_timers[ctx.author.id]
            # Send a message with the elapsed time
            await ctx.send(f"{ctx.message.author}, you've stopped your timer. Time: {elapsed_time:.2f} seconds.")
        else:
            # If the user tries to stop a timer without starting one
            await ctx.send(f"{ctx.message.author}, you don't have an active timer.")



#-----------------------------------------------------------------
# Error Catch
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



#-----------------------------------------------------------------

bot.run("MTE3OTY5MzkzNzYzNjY5MjAyOA.GRIS8z.qem7u_G6XjDcTw8WhF2CuD-R1hb5VK8ldaLENk")