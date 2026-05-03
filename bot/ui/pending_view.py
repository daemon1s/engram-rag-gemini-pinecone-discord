import discord
from core.embeddings import process_and_upload_note
from core.notes import delete_note

class PendingView(discord.ui.View):
    def __init__(self, notes):
        super().__init__(timeout=120)
        self.notes = notes
        self.index = 0

    def create_embed(self):
        if not self.notes:
            return discord.Embed(
                title="✨ Todo limpio", 
                description="No hay más notas pendientes de sincronizar.",
                color=discord.Color.green()
            )
        
        note = self.notes[self.index]
        embed = discord.Embed(
            title=f"📝 Nota #{note['id']} (Pendiente)",
            description=note['contenido'],
            color=discord.Color.orange()
        )
        embed.add_field(name="Tag", value=f"`{note['tag']}`", inline=True)
        embed.add_field(name="Fecha", value=note['created_at'].strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.set_footer(text=f"Página {self.index + 1} de {len(self.notes)}")
        return embed

    async def update_message(self, interaction):
        if not self.notes:
            await interaction.edit_original_response(embed=self.create_embed(), view=None)
            return
        
        await interaction.edit_original_response(embed=self.create_embed(), view=self)

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = (self.index - 1) % len(self.notes)
        await interaction.response.defer()
        await self.update_message(interaction)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = (self.index + 1) % len(self.notes)
        await interaction.response.defer()
        await self.update_message(interaction)

    @discord.ui.button(label="Sincronizar", style=discord.ButtonStyle.success, emoji="✅")
    async def sync(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        note = self.notes[self.index]
        
        try:
            await process_and_upload_note(note['id'], note['contenido'], note['tag'])
            
            self.notes.pop(self.index)
            if self.index >= len(self.notes) and self.notes:
                self.index = len(self.notes) - 1
            
            await self.update_message(interaction)
        except Exception as e:
            await interaction.followup.send(f"❌ Error al sincronizar #{note['id']}: {str(e)}", ephemeral=True)

    @discord.ui.button(label="Borrar", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def discard(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        note = self.notes[self.index]
        
        await delete_note(note['id'])
        
        self.notes.pop(self.index)
        if self.index >= len(self.notes) and self.notes:
            self.index = len(self.notes) - 1
            
        await self.update_message(interaction)
