import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_user_settings

import random

class ChooseCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.language = client.get_cog('language')

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: choose loaded")

    @app_commands.command(name="choose")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def choose(self, interaction: discord.Interaction, options: str, count: Optional[int], unique: Optional[bool]):
        """
        Chooses one or more options.

        Parameters
        ------------
        options: str
            A list of options, split by semicolons.
        count: Optional[int]
            The amount of options to pick.
        unique: Optional[bool]
            If false, options can be picked multiple times.

        """
        settings = get_user_settings(interaction.user.id)

        if count is None:
            count = 1
        if unique is None:
            unique = True

        option_list = options.split(";")
        option_list = [x.strip() for x in option_list]
        if count > 0:
            if unique:
                if len(option_list) >= count:
                    if settings["Global: Compact mode"]:
                        await interaction.response.send_message(f"{self.language.list_format(random.sample(option_list, k=count))}")
                    else:
                        await interaction.response.send_message(
                            embed=embed_template(f"let's pick... {self.language.list_format(random.sample(option_list, k=count))}."))
                else:
                    await interaction.response.send_message(embed=error_template("Asked for too many choices! (Try setting unique to false if you want to pick multiple options)"))
            else:
                if settings["Global: Compact mode"]:
                    await interaction.response.send_message(f"{self.language.list_format(random.choices(option_list, k=count))}")
                else:
                    await interaction.response.send_message(
                        embed=embed_template(f"let's pick... {self.language.list_format(random.choices(option_list,k=count))}."))
        else:
            await interaction.response.send_message(embed=error_template("Asked for zero or negative choices!"))

async def setup(client):
    await client.add_cog(ChooseCog(client))
