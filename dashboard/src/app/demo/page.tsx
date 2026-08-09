import { BackgroundEffects } from "@/components/background-effects";
import { NoteCard } from "@/components/note-card";
import { DashboardControls } from "@/components/dashboard-controls";
import { mockNotes } from "@/lib/mock-notes";
import { Note } from "@/types/note";
import { NeuralNetwork } from "@/components/neural-network";
import Link from "next/link";
import { LogOut } from "lucide-react";

export const dynamic = 'force-dynamic';

export default async function DemoPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; tag?: string; sort?: string }>;
}) {
  const resolvedParams = await searchParams;

  const query = resolvedParams.q || "";
  const tag = resolvedParams.tag || "ALL";
  const sort = resolvedParams.sort || "newest";

  let notes: Note[] = mockNotes;

  if (query) {
    const needle = query.toLowerCase();
    notes = notes.filter(
      (n) =>
        n.titulo.toLowerCase().includes(needle) ||
        n.contenido.toLowerCase().includes(needle) ||
        n.tag.toLowerCase().includes(needle)
    );
  }

  if (tag !== "ALL") {
    notes = notes.filter((n) => n.tag === tag);
  }

  notes = [...notes].sort((a, b) => {
    const diff = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
    return sort === "newest" ? -diff : diff;
  });

  const allTags = [...new Set(mockNotes.map((n) => n.tag))].sort();

  return (
    <main className="relative min-h-screen w-full bg-[#020617] text-white selection:bg-blue-500/30">
      <BackgroundEffects />
      <NeuralNetwork />

      <div className="fixed top-4 right-4 z-50 flex items-center gap-2 rounded-full border border-emerald-500/30 bg-[#0a0a0a]/80 px-4 py-2 backdrop-blur-xl">
        <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
        <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400">Modo demo</span>
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-6 py-12 lg:px-8">
        <header className="mb-12 flex flex-col items-center">
          <h1 className="mb-2 text-4xl font-black tracking-tighter sm:text-5xl">
            ENGRAM<span className="text-blue-500">.</span>
          </h1>
          <p className="mb-8 text-xs font-bold uppercase tracking-[0.3em] text-white/30">
            Notas de ejemplo para explorar la interfaz
          </p>

          <DashboardControls tags={allTags} basePath="/demo" />
        </header>

        {notes.length === 0 ? (
          <div className="flex h-64 items-center justify-center rounded-[2rem] border border-white/5 bg-white/[0.01] backdrop-blur-sm">
            <p className="text-sm font-bold uppercase tracking-widest text-white/20">No se encontraron notas</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            {notes.map((note) => (
              <NoteCard key={note.id} note={note} readOnly />
            ))}
          </div>
        )}

        <footer className="mt-16 flex justify-center">
          <Link
            href="/login"
            className="group flex items-center gap-2 rounded-xl border border-white/5 bg-white/5 px-5 py-2.5 text-[10px] font-bold uppercase tracking-widest text-white/40 transition-all hover:bg-white/10 hover:text-white/60"
          >
            <LogOut size={14} />
            Volver al inicio de sesión
          </Link>
        </footer>
      </div>
    </main>
  );
}
