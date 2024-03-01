import discord
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from datetime import datetime, timezone
import asyncio

from db import *


#----------------------------------------------------------------------

print("Current Working Directory:", os.getcwd())

uri = f"mongodb+srv://Munyin:Kelvinsam1@cluster0.bviirp8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

#----------------------------------------------------------------------

voice_channel_join_times = {}

@bot.event
async def on_voice_state_update(member, before, after):

    channel_id = 1212976255369093190  # Replace with your actual channel ID

    # Get the channel object
    channel = bot.get_channel(channel_id)

    # User joins a voice channel
    if before.channel is None and after.channel is not None:
        voice_channel_join_times[member.id] = datetime.now(timezone.utc)
        await channel.send(f"{member.name} joined a voice channel.")

        member = member.name
        student_exist = check_exist(f"{member}")
        if student_exist == True:
            print(f"{member} joined a voice channel.")
        else:
            create_student(f"{member}")

    # User leaves a voice channel
    elif before.channel is not None and after.channel is None:
        join_time = voice_channel_join_times.pop(member.id, None)

        if join_time:
            await channel.send(f"{member.name} left a voice channel.")
            duration = datetime.now(timezone.utc) - join_time
            minutes = round(divmod(duration.total_seconds(), 60)[0])
            seconds = round(duration.total_seconds())
            message = f"{member.name} left the voice channel after {minutes} minutes. {seconds} seconds"
            print(f"{member.name} left the voice channel after {minutes} minutes. {seconds} seconds")
            update_time(f"{member}", seconds)
            
        else:
            message = f"Could not calculate time for {member.name}."

            # Send the message to the designated channel
        if channel:  # Check if the channel was found
            await channel.send(message)
        else:
            print("Notification channel not found.")


# -----------------------------------------------------------------------------------
            
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# ------------------------------------------------------------------------------------

bot.run("MTE3OTY5MzkzNzYzNjY5MjAyOA.GRIS8z.qem7u_G6XjDcTw8WhF2CuD-R1hb5VK8ldaLENk")