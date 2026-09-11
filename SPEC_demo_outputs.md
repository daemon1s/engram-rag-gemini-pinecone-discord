# Spec demo portfolio: outputs de create, query, edit y delete

Nivel de riesgo: L2. Motivo: toca input de usuario y borrado de datos, altera comandos compartidos del bot y usa patrón nuevo de embeds centralizados.
Decisión aprobada: modo mixto limpio y servidor abierto sin whitelist.

## Requerimiento exacto

Dejar los cuatro comandos listos para grabar demo sin exponer user personal y sin mensajes rotos:
- `/create`: mensaje público persistente con tarjeta de nota.
- `/query`: mensaje público persistente con respuesta y fuentes.
- `/edit`: edita tarjeta original y confirma solo en ephemeral verde.
- `/delete`: borra tarjeta original y confirma solo en ephemeral rojo.
- Corregir encoding roto en `edit_delete.py` y `note_modal.py`.
- No agregar restricción por usuario. Cualquiera del servidor demo puede usar los comandos.

## Contratos de embeds

- `build_note_embed(nota_id: int, titulo: str, contenido: str, tag: str) -> discord.Embed`
  Título: `📌 #<id> | <titulo truncado a 80>`. Límite Discord 256.
  Descripción: `contenido` truncado a 4000.
  Color: `0x3B82F6`.
  Footer: `Categoría: <tag> • ver en dashboard`.
  Timestamp: utcnow.
- `build_query_embed(pregunta: str, respuesta: str, fuentes: list[{id, tag}]) -> discord.Embed`
  Título: `🔍 <pregunta truncada a 200>`. Límite 256.
  Descripción: `respuesta` truncada a 3900 más aviso si se trunca.
  Campo `fuentes`: una línea por fuente ` #<id> • <tag>` o `Sin fuentes` si está vacío.
  Color: `0x3B82F6`.
  Footer: `RAG semántico • top_k=5`.
  Timestamp: utcnow.
- `build_edit_confirm(nota_id: int, titulo: str) -> discord.Embed`
  Título: `✅ Nota #<id> actualizada`.
  Descripción: `**<titulo>** más texto `Contenido y vector actualizados.`.
  Color: `0x22C55E`.
- `build_delete_confirm(nota_id: int) -> discord.Embed`
  Título: `🗑️ Nota #<id> eliminada`.
  Descripción: `Borrada de PostgreSQL, Pinecone y Discord.`.
  Color: `0xEF4444`.
- `resolve_tag(nota_tag: str | None, fallback_channel: str) -> str`
  Usa `nota_tag` si existe, si no usa canal actual. Normaliza con strip.

Envíos:
- Create y query: `followup.send(embed=...)` público sin `delete(delay=...)` y con `allowed_mentions=none`.
- Edit y delete: `followup.send(embed=..., ephemeral=True)` sin timer.
- Mensajes de error de validación o nota no encontrada: ephemeral con `❌` y sin timer largo.

## Archivos a tocar

- `bot/ui/embeds.py`: nuevo, únicos constructores de embeds y truncados.
- `bot/commands/create.py`: usar helper, quitar `delete(delay=30)`, agregar `allowed_mentions`.
- `bot/commands/query.py`: usar helper, agregar fuentes, quitar timer.
- `bot/commands/edit_delete.py`: usar helpers, buscar canal por tag original, borrar mensaje original en delete, ephemeral sin timer, corregir encoding.
- `bot/ui/note_modal.py`: corregir `Título` y `aquí`.
- `tests/test_embeds_demo.py`: nuevo, tests de contratos y regresión de encoding.

## Edge cases y adversariales

- Contenido vacío o mayor a 10000: error ephemeral, no crea nota.
- Título menor a 3 o mayor a 100: lo valida el modal, helper trunca a 80 para el título del embed.
- Respuesta mayor a 4000: truncar a 3900 más aviso.
- Nota inexistente en edit o delete: `❌ No encontré la nota #<id>` ephemeral.
- `discord_message_id` nulo o mensaje ya borrado: no falla, sigue con DB y Pinecone.
- Canal original renombrado: buscar por `nota_tag`, fallback a canal actual, si no existe indicarlo en confirmación.
- Tag con mayúsculas: mostrar original, buscar canal con lower.
- Doble delete o edit concurrente: segundo retorna no encontrada.
- Contenido con `@everyone` o `@here`: enviar con `allowed_mentions=none`.
- Caída de Gemini o Pinecone: create guarda sin vector y muestra retry, query muestra retry. No dejar canal sucio.

## Guion demo para portfolio

1. Servidor demo privado con canales `proyectos` e `ideas`, apodos neutros, lista de miembros oculta.
2. `/create` dos notas del mismo tema para que el query tenga recall.
3. Captura de modal más tarjeta creada.
4. `/query` con pregunta que cruce ambas notas, captura con fuentes visibles.
5. `/edit` desde cualquier canal, captura de tarjeta con marca editado más dashboard sincronizado.
6. `/delete` de nota descartable, captura de canal limpio más confirmación ephemeral y dashboard sin la nota.
7. Tapar emails, tokens y `GUILD_ID`. Tema oscuro y zoom 100 por ciento.

## Análisis crítico

- Contraargumento: centralizar embeds en un helper nuevo agrega un archivo y una importación a cada comando cuando se podría solo corregir los strings rotos. Se acepta porque evita que create, edit y sync del dashboard diverjan otra vez y deja un solo lugar para screenshots consistentes.
- Riesgo no contemplado: borrar el mensaje original en delete puede fallar por permisos del bot y dejar tarjeta huérfana igual que hoy. Se mitiga tolerando el fallo y avisando en la confirmación ephemeral sin romper el borrado en DB.
- Consecuencia de segundo orden: al quitar el autoborrado de 30 segundos el canal demo queda limpio por ephemeral, pero si alguien espera ver confirmaciones públicas para auditar quién borró qué, pierde trazabilidad. Se compensa porque la verdad queda en dashboard y DB.
