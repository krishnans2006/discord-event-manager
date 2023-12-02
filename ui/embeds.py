import discord
from discord.utils import get

from helpers.type_aliases import Author
from helpers.utils import create_embed


class ManageEmbeds:
    @staticmethod
    async def get_add_confirm_embed(author: Author, event: discord.ScheduledEvent):
        start_timestamp = int(event.start_time.timestamp())
        end_timestamp = int(event.end_time.timestamp()) if event.end_time else None
        if isinstance(event.location.value, str):
            location = event.location.value
        elif isinstance(event.location.value, (discord.StageChannel, discord.VoiceChannel)):
            location = event.location.value.mention
        else:
            location = await event.guild.fetch_channel(event.location.value.id)
            location = location.mention if location else "Unknown"

        return create_embed(
            event.name,
            description=event.description,
            author=author,
            fields=[
                [
                    "Starts",
                    f"<t:{start_timestamp}:f> (<t:{start_timestamp}:R>)",
                ],
                [
                    "Ends",
                    f"<t:{end_timestamp}:f> (<t:{end_timestamp}:R>)" if end_timestamp else "-",
                ],
                [
                    "Location",
                    location,
                ],
                ["Status", event.status.name.title(), True],
                # ["Created by", event.creator.mention, True],
                ["Interested Members", event.subscriber_count, True],
            ],
        )
