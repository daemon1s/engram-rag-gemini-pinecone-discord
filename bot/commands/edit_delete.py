import discord
from discord import app_commands
from core.notes import update_note, delete_note, get_note_by_id
from core.embeddings import process_and_upload_note
from services.pinecone_client import PineconeClient
from bot.ui.embeds import build_note_embed, build_edit_confirm, build_delete_confirm, resolve_tag
from bot.ui.note_modal import NoteModal

pinecone = PineconeClient()

async def setup_edit_delete_commands(tree: app_commands.CommandTree):
    
    async def execute_edit(interaction: discord.Interaction, titulo: str, contenido: str, nota_id: int):
        nota_previa = await get_note_by_id(nota_id)
        if not nota_previa:
            return await interaction.followup.send(f"❌ No encontré la nota #{nota_id}", ephemeral=True)
        tag = resolve_tag(nota_previa.get("tag"), interaction.channel.name)
        try:
            await update_note(nota_id, titulo, contenido)
            await process_and_upload_note(nota_id, titulo, contenido, tag)
            
            nota = await get_note_by_id(nota_id)
            msg_id = nota.get('discord_message_id') if nota else None
            aviso = ""
            if msg_id:
                try:
                    guild = interaction.guild
                    channel = discord.utils.get(guild.channels, name=str(tag).lower()) or discord.utils.get(guild.channels, name=tag) or interaction.channel
                    if channel:
                        orig_msg = await channel.fetch_message(int(msg_id))
                        await orig_msg.edit(embed=build_note_embed(nota_id, titulo, contenido, tag))
                    else:
                        aviso = " No pude ubicar el canal original."
                except Exception as ex:
                    print(f"Error actualizando el embed de Discord original: {ex}")
                    aviso = " No pude editar el mensaje original, pero la nota quedó guardada."

            await interaction.followup.send(embed=build_edit_confirm(nota_id, titulo + aviso), ephemeral=True)
              
        except Exception as e:
            print(f"Error en edit: {str(e)}")
            await interaction.followup.send(f"❌ Error al editar: {str(e)}", ephemeral=True)

    @tree.command(name="edit", description="Edita una nota existente mediante un modal")
    @app_commands.describe(id="El ID de la nota (#42)")
    async def edit(interaction: discord.Interaction, id: int):
        nota = await get_note_by_id(id)
        if not nota:
            return await interaction.response.send_message(f"❌ No encontré la nota #{id}", ephemeral=True)
        
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
        await interaction.response.defer(ephemeral=True)
        try:
            nota = await get_note_by_id(id)
            if not nota:
                return await interaction.followup.send(f"❌ No encontré la nota #{id}", ephemeral=True)

            msg_id = nota.get("discord_message_id")
            tag = resolve_tag(nota.get("tag"), interaction.channel.name)

            res = await delete_note(id)
            if not res:
                return await interaction.followup.send(f"❌ No encontré la nota #{id}", ephemeral=True)
            
            pinecone.delete_vector(id)

            if msg_id:
                try:
                    guild = interaction.guild
                    channel = discord.utils.get(guild.channels, name=str(tag).lower()) or discord.utils.get(guild.channels, name=tag)
                    if channel:
                        orig_msg = await channel.fetch_message(int(msg_id))
                        await orig_msg.delete()
                except Exception as ex:
                    print(f"Error borrando mensaje original #{id}: {ex}")
            
            await interaction.followup.send(embed=build_delete_confirm(id), ephemeral=True)
            
        except Exception as e:
            await interaction.followup.send(f"❌ Error al eliminar: {str(e)}", ephemeral=True)
