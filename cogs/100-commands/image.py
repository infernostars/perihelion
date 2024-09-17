import PIL.Image
import discord
from discord import app_commands
from discord.ext import commands
from utils.logging import log
from utils.embeds import *
from typing import Optional
from utils.userdata import get_user_settings

from PIL import Image, ImageDraw, ImageFont
from utils.image import get_wrapped_text, crop_circle
from random import gauss, choice
from math import floor, log10
from io import BytesIO

class ImageCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: image loaded")

    @app_commands.command(name="caption", description="Add a caption above an image.")
    @app_commands.describe(caption="The caption to add.", image="The image to add the caption to.", typ="The type of caption.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.choices(typ = [app_commands.Choice(name="Default",value="default")])
    @app_commands.rename(typ = "type")
    async def caption(self, interaction: discord.Interaction, caption: str, image: discord.Attachment, typ: app_commands.Choice[str] = "default"):
        if hasattr(image, "height"):
            img = await image.read()
            img = Image.open(BytesIO(img))
        else:
            await interaction.response.send_message("This isn't an image!", ephemeral=True)
            return

        w, h = img.size
        bg = Image.new("RGBA", (w, h+50), (255, 255, 255, 255))

        fnt = ImageFont.truetype("assets/Raleway.ttf", 24)
        fnt.set_variation_by_axes([700]) # set font weight
        wrapped_txt = get_wrapped_text(caption, fnt, w-20)
        if wrapped_txt.count("\n") > 0:
            fnt = ImageFont.truetype("assets/Raleway.ttf", 16)
            fnt.set_variation_by_axes([700])  # set font weight
            wrapped_txt = get_wrapped_text(caption, fnt, w - 20)

        d = ImageDraw.Draw(bg)
        d.text((w/2,25), wrapped_txt, font=fnt, anchor="mm", align="center", fill=(0, 0, 0, 255))

        bg.paste(img, (0, 50))

        #send
        b = BytesIO()
        bg.save(b, "PNG")
        b.seek(0)

        await interaction.response.send_message(file=discord.File(b,"image.png"))

async def setup(client):
    await client.add_cog(ImageCog(client))
