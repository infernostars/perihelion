import discord
from discord import CategoryChannel, Forbidden, ForumChannel, Thread, app_commands
from discord.abc import GuildChannel, PrivateChannel
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional

class SlowmodeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: slowmode loaded")

    @app_commands.command(name="slowmode", description="Sets the slowmode for the channel this is ran in.")
    @app_commands.describe(seconds="The amount of time between messages, in seconds.")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def slowmode(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 0, 21600]):
        assert isinstance(interaction.channel, (GuildChannel, Thread)) and not isinstance(interaction.channel, (CategoryChannel, ForumChannel))
        try:
            if seconds == 0:
                await interaction.response.send_message(embed=embed_template("Slowmode disabled", "Slowmode delay set to 0 seconds."))
            await interaction.response.send_message(embed=embed_template("Slowmode enabled", f"Slowmode delay set to {seconds} seconds."))
        except Forbidden as err:
            await interaction.response.send_message(embed=error_template("Perihelion doesn't have permissions to manage channels!"), ephemeral=True)


async def setup(client):
    await client.add_cog(SlowmodeCog(client))
