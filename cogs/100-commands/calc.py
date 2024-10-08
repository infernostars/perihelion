import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_data_manager
from discord.app_commands import locale_str

import cexprtk

class CalculationCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: calc loaded")

    @app_commands.command(name="calc")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def calc(self, interaction: discord.Interaction, equ: str):
        """
        Solve an equation.

        Parameters
        ------------
        equ: str
            The equation to solve [e.g. "2+2"]
        """
        await interaction.response.send_message(cexprtk.evaluate_expression(equ, {}))

async def setup(client):
    await client.add_cog(CalculationCog(client))
