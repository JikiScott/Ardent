'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
--
"Love Theme" Economy Bot -- Version 0.
S.P. 2026
'''

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
from db1.db import initialize_database, get_connection

initialize_database()

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents = intents)

# this stores the UIDs and $ amounts. 
assets = {}

# various level costs
lvl1cost = 25
lvl2cost = 500
lvl3cost = 7500
lvl4cost = 100000

backup = open("currency", "r+")

write = ""

lines = backup.read()
content = lines.split()

if len(lines) != 0:
    for i in range(0, len(content), 3):
        assets[int(content[i])][0] = int(content[i+1])
        assets[int(content[i])][0] = int(content[i+2])

@bot.event
async def on_ready():
    print("Running Love Theme (GPLv3)")

# looks a little ugly, i know, but i have to build the level system somehow
    
class jobMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label="LEVEL 1", style=discord.ButtonStyle.grey)
    async def menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        levelRole = discord.utils.get(interaction.guild.roles, name="LVL 1")
        if assets[interaction.user.id][0] >= lvl1cost:
            await interaction.user.add_roles(levelRole)
            assets[interaction.user.id][0] -= lvl1cost
            assets[interaction.user.id][1] = 10
    @discord.ui.button(label="LEVEL 2", style=discord.ButtonStyle.grey)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        levelRole = discord.utils.get(interaction.guild.roles, name="LVL 2")
        if assets[interaction.user.id][0] >= lvl2cost:
            await interaction.user.add_roles(levelRole)
            assets[interaction.user.id][0] -= lvl2cost
            assets[interaction.user.id][1] = 100
    @discord.ui.button(label="LEVEL 3", style=discord.ButtonStyle.grey)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        levelRole = discord.utils.get(interaction.guild.roles, name="LVL 3")
        if assets[interaction.user.id][0] >= lvl3cost:
            await interaction.user.add_roles(levelRole)
            assets[interaction.user.id][0] -= lvl3cost
            assets[interaction.user.id][1] = 1000
    @discord.ui.button(label="LEVEL 4", style=discord.ButtonStyle.grey)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        levelRole = discord.utils.get(interaction.guild.roles, name="LVL 4")
        if assets[interaction.user.id][0] >= lvl4cost:
            await interaction.user.add_roles(levelRole)
            assets[interaction.user.id][0] -= lvl4cost
            assets[interaction.user.id][1] = 10000
            
@bot.event
async def on_message(message):
    # a reference
    if "amayo" in message.content.lower():
        await message.channel.send("https://www.youtube.com/watch?v=TZtiJN6yiik")
    await bot.process_commands(message)

@bot.command()
async def work(ctx):
    if ctx.author.id in assets:
        assets[ctx.author.id][0] += assets[ctx.author.id][1]
    else:
        assets[ctx.author.id] = [1, 1]
    await ctx.send(f"🔥{ctx.author.mention} worked for ${assets[ctx.author.id][1]}.🔥")
    write = f"{ctx.author.id} {assets[ctx.author.id][0]} {assets[ctx.author.id][1]} "
    print(write)

@bot.command()
async def balance(ctx):
    if ctx.author.id in assets:
        await ctx.send(f"{ctx.author.mention}, your balance is 🔥${assets[ctx.author.id][0]}.🔥")
    else:
        await ctx.send(f"{ctx.author.mention}, you do not have a balance.")
        
@bot.command()
async def job(ctx):
    await ctx.send(f"{ctx.author.mention}, select your job role!", view=jobMenu())

@bot.command()
async def transfer_balance(sender_id: int, recipient_id: int, amount: int):
    if amount <= 0:
        raise ValueError("Please enter a positive value to transfer.")

    with get_connection() as connection:
        connection.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (sender_id,),
        )
        connection.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (recipient_id,),
        )

        sender = connection.execute(
            "SELECT balance FROM users WHERE user_id = ?",
            (sender_id,),
        ).fetchone()

        if sender["balance"] < amount:
            raise ValueError("Insufficient balance.")

        connection.execute(
            """
            UPDATE users
            SET balance = balance - ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (amount, sender_id),
        )

        connection.execute(
            """
            UPDATE users
            SET balance = balance + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            (amount, recipient_id),
        )

        connection.execute(
            """
            INSERT INTO transactions (
                sender_id,
                recipient_id,
                amount,
                transaction_type
            )
            VALUES (?, ?, ?, ?)
            """,
            (sender_id, recipient_id, amount, "transfer"),
        )

# async def transfer(ctx, user: discord.Member, amount: int):
#     if (amount <= assets[ctx.author.id][0]) and (amount > 0):
#         assets[ctx.author.id][0] -= amount
#         assets[user.id][0] += amount
#         await ctx.send(f"{ctx.author.mention}, you transferred {amount} to {user.mention}.")
#     else:
#         await ctx.send(f"{ctx.author.mention}, invalid transfer!")

@bot.command()
async def coin(ctx, guess, wager: int):
    if (wager > 0) and (wager <= assets[ctx.author.id][0]):
        guess = guess.lower()
        cointoss = ["heads", "tails"]
        flip = random.choice(cointoss)
        
        if flip == guess:
            await ctx.send(f"{ctx.author.mention}, you correctly guessed {guess} and thus have won 🔥${wager}🔥!")
            assets[ctx.author.id][0] += wager
        else:
            await ctx.send(f"{ctx.author.mention}, you made an incorrect guess and thus have lost ${wager}.")
            assets[ctx.author.id][0] -= wager
        write = f"{ctx.author.id} {assets[ctx.author.id][0]} {assets[ctx.author.id][1]} "   
    else:
        await ctx.send(f"{ctx.author.mention}, invalid wager!")

backup.write(write)
backup.close()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
