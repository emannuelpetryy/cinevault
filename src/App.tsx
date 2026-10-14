import React, { useState, useEffect, useMemo } from "react";
import { CatalogItem, AppState, MediaStatus } from "@/types";
import { INITIAL_CATALOG } from "@/data/initialCatalog";
import { Header } from "@/components/Header";
import { AppleMailTabs } from "@/components/AppleMailTabs";
import { MovieCard } from "@/components/MovieCard";
import { FilterDrawer } from "@/components/FilterDrawer";
import { CommandMenu } from "@/components/CommandMenu";
import { WizardConcierge } from "@/components/WizardConcierge";
import { RandomizerModal } from "@/components/RandomizerModal";
import { EditModal } from "@/components/EditModal";
import { ExportModal } from "@/components/ExportModal";
import { BottomNav } from "@/components/BottomNav";
import { Film, Tv, Sparkles, Star, Clock, Check, RotateCcw, X, ExternalLink } from "lucide-react";
import { cn, getPlatformBadgeClass } from "@/lib/utils";

const STORAGE_KEY = "cinevault_catalog_v2";
const LEGACY_KEYS = ["cinevault_catalog", "cinevault_catalog_v1"];

const GENRES_LIST = [
  "Todos",
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

export function App() {
  // Load Catalog from localStorage or fallback to INITIAL_CATALOG
  const [catalog, setCatalog] = useState<CatalogItem[]>(() => {
    try {
      let raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        for (const k of LEGACY_KEYS) {
          const leg = localStorage.getItem(k);
          if (leg) { raw = leg; break; }
        }
      }
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length > 0) {
          // Merge user saved state with initial catalog metadata
          const setIds = new Set(parsed.map((p: any) => p.id));
          const merged = parsed.map((item: any) => {
            const init: Partial<CatalogItem> = INITIAL_CATALOG.find(i => i.id === item.id) || {};
            return {
              ...init,
              ...item,
              genre: init.genre || item.genre || 'Drama',
              platform: init.platform || item.platform || 'Netflix',
              year: item.year || init.year || null,
              imdb: item.imdb !== undefined ? item.imdb : (init.imdb ?? null),
              rtCritics: item.rtCritics !== undefined ? item.rtCritics : (init.rtCritics ?? null),
              rtAudience: item.rtAudience !== undefined ? item.rtAudience : (init.rtAudience ?? null),
            };
          });
          for (const it of INITIAL_CATALOG) {
            if (!setIds.has(it.id)) merged.push(it);
          }
          return merged;
        }
      }
    } catch (e) {}
    return INITIAL_CATALOG;
  });

  // Persist Catalog
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(catalog));
    } catch (e) {}
  }, [catalog]);

  // App Filter State
  const [state, setState] = useState<AppState>({
    search: "",
    type: "all",
    status: "all",
    genre: "all",
    platform: "all",
    minImdb: 0,
    rtCritics: "all",
    rtAudience: "all",
    decade: "all",
    sort: "status",
    view: "grid",
    wizardOpen: false,
  });

  // Modals state
  const [filterDrawerOpen, setFilterDrawerOpen] = useState(false);
  const [commandMenuOpen, setCommandMenuOpen] = useState(false);
  const [randomizerOpen, setRandomizerOpen] = useState(false);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [exportModalOpen, setExportModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<CatalogItem | null>(null);

  // Toast state
  const [toast, setToast] = useState<string | null>(null);
  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 2400);
  };

  // Keyboard shortcut for Command Menu
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "/" && document.activeElement?.tagName !== "INPUT" && document.activeElement?.tagName !== "TEXTAREA") {
        e.preventDefault();
        setCommandMenuOpen(true);
      }
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setCommandMenuOpen(true);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Filter & Sort Calculation
  const filteredCatalog = useMemo(() => {
    const q = state.search.trim().toLowerCase();

    return catalog
      .filter((item) => {
        // Formato
        if (state.type !== "all" && item.type !== state.type) return false;

        // Status
        if (state.status !== "all" && item.status !== state.status) return false;

        // Gênero
        if (state.genre !== "all" && item.genre !== state.genre) return false;

        // Plataforma
        if (state.platform !== "all" && item.platform !== state.platform) return false;

        // IMDb
        if (state.minImdb > 0 && (!item.imdb || item.imdb < state.minImdb)) return false;

        // Rotten Tomatoes Crítica
        if (state.rtCritics !== "all" && (!item.rtCritics || item.rtCritics < parseInt(state.rtCritics))) return false;

        // Rotten Tomatoes Público
        if (state.rtAudience !== "all" && (!item.rtAudience || item.rtAudience < parseInt(state.rtAudience))) return false;

        // Década
        if (state.decade !== "all") {
          const yr = item.year || 0;
          if (state.decade === "2020s" && yr < 2020) return false;
          if (state.decade === "2010s" && (yr < 2010 || yr >= 2020)) return false;
          if (state.decade === "classic" && yr >= 2010) return false;
        }

        // Busca textual
        if (q) {
          const matches =
            item.title.toLowerCase().includes(q) ||
            item.genre.toLowerCase().includes(q) ||
            (item.subgenre && item.subgenre.toLowerCase().includes(q)) ||
            item.platform.toLowerCase().includes(q) ||
            (item.note && item.note.toLowerCase().includes(q)) ||
            (item.year && item.year.toString().includes(q));
          if (!matches) return false;
        }

        return true;
      })
      .sort((a, b) => {
        if (state.sort === "title") return a.title.localeCompare(b.title);
        if (state.sort === "imdb") return (b.imdb || 0) - (a.imdb || 0);
        if (state.sort === "year") return (b.year || 0) - (a.year || 0);

        // Default sort: priority -> queue -> watched
        const score = (status: MediaStatus) => (status === "priority" ? 3 : status === "queue" ? 2 : 1);
        if (score(a.status) !== score(b.status)) {
          return score(b.status) - score(a.status);
        }
        return a.title.localeCompare(b.title);
      });
  }, [catalog, state]);

  // Active filter count
  const activeFilterCount = useMemo(() => {
    let count = 0;
    if (state.search) count++;
    if (state.type !== "all") count++;
    if (state.status !== "all") count++;
    if (state.genre !== "all") count++;
    if (state.platform !== "all") count++;
    if (state.minImdb > 0) count++;
    if (state.rtCritics !== "all") count++;
    if (state.rtAudience !== "all") count++;
    if (state.decade !== "all") count++;
    return count;
  }, [state]);

  const resetAllFilters = () => {
    setState((prev) => ({
      ...prev,
      search: "",
      type: "all",
      status: "all",
      genre: "all",
      platform: "all",
      minImdb: 0,
      rtCritics: "all",
      rtAudience: "all",
      decade: "all",
    }));
    showToast("Filtros redefinidos");
  };

  const handleStatusChange = (id: string, newStatus: MediaStatus) => {
    setCatalog((prev) =>
      prev.map((item) => (item.id === id ? { ...item, status: newStatus } : item))
    );
    const labels = {
      priority: "marcado como Prioridade ★",
      queue: "colocado Na Fila ⏳",
      watched: "marcado como Concluído! 🎉",
    };
    const it = catalog.find((i) => i.id === id);
    if (it) showToast(`"${it.title}" ${labels[newStatus]}`);
  };

  const handleSaveItem = (item: CatalogItem) => {
    setCatalog((prev) => {
      const exists = prev.some((i) => i.id === item.id);
      if (exists) {
        return prev.map((i) => (i.id === item.id ? item : i));
      }
      return [item, ...prev];
    });
    showToast(`"${item.title}" salvo com sucesso`);
  };

  const handleDeleteItem = (id: string) => {
    const it = catalog.find((i) => i.id === id);
    setCatalog((prev) => prev.filter((i) => i.id !== id));
    if (it) showToast(`"${it.title}" removido`);
  };

  // Counts for tabs
  const totalCount = catalog.length;
  const watchedCount = catalog.filter((i) => i.status === "watched").length;
  const priorityCount = catalog.filter((i) => i.status === "priority").length;
  const queueCount = catalog.filter((i) => i.status === "queue").length;
  const moviesCount = catalog.filter((i) => i.type === "movie").length;
  const seriesCount = catalog.filter((i) => i.type === "series").length;

  return (
    <div className="min-h-screen bg-[#090A0F] text-slate-100 flex flex-col font-sans pb-20 lg:pb-10 selection:bg-purple-600 selection:text-white">
      {/* Header */}
      <Header
        state={state}
        setState={setState}
        onOpenWizard={() => setState(prev => ({ ...prev, wizardOpen: true }))}
        onOpenFilters={() => setFilterDrawerOpen(true)}
        onOpenRandomizer={() => setRandomizerOpen(true)}
        onOpenSearch={() => setCommandMenuOpen(true)}
        onOpenAdd={() => {
          setEditingItem(null);
          setEditModalOpen(true);
        }}
        onOpenExport={() => setExportModalOpen(true)}
        activeFilterCount={activeFilterCount}
        totalCount={totalCount}
        watchedCount={watchedCount}
      />

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex-1 w-full space-y-4">
        {/* Navigation Section: Format Tabs + Status Tabs (Apple Mail Tabs by Skecher UI) */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pb-1 border-b border-white/[0.04]">
          {/* Formato: Tudo / Filmes / Séries */}
          <AppleMailTabs
            value={state.type}
            onValueChange={(val) => setState(prev => ({ ...prev, type: val }))}
            tabs={[
              { value: 'all', label: 'Tudo', count: totalCount, icon: Sparkles },
              { value: 'movie', label: 'Filmes', count: moviesCount, icon: Film, activeClassName: 'bg-purple-600 text-white' },
              { value: 'series', label: 'Séries', count: seriesCount, icon: Tv, activeClassName: 'bg-indigo-600 text-white' },
            ]}
          />

          {/* Status: Todos / Prioridades / Na Fila / Concluídos */}
          <AppleMailTabs
            value={state.status}
            onValueChange={(val) => setState(prev => ({ ...prev, status: val }))}
            tabs={[
              { value: 'all', label: 'Todos os Status' },
              { value: 'priority', label: 'Prioridades', count: priorityCount, icon: Star, activeClassName: 'bg-amber-500 text-black font-semibold' },
              { value: 'queue', label: 'Na Fila', count: queueCount, icon: Clock, activeClassName: 'bg-slate-700 text-white' },
              { value: 'watched', label: 'Concluídos', count: watchedCount, icon: Check, activeClassName: 'bg-emerald-600 text-white' },
            ]}
          />
        </div>

        {/* Horizontal Genre Selector Strip */}
        <div className="py-1 flex items-center gap-1.5 overflow-x-auto no-scrollbar -mx-1 px-1 text-xs">
          {GENRES_LIST.map((genre) => {
            const isAll = genre === "Todos";
            const val = isAll ? "all" : genre;
            const isSelected = state.genre === val;
            return (
              <button
                key={genre}
                type="button"
                onClick={() => setState(prev => ({ ...prev, genre: val }))}
                className={cn(
                  "px-3 py-1.5 rounded-xl whitespace-nowrap text-xs font-medium transition active:scale-95 border",
                  isSelected
                    ? "bg-purple-600/30 border-purple-500/60 text-purple-200 shadow-sm"
                    : "bg-white/[0.02] border-white/[0.05] text-slate-400 hover:text-white hover:bg-white/[0.05]"
                )}
              >
                {genre}
              </button>
            );
          })}
        </div>

        {/* Unified Concierge Active Filters Banner */}
        {activeFilterCount > 0 && (
          <div className="p-3.5 rounded-2xl bg-purple-950/20 border border-purple-500/25 flex flex-wrap items-center justify-between gap-3 text-xs animate-fade-in shadow-sm">
            <div className="flex flex-wrap items-center gap-1.5 min-w-0">
              <span className="text-purple-300 font-semibold mr-1 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-purple-400" />
                Filtros ativos ({filteredCatalog.length} obras):
              </span>

              {state.type !== "all" && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-white/[0.08] text-slate-200 border border-white/10 font-medium">
                  <span>{state.type === "movie" ? "🎬 Filmes" : "📺 Séries"}</span>
                  <button onClick={() => setState(prev => ({ ...prev, type: "all" }))} className="hover:text-purple-300">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {state.status !== "all" && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-white/[0.08] text-slate-200 border border-white/10 font-medium">
                  <span>Status: {state.status === "priority" ? "Prioridade ★" : state.status === "watched" ? "Concluído ✓" : "Na Fila ⏳"}</span>
                  <button onClick={() => setState(prev => ({ ...prev, status: "all" }))} className="hover:text-purple-300">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {state.genre !== "all" && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-purple-600/30 text-purple-200 border border-purple-500/40 font-medium">
                  <span>{state.genre}</span>
                  <button onClick={() => setState(prev => ({ ...prev, genre: "all" }))} className="hover:text-white">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {state.platform !== "all" && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-blue-600/30 text-blue-200 border border-blue-500/40 font-medium">
                  <span>{state.platform}</span>
                  <button onClick={() => setState(prev => ({ ...prev, platform: "all" }))} className="hover:text-white">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {state.minImdb > 0 && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/30 font-medium font-mono">
                  <span>IMDb {state.minImdb}+</span>
                  <button onClick={() => setState(prev => ({ ...prev, minImdb: 0 }))} className="hover:text-white">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {state.rtCritics !== "all" && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-rose-500/20 text-rose-300 border border-rose-500/30 font-medium font-mono">
                  <span>🍅 {state.rtCritics}%+ Crítica</span>
                  <button onClick={() => setState(prev => ({ ...prev, rtCritics: "all" }))} className="hover:text-white">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {state.rtAudience !== "all" && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-400/20 text-amber-200 border border-amber-400/30 font-medium font-mono">
                  <span>🍿 {state.rtAudience}%+ Público</span>
                  <button onClick={() => setState(prev => ({ ...prev, rtAudience: "all" }))} className="hover:text-white">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {state.search && (
                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-white/[0.08] text-slate-200 border border-white/10 font-medium">
                  <span>"{state.search}"</span>
                  <button onClick={() => setState(prev => ({ ...prev, search: "" }))} className="hover:text-white">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}
            </div>

            {/* Banner Buttons */}
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setState(prev => ({ ...prev, wizardOpen: true }))}
                className="px-3 py-1.5 rounded-lg bg-purple-600/30 hover:bg-purple-600/40 text-purple-200 font-medium text-xs transition active:scale-95"
              >
                Refazer etapas ↺
              </button>
              <button
                type="button"
                onClick={resetAllFilters}
                className="px-3 py-1.5 rounded-lg bg-white/[0.06] hover:bg-white/[0.1] text-slate-300 hover:text-white font-medium text-xs transition active:scale-95"
              >
                Ver tudo tranquilo ✕
              </button>
            </div>
          </div>
        )}

        {/* Catalog Grid View or Table View */}
        {filteredCatalog.length === 0 ? (
          <div className="py-20 text-center space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-white/[0.03] border border-white/[0.06] flex items-center justify-center mx-auto text-slate-500">
              <Film className="w-6 h-6" />
            </div>
            <h3 className="font-semibold text-base text-white">Nenhuma obra encontrada</h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto">
              Nenhum filme ou série coincide com a combinação atual de filtros.
            </p>
            <button
              type="button"
              onClick={resetAllFilters}
              className="mt-2 px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition active:scale-95 shadow-md shadow-purple-600/20"
            >
              Limpar todos os filtros
            </button>
          </div>
        ) : state.view === "grid" ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3.5">
            {filteredCatalog.map((item) => (
              <MovieCard
                key={item.id}
                item={item}
                onStatusChange={handleStatusChange}
                onEdit={(it) => {
                  setEditingItem(it);
                  setEditModalOpen(true);
                }}
                onDelete={handleDeleteItem}
              />
            ))}
          </div>
        ) : (
          <div className="rounded-2xl border border-white/[0.06] bg-[#0E1017] overflow-hidden divide-y divide-white/[0.04]">
            {filteredCatalog.map((item) => {
              const isWatched = item.status === "watched";
              const isPriority = item.status === "priority";
              const dotColor = isPriority
                ? "bg-amber-400 shadow-[0_0_6px_#F59E0B]"
                : isWatched
                ? "bg-emerald-400 shadow-[0_0_6px_#10B981]"
                : "bg-slate-500";

              return (
                <div
                  key={item.id}
                  className="p-3.5 sm:px-4 flex items-center justify-between gap-3 hover:bg-white/[0.02] transition"
                >
                  <div
                    className="min-w-0 flex-1 cursor-pointer"
                    onClick={() => {
                      setEditingItem(item);
                      setEditModalOpen(true);
                    }}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span className={cn("w-2 h-2 rounded-full shrink-0", dotColor)} />
                      <h4 className="font-semibold text-xs sm:text-sm text-white truncate hover:text-purple-300 transition-colors">
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

                    <div className="flex items-center gap-2 text-xs text-slate-400 pl-4">
                      <span className="text-purple-300/80">{item.genre}</span>
                      <span className="text-slate-700">·</span>
                      <span className="font-mono text-amber-400">★ {item.imdb ? item.imdb.toFixed(1) : "—"}</span>
                      <span className="font-mono text-rose-300">🍅 {item.rtCritics ? `${item.rtCritics}%` : "—"}</span>
                      <span className="font-mono text-amber-200">🍿 {item.rtAudience ? `${item.rtAudience}%` : "—"}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <a
                      href={`https://www.justwatch.com/br/busca?q=${encodeURIComponent(item.title)}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="h-8 px-2.5 rounded-lg border border-white/[0.08] text-[11px] font-medium text-slate-300 hover:text-white flex items-center gap-1.5 transition active:scale-95"
                      title="Ver onde assistir no streaming"
                    >
                      <span>Ver plataforma</span>
                      <ExternalLink className="w-3 h-3 text-slate-400" />
                    </a>

                    <button
                      type="button"
                      onClick={() => handleStatusChange(item.id, isWatched ? "queue" : "watched")}
                      className={cn(
                        "h-8 px-2.5 rounded-lg text-[11px] font-semibold transition flex items-center gap-1 active:scale-95",
                        !isWatched
                          ? "bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/25"
                          : "bg-emerald-600/20 text-emerald-300 border border-emerald-500/30"
                      )}
                    >
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      <span>{isWatched ? "Concluído" : "Visto"}</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>

      {/* Mobile Bottom Dock (Thumb Zone) */}
      <BottomNav
        onOpenWizard={() => setState(prev => ({ ...prev, wizardOpen: true }))}
        onOpenFilters={() => setFilterDrawerOpen(true)}
        onOpenRandomizer={() => setRandomizerOpen(true)}
        onOpenSearch={() => setCommandMenuOpen(true)}
        onOpenAdd={() => {
          setEditingItem(null);
          setEditModalOpen(true);
        }}
        activeFilterCount={activeFilterCount}
      />

      {/* Modals & Overlays */}
      <FilterDrawer
        open={filterDrawerOpen}
        onOpenChange={setFilterDrawerOpen}
        state={state}
        setState={setState}
        onReset={resetAllFilters}
        matchCount={filteredCatalog.length}
      />

      <CommandMenu
        isOpen={commandMenuOpen}
        onClose={() => setCommandMenuOpen(false)}
        catalog={catalog}
        onSelect={(it) => {
          setEditingItem(it);
          setEditModalOpen(true);
        }}
      />

      <WizardConcierge
        isOpen={state.wizardOpen}
        onClose={() => setState(prev => ({ ...prev, wizardOpen: false }))}
        catalog={catalog}
        onSkip={() => {
          setState(prev => ({ ...prev, wizardOpen: false }));
          showToast("Visualizando catálogo completo");
        }}
        onComplete={({ type, genre, ratingFilter }) => {
          setState(prev => ({
            ...prev,
            type,
            genre,
            minImdb: ratingFilter === "imdb_8" ? 8.0 : 0,
            rtCritics: ratingFilter === "rt_critics" ? "80" : "all",
            rtAudience: ratingFilter === "rt_audience" ? "85" : "all",
            wizardOpen: false,
          }));
          showToast("Filtros do assistente aplicados!");
        }}
      />

      <RandomizerModal
        isOpen={randomizerOpen}
        onClose={() => setRandomizerOpen(false)}
        catalog={catalog}
        onOpenEdit={(it) => {
          setEditingItem(it);
          setEditModalOpen(true);
        }}
      />

      <EditModal
        isOpen={editModalOpen}
        onClose={() => setEditModalOpen(false)}
        item={editingItem}
        onSave={handleSaveItem}
        onDelete={handleDeleteItem}
      />

      <ExportModal
        isOpen={exportModalOpen}
        onClose={() => setExportModalOpen(false)}
        catalog={catalog}
        onImport={(imported) => {
          setCatalog(imported);
          showToast(`${imported.length} títulos restaurados com sucesso!`);
        }}
      />

      {/* Toast Notification */}
      {toast && (
        <div className="fixed bottom-20 sm:bottom-8 left-1/2 -translate-x-1/2 z-50 bg-[#141722]/95 border border-white/10 px-4 py-2.5 rounded-2xl shadow-2xl backdrop-blur-md flex items-center gap-2 text-xs font-medium text-white animate-pop">
          <Sparkles className="w-3.5 h-3.5 text-purple-400" />
          <span>{toast}</span>
        </div>
      )}
    </div>
  );
}
