import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_data_manager
from discord.app_commands import locale_str

import random
import sys
from typing import List
import traceback

class WriteTextModal(discord.ui.Modal, title='note creation'):
    def __init__(self, wmcog, wikimanager):
        self.wmcog = wmcog
        self.wikimanager = wikimanager
        super().__init__()

    wikipage_title = discord.ui.TextInput(
        label='Write the note\'s **title** below.',
        style=discord.TextStyle.short,
        placeholder='The note\'s name',
        max_length=100,
        required=True
    )

    wikipage_contents = discord.ui.TextInput(
        label='Write the note itself below.',
        style=discord.TextStyle.long,
        placeholder='The note\'s contents',
        max_length=1800,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        page_contents = self.wikipage_contents.value
        page_name = self.wikipage_title.value
        wiki, _ = self.wikimanager.get_or_create_wiki(interaction.user.id, f"{interaction.user.name}'s notes")
        try:
            wiki.write_page(page_name, page_contents)
        except ValueError:
            await interaction.response.send_message(embed=error_template("You've locked that note!"), ephemeral=True)
        self.wikimanager.save_wiki(wiki)
        await interaction.response.send_message(f'Note {page_name} edited! New contents:\n```ansi\n{page_contents}```', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(f'```py\n{''.join(traceback.format_exception(error)).replace("\\n", "\n")}```', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
class NoteCog(commands.GroupCog, group_name="note"):
    def __init__(self, client):
        self.client = client
        self.wmcog = client.get_cog('wikimanager')
        self.wikimanager = self.wmcog.WikiManager()

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: notes loaded")

    @app_commands.command(name="create")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def create(self, interaction: discord.Interaction):
        """
        Pops up a modal for what note to create, and the new contents.
        """
        await interaction.response.send_modal(WriteTextModal(self.wmcog, self.wikimanager))

    @app_commands.command(name="edit")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def edit(self, interaction: discord.Interaction):
        """
        Pops up a modal for what note to edit, and the new contents.
        """
        await interaction.response.send_modal(WriteTextModal(self.wmcog, self.wikimanager))

    @app_commands.command(name="read")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def read(self, interaction: discord.Interaction, page: str):
        """
        Read a note.

        Parameters
        ------------
        page: str
            The note to read.
        """
        wiki, _ = self.wikimanager.get_or_create_wiki(interaction.user.id, f"{interaction.user.name}'s notes")
        try:
            page_content = wiki.read_page(page)
        except ValueError:
            await interaction.response.send_message(embed=error_template("Note not found"), ephemeral=True)
            return
        await interaction.response.send_message(embed=embed_template(page, page_content))

    @app_commands.command(name="lock")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def lock(self, interaction: discord.Interaction, page: str):
        """
        Locks a note.

        Parameters
        ------------
        page: str
            The page to lock.
        """
        wiki, _ = self.wikimanager.get_or_create_wiki(interaction.user.id, f"{interaction.user.name}'s notes")
        try:
            wiki.lock_page(page)
            self.wikimanager.save_wiki(wiki)
        except ValueError:
            await interaction.response.send_message(embed=error_template("Page not found"), ephemeral=True)
        await interaction.response.send_message(embed=embed_template(f"success", f"{page} locked"))

    @app_commands.command(name="delete")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def delete(self, interaction: discord.Interaction, page: str):
        """
        Deletes a note.

        Parameters
        ------------
        page: str
            The note to delete.
        """
        wiki, _ = self.wikimanager.get_or_create_wiki(interaction.user.id, f"{interaction.user.name}'s notes")
        try:
            wiki.delete_page(page)
            self.wikimanager.save_wiki(wiki)
        except ValueError:
            await interaction.response.send_message(embed=error_template("Page not found"), ephemeral=True)
        await interaction.response.send_message(embed=embed_template(f"success", f"{page} wiped"))

    @app_commands.command(name="unlock")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def unlock(self, interaction: discord.Interaction, page: str):
        """
        Unlocks a note.

        Parameters
        ------------
        page: str
            The note to unlock.
        """
        wiki, _ = self.wikimanager.get_or_create_wiki(interaction.user.id, f"{interaction.user.name}'s notes")
        try:
            wiki.unlock_page(page)
            self.wikimanager.save_wiki(wiki)
        except ValueError:
            await interaction.response.send_message(embed=error_template("Page not found"), ephemeral=True)
        await interaction.response.send_message(embed=embed_template(f"success", f"{page} unlocked"))

    @app_commands.command(name="list")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def list(self, interaction: discord.Interaction):
        """
        List out all notes.
        """
        wiki, _ = self.wikimanager.get_or_create_wiki(interaction.user.id, f"{interaction.user.name}'s notes")
        await viewmenu_paginate_entries(interaction, wiki.get_all_page_titles(), "Your notes")


# The `setup` function is required for the cog to work
# Don't change anything in this function, except for the
# name of the cog to the name of your class.
async def setup(client):
    await client.add_cog(NoteCog(client))
