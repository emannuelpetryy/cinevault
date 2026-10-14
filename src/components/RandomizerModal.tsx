import React, { useState } from "react";
import { CatalogItem } from "@/types";
import { Dices, X, ExternalLink, Sparkles } from "lucide-react";
import { cn, getPlatformBadgeClass } from "@/lib/utils";
import confetti from "canvas-confetti";

interface RandomizerModalProps {
  isOpen: boolean;
  onClose: () => void;
  catalog: CatalogItem[];
  onOpenEdit: (item: CatalogItem) => void;
}

export function RandomizerModal({
  isOpen,
  onClose,
  catalog,
  onOpenEdit,
}: RandomizerModalProps) {
  const [selected, setSelected] = useState<CatalogItem | null>(null);
  const [isRolling, setIsRolling] = useState(false);

  if (!isOpen) return null;

  const pool = catalog.filter((i) => i.status !== "watched");

  const roll = () => {
    if (pool.length === 0 || isRolling) return;
    setIsRolling(true);

    let count = 0;
    const interval = setInterval(() => {
      const random = pool[Math.floor(Math.random() * pool.length)];
      setSelected(random);
      count++;
      if (count >= 14) {
        clearInterval(interval);
        setIsRolling(false);
        try {
          confetti({
            particleCount: 35,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#A855F7', '#EC4899', '#3B82F6'],
          });
        } catch (e) {}
      }
    }, 60);
  };

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-md bg-[#0E1017] border border-white/[0.1] rounded-3xl p-6 shadow-2xl text-white relative overflow-hidden"
      >
        {/* Glow circle */}
        <div className="absolute -top-16 -right-16 w-32 h-32 bg-purple-600/20 rounded-full blur-2xl pointer-events-none" />

        <div className="flex items-center justify-between pb-3 border-b border-white/[0.06]">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
              <Dices className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-semibold text-sm">Sortear Obra</h3>
              <p className="text-[11px] text-slate-400">
                {pool.length} obras na sua fila
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Display Area */}
        <div className="py-8 text-center min-h-[160px] flex flex-col items-center justify-center">
          {selected ? (
            <div className="space-y-2 animate-fade-in">
              <span className={cn(
                "inline-block text-[10px] px-2.5 py-0.5 rounded-full font-medium mb-1",
                selected.status === 'priority' ? "bg-amber-500/20 text-amber-300 border border-amber-500/30" : "bg-white/[0.06] text-slate-300"
              )}>
                {selected.status === 'priority' ? '★ Prioridade' : '⏳ Na Fila'}
              </span>

              <h2 className="text-xl font-bold text-white tracking-tight leading-snug">
                {selected.title}
              </h2>

              <p className="text-xs text-purple-300">
                {selected.genre} {selected.year ? `· ${selected.year}` : ''}
              </p>

              <div className="flex items-center justify-center gap-2 pt-1 text-xs text-slate-400">
                <span className="font-mono text-amber-400 font-medium">★ {selected.imdb ? selected.imdb.toFixed(1) : '—'}</span>
                <span>·</span>
                <span className="font-mono text-rose-300">🍅 {selected.rtCritics ? `${selected.rtCritics}%` : '—'}</span>
                <span>·</span>
                <span className="font-mono text-amber-200">🍿 {selected.rtAudience ? `${selected.rtAudience}%` : '—'}</span>
              </div>

              <div className="pt-2">
                <span className={cn("text-[10px] px-2 py-0.5 rounded-md font-medium", getPlatformBadgeClass(selected.platform))}>
                  {selected.platform}
                </span>
              </div>
            </div>
          ) : (
            <div className="text-slate-500 space-y-1">
              <Sparkles className="w-8 h-8 mx-auto text-purple-400/50 mb-2" />
              <p className="text-xs">
                Toque no botão abaixo para escolher o filme da noite aleatoriamente!
              </p>
            </div>
          )}
        </div>

        {/* Action Button */}
        <div className="space-y-2 pt-2 border-t border-white/[0.06]">
          <button
            type="button"
            disabled={isRolling || pool.length === 0}
            onClick={roll}
            className="w-full py-3 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white font-semibold text-xs sm:text-sm transition shadow-lg shadow-purple-600/25 flex items-center justify-center gap-2 active:scale-95"
          >
            <Dices className="w-4 h-4" />
            <span>{isRolling ? "Sorteando..." : selected ? "Sortear Outro" : "Girar Roleta"}</span>
          </button>

          {selected && !isRolling && (
            <div className="flex gap-2">
              <a
                href={`https://www.justwatch.com/br/busca?q=${encodeURIComponent(selected.title)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 py-2 rounded-xl border border-white/[0.1] hover:bg-white/[0.05] text-xs font-medium text-slate-300 text-center flex items-center justify-center gap-1.5 transition"
              >
                <span>Ver plataforma</span>
                <ExternalLink className="w-3 h-3" />
              </a>
              <button
                type="button"
                onClick={() => {
                  onClose();
                  onOpenEdit(selected);
                }}
                className="px-4 py-2 rounded-xl border border-white/[0.1] hover:bg-white/[0.05] text-xs font-medium text-slate-300 transition"
              >
                Detalhes
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
