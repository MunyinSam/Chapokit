import discord
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from datetime import datetime, timezone

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

    channel_id = 922071029998821406  # Replace with your actual channel ID

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

@bot.command(name="crbank")
async def create_id(ctx):

    if ctx.channel.id == 1185882637093588992:  # Replace with the desired channel ID
        
        member = ctx.message.author
        player_exist = check_if_exist(f"{member}")

        if player_exist == True:
            embed = discord.Embed(title=f"@{member} Bank Account Already Exist", color= discord.Color.green())
            await ctx.send(embed=embed)   

        else:
            create_player(f"{member}")
            player_stats = get_stats(f"{member}")

            embed = discord.Embed(title=f"@{member} Bank Account Created", color= discord.Color.green())
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name="Name", value=f"{player_stats['name']}")
            embed.add_field(name="Balance", value=f'{player_stats['balance']}')
            embed.add_field(name="Crimes", value=f'{player_stats['stealCount']}')
            await ctx.send(embed=embed)

            embed = discord.Embed(title=f"@{member} PvP Stats", color=discord.Color.green())
            embed.add_field(name="Health", value=f"{player_stats['health']}", inline=True)
            embed.add_field(name="Attack", value=f'{player_stats["attack"]}', inline=True)
            embed.add_field(name="Defence", value=f'{player_stats["defence"]}', inline=True)
            embed.add_field(name="Evade", value=f'{player_stats["evade"]}', inline=True)
            embed.add_field(name="Wins", value=f'{player_stats["gamesWon"]}', inline=True)
            embed.add_field(name="Losts", value=f'{player_stats["gamesLost"]}', inline=True)
            await ctx.send(embed=embed)


        channel = bot.get_channel(1185891079468363796)

        # Check if the channel exists
        if channel:
            # Send the message to the specified channel
            await channel.send(f'{member} successfully created a Bank Account')

    else:
        await ctx.send('This command can only be used in "bank".')

@bot.command(name="steal")
async def stealing(ctx, victim: discord.Member):

    if ctx.channel.id == 1185882637093588992:
        victim_name = victim.name.lower()
        author_name = ctx.message.author.name.lower()

        luck = int(steal_chance())

        result = steal(author_name, victim_name, luck)
        await ctx.send(result)
    
        channel = bot.get_channel(1185891079468363796)

        # Check if the channel exists
        if channel:
            # Send the message to the specified channel
            await channel.send(f'{author_name} successfully stolen {luck} from {victim_name}')

@bot.command(name='bal')
async def check_balance(ctx):

    if ctx.channel.id == 1185882637093588992:
        member = ctx.message.author
        bankacc = get_stats(f'{member}')

        embed = discord.Embed(title=f"@{member} Balance", color= discord.Color.green())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Money Left", value=f"{bankacc['balance']}",inline=False)
        embed.add_field(name="Crimes", value=f"{bankacc['stealCount']}",inline=False)

        await ctx.send(embed=embed)
    


# ------------- 100% Orange Juice ------------

duel_requests = {}

# ------------- Duel Request ------------

@bot.command(name='c')
async def duel(ctx, opponent: discord.Member):
    if opponent.bot or opponent == ctx.author:
        await ctx.send("Stop abusing glitches")
        return

    if opponent.id in duel_requests:
        await ctx.send(f"{opponent.display_name} has a pending duel request.")
        return

    await ctx.send(f"{opponent.mention}, you have been challenged to a fight by {ctx.author.mention}! Type '.accept' to accept.")
    duel_requests[opponent.id] = {
        'challenger_id': ctx.author.id,
        'opponent_id': opponent.id
    }
    print(duel_requests)

@bot.command(name='a')
async def accept(ctx):
    if ctx.author.id not in duel_requests:
        await ctx.send("You don't have any pending duel requests.")
        return

    duel_info = duel_requests.pop(ctx.author.id)
    challenger = ctx.guild.get_member(duel_info['challenger_id'])
    opponent = ctx.guild.get_member(duel_info['opponent_id'])

    await ctx.send(f"{ctx.author.mention} has accepted the duel challenge from {challenger.mention}!")

    challengerPlayer = get_stats(str(challenger))
    opponentPlayer = get_stats(str(opponent))

    embed_challenger = discord.Embed(title=f"@{challenger} Stats", color=discord.Color.green())
    embed_challenger.set_thumbnail(url=challenger.avatar)
    embed_challenger.add_field(name="Money Left", value=f"{challengerPlayer['balance']}", inline=False)
    embed_challenger.add_field(name="Crimes", value=f"{challengerPlayer['stealCount']}", inline=False)

    await ctx.send(embed=embed_challenger)

    embed_opponent = discord.Embed(title=f"@{opponent} Stats", color=discord.Color.red())
    embed_opponent.set_thumbnail(url=opponent.avatar)
    embed_opponent.add_field(name="Money Left", value=f"{opponentPlayer['balance']}", inline=False)
    embed_opponent.add_field(name="Crimes", value=f"{opponentPlayer['stealCount']}", inline=False)

    await ctx.send(embed=embed_opponent)

    challenger, opponent, FirstTurn, roomID = start_game(challenger, opponent)
    print(challenger, opponent, FirstTurn, roomID)

    view = View()

    if FirstTurn == challenger:
        
        health_value = challengerPlayer['health']
        hearts = "❤️" * health_value

        embed_turn = discord.Embed(title=f"{challenger}'s turn", color=discord.Color.dark_grey())
        embed_turn.add_field(name="Health", value=hearts, inline=False)

        # Create a button with a custom ID
        button_label = "Roll"
        button = Button(label=button_label, style=discord.ButtonStyle.green, custom_id="roll_button")
        view.add_item(button)

        # Send the embed with the view
        await ctx.send(embed=embed_turn, view=view)


    else:

        health_value = opponentPlayer['health']
        hearts = "❤️" * health_value

        embed_turn = discord.Embed(title=f"{opponent}'s turn", color=discord.Color.dark_grey())
        embed_turn.add_field(name="Health", value=hearts, inline=False)

        button_label = "Roll"
        button = Button(label=button_label, style=discord.ButtonStyle.green, custom_id="roll_button")
        view.add_item(button)

        await ctx.send(embed=embed_turn, view=view)


    
# ------------- Duel Gameplay ------------
    
@bot.event
async def on_button_click(interaction):
    if interaction.custom_id == "roll_button":
        # Simulate rolling a six-sided die
        roll_result = random.randint(1, 6)

        # Respond to the button click with the roll result
        await interaction.respond(content=f"{interaction.user.mention} rolled a {roll_result}!")

# Not Related-----------------------------------------------------
    
@bot.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is added to the specific message
    if payload.message_id == 1189196722472239174:
        # Check if the reaction emoji is the one you are looking for
        if str(payload.emoji) == "<:thinkagain:EMOJI_ID>":
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            print("added emoji")
            # Check if the member already has the role
            role = discord.utils.get(guild.roles, name="does not support racer")
            if role and role not in member.roles:
                # Add the role to the member
                await member.add_roles(role)
                print(f"Added role {role.name} to {member.display_name}")


#-----------------------------------------------------------------

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



# -------------------------
    

bot.run("MTE3OTY5MzkzNzYzNjY5MjAyOA.GRIS8z.qem7u_G6XjDcTw8WhF2CuD-R1hb5VK8ldaLENk")