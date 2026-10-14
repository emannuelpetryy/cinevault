import React, { useState, useEffect } from "react";
import { CatalogItem } from "@/types";
import { X, Trash2, Save } from "lucide-react";

interface EditModalProps {
  isOpen: boolean;
  onClose: () => void;
  item: CatalogItem | null;
  onSave: (item: CatalogItem) => void;
  onDelete: (id: string) => void;
}

const GENRE_LIST = [
  "Suspense & Mistério",
  "Thriller Psicológico",
  "Ficção Científica",
  "Drama",
  "Crime & Policial",
  "Terror",
  "Ação & Aventura",
  "Comédia",
  "Biografia & Histórico",
  "Romance",
  "Guerra",
  "Animação"
];

const PLATFORM_LIST = [
  "Netflix",
  "Max",
  "Prime Video",
  "Disney+",
  "Apple TV+",
  "Paramount+",
  "Outros"
];

export function EditModal({
  isOpen,
  onClose,
  item,
  onSave,
  onDelete,
}: EditModalProps) {
  const [formData, setFormData] = useState<Partial<CatalogItem>>({
    title: "",
    type: "movie",
    status: "queue",
    genre: "Drama",
    subgenre: "",
    platform: "Netflix",
    year: 2024,
    imdb: 8.0,
    rtCritics: 85,
    rtAudience: 85,
    note: "",
  });

  useEffect(() => {
    if (item) {
      setFormData(item);
    } else {
      setFormData({
        title: "",
        type: "movie",
        status: "queue",
        genre: "Drama",
        subgenre: "",
        platform: "Netflix",
        year: new Date().getFullYear(),
        imdb: null,
        rtCritics: null,
        rtAudience: null,
        note: "",
      });
    }
  }, [item, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.title?.trim()) return;

    onSave({
      id: item ? item.id : 'custom_' + Date.now(),
      title: formData.title.trim(),
      type: formData.type || 'movie',
      status: formData.status || 'queue',
      genre: formData.genre || 'Drama',
      subgenre: formData.subgenre?.trim() || '',
      origin: formData.origin || 'both',
      platform: formData.platform || 'Netflix',
      year: formData.year ? Number(formData.year) : null,
      imdb: formData.imdb !== null && formData.imdb !== undefined ? Number(formData.imdb) : null,
      rtCritics: formData.rtCritics !== null && formData.rtCritics !== undefined ? Number(formData.rtCritics) : null,
      rtAudience: formData.rtAudience !== null && formData.rtAudience !== undefined ? Number(formData.rtAudience) : null,
      note: formData.note?.trim() || '',
      rating: formData.rating || 0,
    });
    onClose();
  };

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-lg bg-[#0E1017] border border-white/[0.1] rounded-3xl shadow-2xl overflow-hidden flex flex-col text-white max-h-[90vh]"
      >
        {/* Header */}
        <div className="px-5 py-4 border-b border-white/[0.06] flex items-center justify-between">
          <h3 className="font-semibold text-sm">
            {item ? "Editar Obra" : "Nova Obra no Catálogo"}
          </h3>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4 overflow-y-auto no-scrollbar text-xs">
          <div>
            <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
              Título da Obra *
            </label>
            <input
              type="text"
              required
              value={formData.title || ""}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
              placeholder="Ex: Interestelar"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
                Formato
              </label>
              <select
                value={formData.type || "movie"}
                onChange={(e) => setFormData({ ...formData, type: e.target.value as any })}
                className="w-full px-3 py-2 rounded-xl bg-[#141722] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
              >
                <option value="movie">Filme</option>
                <option value="series">Série</option>
              </select>
            </div>

            <div>
              <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
                Status
              </label>
              <select
                value={formData.status || "queue"}
                onChange={(e) => setFormData({ ...formData, status: e.target.value as any })}
                className="w-full px-3 py-2 rounded-xl bg-[#141722] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
              >
                <option value="priority">Prioridade ★</option>
                <option value="queue">Na Fila ⏳</option>
                <option value="watched">Concluído ✓</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
                Gênero Principal
              </label>
              <select
                value={formData.genre || "Drama"}
                onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-[#141722] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
              >
                {GENRE_LIST.map((g) => (
                  <option key={g} value={g}>{g}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
                Plataforma de Streaming
              </label>
              <select
                value={formData.platform || "Netflix"}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                className="w-full px-3 py-2 rounded-xl bg-[#141722] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
              >
                {PLATFORM_LIST.map((p) => (
                  <option key={p} value={p}>{p}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
                Ano
              </label>
              <input
                type="number"
                value={formData.year || ""}
                onChange={(e) => setFormData({ ...formData, year: e.target.value ? parseInt(e.target.value) : null })}
                className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
                placeholder="2024"
              />
            </div>

            <div>
              <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
                IMDb (0-10)
              </label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="10"
                value={formData.imdb || ""}
                onChange={(e) => setFormData({ ...formData, imdb: e.target.value ? parseFloat(e.target.value) : null })}
                className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
                placeholder="8.2"
              />
            </div>

            <div>
              <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
                Rotten Crítica %
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={formData.rtCritics || ""}
                onChange={(e) => setFormData({ ...formData, rtCritics: e.target.value ? parseInt(e.target.value) : null })}
                className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
                placeholder="88"
              />
            </div>
          </div>

          <div>
            <label className="text-[11px] font-mono uppercase text-slate-400 block mb-1">
              Anotações Pessoais
            </label>
            <textarea
              rows={2}
              value={formData.note || ""}
              onChange={(e) => setFormData({ ...formData, note: e.target.value })}
              className="w-full px-3 py-2 rounded-xl bg-white/[0.04] border border-white/[0.08] text-white focus:outline-none focus:border-purple-500"
              placeholder="Ex: Recomendação do fulano, assistir no fim de semana..."
            />
          </div>

          {/* Action Buttons */}
          <div className="pt-3 border-t border-white/[0.06] flex items-center justify-between gap-3">
            {item && (
              <button
                type="button"
                onClick={() => {
                  if (confirm(`Remover "${item.title}" do catálogo?`)) {
                    onDelete(item.id);
                    onClose();
                  }
                }}
                className="px-3.5 py-2.5 rounded-xl border border-rose-500/30 text-rose-400 hover:bg-rose-500/10 flex items-center gap-1.5 transition text-xs"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Excluir</span>
              </button>
            )}

            <div className="flex items-center gap-2 ml-auto">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2.5 rounded-xl border border-white/[0.08] text-slate-400 hover:text-white text-xs transition"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition shadow-lg shadow-purple-600/20 flex items-center gap-1.5"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Salvar</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
