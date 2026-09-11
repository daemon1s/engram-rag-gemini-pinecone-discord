import discord
from discord import app_commands
from core.rag import answer_with_rag
from core.search import get_context
from bot.ui.embeds import build_query_embed
from bot.ui.retry_view import RetryView

ALLOWED_NONE = discord.AllowedMentions.none()

async def setup_query_command(tree: app_commands.CommandTree):
    
    async def execute_query(interaction: discord.Interaction, pregunta: str):
        try:
            respuesta = await answer_with_rag(pregunta)

            try:
                contexto = await get_context(pregunta)
                fuentes = [{"id": int(match.id), "tag": (match.metadata or {}).get("tag", "?")} for match in contexto.matches]
            except Exception:
                fuentes = []
            
            embed = build_query_embed(pregunta, respuesta, fuentes)
            await interaction.followup.send(embed=embed, allowed_mentions=ALLOWED_NONE)
            
        except Exception as e:
            friendly_message = (
                "❌ **Error:** No se pudo completar la consulta. "
                "Gemini no responde tras varios intentos.\n"
                "*Este mensaje se eliminará en 30s.*"
            )
            print(f"Error en query: {str(e)}")
            
            view = RetryView(execute_query, pregunta)
            await interaction.followup.send(
                friendly_message, 
                view=view, 
                ephemeral=True
            )

    @tree.command(name="query", description="Consulta a engram (Búsqueda Semántica)")
    @app_commands.describe(pregunta="Lo que quieres saber basado en tus notas")
    async def query(interaction: discord.Interaction, pregunta: str):
        await interaction.response.defer()
        await execute_query(interaction, pregunta)
