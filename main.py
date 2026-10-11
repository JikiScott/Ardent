'''
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
todo AVE ARDERA!
'''

# Main.py
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from db1.db import (
    initialize_database,
    get_balance,
    work_user,
    get_connection,
    transfer_balance,
    coin_flip,
    add_crystals,
    get_user_firm,
    create_firm,
    get_firm_members,
    get_firm_invites,
    create_firm_invite,
    accept_firm_invite,
    decline_firm_invite,
    leave_firm,
    dismiss_firm_member
)
from econ.mine import mine
import time
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
    print("Running Love Theme (GPLv3) READY")

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
# LEG END


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def work(ctx):
    result = work_user(ctx.author.id)
    await ctx.send(
        f"{ctx.author.mention} worked for 🔥{result['wage']} Sovereign!🔥"
    )


@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        retry_timestamp = int(time.time() + error.retry_after)
        await ctx.send(
            f"{ctx.author.mention}, you can work again in "
            f"<t:{retry_timestamp}:R>."
        )
    else:
        raise error

@bot.command()
async def balance(ctx):
    current_balance = get_balance(ctx.author.id)
    await ctx.send(
        f"{ctx.author.mention}, your balance is 🔥{current_balance} Sovereign.🔥"
    )

@bot.command(name="pay")
async def pay(ctx, member: discord.Member, amount: int):
    # Prevent payments to bots
    if member.bot:
        await ctx.send("You cannot send money to bots.")
        return

    # Prevent self-transfers
    if member.id == ctx.author.id:
        await ctx.send("You cannot pay yourself.")
        return

    # Validate amount
    if amount <= 0:
        await ctx.send("Payment must be greater than zero.")
        return

    # Execute transfer
    try:
        transfer_balance(
            ctx.author.id,
            member.id,
            amount
        )

    except ValueError as error:
        await ctx.send(f"Payment failed: {error}")
        return

    # Confirmation embed
    embed = discord.Embed(
        title="Sovereign Transfer",
        description="Payment completed successfully.",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="*Sender*",
        value=ctx.author.mention,
        inline=True
    )

    embed.add_field(
        name="*Recipient*",
        value=member.mention,
        inline=True
    )

    embed.add_field(
        name="**Amount**",
        value=f"{amount:,} Sovereigns",
        inline=False
    )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )


@pay.error
async def pay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: `.pay @user <amount>`")

    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(
            "User not found. Please mention a member of this server."
        )

    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Invalid amount. Sovereigns must be whole numbers."
        )

    else:
        raise error

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

# MINING START
@bot.command(name="mine")
@commands.cooldown(1, 30, commands.BucketType.user)
async def mine_command(ctx):
    firm = get_user_firm(ctx.author.id)

    if firm is None:
        await ctx.send(
            f"{ctx.author.mention}, you must be employed by a firm to work."
        )
        return

    result = mine()

    if result.crystal_class is None:
        await ctx.send(
            f"{ctx.author.mention} completed a mining shift for "
            f"**{firm['name']}**, but no crystals were recovered."
        )
        return

    new_balance = add_crystals(
        "firm",
        firm["firm_id"],
        result.crystal_class,
        result.grade,
        result.quantity
    )

    await ctx.send(
        f"{ctx.author.mention} mined **{result.quantity} stone of "
        f"{result.grade.title()} {result.crystal_class.title()} crystal** "
        f"for **{firm['name']}**.\n"
        f"Firm inventory now holds **{new_balance} stone** of this crystal."
    )

@mine_command.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"{ctx.author.mention}, you can mine again in "
            f"{error.retry_after:.0f} seconds."
        )
    else:
        raise error

# MINING END
# FIRM START
@bot.group(invoke_without_command=True)
async def firm(ctx):
    await ctx.send(
        "Firm commands:\n"
        "`.firm create <name>` - Create a firm\n"
        "`.firm info` - View your current firm"
    )

@firm.command(name="create")
async def firm_create(ctx, *, name: str):
    existing_firm = get_user_firm(ctx.author.id)

    if existing_firm is not None:
        await ctx.send(
            f"{ctx.author.mention}, you are already employed by "
            f"**{existing_firm['name']}**."
        )
        return

    try:
        firm_id = create_firm(
            ctx.author.id,
            name
        )

        await ctx.send(
            f"🔥 **{ctx.author.mention} founded __{name.strip()}__**! 🔥\n"
            f"Firm ID: **{firm_id}**",
        allowed_mentions = discord.AllowedMentions(
            users=False,
            roles=False,
            everyone=False
        )
        )

    except ValueError as error:
        await ctx.send(
            f"{ctx.author.mention}, {error}"
        )

@firm_create.error
async def firm_create_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"{ctx.author.mention}, you must provide a firm name.\n"
            f"Usage: `.firm create <name>`"
        )
    else:
        raise error


@firm.command(name="info")
async def firm_info(ctx):
    user_id = ctx.author.id

    firm_data = get_user_firm(user_id)

    if firm_data is None:
        await ctx.send(
            "You are not currently employed by a firm."
        )
        return

    firm_id = firm_data["firm_id"]
    firm_name = firm_data["name"]
    owner_id = firm_data["owner_id"]

    members = get_firm_members(firm_id)
    employee_count = sum(
        1 for member in members
        if member["role"] != "owner"
    )

    embed = discord.Embed(
        title=f"🔥`{firm_name}`🔥",
        description=f"Firm ID: `{firm_id}`",
        color=discord.Color.red()
    )

    embed.add_field(
        name="Owner",
        value=f"<@{owner_id}>",
        inline=True
    )

    embed.add_field(
        name="Employees",
        value=str(employee_count),
        inline=True
    )

    embed.add_field(
        name="Your Position",
        value=firm_data["role"].capitalize(),
        inline=False
    )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )

@firm.command(name="hire")
async def firm_hire(ctx, member: discord.Member):
    firm_data = get_user_firm(ctx.author.id)

    if firm_data is None:
        await ctx.send("You must have a firm to hire employees.")
        return

    # Only firm owners
    if firm_data["owner_id"] != ctx.author.id:
        await ctx.send("Only the owner of the firm can hire employees.")
        return

    # Reject bots
    if member.bot:
        await ctx.send("You cannot hire bots.")
        return

    # Create invite
    try:
        create_firm_invite(
            firm_data["firm_id"],
            ctx.author.id,
            member.id
        )
    except ValueError as error:
        await ctx.send(f"Unable to hire employee: {error}")
        return

    # Confirm invitation
    await ctx.send(
        f"🔥**{member.display_name}** has been invited to join "
        f"**{firm_data['name']}**!🔥\n"
        f"You can accept with "
        f"`.firm accept {firm_data['firm_id']}`.",
        allowed_mentions=discord.AllowedMentions.none()
    )

@firm.command(name="invites")
async def firm_invites(ctx):
    invites = get_firm_invites(ctx.author.id)

    if not invites:
        await ctx.send("You have no pending employment invitations.")
        return

    message = "🔥**Pending Employment Invitations:**🔥\n"

    for invite in invites:
        message += (
            f"\n- **{invite['name']}** \n"
            f"-# (*Firm ID: `{invite['firm_id']}`*)\n"
            f"To Accept: `.firm accept {invite['firm_id']}`\n"
            f"To Decline: `.firm decline {invite['firm_id']}`\n"
        )

    await ctx.send(
        message,
        allowed_mentions=discord.AllowedMentions.none()
    )

@firm.command(name="accept")
async def firm_accept(ctx, firm_id: int):
    try:
        firm_name = accept_firm_invite(
            ctx.author.id,
            firm_id
        )

    except ValueError as error:
        await ctx.send(f"Unable to accept invitation: {error}")
        return

    await ctx.send(
        f"🔥**{ctx.author.display_name}** has joined "
        f"**{firm_name}** as a laborer!🔥",
        allowed_mentions=discord.AllowedMentions.none()
    )
@firm_accept.error
async def firm_accept_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: `.firm accept <firm_id>`")

    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Invalid firm ID. Use `.firm invites` to find the correct ID."
        )

    else:
        raise error


@firm.command(name="decline")
async def firm_decline(ctx, firm_id: int):
    try:
        decline_firm_invite(
            ctx.author.id,
            firm_id
        )

    except ValueError as error:
        await ctx.send(f"Unable to decline invitation: {error}")
        return

    await ctx.send(
        f"Employment invitation from firm `{firm_id}` declined."
    )

@firm_decline.error
async def firm_decline_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: `.firm decline <firm_id>`")

    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Invalid firm ID. Please use `.firm invites` to find the correct ID."
        )

    else:
        raise error

@firm.command(name="leave")
async def firm_leave(ctx):
    try:
        firm_name = leave_firm(ctx.author.id)

    except ValueError as error:
        await ctx.send(f"Unable to leave firm: {error}")
        return

    await ctx.send(
        f"**{ctx.author.display_name}** has left **{firm_name}**.",
        allowed_mentions=discord.AllowedMentions.none()
    )

@firm.command(name="dismiss")
async def firm_dismiss(ctx, member: discord.Member):
    try:
        firm_name = dismiss_firm_member(
            ctx.author.id,
            member.id
        )

    except ValueError as error:
        await ctx.send(f"Unable to dismiss employee: {error}")
        return

    await ctx.send(
        f"**{member.display_name}** has been dismissed "
        f"from **{firm_name}**.",
        allowed_mentions=discord.AllowedMentions.none()
    )
@firm_dismiss.error
async def firm_dismiss_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: `.firm dismiss @user`")

    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(
            "User not found. Please mention an employee."
        )

    else:
        raise error

@firm.command(name="members")
async def firm_members(ctx):
    # Find the user's firm
    firm_data = get_user_firm(ctx.author.id)

    if firm_data is None:
        await ctx.send("You are not currently employed by a firm.")
        return

    firm_id = firm_data["firm_id"]
    firm_name = firm_data["name"]

    # Retrieve firm members
    members = get_firm_members(firm_id)

    owners = []
    laborers = []

    for member in members:
        user_id = member["user_id"]
        mention = f"<@{user_id}>"

        if member["role"] == "owner":
            owners.append(mention)
        else:
            laborers.append(mention)

    # Build embed
    embed = discord.Embed(
        title=f"{firm_name}: *Members*",
        description=f"-# Firm ID: `{firm_id}`",
        color=discord.Color.red()
    )

    embed.add_field(
        name="**Owner**",
        value="\n".join(owners) if owners else "None",
        inline=False
    )

    embed.add_field(
        name=f"**Laborers** ({len(laborers)})",
        value="\n".join(laborers) if laborers else "No employees",
        inline=False
    )

    embed.set_footer(
        text=f"Total members: {len(members)}"
    )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )
# FIRM END

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
