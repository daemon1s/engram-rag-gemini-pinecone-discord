"use client"
import React, { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Search, Clock, ArrowUpDown } from "lucide-react";
import { motion } from "framer-motion";

export function DashboardControls({ tags }: { tags: string[] }) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [tag, setTag] = useState(searchParams.get('tag') || 'ALL');
  const [sort, setSort] = useState(searchParams.get('sort') || 'newest');

  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    if (tag !== 'ALL') params.set('tag', tag);
    if (sort !== 'newest') params.set('sort', sort);

    const timeout = setTimeout(() => {
      router.push(`/dashboard?${params.toString()}`);
    }, 300);

    return () => clearTimeout(timeout);
  }, [query, tag, sort, router]);

  return (
    <div className="flex w-full flex-col items-center gap-8">
      <div className="flex w-full max-w-2xl items-center gap-6">
        <div className="relative flex-1">
          <div className="relative overflow-hidden rounded-2xl p-[1.5px] bg-blue-500/20 shadow-[0_0_20px_rgba(59,130,246,0.15)]">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
              className="absolute inset-[-200%] pointer-events-none"
              style={{
                background: 'conic-gradient(from 0deg, transparent 0%, transparent 40%, #3b82f6 50%, #fff 52%, #3b82f6 54%, transparent 60%, transparent 100%)'
              }}
            />
            <div className="relative flex w-full items-center rounded-2xl bg-[#0a0a0a] py-3 pl-14 pr-6 backdrop-blur-xl">
              <Search className="absolute left-6 h-4 w-4 text-blue-400/80 transition-colors group-focus-within:text-blue-400" />
              <input
                type="text"
                placeholder="Buscar nota..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full bg-transparent text-sm text-white placeholder:text-white/20 outline-none"
              />
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4 px-2">
          <button
            onClick={() => setSort(sort === 'newest' ? 'oldest' : 'newest')}
            className={`transition-all duration-300 ${sort === 'newest' ? 'text-blue-400' : 'text-white/20 hover:text-blue-400/80'} hover:scale-110 active:scale-95`}
            title="Ordenar por fecha"
          >
            <Clock className="h-5 w-5" />
          </button>
          <button
            className="text-white/20 hover:text-blue-400/80 transition-all duration-300 hover:scale-110 active:scale-95"
            title="Dirección de orden"
          >
            <ArrowUpDown className="h-5 w-5" />
          </button>
        </div>
      </div>

      <div className="flex flex-wrap justify-center gap-2">
        <button
          onClick={() => setTag('ALL')}
          className={`rounded-full px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest transition-all ${tag === 'ALL'
            ? "bg-blue-500/20 text-blue-400 border border-blue-500/30"
            : "bg-white/5 text-white/40 border border-white/5 hover:bg-white/10 hover:text-white/60"
            }`}
        >
          TODOS
        </button>
        {tags.map((t) => (
          <button
            key={t}
            onClick={() => setTag(t)}
            className={`rounded-full px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest transition-all ${tag === t
              ? "bg-blue-500/20 text-blue-400 border border-blue-500/30"
              : "bg-white/5 text-white/40 border border-white/5 hover:bg-white/10 hover:text-white/60"
              }`}
          >
            {t}
          </button>
        ))}
      </div>
    </div>
  );
}
