import discord
from discord import app_commands
from cfg import DEVELOPERS

def developer_only():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id in DEVELOPERS
    return app_commands.check(predicate)
