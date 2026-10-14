import React from "react";
import { Drawer } from "vaul";
import { AppState, CatalogItem } from "@/types";
import { cn } from "@/lib/utils";
import { SlidersHorizontal, X, RotateCcw } from "lucide-react";

interface FilterDrawerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  state: AppState;
  setState: React.Dispatch<React.SetStateAction<AppState>>;
  onReset: () => void;
  matchCount: number;
}

const GENRES = [
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

const PLATFORMS = [
  "Netflix",
  "Max",
  "Prime Video",
  "Disney+",
  "Apple TV+",
  "Paramount+"
];

export function FilterDrawer({
  open,
  onOpenChange,
  state,
  setState,
  onReset,
  matchCount,
}: FilterDrawerProps) {
  return (
    <Drawer.Root open={open} onOpenChange={onOpenChange}>
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 transition-opacity" />
        <Drawer.Content className="bg-[#0E1017] border-t border-white/[0.1] flex flex-col rounded-t-[28px] max-h-[90vh] fixed bottom-0 left-0 right-0 z-50 outline-none text-white shadow-2xl">
          {/* Drag Handle Bar */}
          <div className="p-3 bg-transparent rounded-t-[28px] flex-shrink-0 cursor-grab active:cursor-grabbing">
            <div className="w-12 h-1.5 bg-white/20 rounded-full mx-auto" />
          </div>

          {/* Header */}
          <div className="px-5 pb-3 border-b border-white/[0.06] flex items-center justify-between">
            <div className="flex items-center gap-2">
              <SlidersHorizontal className="w-4 h-4 text-purple-400" />
              <Drawer.Title className="text-sm font-semibold text-white">
                Filtros Avançados
              </Drawer.Title>
            </div>
            <button
              type="button"
              onClick={() => onOpenChange(false)}
              className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Scrollable Filters Content */}
          <div className="p-5 overflow-y-auto space-y-5 no-scrollbar text-xs">
            {/* Formato */}
            <div>
              <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                Formato
              </label>
              <div className="flex flex-wrap gap-1.5">
                {[
                  { value: 'all', label: 'Tudo' },
                  { value: 'movie', label: '🎬 Filmes' },
                  { value: 'series', label: '📺 Séries' },
                ].map((f) => (
                  <button
                    key={f.value}
                    type="button"
                    onClick={() => setState(prev => ({ ...prev, type: f.value as any }))}
                    className={cn(
                      "px-3 py-1.5 rounded-lg border text-xs font-medium transition",
                      state.type === f.value
                        ? "bg-purple-600/30 border-purple-500/50 text-purple-200"
                        : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                    )}
                  >
                    {f.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Status */}
            <div>
              <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                Status
              </label>
              <div className="flex flex-wrap gap-1.5">
                {[
                  { value: 'all', label: 'Todos' },
                  { value: 'priority', label: 'Prioridade ★', color: 'text-amber-300' },
                  { value: 'queue', label: 'Na Fila ⏳' },
                  { value: 'watched', label: 'Concluídos ✓', color: 'text-emerald-400' },
                ].map((s) => (
                  <button
                    key={s.value}
                    type="button"
                    onClick={() => setState(prev => ({ ...prev, status: s.value as any }))}
                    className={cn(
                      "px-3 py-1.5 rounded-lg border text-xs font-medium transition",
                      s.color,
                      state.status === s.value
                        ? "bg-purple-600/30 border-purple-500/50 text-white"
                        : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                    )}
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Gênero */}
            <div>
              <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                Gênero
              </label>
              <div className="flex flex-wrap gap-1.5">
                <button
                  type="button"
                  onClick={() => setState(prev => ({ ...prev, genre: 'all' }))}
                  className={cn(
                    "px-2.5 py-1.5 rounded-lg border text-xs transition",
                    state.genre === 'all'
                      ? "bg-purple-600/30 border-purple-500/50 text-purple-200"
                      : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                  )}
                >
                  Todos os Gêneros
                </button>
                {GENRES.map((g) => (
                  <button
                    key={g}
                    type="button"
                    onClick={() => setState(prev => ({ ...prev, genre: g }))}
                    className={cn(
                      "px-2.5 py-1.5 rounded-lg border text-xs transition",
                      state.genre === g
                        ? "bg-purple-600/30 border-purple-500/50 text-purple-200"
                        : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                    )}
                  >
                    {g}
                  </button>
                ))}
              </div>
            </div>

            {/* Plataforma de Streaming */}
            <div>
              <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                Plataforma de Streaming (Brasil)
              </label>
              <div className="flex flex-wrap gap-1.5">
                <button
                  type="button"
                  onClick={() => setState(prev => ({ ...prev, platform: 'all' }))}
                  className={cn(
                    "px-2.5 py-1.5 rounded-lg border text-xs transition",
                    state.platform === 'all'
                      ? "bg-blue-600/30 border-blue-500/50 text-blue-200"
                      : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                  )}
                >
                  Todas
                </button>
                {PLATFORMS.map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => setState(prev => ({ ...prev, platform: p }))}
                    className={cn(
                      "px-2.5 py-1.5 rounded-lg border text-xs transition",
                      state.platform === p
                        ? "bg-blue-600/30 border-blue-500/50 text-white"
                        : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                    )}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            {/* Notas Mínimas */}
            <div>
              <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                Nota Mínima IMDb
              </label>
              <div className="flex flex-wrap gap-1.5">
                {[
                  { value: 0, label: 'Qualquer nota' },
                  { value: 7.0, label: '★ 7.0+' },
                  { value: 7.5, label: '★ 7.5+' },
                  { value: 8.0, label: '★ 8.0+ (Obras-Primas)' },
                  { value: 8.5, label: '★ 8.5+' },
                ].map((score) => (
                  <button
                    key={score.value}
                    type="button"
                    onClick={() => setState(prev => ({ ...prev, minImdb: score.value }))}
                    className={cn(
                      "px-2.5 py-1.5 rounded-lg border font-mono text-xs transition",
                      state.minImdb === score.value
                        ? "bg-amber-500/30 border-amber-500/60 text-amber-200 font-semibold"
                        : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                    )}
                  >
                    {score.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Rotten Tomatoes */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                  Rotten Tomatoes (Crítica)
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    { value: 'all', label: 'Todas' },
                    { value: '80', label: '🍅 80%+ Crítica' },
                    { value: '90', label: '🍅 90%+ Top' },
                  ].map((r) => (
                    <button
                      key={r.value}
                      type="button"
                      onClick={() => setState(prev => ({ ...prev, rtCritics: r.value }))}
                      className={cn(
                        "px-2.5 py-1.5 rounded-lg border font-mono text-xs transition",
                        state.rtCritics === r.value
                          ? "bg-rose-500/30 border-rose-500/60 text-rose-200 font-semibold"
                          : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                      )}
                    >
                      {r.label}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                  Rotten Tomatoes (Público)
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    { value: 'all', label: 'Todas' },
                    { value: '85', label: '🍿 85%+ Público' },
                  ].map((r) => (
                    <button
                      key={r.value}
                      type="button"
                      onClick={() => setState(prev => ({ ...prev, rtAudience: r.value }))}
                      className={cn(
                        "px-2.5 py-1.5 rounded-lg border font-mono text-xs transition",
                        state.rtAudience === r.value
                          ? "bg-amber-400/30 border-amber-400/60 text-amber-200 font-semibold"
                          : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                      )}
                    >
                      {r.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Década */}
            <div>
              <label className="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">
                Época / Década
              </label>
              <div className="flex flex-wrap gap-1.5">
                {[
                  { value: 'all', label: 'Todas as décadas' },
                  { value: '2020s', label: 'Anos 2020' },
                  { value: '2010s', label: 'Anos 2010' },
                  { value: 'classic', label: 'Anteriores a 2010' },
                ].map((dec) => (
                  <button
                    key={dec.value}
                    type="button"
                    onClick={() => setState(prev => ({ ...prev, decade: dec.value }))}
                    className={cn(
                      "px-2.5 py-1.5 rounded-lg border text-xs transition",
                      state.decade === dec.value
                        ? "bg-purple-600/30 border-purple-500/50 text-purple-200"
                        : "bg-white/[0.02] border-white/[0.06] text-slate-400 hover:text-white"
                    )}
                  >
                    {dec.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Footer Actions */}
          <div className="p-4 border-t border-white/[0.08] bg-[#0A0C12] flex items-center justify-between gap-3">
            <button
              type="button"
              onClick={onReset}
              className="px-3.5 py-2 rounded-xl border border-white/[0.1] text-xs font-medium text-slate-400 hover:text-white hover:bg-white/[0.05] flex items-center gap-1.5 transition active:scale-95"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Limpar</span>
            </button>

            <button
              type="button"
              onClick={() => onOpenChange(false)}
              className="flex-1 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition shadow-lg shadow-purple-600/20 active:scale-95 flex items-center justify-center gap-1.5"
            >
              <span>Ver {matchCount} {matchCount === 1 ? 'Título' : 'Títulos'}</span>
            </button>
          </div>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}
