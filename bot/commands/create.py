import discord
from discord import app_commands
from core.notes import create_note
from core.embeddings import process_and_upload_note
from bot.ui.retry_view import RetryView

async def setup_create_command(tree: app_commands.CommandTree):
    
    async def execute_create(interaction: discord.Interaction, contenido: str, nota_id: int = None):
        tag = interaction.channel.name
        if not contenido or len(contenido) > 10000:
            msg = await interaction.followup.send("La nota es demasiado larga (máx 10,000 caracteres) o está vacía.", wait=True)
            return await msg.delete(delay=30)

        try:
            if not nota_id:
                nota_data = await create_note(contenido, tag, str(interaction.id))
                
                if "error" in nota_data and nota_data["error"] == "duplicate":
                    msg_text = f"⚠️ Ya tienes una nota exactamente igual con el ID **#{nota_data['id']}**."
                    msg = await interaction.followup.send(msg_text, wait=True)
                    return await msg.delete(delay=30)
                
                nota_id = nota_data['id']
            
            await process_and_upload_note(nota_id, contenido, tag)
            
            sticky_note = f"📝 #{nota_id}\n{contenido}"
            await interaction.followup.send(sticky_note)
            
        except Exception as e:
            friendly_message = (
                "❌ **Error:** No se pudo procesar la nota correctamente. "
                "Tu nota fue guardada en la base de datos pero no tiene búsqueda semántica aún.\n"
                "*Este mensaje se eliminará en 30s.*"
            )
            print(f"Error en create: {str(e)}")
            
            view = RetryView(execute_create, contenido, nota_id)
            error_msg = await interaction.followup.send(
                friendly_message, 
                view=view, 
                wait=True
            )
            await error_msg.delete(delay=30)

    @tree.command(name="create", description="Crea una nueva nota (Sticky Note)")
    @app_commands.describe(contenido="El texto de la nota")
    async def create(interaction: discord.Interaction, contenido: str):
        await interaction.response.defer()
        await execute_create(interaction, contenido)
