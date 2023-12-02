import discord
from discord import ButtonStyle, Interaction, SelectOption
from discord.ui import Button, View, Select

from helpers.type_aliases import Author
from ui.selects import AddSelect


class CustomizedView(View):
    def __init__(self, user: Author, timeout: int = 300, disable_on_timeout: bool = True):
        super().__init__(timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.user = user
        self.message = None
        self.disable_on_timeout = disable_on_timeout

    async def interaction_check(self, interaction: Interaction):
        if interaction.user == self.user:
            return True
        print(str(interaction.user) + " tried interacting with " + str(self.user) + "'s view!")
        await interaction.response.send_message(
            interaction.user.mention + " You can't interact with this!", ephemeral=True
        )
        return False

    async def on_timeout(self):
        if not self.disable_on_timeout:
            return
        self.disable_all_items()
        if isinstance(self.message, discord.Interaction):
            try:
                await self.message.edit_original_response(view=self)
            except AttributeError:
                print(type(self), "has no response attribute!")


class ConfirmCancelView(CustomizedView):
    def __init__(self, user: Author):
        super().__init__(user)
        self.confirmed = False

    @discord.ui.button(label="Confirm", custom_id="y", style=ButtonStyle.green, emoji="✔️", row=4)
    async def confirm_callback(self, _: Button, interaction: Interaction):
        if interaction.user.id == self.user.id:
            self.confirmed = True
            self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Cancel", custom_id="n", style=ButtonStyle.red, emoji="✖️", row=4)
    async def cancel_callback(self, _: Button, interaction: Interaction):
        if interaction.user.id == self.user.id:
            self.stop()
        await interaction.response.defer()


class ConfirmCancelExitView(ConfirmCancelView):
    def __init__(self, user: Author):
        super().__init__(user)
        self.exited = False

    @discord.ui.button(label="Exit", custom_id="e", style=ButtonStyle.gray, emoji="🚪", row=4)
    async def exit_callback(self, _: Button, interaction: Interaction):
        if interaction.user.id == self.user.id:
            self.exited = True
            self.stop()
        await interaction.response.defer()


class AddView(ConfirmCancelView):
    def __init__(self, user: Author, server_events):
        super().__init__(user)
        self.server_events = server_events

        self.add_item(AddSelect(server_events))
        self.selections = []
