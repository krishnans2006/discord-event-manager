import discord

import json
import requests

from discord.ext import tasks

with open("config.json") as f:
    config = json.load(f)


intents = discord.Intents.default()

client = discord.Bot(
    intents=intents, debug_guilds=config["test_guilds"], owner_id=731604933773885521
)

cogs = ["cogs.help"]
for cog in cogs:
    client.load_extension(cog)


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="planes fly")
    )
    print("Ready!")


@client.event
async def on_application_command_error(
    context: discord.ApplicationContext, error: discord.DiscordException
):
    if isinstance(error, discord.ApplicationCommandInvokeError):
        msg = await context.respond(
            f"This command raised an error!",
            ephemeral=True,
        )
    raise error


@tasks.loop(minutes=5)
async def heartbeat():
    print("Sending heartbeat")
    requests.post(f"https://uptime.betterstack.com/api/v1/heartbeat/{config['heartbeat']}")


@heartbeat.before_loop
async def heartbeat_is_ready():
    await client.wait_until_ready()


heartbeat.start()


if __name__ == "__main__":
    client.run(config["token"])
