'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
--
"Love Theme" Economy Bot -- Version 0.
S.P. 2026
'''

# Main.py
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
from db1.db import (
    initialize_database,
    get_balance,
    work_user,
    get_connection,
    transfer_balance,
    coin_flip,
)
initialize_database()

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents = intents)

# this stores the UIDs and $ amounts. (LEG)
# assets = {}

# various level costs
lvl1cost = 25
lvl2cost = 500
lvl3cost = 7500
lvl4cost = 100000

# backup = open("currency", "r+")
#
# write = ""
#
# lines = backup.read()
# content = lines.split()
#
# if len(lines) != 0:
#     for i in range(0, len(content), 3):
# #         assets[int(content[i])][0] = int(content[i+1])
# #         assets[int(content[i])][0] = int(content[i+2])
# Legacy persis sys

@bot.event
async def on_ready():
    print("Running Love Theme (GPLv3)")

class jobMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
    @discord.ui.button(label="LEVEL 1", style=discord.ButtonStyle.grey)
    async def menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        levelRole = discord.utils.get(interaction.guild.roles, name="LVL 1")
#         if assets[interaction.user.id][0] >= lvl1cost:
#             await interaction.user.add_roles(levelRole)
#             assets[interaction.user.id][0] -= lvl1cost
#             assets[interaction.user.id][1] = 10
    @discord.ui.button(label="LEVEL 2", style=discord.ButtonStyle.grey)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        levelRole = discord.utils.get(interaction.guild.roles, name="LVL 2")
#         if assets[interaction.user.id][0] >= lvl2cost:
#             await interaction.user.add_roles(levelRole)
#             assets[interaction.user.id][0] -= lvl2cost
#             assets[interaction.user.id][1] = 100
    @discord.ui.button(label="LEVEL 3", style=discord.ButtonStyle.grey)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        levelRole = discord.utils.get(interaction.guild.roles, name="LVL 3")
#         if assets[interaction.user.id][0] >= lvl3cost:
#             await interaction.user.add_roles(levelRole)
#             assets[interaction.user.id][0] -= lvl3cost
#             assets[interaction.user.id][1] = 1000
    @discord.ui.button(label="LEVEL 4", style=discord.ButtonStyle.grey)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        levelRole = discord.utils.get(interaction.guild.roles, name="LVL 4")
#         if assets[interaction.user.id][0] >= lvl4cost:
#             await interaction.user.add_roles(levelRole)
#             assets[interaction.user.id][0] -= lvl4cost
#             assets[interaction.user.id][1] = 10000
# Todo: move leg code to SQLite

@bot.event
async def on_message(message):
    # a reference
    if "amayo" in message.content.lower():
        await message.channel.send("https://www.youtube.com/watch?v=TZtiJN6yiik")
    await bot.process_commands(message)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def work(ctx):
    result = work_user(ctx.author.id)
    await ctx.send(
        f"{ctx.author.mention} worked for 🔥${result['wage']}.🔥"
    )
@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"{ctx.author.mention}, you can work again in "
            f"{error.retry_after:.0f} seconds."
        )
    else:
        raise error

@bot.command()
async def balance(ctx):
    current_balance = get_balance(ctx.author.id)
    await ctx.send(
        f"{ctx.author.mention}, your balance is 🔥${current_balance}.🔥"
    )
        
@bot.command()
async def job(ctx):
    await ctx.send(f"{ctx.author.mention}, the job system is currerntly being migrated to *SQLite*. Please check back later! 🔥", view=jobMenu())

# async def transfer(ctx, user: discord.Member, amount: int):
# #     if (amount <= assets[ctx.author.id][0]) and (amount > 0):
# #         assets[ctx.author.id][0] -= amount
# #         assets[user.id][0] += amount
#         await ctx.send(f"{ctx.author.mention}, you transferred {amount} to {user.mention}.")
#     else:
#         await ctx.send(f"{ctx.author.mention}, invalid transfer!")

# @bot.command()
# async def coin(ctx, guess, wager: int):
# #     if (wager > 0) and (wager <= assets[ctx.author.id][0]):
#         guess = guess.lower()
#         cointoss = ["heads", "tails"]
#         flip = random.choice(cointoss)
#
#         if flip == guess:
#             await ctx.send(f"{ctx.author.mention}, you correctly guessed {guess} and thus have won 🔥${wager}🔥!")
# #             assets[ctx.author.id][0] += wager
#         else:
#             await ctx.send(f"{ctx.author.mention}, you made an incorrect guess and thus have lost ${wager}.")
# #             assets[ctx.author.id][0] -= wager
# #         write = f"{ctx.author.id} {assets[ctx.author.id][0]} {assets[ctx.author.id][1]} "
#     else:
#         await ctx.send(f"{ctx.author.mention}, invalid wager!")
# Legacy gamba
#
# Gamba add:
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def coin(ctx, guess: str, wager: int):
    try:
        result, won, new_balance = coin_flip(
            ctx.author.id,
            guess,
            wager,
        )

        if won:
            await ctx.send(
                f"🫴🪙  **{result.title()}!** "
                f"{ctx.author.mention} won 🔥${wager}!🔥 "
                f"New Balance: ${new_balance}"
            )
        else:
            await ctx.send(
                f"🫴🪙 **{result.title()}!** "
                f"{ctx.author.mention} lost ${wager}. "
                f"New Balance: ${new_balance}"
            )

    except ValueError as error:
        await ctx.send(f"{ctx.author.mention}, {error}")
@coin.error
async def coin_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"{ctx.author.mention}, you can flip a coin again in "
            f"🔥{error.retry_after:.0f} seconds.🔥"
        )
    else:
        raise error



bot.run(token, log_handler=handler, log_level=logging.DEBUG)
