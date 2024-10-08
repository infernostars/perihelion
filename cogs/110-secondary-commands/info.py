import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_data_manager
from discord.app_commands import locale_str

from cfg import VERSION, BOT_NAME
import sys
from importlib import metadata

class InfoCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.economy = client.get_cog('economy')

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: info loaded")

    @app_commands.command(name="info", description="Shows info about the bot.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def info(self, interaction: discord.Interaction):
        embed = embed_template(f"{BOT_NAME} version {VERSION} info")
        embed.add_field(name="rollplayerlib version", value=metadata.version("rollplayerlib"))
        embed.add_field(name="python version", value=sys.version)
        embed.add_field(name="discord.py version", value=discord.__version__)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(client):
    await client.add_cog(InfoCog(client))
