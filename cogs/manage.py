from discord import ApplicationContext, slash_command
from discord.ext import commands

import data
from ui.embeds import ManageEmbeds
from ui.views import AddView, ConfirmCancelView, ConfirmCancelExitView


class Manage(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @slash_command(name="add", description="Add an existing server event to the bot")
    async def add(self, context: ApplicationContext):
        await context.defer(ephemeral=True)
        data.User.create_and_update_tag(context.author.id, context.author.name)

        server_events = await context.guild.fetch_scheduled_events()

        if not server_events:
            await context.respond(
                "This server doesn't have any events yet! Use `/create` to create one.",
                ephemeral=True,
            )
            return

        view = AddView(context.author, server_events)
        view.message = await context.interaction.original_response()
        await context.respond("", view=view, ephemeral=True)

        timeout = await view.wait()
        if timeout or not view.confirmed:
            await context.edit(
                content="Canceled!",
                view=None,
            )
            return

        for event_id in view.selections:
            event = await context.guild.fetch_scheduled_event(event_id)
            if not event:
                continue

            view = ConfirmCancelExitView(context.author)
            view.message = await context.interaction.original_response()
            await context.edit(
                content="Add this event?",
                embed=await ManageEmbeds.get_add_confirm_embed(context.author, event),
                view=view,
            )
            timeout = await view.wait()
            if timeout or view.exited:
                await context.edit(
                    content="Exited!",
                    embed=None,
                    view=None,
                )
                return
            if not view.confirmed:
                continue

            interested = {str(u.id): u.name async for u in event.subscribers(limit=12)}

            data.Event.create(
                event_id,
                {
                    "Name": event.name,
                    "Description": event.description,
                    "Guild": str(event.guild.id),
                    "Status": event.status.name,
                    "Time": {
                        "Start": event.start_time,
                        "StartUnix": event.start_time.timestamp(),
                        "End": event.end_time if event.end_time else None,
                        "EndUnix": event.end_time.timestamp() if event.end_time else None,
                    },
                    "InterestedCount": event.subscriber_count,
                },
            )
            data.Event.add_interested(event_id, interested)

        await context.edit(
            content="Done!",
            embed=None,
            view=None,
        )


def setup(client) -> None:
    client.add_cog(Manage(client))
