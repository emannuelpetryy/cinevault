import React, { useEffect, useState, useRef } from "react";
import { CatalogItem } from "@/types";
import { Search, X, Film, Tv, Star, ExternalLink } from "lucide-react";
import { cn, getPlatformBadgeClass } from "@/lib/utils";

interface CommandMenuProps {
  isOpen: boolean;
  onClose: () => void;
  catalog: CatalogItem[];
  onSelect: (item: CatalogItem) => void;
}

export function CommandMenu({ isOpen, onClose, catalog, onSelect }: CommandMenuProps) {
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery("");
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const q = query.trim().toLowerCase();
  const results = q
    ? catalog.filter(item => {
        return (
          item.title.toLowerCase().includes(q) ||
          item.genre.toLowerCase().includes(q) ||
          (item.subgenre && item.subgenre.toLowerCase().includes(q)) ||
          item.platform.toLowerCase().includes(q) ||
          (item.note && item.note.toLowerCase().includes(q)) ||
          (item.year && item.year.toString().includes(q))
        );
      }).slice(0, 8)
    : catalog.slice(0, 6);

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-start justify-center pt-16 sm:pt-24 px-4 animate-fade-in"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-xl bg-[#0E1017] border border-white/[0.1] rounded-2xl shadow-2xl overflow-hidden flex flex-col"
      >
        {/* Input Row */}
        <div className="flex items-center gap-3 px-4 py-3.5 border-b border-white/[0.08]">
          <Search className="w-4 h-4 text-slate-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Buscar por título, gênero, plataforma, ano..."
            className="flex-1 bg-transparent text-sm text-white placeholder-slate-500 focus:outline-none"
          />
          {query ? (
            <button
              onClick={() => setQuery("")}
              className="p-1 rounded-md text-slate-400 hover:text-white"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          ) : (
            <kbd className="hidden sm:inline-block px-2 py-0.5 text-[10px] font-mono text-slate-500 bg-white/[0.04] border border-white/[0.08] rounded">
              ESC
            </kbd>
          )}
        </div>

        {/* Results List */}
        <div className="p-2 max-h-[60vh] overflow-y-auto no-scrollbar space-y-1">
          {results.length === 0 ? (
            <div className="py-12 text-center text-slate-500 text-xs">
              Nenhuma obra encontrada para "{query}"
            </div>
          ) : (
            results.map((item) => {
              const isPriority = item.status === "priority";
              const isWatched = item.status === "watched";
              const dotColor = isPriority
                ? "bg-amber-400"
                : isWatched
                ? "bg-emerald-400"
                : "bg-slate-500";

              return (
                <div
                  key={item.id}
                  onClick={() => {
                    onSelect(item);
                    onClose();
                  }}
                  className="p-3 rounded-xl hover:bg-white/[0.04] transition flex items-center justify-between gap-3 cursor-pointer group"
                >
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span className={cn("w-1.5 h-1.5 rounded-full shrink-0", dotColor)} />
                      <h4 className="font-medium text-xs sm:text-sm text-white truncate group-hover:text-purple-300 transition-colors">
                        {item.title}
                      </h4>
                      {item.year && (
                        <span className="font-mono text-[11px] text-slate-500">
                          ({item.year})
                        </span>
                      )}
                      <span className={cn("text-[9px] px-1.5 py-0.2 rounded font-medium", getPlatformBadgeClass(item.platform))}>
                        {item.platform}
                      </span>
                    </div>

                    <div className="flex items-center gap-2 text-[11px] text-slate-400 pl-3.5 mt-0.5">
                      <span className="text-purple-300/80">{item.genre}</span>
                      <span className="text-slate-700">·</span>
                      <span className="font-mono text-amber-400">★ {item.imdb ? item.imdb.toFixed(1) : '—'}</span>
                      <span className="font-mono text-rose-300">🍅 {item.rtCritics ? `${item.rtCritics}%` : '—'}</span>
                    </div>
                  </div>

                  <a
                    href={`https://www.justwatch.com/br/busca?q=${encodeURIComponent(item.title)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="p-2 rounded-lg bg-white/[0.03] hover:bg-white/[0.08] text-slate-400 hover:text-white transition"
                    title="Ver plataforma"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
