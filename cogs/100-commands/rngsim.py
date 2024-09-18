from typing import Union, List, Optional

import discord
from discord import User, Member, app_commands
from discord.ext import commands
from utils.logging import log
import random
from math import floor
from utils.userdata import get_settings_manager

# This is what happens when the most retarded programmer in existence gets his hands on an actually good codebase!

class RngSimCog(commands.Cog, name="games/rngsim"):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: the worst cog loaded")

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
        while count != repet:
            numbr += random.randint(0, denom)
            count+=1
        numbr*=multi

        old_highscore = settings["RngSim: Highscore"]

        if numbr > settings["RngSim: Highscore"]:
            settings.write_protected("RngSim: Highscore", numbr)
            await interaction.response.send_message(f"## Your score is {numbr}.\n\n# [ NEW HIGHSCORE ]\n## Previous Highscore: {old_highscore}\n## New Highscore: {numbr}\n### Congratulations!")
        else:
            await interaction.response.send_message(f"## Your score is {numbr}.\n\n### Your current highscore is {old_highscore}.")

async def setup(client):
    await client.add_cog(RngSimCog(client))

