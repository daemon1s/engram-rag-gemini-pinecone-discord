import discord
from discord import app_commands
from core.notes import create_note
from core.embeddings import process_and_upload_note
from bot.ui.note_modal import NoteModal
from bot.ui.retry_view import RetryView

async def setup_create_command(tree: app_commands.CommandTree):
    
    async def execute_create(interaction: discord.Interaction, titulo: str, contenido: str, nota_id: int = None):
        tag = interaction.channel.name
        if not contenido or len(contenido) > 10000:
            msg = await interaction.followup.send("La nota es demasiado larga o está vacía.", wait=True)
            return await msg.delete(delay=30)

        try:
            if not nota_id:
                nota_data = await create_note(titulo, contenido, tag, str(interaction.id))
                
                if "error" in nota_data and nota_data["error"] == "duplicate":
                    msg_text = f"⚠️ Ya existe una nota igual con el ID **#{nota_data['id']}**."
                    msg = await interaction.followup.send(msg_text, wait=True)
                    return await msg.delete(delay=30)
                
                nota_id = nota_data['id']
            
            await process_and_upload_note(nota_id, titulo, contenido, tag)
            
            embed = discord.Embed(
                title=f"📌 #{nota_id} | {titulo}",
                description=contenido,
                color=0x3B82F6
            )
            embed.set_footer(text=f"Categoría: {tag} • Ver en Dashboard")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            friendly_message = (
                "❌ **Error:** No se pudo procesar la nota correctamente. "
                "Guardada sin búsqueda semántica aún.\n"
                "*Este mensaje se eliminará en 30s.*"
            )
            print(f"Error en create: {str(e)}")
            
            view = RetryView(execute_create, titulo, contenido, nota_id)
            error_msg = await interaction.followup.send(
                friendly_message, 
                view=view, 
                wait=True
            )
            await error_msg.delete(delay=30)

    @tree.command(name="create", description="Crea una nueva nota (Sticky Note)")
    async def create(interaction: discord.Interaction):
        modal = NoteModal(execute_create)
        await interaction.response.send_modal(modal)
