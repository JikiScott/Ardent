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
    get_connection,
    get_balance,
    transfer_balance,
    work_user,
    coin_flip,
    add_crystals,
    get_inventory,
    get_user_firm,
    create_firm,
    get_firm_members,
    get_firm_invites,
    create_firm_invite,
    accept_firm_invite,
    decline_firm_invite,
    leave_firm,
    dismiss_firm_member,
    disband_firm,
    rename_firm,
    get_firm_balance,
    get_treasury_balance
)
from econ.mine import mine
import time
from econ.currency import format_currency, to_farthings
from decimal import Decimal

# Shared embed helpers. All Ardent messages use one visual style.
def make_embed(*, title=None, description=None, color=None, fields=None, footer=None):
    embed = discord.Embed(
        title=title, description=description,
        color=color if color is not None else discord.Color.red()
    )
    for name, value, inline in (fields or []):
        embed.add_field(name=str(name), value=str(value), inline=inline)
    if footer:
        embed.set_footer(text=footer)
    return embed


async def send_embed(ctx, *, title=None, description=None, color=None,
                     fields=None, footer=None, view=None):
    await ctx.send(
        embed=make_embed(title=title, description=description, color=color,
                         fields=fields, footer=footer),
        view=view, allowed_mentions=discord.AllowedMentions.none()
    )


async def send_notice(ctx, message, *, error=False):
    await send_embed(ctx, description=message,
                     color=discord.Color.dark_red() if error else discord.Color.red())


async def send_cooldown(ctx, action, retry_after):
    timestamp = int(time.time() + retry_after)
    await send_notice(ctx, f"{ctx.author.mention}, you can {action} again <t:{timestamp}:R>.")


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

    await send_embed(
        ctx,
        title="🔥 Work Complete! 🔥",
        description=f"*{ctx.author.mention} has completed a shift!*",
        fields=[
            ("***Wages Earned***", format_currency(result["wage"]), True),
            ("***New Balance***", format_currency(result["balance"]), True),
        ],
    )


@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await send_cooldown(ctx, "work", error.retry_after)
    else:
        raise error

@bot.command(aliases=["bal"])
async def balance(ctx):
    current_balance = get_balance(ctx.author.id)

    embed = make_embed(
        title="*Arderian Holdings*",
        description=(
            f"**User:** {ctx.author.mention}\n"
            f"**Balance:** 🔥 {format_currency(current_balance)} 🔥"
        ),
        color=discord.Color.orange()
    )

    await ctx.send(embed=embed)
@bot.command(name="pay")
async def pay(ctx, member: discord.Member, amount: int, denomination: str = "sovereign"):    # Prevent payments to bots
    if member.bot:
        await send_notice(ctx, "You cannot send money to bots.")
        return

    # Prevent self-transfers
    if member.id == ctx.author.id:
        await send_notice(ctx, "You cannot pay yourself.")
        return

    # Convert into farthings
    try:
        farthings = to_farthings(amount, denomination)

        if farthings <= 0:
            raise ValueError("Payment must be greater than zero.")

    # Execute transfer in farthings
        transfer_balance(
            ctx.author.id,
            member.id,
            farthings
        )

    except ValueError as error:
        await send_notice(ctx, f"Payment failed: {error}")
        return
    # Confirmation embed
    embed = make_embed(
        title="*Arderian Holdings Transfer*",
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
        value=f"🔥 {format_currency(farthings)} 🔥",
        inline=False
    )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )


@pay.error
async def pay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_notice(ctx, "Usage: `.pay @user <amount>`")

    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(
            "User not found. Please mention a member of this server."
        )

    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Invalid amount. Please enter a whole number."
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
#         await send_notice(ctx, f"{ctx.author.mention}, you transferred {amount} to {user.mention}.")
#     else:
#         await send_notice(ctx, f"{ctx.author.mention}, invalid transfer!")

# @bot.command()
# async def coin(ctx, guess, wager: int):
# #     if (wager > 0) and (wager <= assets[ctx.author.id][0]):
#         guess = guess.lower()
#         cointoss = ["heads", "tails"]
#         flip = random.choice(cointoss)
#
#         if flip == guess:
#             await send_notice(ctx, f"{ctx.author.mention}, you correctly guessed {guess} and thus have won 🔥${wager}🔥!")
# #             assets[ctx.author.id][0] += wager
#         else:
#             await send_notice(ctx, f"{ctx.author.mention}, you made an incorrect guess and thus have lost ${wager}.")
# #             assets[ctx.author.id][0] -= wager
# #         write = f"{ctx.author.id} {assets[ctx.author.id][0]} {assets[ctx.author.id][1]} "
#     else:
#         await send_notice(ctx, f"{ctx.author.mention}, invalid wager!")
# Legacy gamba
#
# Gamba add:

@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def coin(
    ctx,
    guess: str,
    wager: int,
    denomination: str = "sovereign"
):
    try:
        # Convert the wager to farthings
        wager_farthings = to_farthings(wager, denomination)

        if wager_farthings <= 0:
            raise ValueError("Your wager must be greater than zero.")

        # coin_flip() works with farthings
        result, won, new_balance = coin_flip(
            ctx.author.id,
            guess,
            wager_farthings
        )

        wager_display = format_currency(wager_farthings)
        balance_display = format_currency(new_balance)

        if won:
            embed = make_embed(
                title="🫴🪙 Coin Flip: 🔥 WINNER! 🔥",
                description=(
                    f"*The coin landed on **{result.title()}**!*\n\n"
                    f"{ctx.author.mention} won "
                    f"🔥 **{wager_display}** 🔥!"
                ),
                color=discord.Color.red()
            )
        else:
            embed = make_embed(
                title="🫴🪙 Coin Flip: Loss",
                description=(
                    f"*The coin landed on **{result.title()}**!*\n\n"
                    f"{ctx.author.mention} lost "
                    f"**{wager_display}**."
                ),
                color=discord.Color.dark_grey()
            )

        embed.add_field(
            name="*New Balance*",
            value=f"**{balance_display}**",
            inline=False
        )

        await ctx.send(
            embed=embed,
            allowed_mentions=discord.AllowedMentions.none()
        )

    except ValueError as error:
        await ctx.send(
            f"{ctx.author.mention}, {error}"
        )


@coin.error
async def coin_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await send_cooldown(ctx, "flip a coin", error.retry_after)
    else:
        logging.exception("Coin command failed", exc_info=(type(error), error, error.__traceback__))
        await send_notice(ctx, f"Coin flip failed: `{type(error).__name__}`. Check the bot logs.", error=True)

# MINING START
@bot.command(name="mine")
@commands.cooldown(1, 30, commands.BucketType.user)
async def mine_command(ctx):
    firm = get_user_firm(ctx.author.id)

    if firm is None:
        await send_notice(ctx, f"{ctx.author.mention}, you must be employed by a firm to mine.", error=True)
        return

    result = mine()

    if result.crystal_class is None:
        await send_notice(ctx, f"{ctx.author.mention} completed a mining shift for **{firm['name']}**, but no crystals were recovered.")
        return

    new_balance = add_crystals(
        "firm",
        firm["firm_id"],
        result.crystal_class,
        result.grade,
        result.quantity
    )

    await send_embed(
        ctx, title="🔥 Mining Shift Complete 🔥",
        description=(
            f"{ctx.author.mention} mined **{result.quantity} stone of "
            f"{result.grade.title()} {result.crystal_class.title()} crystal** "
            f"for **{firm['name']}**."
        ),
        fields=[("Firm Inventory", f"**{new_balance} stone** of this crystal", False)],
    )

@mine_command.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await send_cooldown(ctx, "mine", error.retry_after)
    else:
        raise error



# MINING END
# FIRM START
@bot.group(invoke_without_command=True)
async def firm(ctx):
    embed = make_embed(
        title="🔥 Firm Commands 🔥",
        description="*Available firm management commands:*",
        color=discord.Color.red()
    )

    for command in sorted(firm.commands, key=lambda cmd: cmd.name):
        if command.hidden:
            continue

        embed.add_field(
            name=f"`{ctx.prefix}{command.qualified_name} {command.signature}`".strip(),
            value=command.brief or command.help or "",
            inline=False
        )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )

@firm.command(name="create", help="Create a new firm.")
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


@firm.command(name="info", help="Show firm information.")
async def firm_info(ctx):
    user_id = ctx.author.id
    firm_data = get_user_firm(user_id)

    if firm_data is None:
        await send_notice(ctx, "You are not currently employed by a firm.")
        return

    firm_id = firm_data["firm_id"]
    firm_name = firm_data["name"]
    owner_id = firm_data["owner_id"]
    firm_balance = get_firm_balance(firm_id)
    firm_inventory = get_inventory("firm", firm_id)
    total_stone = sum(
        (Decimal(str(crystal["quantity"])) for crystal in firm_inventory),
        Decimal("0")
    )

    members = get_firm_members(firm_id)
    employee_count = sum(
        1 for member in members
        if member["role"] != "owner"
    )

    embed = make_embed(
        title=f"🔥 `{firm_name}` 🔥",
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

    embed.add_field(
        name="Firm Account Balance",
        value=f"**{format_currency(firm_balance)}**",
        inline=True
    )

    embed.add_field(
        name="Total Crystal Holdings",
        value=f"**{total_stone:,.2f} stone**",
        inline=True
    )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )

@firm.command(
    name="inv",
    aliases=["inventory"],
    help="View your firm's crystal inventory."
)
async def firm_inventory(ctx):
    # Find the user's firm
    firm = get_user_firm(ctx.author.id)

    if firm is None:
        await ctx.send(
            "You must be employed by a firm to view its inventory."
        )
        return

    # Retrieve the firm's inventory
    current_inventory = get_inventory(
        "firm",
        firm["firm_id"]
    )

    grade_order = {
        "alpha": 0,
        "beta": 1,
        "gamma": 2,
        "delta": 3,
    }

    current_inventory = sorted(
        current_inventory,
        key=lambda crystal: (
            grade_order.get(crystal["grade"].lower(), 99),
            crystal["crystal_class"].lower()
        )
    )

    embed = make_embed(
        title=f"🔥 {firm['name']}: *Crystal Inventory* 🔥",
        description=f"-# Firm ID: `{firm['firm_id']}`",
        color=discord.Color.dark_gold()
    )

    if not current_inventory:
        embed.add_field(
            name="*Inventory Empty*",
            value="**This firm has not mined any crystals yet.**",
            inline=False
        )

    else:
        for crystal in current_inventory:
            crystal_class = crystal["crystal_class"].title()
            grade = crystal["grade"].title()
            quantity = crystal["quantity"]

            embed.add_field(
                name=f"__{grade} {crystal_class}__",
                value=f"**{quantity} stone**",
                inline=True
            )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )

@firm.command(name="hire", help="Hire a firm employee.")
@commands.cooldown(1, 30, commands.BucketType.user)
async def firm_hire(ctx, member: discord.Member):
    firm_data = get_user_firm(ctx.author.id)

    if firm_data is None:
        await send_notice(ctx, "You must have a firm to hire employees.")
        return

    # Only firm owners
    if firm_data["owner_id"] != ctx.author.id:
        await send_notice(ctx, "Only the owner of the firm can hire employees.")
        return

    # Reject bots
    if member.bot:
        await send_notice(ctx, "You cannot hire bots.")
        return

    # Create invite
    try:
        create_firm_invite(
            firm_data["firm_id"],
            ctx.author.id,
            member.id
        )
    except ValueError as error:
        await send_notice(ctx, f"Unable to hire employee: {error}")
        return


    # Build embed
    embed = make_embed(
        description=f"# FIRM INVITATION\n"
                    f"🔥 **{member.mention}** has been invited to join "
                    f"**{firm_data['name']}**! 🔥\n",
        color=discord.Color.red()
    )

    embed.add_field(
        name="*To accept...*",
        value=f"`.firm accept {firm_data['firm_id']}`",
        inline=True
    )

    embed.add_field(
        name="*To decline...*",
        value=f"`.firm decline {firm_data['firm_id']}`",
        inline=True
    )
    embed.add_field(
        name="*To view more info...*",
        value=f"`.firm invites`",
        inline=True
    )
    # Confirm invitation
    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )
@firm_hire.error
async def firm_hire_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await send_cooldown(ctx, "hire an employee", error.retry_after)
    else:
        raise error


class SmartInvite(discord.ui.View):
    def __init__(self, owner_id: int, firm_id: int):
        super().__init__(timeout=60)
        self.owner_id = owner_id
        self.firm_id = firm_id

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Only the invite recipient can respond.",
                ephemeral=True
            )
            return False

        return True

    async def finish(self, interaction, description, title=None):
        for item in self.children:
            item.disabled = True

        embed = make_embed(
            title=title,
            description=description,
            color=discord.Color.red()
        )

        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=self
        )

        self.stop()

    @discord.ui.button(
        label="Accept Invite",
        style=discord.ButtonStyle.success,
        emoji="☑️"
    )
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        try:
            firm_name = accept_firm_invite(
                interaction.user.id,
                self.firm_id
            )

        except ValueError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True
            )
            return

        firm_data = get_user_firm(interaction.user.id)
        job_title = firm_data["role"].title()

        await self.finish(
            interaction,
            title=f"🔥 {interaction.user.display_name} has joined {firm_name}! 🔥",
            description=f"***New Role:*** `{job_title}`"
        )

    @discord.ui.button(
        label="Decline Invite",
        style=discord.ButtonStyle.danger,
        emoji="🇽"
    )
    async def decline(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        # Get the firm name before deleting the invitation
        invites = get_firm_invites(interaction.user.id)

        firm_name = next(
            (
                invite["name"]
                for invite in invites
                if invite["firm_id"] == self.firm_id
            ),
            f"Firm #{self.firm_id}"
        )

        try:
            decline_firm_invite(
                interaction.user.id,
                self.firm_id
            )

        except ValueError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True
            )
            return

        await self.finish(
            interaction,
            f"*{interaction.user.display_name} has declined "
            f"employment with **{firm_name}**.*"
        )

    async def on_timeout(self):
        # Disable buttons after 60 seconds
        for item in self.children:
            item.disabled = True

        if hasattr(self, "message"):
            try:
                await self.message.edit(view=self)
            except discord.HTTPException:
                pass

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.secondary
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Only the firm owner can cancel this request.",
                ephemeral=True
            )
            return

        for item in self.children:
            item.disabled = True

        embed = make_embed(
            title="Firm Disbandment Cancelled",
            description="Your firm has been preserved. No changes were made.",
            color=discord.Color.green()
        )

        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=self
        )

        self.stop()

@firm.command(name="invites", help="View firm invites.")
async def firm_invites(ctx):
    invites = get_firm_invites(ctx.author.id)

    if not invites:
        await send_notice(
            ctx,
            "You have no pending employment invitations."
        )
        return

    for invite in invites:
        embed = make_embed(
            title="🔥 Employment Invitation 🔥",
            description=(
                f"You have been invited to join "
                f"**{invite['name']}**!\n"
                f"-# Firm ID: `{invite['firm_id']}`\n\n"
                f"***Offered Position:*** `Laborer`"
            ),
            color=discord.Color.red()
        )

        view = SmartInvite(
            owner_id=ctx.author.id,
            firm_id=invite["firm_id"]
        )

        message = await ctx.send(
            embed=embed,
            view=view,
            allowed_mentions=discord.AllowedMentions.none()
        )

        # Save the message so the view can disable buttons on timeout
        view.message = message

@firm.command(name="accept", help="Accept an invitation to a firm.")
async def firm_accept(ctx, firm_id: int):
    try:
        firm_name = accept_firm_invite(
            ctx.author.id,
            firm_id
        )

    except ValueError as error:
        await send_notice(ctx, f"Unable to accept invitation: {error}")
        return

    # Get new firm info
    firm_data = get_user_firm(ctx.author.id)
    job_title = firm_data["role"].title()

    # Build embed
    embed = make_embed(
        description=f"#🔥 {ctx.author.mention} has joined {firm_name}! 🔥"
                    f"***New Role:*** `{job_title}`",
        color=discord.Color.red()
    )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )
@firm_accept.error
async def firm_accept_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_notice(ctx, "Usage: `.firm accept <firm_id>`")

    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Invalid firm ID. Use `.firm invites` to find the correct ID."
        )

    else:
        raise error


@firm.command(name="decline", help="Decline an invitation to a firm.")
async def firm_decline(ctx, firm_id: int):
    # Find the invitation before deleting it
    invites = get_firm_invites(ctx.author.id)

    firm_name = next(
        (invite["name"] for invite in invites if invite["firm_id"] == firm_id),
        None
    )

    try:
        decline_firm_invite(
            ctx.author.id,
            firm_id
        )

    except ValueError as error:
        await send_notice(ctx, f"Unable to decline invitation: {error}")
        return

    # Build description-only embed
    embed = make_embed(
        description=(
            f"*{ctx.author.display_name} has declined employment with **{firm_name or f'Firm #{firm_id}'}**.*"
        ),
        color=discord.Color.red()
    )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )
@firm_decline.error
async def firm_decline_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_notice(ctx, "Usage: `.firm decline <firm_id>`")

    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Invalid firm ID. Please use `.firm invites` to find the correct ID."
        )

    else:
        raise error

@firm.command(name="leave", help="Leave a firm.")
async def firm_leave(ctx):
    try:
        firm_name = leave_firm(ctx.author.id)
    except ValueError as error:
        await send_notice(ctx, f"Unable to leave firm: {error}", error=True)
        return
    await send_notice(ctx, f"*{ctx.author.mention} has left **{firm_name}**.*")

@firm.command(name="dismiss", help="Dismiss an employee from your firm.")
async def firm_dismiss(ctx, member: discord.Member):
    try:
        firm_name = dismiss_firm_member(ctx.author.id, member.id)
    except ValueError as error:
        await send_notice(ctx, f"Unable to dismiss employee: {error}", error=True)
        return
    await send_notice(ctx, f"*{member.display_name} has been dismissed from **{firm_name}**.*")

@firm_dismiss.error
async def firm_dismiss_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await send_notice(ctx, "Usage: `.firm dismiss @user`")

    elif isinstance(error, commands.MemberNotFound):
        await ctx.send(
            "User not found. Please mention an employee."
        )

    else:
        raise error

@firm.command(name="members", help="View firm members.")
async def firm_members(ctx):
    # Find the user's firm
    firm_data = get_user_firm(ctx.author.id)

    if firm_data is None:
        await send_notice(ctx, "You are not currently employed by a firm.")
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
    embed = make_embed(
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

class ConfirmDisband(discord.ui.View):
    def __init__(self, owner_id: int):
        super().__init__(timeout=60)
        self.owner_id = owner_id

    @discord.ui.button(
        label="Disband Firm",
        style=discord.ButtonStyle.danger,
        emoji="🅾️"
    )
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Only the firm owner can confirm disbandment.",
                ephemeral=True
            )
            return

        try:
            firm_name = disband_firm(self.owner_id)

        except ValueError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True
            )
            return

        # Disable buttons after successful disbandment
        for item in self.children:
            item.disabled = True

        # Create confirmation embed
        embed = make_embed(
            description=(
                "# FIRM DISBANDED\n"
                f"**{firm_name}** has been permanently disbanded.\n\n"
                "All employees have been dismissed, pending invitations "
                "have been cancelled, and the firm's crystal inventory "
                "has been deleted."
            ),
            color=discord.Color.red()
        )

        embed.set_footer(
            text="This action cannot be undone."
        )

        # Replace original confirmation with result
        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=self
        )

        self.stop()

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.secondary
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Only the firm owner can cancel this request.",
                ephemeral=True
            )
            return

        for item in self.children:
            item.disabled = True

        embed = make_embed(
            title="Firm Disbandment Cancelled",
            description="Your firm has been preserved. No changes were made.",
            color=discord.Color.green()
        )

        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=self
        )

        self.stop()


@firm.command(name="disband", help="Disband a firm.")
async def firm_disband(ctx):
    firm_data = get_user_firm(ctx.author.id)

    if firm_data is None:
        await send_notice(ctx, "You do not belong to a firm.")
        return

    if firm_data["owner_id"] != ctx.author.id:
        await send_notice(ctx, "Only the firm owner can disband a firm.")
        return

    embed = make_embed(
        description=(
            f"# DISBAND FIRM?\n"
            f"Are you sure you want to permanently disband "
            f"**{firm_data['name']}**?\n\n"
            "__**This action cannot be undone.**__\n\n"
            "- All employees will be dismissed,\n"
            "- pending invitations will be cancelled,\n "
            "- and the firm's crystal inventory will be deleted."
        ),
        color=discord.Color.red()
    )

    await ctx.send(
        embed=embed,
        view=ConfirmDisband(ctx.author.id),
        allowed_mentions=discord.AllowedMentions.none()
    )


@firm.command(name="rename", help="Rename your firm.")
async def firm_rename(ctx, *, new_name: str):
    try:
        old_name, updated_name = rename_firm(
            ctx.author.id,
            new_name
        )

    except ValueError as error:
        await send_notice(ctx, f"Unable to rename firm: {error}")
        return

    embed = make_embed(
        title="🔥 Firm Renamed 🔥",
        description=(
            "Your firm has been successfully renamed!"
        ),
        color=discord.Color.orange()
    )

    embed.add_field(
        name="***Previous Name***",
        value=old_name,
        inline=False
    )

    embed.add_field(
        name="***New Name***",
        value=f"**{updated_name}**",
        inline=False
    )

    embed.set_footer(
        text="All employees and firm assets have been preserved."
    )

    await ctx.send(
        embed=embed,
        allowed_mentions=discord.AllowedMentions.none()
    )


@firm_rename.error
async def firm_rename_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Usage: `.firm rename <new name>`"
        )
    else:
        raise error

# FIRM END
# TREASURY START

@bot.group(name="treasury", invoke_without_command=True)
async def treasury(ctx):
#  Treasury management.

    await send_notice(
        ctx,
        "Use `.treasury help` to view Treasury commands."
    )

@treasury.command(name="balance", help="View Treasury balance.")
async def treasury_balance(ctx):
    balance = get_treasury_balance()

    await send_embed(
        ctx,
        title="Arderian Treasury Report",
        description=f"**Available Funds:** {format_currency(balance)}",
        color=discord.Color.gold()
    )

@treasury.command(name="help", help="List Treasury commands.")
async def treasury_help(ctx):
    fields = []

    for command in sorted(treasury.commands, key=lambda c: c.name):
        if command.hidden:
            continue

        fields.append((
            f".{command.qualified_name} {command.signature}".strip(),
            command.help or "No description available.",
            False
        ))

    await send_embed(
        ctx,
        title="Treasury Command List",
        fields=fields,
        color=discord.Color.gold()
    )

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
