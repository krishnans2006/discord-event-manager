from discord import ApplicationContext, slash_command
from discord.commands import Option
from discord.ext import commands

import data


class View(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @slash_command(name="filter", description="Filter server events")
    async def filter(self, context: ApplicationContext):
        await context.defer(ephemeral=True)
        data.User.create_and_update_tag(context.author.id, context.author.name)
        await context.respond(
            "This command is still in development!",
            ephemeral=True,
        )


def setup(client) -> None:
    client.add_cog(View(client))
