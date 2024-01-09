import discord
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

from db import *

#----------------------------------------------------------------------

print("Current Working Directory:", os.getcwd())

uri = f"mongodb+srv://Munyin:Kelvinsam1@cluster0.bviirp8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

#----------------------------------------------------------------------

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

@bot.command(name='duel')
async def duel(ctx, opponent: discord.Member):
    if opponent.bot or opponent == ctx.author:
        await ctx.send("You can't duel a bot or yourself!")
        return

    if opponent.id in duel_requests:
        await ctx.send(f"{opponent.display_name} already has a pending duel request.")
        return

    await ctx.send(f"{opponent.mention}, you have been challenged to a duel by {ctx.author.mention}! Type '.accept' to accept the challenge.")
    duel_requests[opponent.id] = {
        'challenger_id': ctx.author.id,
        'opponent_id': opponent.id
    }
    print(duel_requests)

@bot.command(name='accept')
async def accept(ctx):
    if ctx.author.id not in duel_requests:
        await ctx.send("You don't have any pending duel requests.")
        return

    duel_info = duel_requests.pop(ctx.author.id)
    challenger = ctx.guild.get_member(duel_info['challenger_id'])
    opponent = ctx.guild.get_member(duel_info['opponent_id'])

    await ctx.send(f"{ctx.author.mention} has accepted the duel challenge from {challenger.mention}! Let the duel begin!")

    challengerPlayer = get_stats(f'{challenger}')
    opponentPlayer = get_stats(f'{opponent}')

    embed = discord.Embed(title=f"@{challenger} Stats", color= discord.Color.green())
    embed.set_thumbnail(url=challenger.avatar)
    embed.add_field(name="Money Left", value=f"{challengerPlayer['balance']}",inline=False)
    embed.add_field(name="Crimes", value=f"{challengerPlayer['stealCount']}",inline=False)

    await ctx.send(embed=embed)

    embed = discord.Embed(title=f"@{opponent} Stats", color= discord.Color.red())
    embed.set_thumbnail(url=opponent.avatar)
    embed.add_field(name="Money Left", value=f"{opponentPlayer['balance']}",inline=False)
    embed.add_field(name="Crimes", value=f"{opponentPlayer['stealCount']}",inline=False)

    await ctx.send(embed=embed)

    start_game(challenger,opponent)

    
# ------------- Duel Gameplay ------------
    
@bot.command()

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
    

bot.run("MTE3OTY5MzkzNzYzNjY5MjAyOA.G9rkp2.l4myIEQHH21JoGB0p71BqNyxMmLUmZh5nW6agI")