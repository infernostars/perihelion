import discord
from discord import User, Member, app_commands
from discord.ext import commands
from utils.logging import log
import random
from math import floor
from utils.userdata import get_settings_manager

from typing import Union, List, Optional

class RngSimCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: rngsim loaded")

    @app_commands.command(name="rngsim")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def rngsim(self, interaction: discord.Interaction, query: Optional[str]):
        settings = get_settings_manager("user", interaction.user.id)
        denom = floor(1/random.random())
        repet = floor(1/random.random())
        multi = 1/random.random()
        count = 0
        numbr = 0
        while count < repet:
            numbr += random.randint(0, denom)
            count+=1
        numbr*=multi

        old_highscore = settings["RngSim: Highscore"]

        if numbr > old_highscore:
            settings["RngSim: Highscore"] = numbr
            await interaction.response.send_message(f"## [ NEW HIGHSCORE ({old_highscore:2f} > {numbr:2f}) ]\n\nYour score is **{numbr:2f}**.\n\nCongratulations!")
        else:
            await interaction.response.send_message(f"Your score is **{numbr:2f}**.\n\n-# Your current highscore is {old_highscore:2f}.", ephemeral=True)

async def setup(client):
    await client.add_cog(RngSimCog(client))
