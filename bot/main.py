import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from db.connection import DBConnection

load_dotenv()

from bot.commands.create import setup_create_command
from bot.commands.query import setup_query_command
from bot.commands.edit_delete import setup_edit_delete_commands
from bot.commands.pending import setup_pending_command

class engramBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await setup_create_command(self.tree)
        await setup_query_command(self.tree)
        await setup_edit_delete_commands(self.tree)
        await setup_pending_command(self.tree)
        
        await self.tree.sync()
        print(f"Comandos sincronizados para {self.user}")

    async def on_ready(self):
        # Crear señal de salud para Docker
        with open("/tmp/bot_ready", "w") as f:
            f.write("ready")
            
        print(f"Conectado como {self.user} (ID: {self.user.id})")
        print("------")

bot = engramBot()

@bot.tree.command(name="ping", description="Verifica que el bot esté vivo")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("engram está en línea.")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
