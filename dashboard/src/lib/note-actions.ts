"use server"

import { db } from "@/lib/db"
import { getEmbedding } from "@/lib/gemini"
import { upsertVector, deleteVector } from "@/lib/pinecone"
import { revalidatePath } from "next/cache"

export async function deleteNote(id: number) {
  try {
    await db.query('DELETE FROM notas WHERE id = $1', [id]);
    await deleteVector(id.toString());
    revalidatePath('/dashboard');
    return { success: true };
  } catch (error) {
    throw new Error("Delete failed");
  }
}

export async function updateNote(id: number, content: string, tag: string) {
  try {
    await db.query(
      'UPDATE notas SET contenido = $1, tag = $2 WHERE id = $3',
      [content, tag.toUpperCase(), id]
    );

    const embedding = await getEmbedding(content);

    await upsertVector(id.toString(), embedding, {
      contenido: content,
      tag: tag.toUpperCase()
    });

    revalidatePath('/dashboard');
    return { success: true };
  } catch (error) {
    throw new Error("Update failed");
  }
}
