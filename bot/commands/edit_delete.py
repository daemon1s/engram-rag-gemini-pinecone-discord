import discord
from discord import app_commands
from core.notes import update_note, delete_note
from core.embeddings import process_and_upload_note
from services.pinecone_client import PineconeClient
from datetime import datetime

pinecone = PineconeClient()

async def setup_edit_delete_commands(tree: app_commands.CommandTree):
    
    @tree.command(name="edit", description="Edita una nota existente")
    @app_commands.describe(id="El ID de la nota (#42)", nuevo_contenido="El nuevo texto")
    async def edit(interaction: discord.Interaction, id: int, nuevo_contenido: str):
        await interaction.response.defer()
        
        try:
            res = await update_note(id, nuevo_contenido)
            if not res:
                return await interaction.followup.send(f"No encontré la nota #{id}")
            
            tag = interaction.channel.name
            await process_and_upload_note(id, nuevo_contenido, tag, datetime.now())
            
            msg = await interaction.followup.send(f"Nota #{id} actualizada correctamente.", wait=True)
            await msg.delete(delay=30)
            
        except Exception as e:
            msg = await interaction.followup.send(f"Error al editar: {str(e)}", wait=True)
            await msg.delete(delay=30)

    @tree.command(name="delete", description="Borra una nota permanentemente")
    @app_commands.describe(id="El ID de la nota a eliminar")
    async def delete(interaction: discord.Interaction, id: int):
        await interaction.response.defer()
        
        try:
            res = await delete_note(id)
            if not res:
                return await interaction.followup.send(f"No encontré la nota #{id}")
            
            pinecone.delete_vector(id)
            
            msg = await interaction.followup.send(f"Nota #{id} eliminada de PostgreSQL y Pinecone.", wait=True)
            await msg.delete(delay=30)
            
        except Exception as e:
            msg = await interaction.followup.send(f"Error al eliminar: {str(e)}", wait=True)
            await msg.delete(delay=30)
