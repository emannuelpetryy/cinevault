import React from "react";
import { CatalogItem, MediaStatus } from "@/types";
import { cn, getPlatformBadgeClass } from "@/lib/utils";
import { StatusDropdown } from "./StatusDropdown";
import { ExternalLink, Check, Pencil, Trash2 } from "lucide-react";
import confetti from "canvas-confetti";

interface MovieCardProps {
  item: CatalogItem;
  onStatusChange: (id: string, newStatus: MediaStatus) => void;
  onEdit: (item: CatalogItem) => void;
  onDelete: (id: string) => void;
}

export function MovieCard({ item, onStatusChange, onEdit, onDelete }: MovieCardProps) {
  const isWatched = item.status === "watched";

  const handleMarkWatched = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!isWatched) {
      // Micro celebration confetti pop
      try {
        confetti({
          particleCount: 28,
          spread: 60,
          origin: {
            x: e.clientX / window.innerWidth,
            y: e.clientY / window.innerHeight,
          },
          colors: ['#10B981', '#34D399', '#6EE7B7'],
          ticks: 120,
          scalar: 0.8,
        });
      } catch (err) {}
      onStatusChange(item.id, "watched");
    } else {
      onStatusChange(item.id, "queue");
    }
  };

  const justWatchUrl = `https://www.justwatch.com/br/busca?q=${encodeURIComponent(item.title)}`;

  return (
    <div className="rounded-2xl p-4 flex flex-col justify-between group relative bg-[#0E1017] border border-white/[0.05] hover:border-white/[0.12] hover:bg-[#11131c] transition-all shadow-sm hover:shadow-lg">
      <div>
        {/* Top Header: Direct Status Dropdown + Platform Badge + Year */}
        <div className="flex items-center justify-between text-xs mb-2.5">
          <StatusDropdown
            status={item.status}
            onChange={(newStatus) => onStatusChange(item.id, newStatus)}
          />

          <div className="flex items-center gap-1.5 text-xs">
            <span className={cn("text-[10px] px-2 py-0.5 rounded-md font-medium tracking-wide", getPlatformBadgeClass(item.platform))}>
              {item.platform}
            </span>
            {item.year && (
              <span className="font-mono text-slate-500 text-[11px]">
                {item.year}
              </span>
            )}
          </div>
        </div>

        {/* Title & Info */}
        <div className="cursor-pointer" onClick={() => onEdit(item)}>
          <h3 className="font-semibold text-sm sm:text-base text-white group-hover:text-purple-300 transition-colors line-clamp-2 leading-snug">
            {item.title}
          </h3>

          <div className="flex items-center gap-2 mt-1 text-xs text-purple-300/80">
            <span>{item.genre}</span>
            {item.subgenre && (
              <>
                <span className="text-slate-700">·</span>
                <span className="text-slate-400 truncate max-w-[150px]">{item.subgenre}</span>
              </>
            )}
          </div>

          {/* Ratings: IMDb + Rotten Tomatoes Critics + Audience */}
          <div className="flex items-center gap-2.5 mt-2.5 text-xs text-slate-400">
            <span className="font-mono font-medium text-amber-400/90 inline-flex items-center gap-1">
              ★ {item.imdb ? item.imdb.toFixed(1) : '—'}
            </span>
            <span className="text-slate-700">·</span>
            <span className="font-mono text-rose-300/90 inline-flex items-center gap-1" title="Rotten Tomatoes Tomatometer (Crítica)">
              🍅 {item.rtCritics ? `${item.rtCritics}%` : '—'}
            </span>
            <span className="text-slate-700">·</span>
            <span className="font-mono text-amber-200/90 inline-flex items-center gap-1" title="Rotten Tomatoes Popcornmeter (Público)">
              🍿 {item.rtAudience ? `${item.rtAudience}%` : '—'}
            </span>
          </div>

          {/* Optional Note */}
          {item.note && (
            <p className="mt-2 text-[11px] text-slate-400/80 line-clamp-2 italic bg-white/[0.02] p-1.5 rounded-lg border border-white/[0.04]">
              "{item.note}"
            </p>
          )}
        </div>
      </div>

      {/* Bottom Action Bar */}
      <div className="mt-3.5 pt-2.5 border-t border-white/[0.04] flex items-center justify-between gap-2 text-xs">
        {/* 'Ver plataforma' Button (JustWatch direct search) */}
        <a
          href={justWatchUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="h-7 px-2.5 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] active:scale-95 border border-white/[0.08] text-slate-300 hover:text-white text-[11px] font-medium transition inline-flex items-center gap-1.5 shrink-0"
          title={`Ver onde assistir ${item.title} (${item.platform})`}
        >
          <span>Ver plataforma</span>
          <ExternalLink className="w-2.5 h-2.5 opacity-60" />
        </a>

        <div className="flex items-center gap-1.5 ml-auto">
          {/* 1-Click 'Visto' Button */}
          <button
            type="button"
            onClick={handleMarkWatched}
            className={cn(
              "h-7 px-2.5 rounded-lg text-[11px] font-semibold transition flex items-center gap-1 active:scale-95",
              !isWatched
                ? "bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/25"
                : "bg-emerald-600/20 text-emerald-300 border border-emerald-500/30"
            )}
            title={!isWatched ? "Marcar como Concluído em 1 clique" : "Já assistido (clique para voltar para a fila)"}
          >
            <Check className="w-3 h-3 text-emerald-400" />
            <span>{isWatched ? "Concluído" : "Visto"}</span>
          </button>

          {/* Edit */}
          <button
            type="button"
            onClick={() => onEdit(item)}
            className="h-7 w-7 rounded-lg bg-white/[0.03] hover:bg-white/[0.08] flex items-center justify-center text-slate-400 hover:text-white transition"
            title="Editar obra"
          >
            <Pencil className="w-3 h-3" />
          </button>

          {/* Delete */}
          <button
            type="button"
            onClick={() => onDelete(item.id)}
            className="h-7 w-7 rounded-lg bg-white/[0.03] hover:bg-rose-500/20 hover:text-rose-400 flex items-center justify-center text-slate-500 transition"
            title="Remover"
          >
            <Trash2 className="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  );
}
