"use client"

import React, { useState } from "react";
import { motion } from "framer-motion";
import { deleteNote, updateNote } from "@/lib/note-actions";
import { Note } from "@/types/note";

export function NoteCard({ note }: { note: Note }) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [content, setContent] = useState(note.contenido);
  const [tag, setTag] = useState(note.tag);

  const handleDelete = async () => {
    if (!confirm("¿Seguro que quieres borrar esta nota?")) return;
    setIsDeleting(true);
    await deleteNote(note.id);
  };

  const handleSave = async () => {
    setIsEditing(false);
    await updateNote(note.id, content, tag);
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: isDeleting ? 0 : 1, scale: isDeleting ? 0.9 : 1 }}
      className="group relative flex flex-col overflow-hidden rounded-xl bg-[#0a0a0a]/95 border border-blue-500/20 p-6 transition-all duration-500 hover:border-blue-400/40 hover:shadow-[0_0_40px_rgba(59,130,246,0.1)]"
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
        <span className="text-[11px] font-bold tracking-tight text-white/40">
          {new Date(note.created_at).toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' })}
        </span>
      </div>

      <div className="relative mb-4 px-2">
        {isEditing ? (
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full min-h-[100px] bg-white/5 rounded-xl p-4 text-[13px] leading-relaxed text-slate-300 outline-none border border-blue-500/20 focus:border-blue-500/50 transition-all"
          />
        ) : (
          <p className="text-[13px] leading-relaxed text-slate-400 transition-colors group-hover:text-slate-200">
            {note.contenido}
          </p>
        )}
      </div>

      <div className="flex justify-between items-center opacity-0 transition-opacity group-hover:opacity-100">
        <div className="h-px flex-1 bg-gradient-to-r from-blue-500/20 to-transparent" />
        <div className="flex gap-4 ml-4">
          {isEditing ? (
            <>
              <button onClick={handleSave} className="text-[10px] font-bold text-green-400 hover:text-green-300 uppercase tracking-widest">Guardar</button>
              <button onClick={() => setIsEditing(false)} className="text-[10px] font-bold text-slate-500 hover:text-slate-400 uppercase tracking-widest">Cancelar</button>
            </>
          ) : (
            <>
              <button onClick={() => setIsEditing(true)} className="text-[10px] font-bold text-blue-400/60 hover:text-blue-400 uppercase tracking-widest transition-colors">Editar</button>
              <button onClick={handleDelete} className="text-[10px] font-bold text-red-400/60 hover:text-red-400 uppercase tracking-widest transition-colors">Borrar</button>
            </>
          )}
        </div>
      </div>
    </motion.div>
  );
}
