import discord
from discord import app_commands
from core.notes import update_note, delete_note, get_note_by_id
from core.embeddings import process_and_upload_note
from services.pinecone_client import PineconeClient
from bot.ui.note_modal import NoteModal

pinecone = PineconeClient()

async def setup_edit_delete_commands(tree: app_commands.CommandTree):
    
    async def execute_edit(interaction: discord.Interaction, titulo: str, contenido: str, nota_id: int):
        tag = interaction.channel.name
        try:
            await update_note(nota_id, titulo, contenido)
            await process_and_upload_note(nota_id, titulo, contenido, tag)
            
            embed = discord.Embed(
                title=f"o. Nota #{nota_id} Actualizada",
                description=f"**{titulo}**\n\nEl contenido y el vector semǭntico han sido actualizados.",
                color=0x3B82F6
            )
            msg = await interaction.followup.send(embed=embed, wait=True)
            await msg.delete(delay=30)
            
        except Exception as e:
            print(f"Error en edit: {str(e)}")
            await interaction.followup.send(f"?O Error al editar: {str(e)}", ephemeral=True)

    @tree.command(name="edit", description="Edita una nota existente mediante un modal")
    @app_commands.describe(id="El ID de la nota (#42)")
    async def edit(interaction: discord.Interaction, id: int):
        nota = await get_note_by_id(id)
        if not nota:
            return await interaction.response.send_message(f"?O No encontrǸ la nota #{id}", ephemeral=True)
        
        modal = NoteModal(
            execute_edit, 
            modal_title=f"Editar Nota #{id}",
            initial_title=nota['titulo'],
            initial_content=nota['contenido'],
            nota_id=id
        )
        await interaction.response.send_modal(modal)

    @tree.command(name="delete", description="Borra una nota permanentemente")
    @app_commands.describe(id="El ID de la nota a eliminar")
    async def delete(interaction: discord.Interaction, id: int):
        await interaction.response.defer()
        try:
            res = await delete_note(id)
            if not res:
                return await interaction.followup.send(f"?O No encontrǸ la nota #{id}")
            
            pinecone.delete_vector(id)
            
            embed = discord.Embed(
                title=f"Y-' Nota #{id} Eliminada",
                description="La nota ha sido borrada de PostgreSQL y Pinecone.",
                color=0xEF4444
            )
            msg = await interaction.followup.send(embed=embed, wait=True)
            await msg.delete(delay=30)
            
        except Exception as e:
            await interaction.followup.send(f"?O Error al eliminar: {str(e)}", ephemeral=True)
