import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_data_manager
from discord.app_commands import locale_str

from cfg import BOT_NAME, VERSION

import requests

class WikipediaCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: wikipedia loaded")

    @app_commands.command(name="wikipedia")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def wikipedia(self, interaction: discord.Interaction, query: str):
        """
        Get the introduction to a Wikipedia article, as well as a link.
        """
        url = 'https://en.wikipedia.org/w/rest.php/v1/search/title'
        headers = {
            'User-Agent': f'{BOT_NAME}/{VERSION} (@whirlingstars on Discord)'
        }
        params = {
            'q': query,
            'limit': '1'
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data['pages']:
            await interaction.response.send_message(embed=error_template(f"No search results found for query `{query}`!"))

        url2 = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=true&exlimit=1&titles={data['pages'][0]['key']}&explaintext=1&format=json&formatversion=2"
        response2 = requests.get(url2, headers=headers)
        data2 = response2.json()
        await interaction.response.send_message(embed=embed_template(f"{data['pages'][0]['title']}", f"## [Link to page](https://en.wikipedia.org/wiki/{data['pages'][0]['key']})\n\n{data2["query"]["pages"][0]["extract"]}"))

async def setup(client):
    await client.add_cog(WikipediaCog(client))
