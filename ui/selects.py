from discord import SelectOption, ScheduledEvent
from discord.ui import Button, View, Select


class AddSelect(Select):
    def __init__(self, server_events: list[ScheduledEvent]):
        options = []
        for event in server_events:
            options.append(
                SelectOption(
                    label=event.name,
                    value=str(event.id),
                )
            )
        super().__init__(
            placeholder="Select events to add",
            options=options,
            min_values=1,
            max_values=min(len(options), 25),
        )

    async def callback(self, interaction):
        self.view.selections = self.values
        await interaction.response.defer()


class FilterSelect(Select):
    def __init__(self, events):
        pass

    async def callback(self, interaction):
        await interaction.response.defer()
        await interaction.message.edit(
            content="You selected " + self.values[0],
            view=None,
        )
