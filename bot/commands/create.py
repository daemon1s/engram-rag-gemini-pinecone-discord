import discord
from discord import app_commands
from core.notes import create_note, update_discord_message_id
from core.embeddings import process_and_upload_note
from bot.ui.embeds import build_note_embed
from bot.ui.note_modal import NoteModal
from bot.ui.retry_view import RetryView

ALLOWED_NONE = discord.AllowedMentions.none()

async def setup_create_command(tree: app_commands.CommandTree):
    
    async def execute_create(interaction: discord.Interaction, titulo: str, contenido: str, nota_id: int = None):
        tag = interaction.channel.name
        if not contenido or len(contenido) > 10000:
            return await interaction.followup.send("La nota es demasiado larga o está vacía.", ephemeral=True)

        try:
            if not nota_id:
                nota_data = await create_note(titulo, contenido, tag, str(interaction.id))
                
                if "error" in nota_data and nota_data["error"] == "duplicate":
                    msg_text = f"⚠️ Ya existe una nota igual con el ID **#{nota_data['id']}**."
                    return await interaction.followup.send(msg_text, ephemeral=True)
                
                nota_id = nota_data['id']
            
            await process_and_upload_note(nota_id, titulo, contenido, tag)
            
            embed = build_note_embed(nota_id, titulo, contenido, tag)
            
            msg = await interaction.followup.send(embed=embed, allowed_mentions=ALLOWED_NONE)
            await update_discord_message_id(nota_id, str(msg.id))
            
        except Exception as e:
            friendly_message = (
                "❌ **Error:** No se pudo procesar la nota correctamente. "
                "Guardada sin búsqueda semántica aún.\n"
                "*Este mensaje se eliminará en 30s.*"
            )
            print(f"Error en create: {str(e)}")
            
            view = RetryView(execute_create, titulo, contenido, nota_id)
            await interaction.followup.send(
                friendly_message, 
                view=view, 
                ephemeral=True
            )

    @tree.command(name="create", description="Crea una nueva nota (Sticky Note)")
    async def create(interaction: discord.Interaction):
        modal = NoteModal(execute_create)
        await interaction.response.send_modal(modal)
