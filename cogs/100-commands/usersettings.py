import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_data_manager
from discord.app_commands import locale_str

def _get_choices_from_list_settings():
    return [app_commands.Choice(name=x,value=x) for x in get_data_manager("user", 0).get_available_data_keys(bypass_locked=False)]

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
class UserSettingsCog(commands.GroupCog, group_name="usersettings"):
    def __init__(self, client):
        self.client = client
        self.language = client.get_cog('language')

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: user settings loaded")

    @app_commands.command(name="set")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.choices(setting=_get_choices_from_list_settings())
    async def set(self, interaction: discord.Interaction, setting: app_commands.Choice[str], value: str):
        """
        Changes a setting to a new value.

        Parameters
        ------------
        setting: app_commands.Choice[str]
            The setting to set.
        value: str
            The setting's new value.
        """
        settings = get_data_manager("user", interaction.user.id)

        setting_val = setting.value
        setting_type = settings.get_data_type(setting_val)
        if setting_type is bool:
            if value.lower() in ["1", "yes", "y", "true", "t"]:
                value_typed = True
            elif value.lower() in ["0", "no", "n", "false", "f"]:
                value_typed = False
            else:
                await interaction.response.send_message(embed=error_template("The setting you're trying to set is a boolean, so it must be true or false!"))
                return
        elif setting_type is str:
            value_typed = value
        else:
            await interaction.response.send_message(embed=error_template("The option can't find the correct typing. Please report this bug."))
            return
        settings.write_unprivileged(setting_val, value_typed)

        if settings["Global: Compact mode"]:
            await interaction.response.send_message(f"{setting_val} set to {value_typed}", ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed_template("Setting set successfully!", f"{setting_val} set to {value_typed}"), ephemeral=True)

    @app_commands.command(name="get")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.choices(setting=_get_choices_from_list_settings())
    async def get(self, interaction: discord.Interaction, setting: app_commands.Choice[str]):
        """
        Gets the current value of a setting.

        Parameters
        ------------
        setting: app_commands.Choice[str]
            The setting to get.
        """
        setting_val = setting.value
        settings = get_data_manager("user", interaction.user.id)

        setting_value = settings[setting_val]

        if settings["Global: Compact mode"]:
            await interaction.response.send_message(f"{setting_val} is set to {setting_value}", ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed_template(f"{setting_val}'s value", f"{setting_value}"), ephemeral=True)


async def setup(client):
    await client.add_cog(UserSettingsCog(client))
