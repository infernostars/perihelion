import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_user_settings

import random

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
class RstCog(commands.GroupCog, group_name="rst"):
    def __init__(self, client):
        self.client = client
        self.filename = "./data/custom_texts.txt"

        # Ensure the file exists
        try:
            with open(self.filename, 'a'):
                pass
        except IOError as e:
            log.error(f"Error creating or accessing the file: {e}")

    def add_text(self, text):
        print("add_text ", text)
        try:
            with open(self.filename, 'a') as file:
                file.write(text + '\n')
        except IOError as e:
            log.error(f"Error writing to file: {e}")

    def get_random_text(self):
        try:
            with open(self.filename, 'r') as file:
                texts = file.readlines()
            return random.choice(texts).strip() if texts else "[No texts in database]"
        except IOError as e:
            log.error(f"Error reading from file: {e}")
            return "[Error reading from database]"

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: rst loaded")

    @app_commands.command(name="add")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def add(self, interaction: discord.Interaction, text: str):
        """
        Add a string to the database.

        Parameters
        ------------
        text: str
            The text to add.
        """
        self.add_text(text)
        settings = get_user_settings(interaction.user.id)

        if settings["Global: Compact mode"]:
            await interaction.response.send_message("Your text has been added to the database.")
        else:
            await interaction.response.send_message(embeds=[embed_template("text added", "Your text has been added to the database.")])

    @app_commands.command(name="get")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def get(self, interaction: discord.Interaction):
        """
        Get a random quote.
        """
        settings = get_user_settings(interaction.user.id)
        text = self.get_random_text()
        if settings["Global: Compact mode"]:
            await interaction.response.send_message(text)
        else:
            await interaction.response.send_message(embed=embed_template("random text", text))

async def setup(client):
    await client.add_cog(RstCog(client))
