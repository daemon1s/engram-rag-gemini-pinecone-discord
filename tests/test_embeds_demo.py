import sys
import types


def _ensure_discord_stub():
    if "discord" in sys.modules:
        return
    fake = types.ModuleType("discord")

    class FakeEmbed:
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

    fake.Embed = FakeEmbed
    fake.Color = types.SimpleNamespace(green=lambda: 0x22C55E, red=lambda: 0xEF4444, blue=lambda: 0x3B82F6)
    sys.modules["discord"] = fake


_ensure_discord_stub()

from bot.ui.embeds import build_note_embed, build_query_embed, build_edit_confirm, build_delete_confirm, resolve_tag


def test_note_embed_formato_basico():
    embed = build_note_embed(42, "Pipeline Rag", "contenido demo", "proyectos")
    assert embed.title == "📌 #42 | Pipeline Rag"
    assert embed.description == "contenido demo"
    assert int(embed.color) == 0x3B82F6
    assert "proyectos" in embed.footer.text
    assert embed.timestamp is not None


def test_note_embed_trunca_titulo_y_contenido():
    embed = build_note_embed(1, "x" * 200, "y" * 5000, "ideas")
    assert len(embed.title) <= 256
    assert len(embed.description) <= 4096
    assert "#1" in embed.title


def test_query_embed_con_fuentes():
    embed = build_query_embed("como busco notas?", "respuesta demo", [{"id": 1, "tag": "proyectos"}, {"id": 2, "tag": "ideas"}])
    assert "como busco notas?" in embed.title
    assert "respuesta demo" in embed.description
    texto_campos = " ".join(f.name + " " + f.value for f in embed.fields)
    assert "#1" in texto_campos
    assert "#2" in texto_campos
    assert embed.timestamp is not None


def test_query_embed_sin_fuentes_y_trunca_respuesta():
    embed = build_query_embed("p" * 300, "r" * 5000, [])
    assert len(embed.title) <= 256
    assert len(embed.description) <= 4096
    assert "truncada" in embed.description.lower()


def test_edit_confirm_es_verde():
    embed = build_edit_confirm(7, "Nuevo titulo")
    assert "7" in embed.title
    assert "Nuevo titulo" in embed.description
    assert int(embed.color) == 0x22C55E


def test_delete_confirm_es_roja():
    embed = build_delete_confirm(9)
    assert "9" in embed.title
    assert int(embed.color) == 0xEF4444


def test_resolve_tag_prefiere_nota():
    assert resolve_tag("Proyectos", "ideas") == "Proyectos"
    assert resolve_tag("", "ideas") == "ideas"
    assert resolve_tag(None, "ideas") == "ideas"
    assert resolve_tag("  ideas  ", "proyectos") == "ideas"


def test_no_quedan_strings_rotos_en_comandos():
    rotos = ["?O", "Y-'", "encontr", "Ttulo", "aqu tu"]
    rutas = [
        "bot/commands/edit_delete.py",
        "bot/commands/create.py",
        "bot/commands/query.py",
        "bot/ui/note_modal.py",
        "bot/ui/embeds.py",
    ]
    for ruta in rutas:
        with open(ruta, encoding="utf-8") as archivo:
            texto = archivo.read()
        assert "?O" not in texto, ruta
        assert "Y-'" not in texto, ruta
        assert "encontrǸ" not in texto, ruta
        assert "Ttulo" not in texto, ruta
    with open("bot/commands/edit_delete.py", encoding="utf-8") as archivo:
        texto_edit = archivo.read()
    assert "No encontré la nota" in texto_edit
    assert "ephemeral=True" in texto_edit
    assert "delete(delay=30)" not in texto_edit
