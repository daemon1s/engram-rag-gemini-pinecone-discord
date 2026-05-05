import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { db } from "@/lib/db";
import { BackgroundEffects } from "@/components/background-effects";
import { NoteCard } from "@/components/note-card";
import { DashboardControls } from "@/components/dashboard-controls";
import { Note } from "@/types/note";
import { NeuralNetwork } from "@/components/neural-network";

export const dynamic = 'force-dynamic';

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; tag?: string; sort?: string }>;
}) {
  const resolvedParams = await searchParams;
  const session = await auth();
  if (!session) redirect("/login");

  const query = resolvedParams.q || "";
  const tag = resolvedParams.tag || "ALL";
  const sort = resolvedParams.sort || "newest";

  let sql = "SELECT * FROM notas WHERE 1=1";
  const params: any[] = [];

  if (query) {
    sql += " AND (titulo ILIKE $1 OR contenido ILIKE $1 OR tag ILIKE $1)";
    params.push(`%${query}%`);
  }

  if (tag !== "ALL") {
    sql += ` AND tag = $${params.length + 1}`;
    params.push(tag);
  }

  sql += sort === "newest" ? " ORDER BY created_at DESC" : " ORDER BY created_at ASC";

  const { rows: notes } = await db.query<Note>(sql, params);
  const { rows: tagRows } = await db.query("SELECT DISTINCT tag FROM notas ORDER BY tag ASC");
  const allTags = tagRows.map(r => r.tag);

  return (
    <main className="relative min-h-screen w-full bg-[#020617] text-white selection:bg-blue-500/30">
      <BackgroundEffects />
      <NeuralNetwork />

      <div className="relative z-10 mx-auto max-w-7xl px-6 py-12 lg:px-8">
        <header className="mb-12 flex flex-col items-center">
          <h1 className="mb-8 text-4xl font-black tracking-tighter sm:text-5xl">
            ENGRAM<span className="text-blue-500">.</span>
          </h1>

          <DashboardControls tags={allTags} />
        </header>

        {notes.length === 0 ? (
          <div className="flex h-64 items-center justify-center rounded-[2rem] border border-white/5 bg-white/[0.01] backdrop-blur-sm">
            <p className="text-sm font-bold uppercase tracking-widest text-white/20">No se encontraron notas</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {notes.map((note) => (
              <NoteCard key={note.id} note={note} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
