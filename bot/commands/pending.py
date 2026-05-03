import discord
from discord import app_commands
from core.notes import get_pending_notes
from bot.ui.pending_view import PendingView

async def setup_pending_command(tree: app_commands.CommandTree):
    @tree.command(name="pending", description="Gestiona notas que no se pudieron sincronizar con la IA")
    async def pending(interaction: discord.Interaction):
        await interaction.response.defer()
        
        notes = await get_pending_notes()
        
        if not notes:
            return await interaction.followup.send("✅ No hay notas pendientes de sincronización.", ephemeral=True)
            
        view = PendingView(notes)
        await interaction.followup.send(embed=view.create_embed(), view=view)
