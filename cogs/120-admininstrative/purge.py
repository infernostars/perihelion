import discord
from discord import CategoryChannel, Forbidden, ForumChannel, Thread, app_commands
from discord.abc import GuildChannel, PrivateChannel
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional

class PurgeCommandCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: purge loaded")

    @app_commands.command(name="purge", description="Purge the latest messages from the channel this is ran at.")
    @app_commands.describe(count="The amount of messages to purge.")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
    async def purge(self, interaction: discord.Interaction, count: app_commands.Range[int, 1, 100]):
        assert isinstance(interaction.channel, (GuildChannel, Thread)) and not isinstance(interaction.channel, (CategoryChannel, ForumChannel))
        try:
            deleted = await interaction.channel.purge(limit=count)
            await interaction.response.send_message(embed=embed_template("Purged messages", f"{len(deleted)} messages were purged."), ephemeral=True)
        except Forbidden as err:
            await interaction.response.send_message(embed=error_template("Perihelion doesn't have permissions to manage messages!"), ephemeral=True)


async def setup(client):
    await client.add_cog(PurgeCommandCog(client))
