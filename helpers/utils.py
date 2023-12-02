from typing import Optional

import discord
from discord.utils import utcnow


def create_embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    author: Optional[discord.User] = None,
    fields: Optional[list] = None,
    image: Optional[str] = None,
    thumbnail: Optional[str] = "https://avatars.githubusercontent.com/u/47068591",
    color: Optional[hex] = 0x306ABF,
) -> discord.Embed:
    if title:
        embed = discord.Embed(title=title, color=color)
    else:
        embed = discord.Embed(color=color)
    if description:
        embed.description = description
    if author:
        embed.set_author(name=author.name, icon_url=author.display_avatar.url)
    if fields:
        for field in fields:
            embed.add_field(
                name=field[0],
                value=field[1],
                inline=field[2] if len(field) > 2 else False,
            )
    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    embed.timestamp = utcnow()
    return embed
