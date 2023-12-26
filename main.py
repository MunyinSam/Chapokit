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
    
@bot.command(name='auc')
async def auction_command(ctx):
    
    price = auction()
    await ctx.send(price)

# ------------- 100% Orange Juice ------------

duel_requests = {}

@bot.command(name='duel')
async def duel(ctx, opponent: discord.Member):
    if opponent.bot or opponent == ctx.author:
        await ctx.send("You can't duel a bot or yourself!")
        return

    if opponent.id in duel_requests:
        await ctx.send(f"{opponent.display_name} already has a pending duel request.")
        return

    await ctx.send(f"{opponent.mention}, you have been challenged to a duel by {ctx.author.mention}! Type '.accept' to accept the challenge.")

    duel_requests[opponent.id] = ctx.author.id
    print(duel_requests)
    print(opponent.id)

@bot.command(name='accept')
async def accept(ctx):
    if ctx.author.id not in duel_requests:
        await ctx.send("You don't have any pending duel requests.")
        return

    challenger_id = duel_requests.pop(ctx.author.id)

    await ctx.send(f"{ctx.author.mention} has accepted the duel challenge from <@{challenger_id}>! Let the duel begin!")

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