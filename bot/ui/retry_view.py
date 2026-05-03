import discord

class RetryView(discord.ui.View):
    def __init__(self, retry_func, *args, **kwargs):
        super().__init__(timeout=60) 
        self.retry_func = retry_func
        self.args = args
        self.kwargs = kwargs

    @discord.ui.button(label="Retry", style=discord.ButtonStyle.primary, emoji="🔄")
    async def retry(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await self.retry_func(interaction, *self.args, **self.kwargs)
        self.stop()
