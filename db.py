from datetime import datetime, timezone
from bson import ObjectId
from mongoengine import Document, fields, connect
import discord
from discord import app_commands
from discord.ext import commands
import random

# Connect to MongoDB
connect('RealDB', host='mongodb+srv://Munyin:Kelvinsam1@cluster0.bviirp8.mongodb.net/?retryWrites=true&w=majority')

# maindb--------------------------------

class Player(Document):
    name = fields.StringField(required=True)
    money = fields.IntField()
    stealCount = fields.IntField()
    health = fields.IntField()
    attack = fields.IntField()
    defence = fields.IntField()
    evade = fields.IntField()
    gamesWon = fields.IntField()
    gamesLost = fields.IntField()

class Item(Document):
    name = fields.StringField()
    attack = fields.IntField()
    defence = fields.IntField()

class FightRoom(Document):
    challenger = fields.StringField()
    opponent = fields.StringField()
    turn = fields.StringField()
    FirstTurn = fields.StringField()

def create_player(name):
    player_data = {
        'name': name,
        'money' : 1000,
        'stealCount' : 0,
        'health' : 5,
        'attack' : 2,
        'defence' : 1,
        'evade' : 1,
        'gamesWon' : 0,
        'gamesLost' : 0
    }
    player = Player(**player_data)
    player.save()

def create_item(name):
    Item_data = {
        'name': name,
        'attack' : 1000,
        'defence' : 3
    }
    item = Item(**Item_data)
    item.save()

#-----------------------------------------
    
def get_stats_item(item_name):
    
    item = Item.objects(name=item_name).first()

    if item:
        name = item.name
        attack = item.attack
        defence = item.defence

        print(name, attack, defence)

        return {
            "name": name,
            "attack": attack,
            "defence": defence
        }
    
    else:
        return None  

def get_stats(player_name):
    #print(player_name)
    player = Player.objects(name=player_name).first()
    
    if player:
        name = player.name
        balance = player.money
        stealCount = player.stealCount
        health = player.health
        attack = player.attack
        defence = player.defence
        evade = player.evade
        gamesWon = player.gamesWon
        gamesLost = player.gamesLost
        
        return {
            "name": name,
            "balance": balance,
            "stealCount": stealCount,
            'health' : health,
            'attack' : attack,
            'defence' : defence,
            'evade' : evade,
            'gamesWon' : gamesWon,
            'gamesLost' : gamesLost
        }
    else:
        return None

def steal(author, victim, amount):
    # Retrieve the player initiating the steal
    player_author = Player.objects(name=author).first()

    # Retrieve the victim
    player_victim = Player.objects(name=victim).first()

    if player_author and player_victim:
        # Check if the author has attempted too many steals

        # Increment the steal count for the author
        player_author.stealCount += 1
        player_author.save()

        stolen_amount = amount  

        # Check if the victim has enough balance to be stolen
        if player_victim.money >= stolen_amount:
            player_author.money += stolen_amount
            player_victim.money -= stolen_amount

            if stolen_amount == 1000:
                return f"JACKPOT!!! You successfully stole {stolen_amount} from {victim}!"
            elif stolen_amount == 600:
                return f"LUCKY!!! You successfully stole {stolen_amount} from {victim}!" 

            # Save changes to the database
            player_author.save()
            player_victim.save()

            return f"You successfully stole {stolen_amount} from {victim}!"
        else:
            return f"{victim} does not have enough money to be stolen."
    else:
        return "Invalid player names. Make sure both players exist."

def steal_chance():

    chance = random.randint(0,100)

    if chance < 50:
        return "50"
    elif chance >= 50 and chance < 70:
        return "100"
    elif chance >= 70 and chance < 80:
        return "150"
    elif chance >= 70 and chance < 80:
        return "200"
    elif chance >= 80 and chance < 90:
        return "400"
    elif chance >= 90 and chance < 99:
        return "600"
    elif chance == 100:
        return "1000"
       
# -------------- 100% Orange Juice -------------------------

def rolldice():
    diceNum = random.randint(1,6)
    return diceNum

def doDamage(challenger, opponent):
    pass

def fightMenu(Player1,Player2):
    pass

def start_game(challenger, opponent):
    challenger_str = str(challenger)
    opponent_str = str(opponent)

    FirstTurn = str(random.choice([challenger_str, opponent_str]))
    print(f"First Turn: {FirstTurn}")
    print(challenger_str, opponent_str)

    room_data = {
        'challenger': challenger_str,
        'opponent': opponent_str,
        'turn': '1',  # Assuming turn should be a string
        'FirstTurn': FirstTurn
    }
    room = FightRoom(**room_data)
    room.save()



# Check ----------------------------------------

def check_if_exist(player_name):

    player = Player.objects(name=player_name).first()

    if player:
        print("Player already Exist")
        return True
    else:
        print("Player doesn't Exist")
        return False