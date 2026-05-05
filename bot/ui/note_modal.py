import discord
from discord import ui

class NoteModal(ui.Modal):
    def __init__(self, callback_func, modal_title="Crear nueva nota", initial_title="", initial_content="", nota_id=None):
        super().__init__(title=modal_title)
        self.callback_func = callback_func
        self.nota_id = nota_id

        self.titulo_input = ui.TextInput(
            label="Ttulo de la nota",
            placeholder="Un titulo descriptivo...",
            default=initial_title,
            min_length=3,
            max_length=100
        )
        self.add_item(self.titulo_input)

        self.contenido_input = ui.TextInput(
            label="Contenido de la nota",
            style=discord.TextStyle.long,
            placeholder="Escribe o pega aqu tu nota con formato Markdown...",
            default=initial_content,
            min_length=1,
            max_length=4000
        )
        self.add_item(self.contenido_input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.nota_id:
            await self.callback_func(interaction, self.titulo_input.value, self.contenido_input.value, self.nota_id)
        else:
            await self.callback_func(interaction, self.titulo_input.value, self.contenido_input.value)
