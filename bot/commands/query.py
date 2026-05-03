import discord
from discord import app_commands
from core.rag import answer_with_rag
from bot.ui.retry_view import RetryView

async def setup_query_command(tree: app_commands.CommandTree):
    
    async def execute_query(interaction: discord.Interaction, pregunta: str):
        try:
            respuesta = await answer_with_rag(pregunta)
            
            header = f"**Consulta:** {pregunta}\n───────────────────────\n"
            await interaction.followup.send(f"{header}{respuesta}")
            
        except Exception as e:
            friendly_message = (
                "❌ **Error:** No se pudo completar la consulta. "
                "Gemini no responde tras varios intentos.\n"
                "*Este mensaje se eliminará en 30s.*"
            )
            print(f"Error en query: {str(e)}")
            
            view = RetryView(execute_query, pregunta)
            error_msg = await interaction.followup.send(
                friendly_message, 
                view=view, 
                wait=True
            )
            await error_msg.delete(delay=30)

    @tree.command(name="query", description="Consulta a engram (Búsqueda Semántica)")
    @app_commands.describe(pregunta="Lo que quieres saber basado en tus notas")
    async def query(interaction: discord.Interaction, pregunta: str):
        await interaction.response.defer()
        await execute_query(interaction, pregunta)
