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

export async function updateNote(id: number, content: string, tag: string) {
  const session = await auth();
  if (!session || session.user?.email !== process.env.ALLOWED_EMAIL) {
    throw new Error("Unauthorized");
  }

  if (!content || content.length > 10000) {
    throw new Error("Content too long or empty");
  }

  try {
    await db.query(
      'UPDATE notas SET contenido = $1, tag = $2 WHERE id = $3',
      [content, tag.toUpperCase(), id]
    );

    const embedding = await getEmbedding(content);

    await upsertVector(id.toString(), embedding, {
      tag: tag.toUpperCase()
    });

    revalidatePath('/dashboard');
    return { success: true };
  } catch (error) {
    throw new Error("Update failed");
  }
}
