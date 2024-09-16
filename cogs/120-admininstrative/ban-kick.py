import discord
from discord import CategoryChannel, Forbidden, ForumChannel, Member, Thread, app_commands
from discord.abc import GuildChannel, PrivateChannel
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional

class BanCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: ban loaded")

    @app_commands.command(name="ban", description="Ban a specific user.")
    @app_commands.describe(user="The user to ban.", reason="The reason to ban the user.")
    @app_commands.default_permissions(ban_members=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def ban(self, interaction: discord.Interaction, user: Member, reason: Optional[str]):
        try:
            if reason is None:
                reason = f"Rollplayer managed ban by @{interaction.user.name}"
            else:
                reason = f"{reason} | Rollplayer managed ban by @{interaction.user.name}"
            await user.ban(reason=reason)
            await interaction.response.send_message(embed=embed_template("Banned user", f"{user.mention} has been banned!"), ephemeral=True)
        except Forbidden as err:
            await interaction.response.send_message(embed=error_template("Perihelion doesn't have permissions to ban members, or the user is above Perihelion's role!"), ephemeral=True)

    @app_commands.command(name="kick", description="Kick a specific user.")
    @app_commands.describe(user="The user to kick.", reason="The reason to kick the user.")
    @app_commands.default_permissions(kick_members=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def kick(self, interaction: discord.Interaction, user: Member, reason: Optional[str]):
        try:
            if reason is None:
                reason = f"Rollplayer managed kick by @{interaction.user.name}"
            else:
                reason = f"{reason} | Rollplayer managed kick by @{interaction.user.name}"
            await user.kick(reason=reason)
            await interaction.response.send_message(embed=embed_template("Kicked user", f"{user.mention} has been kicked!"), ephemeral=True)
        except Forbidden as err:
            await interaction.response.send_message(embed=error_template("Perihelion doesn't have permissions to kick members, or the user is above Perihelion's role!"), ephemeral=True)

    @app_commands.command(name="timeout", description="Time out a specific user.", )
    @app_commands.describe(user="The user to mute.", reason="The reason to time out the user.")
    @app_commands.default_permissions(moderate_members=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def timeout(self, interaction: discord.Interaction, user: Member, reason: Optional[str]):
        try:
            if reason is None:
                reason = f"Rollplayer managed mute by @{interaction.user.name}"
            else:
                reason = f"{reason} | Rollplayer managed mute by @{interaction.user.name}"
            await user.kick(reason=reason)
            await interaction.response.send_message(embed=embed_template("Muted user", f"{user.mention} has been timed out!"), ephemeral=True)
        except Forbidden as err:
            await interaction.response.send_message(embed=error_template("Perihelion doesn't have permissions to moderate members, or the user is above Perihelion's role!"), ephemeral=True)


async def setup(client):
    await client.add_cog(BanCog(client))
