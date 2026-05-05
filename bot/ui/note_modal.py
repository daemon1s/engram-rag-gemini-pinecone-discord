import discord
from discord import ui

class NoteModal(ui.Modal, title="Crear nueva nota"):
    titulo = ui.TextInput(
        label="Título de la nota",
        placeholder="Un título descriptivo...",
        min_length=3,
        max_length=100
    )
    contenido = ui.TextInput(
        label="Contenido de la nota",
        style=discord.TextStyle.long,
        placeholder="Escribe o pega aquí tu nota con formato Markdown...",
        min_length=1,
        max_length=4000
    )

    def __init__(self, callback_func):
        super().__init__()
        self.callback_func = callback_func

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.callback_func(interaction, self.titulo.value, self.contenido.value)
