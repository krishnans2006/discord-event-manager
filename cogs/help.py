from discord import ApplicationContext, SlashCommand, SlashCommandGroup
from discord.commands import slash_command
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.cogs = [c for c in self.client.cogs.keys()]
        self.text = ""

    @slash_command(name="help", description="Learn about the bot's commands")
    async def _help(self, context: ApplicationContext):
        await context.defer(ephemeral=True)
        text = ""
        if not self.text:
            self.cogs = [c for c in self.client.cogs.keys()]
            for cog in self.cogs:
                cog = self.client.get_cog(cog)
                text += f"\n\n**All `{cog.qualified_name}` Commands:**\n"
                for cmd in cog.get_commands():
                    if isinstance(cmd, SlashCommand):
                        text += f" • {cmd.mention} - {cmd.description}\n"
                    if isinstance(cmd, SlashCommandGroup):
                        for subcmd in cmd.walk_commands():
                            if isinstance(subcmd, SlashCommand):
                                text += f" • {subcmd.mention} - {subcmd.description}\n"
            self.text = text.lstrip()
        await context.respond(
            content=self.text,
            ephemeral=True,
        )

    @slash_command(name="ping", description="Check the bot's current latency")
    async def _ping(self, context: ApplicationContext) -> None:
        await context.defer(ephemeral=True)
        await context.respond(
            f"*{round(self.client.latency * 1000, 2)}ms later...*\nPong! ",
            ephemeral=True,
        )


def setup(client) -> None:
    client.add_cog(Help(client))
