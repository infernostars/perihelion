# type: ignore
# TODO: refactor


from typing import Optional

import os, json

import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log

class WikiManagerCog(commands.Cog, name="wikimanager"):
    def __init__(self, client):
        self.client = client

    class WikiPage:
        def __init__(self, title, content, is_locked=False):
            self.title = title
            self.content = content
            self.is_locked = is_locked

        def to_dict(self):
            return {
                "title": self.title,
                "content": self.content,
                "is_locked": self.is_locked
            }

        @classmethod
        def from_dict(cls, data):
            return cls(data["title"], data["content"], data["is_locked"])

    class TextWiki:
        def __init__(self, name, wiki_id=None):
            self.name = name
            self.id = wiki_id or str(uuid.uuid4())
            self.pages = {}

        def add_page(self, title, content):
            if title not in self.pages:
                self.pages[title] = WikiManagerCog.WikiPage(title, content)
            else:
                raise ValueError(f"Page '{title}' already exists")

        def delete_page(self, title):
            if title not in self.pages:
                del self.pages[title]
            else:
                raise ValueError(f"Page '{title}' already exists")

        def read_page(self, title):
            if title in self.pages:
                return self.pages[title].content
            else:
                raise ValueError(f"Page '{title}' not found")

        def write_page(self, title, content):
            if title in self.pages:
                if not self.pages[title].is_locked:
                    self.pages[title].content = content
                else:
                    raise ValueError(f"Page '{title}' is locked")
            else:
                self.add_page(title, content)

        def lock_page(self, title):
            if title in self.pages:
                self.pages[title].is_locked = True
            else:
                raise ValueError(f"Page '{title}' not found")

        def unlock_page(self, title):
            if title in self.pages:
                self.pages[title].is_locked = False
            else:
                raise ValueError(f"Page '{title}' not found")

        def get_all_page_titles(self):
            return list(self.pages.keys())

        def to_dict(self):
            return {
                "name": self.name,
                "id": self.id,
                "pages": {title: page.to_dict() for title, page in self.pages.items()}
            }

        @classmethod
        def from_dict(cls, data):
            wiki = cls(data["name"], data["id"])
            for title, page_data in data["pages"].items():
                wiki.pages[title] = WikiManagerCog.WikiPage.from_dict(page_data)
            return wiki

    class WikiManager:
        _instance = None

        def __new__(cls, storage_dir="data/wikis"):
            if cls._instance is None:
                cls._instance = super(WikiManagerCog.WikiManager, cls).__new__(cls)
                cls._instance.storage_dir = storage_dir
                cls._instance.wikis = {}
                cls._instance.load_wikis()
            return cls._instance

        def create_wiki(self, name, wiki_id=None):
            if wiki_id and wiki_id in self.wikis:
                raise ValueError(f"Wiki with ID '{wiki_id}' already exists")
            wiki = WikiManagerCog.TextWiki(name, wiki_id)
            self.wikis[wiki.id] = wiki
            self.save_wiki(wiki)
            return wiki

        def get_wiki(self, wiki_id):
            return self.wikis.get(wiki_id)

        def get_or_create_wiki(self, wiki_id, name=None):
            if wiki_id in self.wikis:
                return self.wikis[wiki_id], False
            else:
                if name is None:
                    raise ValueError("Name must be provided when creating a new wiki")
                new_wiki = self.create_wiki(name, wiki_id)
                return new_wiki, True

        def save_wiki(self, wiki):
            if not os.path.exists(self.storage_dir):
                os.makedirs(self.storage_dir)

            filename = os.path.join(self.storage_dir, f"{wiki.id}.json")
            with open(filename, "w") as f:
                json.dump(wiki.to_dict(), f)

        def load_wikis(self):
            if not os.path.exists(self.storage_dir):
                return

            for filename in os.listdir(self.storage_dir):
                if filename.endswith(".json"):
                    with open(os.path.join(self.storage_dir, filename), "r") as f:
                        data = json.load(f)
                        wiki = WikiManagerCog.TextWiki.from_dict(data)
                        self.wikis[wiki.id] = wiki

        def get_all_page_titles(self, wiki_id):
            wiki = self.get_wiki(wiki_id)
            if wiki:
                return wiki.get_all_page_titles()
            else:
                raise ValueError(f"Wiki with ID '{wiki_id}' not found")


    def get_id_from_interaction(self, interaction: discord.Interaction) -> int:
        if interaction.guild_id is not None:
            return interaction.guild_id
        if interaction.channel_id is not None:
            return interaction.channel_id
        raise ValueError("Where the hell are you running this at?")

    def get_name_from_interaction(self, interaction: discord.Interaction) -> str:
        if interaction.guild_id is not None:
            return interaction.guild.name
        if interaction.channel_id is not None:
            if isinstance(interaction.channel, discord.channel.GroupChannel):
                return interaction.channel.name if interaction.channel.name else f"{interaction.channel.owner.name}'s GC"
        return str(self.get_id_from_interaction(interaction))

    def can_lock_page(self, interaction: discord.Interaction) -> bool:
        if interaction.guild_id is not None:
            return interaction.user.resolved_permissions.manage_messages
        if interaction.channel_id is not None:
            if isinstance(interaction.channel, GroupChannel):
                return interaction.channel.owner_id == interaction.user.id
        return True # should always be able to lock in dms



async def setup(client):
    await client.add_cog(WikiManagerCog(client))
