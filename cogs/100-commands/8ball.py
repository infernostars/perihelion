import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_data_manager
from discord.app_commands import locale_str

from assets.eightball_responses import responses

import random

class EightBallCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: 8ball loaded")

    @app_commands.command(name="8ball")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def eightball(self, interaction: discord.Interaction, query: Optional[str]):
        """
        Query Tyche(lion) for the answers to all your questions. As long as they have a yes/maybe/no answer.
        """
        settings = get_data_manager("user", interaction.user.id)

        response = random.choice(responses)

        if not query:
            await interaction.response.send_message(f"🎱 {response}")
            return

        if settings["Global: Compact mode"]:
            await interaction.response.send_message(f"🎱 **{query}** | {response}")
        else:
            await interaction.response.send_message(embed=embed_template(f"🎱 {query}", f"{response}"))

async def setup(client):
    await client.add_cog(EightBallCog(client))
