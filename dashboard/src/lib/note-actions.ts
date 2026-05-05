"use server"

import { db } from "@/lib/db"
import { getEmbedding } from "@/lib/gemini"
import { upsertVector, deleteVector } from "@/lib/pinecone"
import { revalidatePath } from "next/cache"
import { auth } from "@/auth"

export async function deleteNote(id: number) {
  const session = await auth();
  if (!session || session.user?.email !== process.env.ALLOWED_EMAIL) {
    throw new Error("Unauthorized");
  }

  try {
    await db.query('DELETE FROM notas WHERE id = $1', [id]);
    await deleteVector(id.toString());
    revalidatePath('/dashboard');
    return { success: true };
  } catch (error) {
    throw new Error("Delete failed");
  }
}

export async function updateNote(id: number, title: string, content: string, tag: string) {
  const session = await auth();
  if (!session || session.user?.email !== process.env.ALLOWED_EMAIL) {
    throw new Error("Unauthorized");
  }

  if (!content || content.length > 10000) {
    throw new Error("Content too long or empty");
  }

  try {
    const res = await db.query(
      'UPDATE notas SET titulo = $1, contenido = $2, tag = $3 WHERE id = $4 RETURNING discord_message_id',
      [title, content, tag.toUpperCase(), id]
    );

    const msg_id = res.rows[0]?.discord_message_id;

    const inputText = `Ttulo: ${title}\n\nContenido: ${content}`;
    const embedding = await getEmbedding(inputText);

    await upsertVector(id.toString(), embedding, {
      titulo: title,
      tag: tag.toUpperCase()
    });

    if (msg_id) {
      try {
        await fetch('http://engram_bot:5000/update_note', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            id,
            titulo: title,
            contenido: content,
            discord_message_id: msg_id,
            tag: tag.toLowerCase()
          })
        });
      } catch (e) {
        console.error("Bot sync failed:", e);
      }
    }

    revalidatePath('/dashboard');
    return { success: true };
  } catch (error) {
    throw new Error("Update failed");
  }
}
