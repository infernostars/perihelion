from typing import Optional

from bs4 import BeautifulSoup

import discord, requests
from discord import app_commands
from discord.ext import commands
from utils.logging import log

class LanguageSystemCog(commands.Cog, name="language"):
    def __init__(self, client):
        self.client = client

    def list_format(self, input_list):
        """
        Formats a list for English.
        """
        if len(input_list) == 0:
            return "nothing"
        if len(input_list) == 1:
            return str(input_list[0])
        if len(input_list) == 2:
            return f"{input_list[0]} and {input_list[1]}"
        else:
            return ", ".join(input_list[:-1])+f", and {input_list[-1]}"

    def s(self, number):
        """
        Plural. "s" if the number is not 1, else "".
        """
        return "" if number == 1 else "s"

    def clean_html(self, html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        return soup.get_text()

    def process_json(self, json_data):
        result = {}
        for lang, entries in json_data.items():
            lang_data = []
            for entry in entries:
                cleaned_definitions = [self.clean_html(def_entry.get('definition', '').strip())
                                       for def_entry in entry.get('definitions', [])
                                       if def_entry.get('definition', '').strip()]
                if cleaned_definitions:
                    lang_data.append({
                        'partOfSpeech': entry.get('partOfSpeech', ''),
                        'definitions': cleaned_definitions
                    })
            if lang_data:
                result[lang] = {
                    'language': entries[0].get('language', ''),
                    'entries': lang_data
                }
        return result


    def define(self, word: str):
        """
        Define a word. Uses Wiktionary on the backend.
        """
        url = f'https://en.wiktionary.org/api/rest_v1/page/definition/{word}'
        headers = {
            'User-Agent': 'RollplayerPlus/4 (@whirlingstars on Discord)'
        }
        params = {
            'redirect': 'false'
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        data = self.process_json(data)
        return data

    def json_to_markdown(self, data):
        markdown = ""
        for lang, lang_data in data.items():
            markdown += f"### {lang_data['language']}\n"
            for entry in lang_data['entries']:
                markdown += f"*{entry['partOfSpeech']}*\n"
                markdown += "\n".join(f"{i}. {definition}" for i, definition in enumerate(entry['definitions'], 1))
                markdown += "\n"
        return markdown.strip()

    def english_json_to_markdown(self, data):
        markdown = ""
        if 'en' in data:
            markdown += "### English\n"
            for entry in data['en']['entries']:
                markdown += f"*{entry['partOfSpeech']}*\n"
                markdown += "\n".join(f"{i}. {definition}" for i, definition in enumerate(entry['definitions'], 1))
                markdown += "\n"
        return markdown.strip()


async def setup(client):
    await client.add_cog(LanguageSystemCog(client))
