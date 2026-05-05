import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from aiohttp import web
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
        with open("/tmp/bot_ready", "w") as f:
            f.write("ready")

        await setup_create_command(self.tree)
        await setup_query_command(self.tree)
        await setup_edit_delete_commands(self.tree)
        await setup_pending_command(self.tree)
        
        await self.tree.sync()
        print(f"Comandos sincronizados para {self.user}")
        
        self.loop.create_task(self.start_web_server())

    async def start_web_server(self):
        app = web.Application()
        app.router.add_post('/update_note', self.handle_update_note)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 5000)
        await site.start()
        print(">> API de Sincronizacin Interna activa en puerto 5000")

    async def handle_update_note(self, request):
        try:
            data = await request.json()
            nota_id = data.get('id')
            titulo = data.get('titulo')
            contenido = data.get('contenido')
            msg_id = data.get('discord_message_id')
            tag = data.get('tag')

            if not msg_id or not tag:
                return web.Response(text="No message reference", status=200)

            guild = self.get_guild(int(os.getenv("DISCORD_GUILD_ID")))
            if not guild:
                return web.Response(text="Guild not found", status=500)
            
            channel = discord.utils.get(guild.channels, name=tag)
            if not channel:
                return web.Response(text="Channel not found", status=404)

            try:
                msg = await channel.fetch_message(int(msg_id))
                embed = discord.Embed(
                    title=f"Y\"O #{nota_id} | {titulo}",
                    description=contenido,
                    color=0x3B82F6
                )
                await msg.edit(embed=embed)
                return web.Response(text="Sync OK")
            except Exception as e:
                return web.Response(text=f"Message not found or error: {str(e)}", status=200)
        except Exception as e:
            return web.Response(text=str(e), status=500)

    async def on_ready(self):
        print(f"Conectado como {self.user} (ID: {self.user.id})")
        print("------")

bot = engramBot()

@bot.tree.command(name="ping", description="Verifica que el bot est vivo")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("engram est en lnea.")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
