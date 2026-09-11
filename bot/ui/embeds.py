import datetime

try:
    import discord
except ModuleNotFoundError:
    import types

    discord = types.SimpleNamespace()

    class _Embed:
        def __init__(self, title="", description="", color=0):
            self.title = title
            self.description = description
            self.color = color
            self.footer = None
            self.timestamp = None
            self.fields = []

        def set_footer(self, text=""):
            self.footer = types.SimpleNamespace(text=text)
            return self

        def add_field(self, name="", value="", inline=True):
            self.fields.append(types.SimpleNamespace(name=name, value=value, inline=inline))
            return self

    discord.Embed = _Embed

NOTE_COLOR = 0x3B82F6
EDIT_COLOR = 0x22C55E
DELETE_COLOR = 0xEF4444


def _truncate(texto, limite):
    if texto is None:
        return ""
    texto = str(texto)
    if len(texto) <= limite:
        return texto
    return texto[: limite - 1] + "…"


def resolve_tag(nota_tag, fallback_channel):
    if nota_tag and str(nota_tag).strip():
        return str(nota_tag).strip()
    return fallback_channel


def build_note_embed(nota_id, titulo, contenido, tag):
    titulo_corto = _truncate(titulo, 80)
    embed = discord.Embed(
        title=f"📌 #{nota_id} | {titulo_corto}",
        description=_truncate(contenido, 4000),
        color=NOTE_COLOR,
    )
    embed.set_footer(text=f"Categoría: {tag} • ver en dashboard")
    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
    return embed


def build_query_embed(pregunta, respuesta, fuentes):
    respuesta_corta = _truncate(respuesta, 3900)
    if len(str(respuesta)) > 3900:
        respuesta_corta = respuesta_corta + "\n\n*(Respuesta truncada por límites de longitud)*"
    embed = discord.Embed(
        title=f"🔍 {_truncate(pregunta, 200)}",
        description=respuesta_corta,
        color=NOTE_COLOR,
    )
    if fuentes:
        lineas = [f"#{item.get('id')} • {item.get('tag')}" for item in fuentes]
        embed.add_field(name="Fuentes", value="\n".join(lineas)[:1024], inline=False)
    else:
        embed.add_field(name="Fuentes", value="Sin fuentes", inline=False)
    embed.set_footer(text="RAG semántico • top_k=5")
    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
    return embed


def build_edit_confirm(nota_id, titulo):
    embed = discord.Embed(
        title=f"✅ Nota #{nota_id} actualizada",
        description=f"**{titulo}**\n\nContenido y vector actualizados.",
        color=EDIT_COLOR,
    )
    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
    return embed


def build_delete_confirm(nota_id):
    embed = discord.Embed(
        title=f"🗑️ Nota #{nota_id} eliminada",
        description="Borrada de PostgreSQL, Pinecone y Discord.",
        color=DELETE_COLOR,
    )
    embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
    return embed
