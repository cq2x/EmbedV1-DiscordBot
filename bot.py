"""
VERSION: 1.0.1
CODE LAST EDITED: 10/11/23
CODE CREATE BY: https://discord.com/users/973615253814378526 (DISCORD)
"""
from typing import Optional, Union

import re
import os

import discord
from discord import Interaction, TextStyle, ui, app_commands
from dotenv import load_dotenv

load_dotenv()

def is_value(value: str) -> Union[str, bool]:
    """Check if the given string has a non-zero length."""
    return value if len(value) != 0 else False
  
def valid_hex(color: str) -> Optional[int]:
    """Check if the HEX color code is valid and return its integer representation."""
    try:
        color_int = int(color, 16)
        return color_int
    except ValueError:
        return None

def valid_url(url: str) -> Optional[str]:
    """Check if the given string is a valid URL."""
    pattern = re.compile(
        r'^(http|https)://' 
        r'([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,}'
        r'(:\d+)?'
        r'(/([^\s]*)?)?$'
    )
    return url if pattern.match(url) else None

class Embed_UI(ui.Modal, title='Setup-Embed format'):
    """Modal for creating embed in Discord"""

    def __init__(self, custom_id: str) -> None:
        super().__init__(timeout=None, custom_id=custom_id)

    embed_color = ui.TextInput(label='Input Color (HEX)', max_length=6, style=TextStyle.short, required=False)
    embed_title = ui.TextInput(label='Input Title', max_length=256, style=TextStyle.short, required=False)
    embed_description = ui.TextInput(label='Input Description', max_length=4000, style=TextStyle.long, required=True)
    embed_image_url = ui.TextInput(label='Input Image (URL)', max_length=4000, style=TextStyle.short, required=False)
    embed_footer = ui.TextInput(label='Input Footer', max_length=2048, style=TextStyle.short, required=False)

    async def on_submit(self, interaction: Interaction) -> None:
        """Callback method triggered when the form is submitted."""
        embed = discord.Embed(
            title=title if (title:=is_value(self.embed_title.value)) else None,
            description=description if (description:=is_value(self.embed_description.value)) else None, 
            color=valid_hex(color) if (color:=is_value(self.embed_color.value)) else None
        )
        embed.set_footer(text=text if (text:=is_value(self.embed_footer.value)) else None)
        embed.set_image(url=valid_url(image_url) if (image_url:=is_value(self.embed_image_url.value)) else None)

        # send
        await interaction.channel.send(embed=embed)
        # success
        await interaction.response.send_message(content='Successfully embed created.', ephemeral=True)

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        """Callback method triggered on error during interaction processing."""
        print("Embed_UI:", error)
        embed = discord.Embed(description='An unknown error occurred.', color=0xFF1A53)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# intents
intents = discord.Intents.default()
intents.messages = True

# client
client = discord.Client(intents=intents)
# command tree
tree = app_commands.CommandTree(client)

@client.event
async def on_ready() -> None:
    # sync commands
    await tree.sync()
    print(f'\nLogged in as: {client.user.name} (START WORKING)')

    # bot presence
    activity_type = discord.ActivityType.listening
    await client.change_presence(activity=discord.Activity(type=activity_type, name="∘◦⛧ﾐ"))

@tree.command(description="Embed setup command.") 
async def setup_embed(interaction: Interaction) -> None:
    # embed ui
    model = Embed_UI(custom_id=f"{client.user.id}_{interaction.user.id}")
    await interaction.response.send_modal(model)

def run_bot() -> None:
    client.run(token=os.getenv('DISCORD_BOT_TOKEN'), reconnect=True)

if __name__ == '__main__':
    run_bot()