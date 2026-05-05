"use client"

import React, { useState } from "react";
import { motion } from "framer-motion";
import { deleteNote, updateNote } from "@/lib/note-actions";
import { Note } from "@/types/note";
import ReactMarkdown from "react-markdown";
import { AnimatePresence } from "framer-motion";
import { X, Maximize2 } from "lucide-react";

export function NoteCard({ note }: { note: Note }) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(note.titulo);
  const [content, setContent] = useState(note.contenido);
  const [tag, setTag] = useState(note.tag);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleDelete = async () => {
    if (!confirm("¿Seguro que quieres borrar esta nota?")) return;
    setIsDeleting(true);
    await deleteNote(note.id);
  };

  const handleSave = async () => {
    setIsEditing(false);
    await updateNote(note.id, title, content, tag);
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: isDeleting ? 0 : 1, scale: isDeleting ? 0.9 : 1 }}
      className="group relative flex h-[480px] flex-col overflow-hidden rounded-xl bg-[#0a0a0a] border border-blue-500/20 p-6 transition-all duration-500 hover:border-blue-400/40 hover:shadow-[0_0_40px_rgba(59,130,246,0.1)]"
    >
      <div className="absolute top-0 left-0 h-4 w-4 border-l-[1px] border-t-[1px] border-blue-400/40 transition-all duration-500 group-hover:h-6 group-hover:w-6 group-hover:border-blue-400" />
      <div className="absolute top-0 right-0 h-4 w-4 border-r-[1px] border-t-[1px] border-blue-400/40 transition-all duration-500 group-hover:h-6 group-hover:w-6 group-hover:border-blue-400" />
      <div className="absolute bottom-0 left-0 h-4 w-4 border-l-[1px] border-b-[1px] border-blue-400/40 transition-all duration-500 group-hover:h-6 group-hover:w-6 group-hover:border-blue-400" />
      <div className="absolute bottom-0 right-0 h-4 w-4 border-r-[1px] border-b-[1px] border-blue-400/40 transition-all duration-500 group-hover:h-6 group-hover:w-6 group-hover:border-blue-400" />

      <div className="mb-6 flex items-center justify-between px-2">
        <div className="flex items-center gap-3">
          <span className="text-[11px] font-black tracking-widest text-blue-400">
            {note.id} —
          </span>
          {isEditing ? (
            <input
              value={tag}
              onChange={(e) => setTag(e.target.value)}
              className="bg-transparent text-[11px] font-black uppercase tracking-widest text-white outline-none border-b border-blue-500/50"
            />
          ) : (
            <span className="text-[11px] font-black uppercase tracking-widest text-white/90">
              {note.tag}
            </span>
          )}
        </div>
        <span className="text-[13px] font-black tracking-tight text-white">
          {new Date(note.created_at).toLocaleDateString('es-CL', { day: '2-digit', month: '2-digit', year: 'numeric' })}
        </span>
      </div>

      <div className="relative mb-4 px-2">
        {isEditing ? (
          <div className="flex flex-col gap-4">
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Título de la nota..."
              className="w-full bg-white/5 rounded-lg px-4 py-2.5 text-[15px] font-black text-white outline-none border border-blue-500/20 focus:border-blue-500/50 transition-all"
            />
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="w-full h-[280px] bg-white/5 rounded-xl p-4 text-[13px] leading-relaxed text-slate-300 outline-none border border-blue-500/20 focus:border-blue-500/50 transition-all resize-none scrollbar-thin scrollbar-thumb-blue-500/20 scrollbar-track-transparent"
            />
          </div>
        ) : (
          <div className="relative flex-1 !bg-transparent !shadow-none !border-none overflow-hidden">
            <h3 
              className="mb-2 text-3xl font-black leading-[0.9] tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-white via-blue-50 to-blue-400 group-hover:via-blue-300 transition-all duration-700"
              style={{ textShadow: '0 0 25px rgba(59,130,246,0.2), 0 0 50px rgba(59,130,246,0.1)' }}
            >
              {note.titulo}
            </h3>
            <div className="markdown-content !bg-transparent text-slate-300 transition-colors group-hover:text-slate-100 max-h-[220px] overflow-hidden">
              <ReactMarkdown>{note.contenido}</ReactMarkdown>
              {note.contenido.length > 200 && (
                <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-[#0a0a0a] to-transparent pointer-events-none" />
              )}
            </div>
            {note.contenido.length > 200 && (
              <button 
                onClick={() => setIsModalOpen(true)}
                className="relative z-10 mt-4 flex items-center gap-2 rounded-lg border border-blue-500/30 bg-blue-500/5 px-3 py-1.5 text-[10px] font-bold text-blue-400 transition-all hover:bg-blue-500/20 hover:text-blue-300 uppercase tracking-widest"
              >
                <Maximize2 size={12} /> Leer nota completa
              </button>
            )}
          </div>
        )}
      </div>

      <AnimatePresence>
        {isModalOpen && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsModalOpen(false)}
              className="absolute inset-0 bg-black/80 backdrop-blur-md"
            />
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              className="relative flex w-full max-w-3xl max-h-[85vh] flex-col overflow-hidden rounded-[2rem] border border-blue-500/30 bg-[#0a0a0a] shadow-2xl"
            >
              <div className="flex shrink-0 items-center justify-between border-b border-white/5 px-8 py-6">
                <div className="flex items-center gap-3">
                  <span className="text-[11px] font-black tracking-widest text-blue-400">#{note.id}</span>
                  <span className="text-[11px] font-black uppercase tracking-widest text-white/90">{note.tag}</span>
                </div>
                <button 
                  onClick={() => setIsModalOpen(false)}
                  className="rounded-full bg-white/5 p-2 text-slate-400 transition-colors hover:bg-white/10 hover:text-white"
                >
                  <X size={20} />
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-8 sm:p-12 scrollbar-thin scrollbar-thumb-blue-500/20 scrollbar-track-transparent">
                <h2 
                  className="mb-6 text-4xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-white to-blue-400"
                  style={{ textShadow: '0 0 30px rgba(59,130,246,0.3)' }}
                >
                  {note.titulo}
                </h2>
                <div className="markdown-content prose-invert">
                  <ReactMarkdown>{note.contenido}</ReactMarkdown>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      <div className="flex items-center justify-between opacity-0 transition-all duration-300 group-hover:opacity-100">
        <div className="h-px flex-1 bg-gradient-to-r from-blue-500/30 to-transparent" />
        <div className="ml-4 flex gap-6">
          {isEditing ? (
            <>
              <button onClick={handleSave} className="relative z-10 text-[10px] font-black tracking-widest text-blue-400 hover:text-blue-300 uppercase transition-colors">Guardar</button>
              <button onClick={() => setIsEditing(false)} className="relative z-10 text-[10px] font-black tracking-widest text-slate-500 hover:text-slate-400 uppercase transition-colors">Cancelar</button>
            </>
          ) : (
            <>
              <button onClick={() => setIsEditing(true)} className="relative z-10 text-[10px] font-black tracking-widest text-blue-400 hover:text-blue-300 uppercase transition-colors">Editar</button>
              <button onClick={handleDelete} className="relative z-10 text-[10px] font-black tracking-widest text-red-500/80 hover:text-red-400 uppercase transition-colors">Borrar</button>
            </>
          )}
        </div>
      </div>
    </motion.div>
  );
}
