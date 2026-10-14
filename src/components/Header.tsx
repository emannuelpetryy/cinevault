import React from "react";
import { AppState } from "@/types";
import {
  Compass,
  SlidersHorizontal,
  Dices,
  Plus,
  Download,
  LayoutGrid,
  List,
  Search,
} from "lucide-react";

interface HeaderProps {
  state: AppState;
  setState: React.Dispatch<React.SetStateAction<AppState>>;
  onOpenWizard: () => void;
  onOpenFilters: () => void;
  onOpenRandomizer: () => void;
  onOpenSearch: () => void;
  onOpenAdd: () => void;
  onOpenExport: () => void;
  activeFilterCount: number;
  totalCount: number;
  watchedCount: number;
}

export function Header({
  state,
  setState,
  onOpenWizard,
  onOpenFilters,
  onOpenRandomizer,
  onOpenSearch,
  onOpenAdd,
  onOpenExport,
  activeFilterCount,
  totalCount,
  watchedCount,
}: HeaderProps) {
  const pct = totalCount > 0 ? Math.round((watchedCount / totalCount) * 100) : 0;

  return (
    <header className="sticky top-0 z-30 bg-[#090A0F]/90 backdrop-blur-xl border-b border-white/[0.05]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <div className="flex items-center justify-between gap-3">
          {/* Logo & Telemetry */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-xl bg-purple-600 flex items-center justify-center font-bold text-white shadow-lg shadow-purple-600/30 text-sm">
                CV
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-sm font-bold text-white tracking-tight">CineVault</h1>
                  <span className="text-[10px] font-mono px-1.5 py-0.2 rounded-full bg-white/[0.06] text-purple-300">
                    2.0
                  </span>
                </div>
                <div className="flex items-center gap-2 text-[11px] text-slate-400">
                  <span>{watchedCount} de {totalCount} assistidos ({pct}%)</span>
                </div>
              </div>
            </div>
          </div>

          {/* Search Trigger Bar (Desktop & Tablet) */}
          <button
            type="button"
            onClick={onOpenSearch}
            className="hidden md:flex items-center gap-2.5 h-9 px-3 rounded-xl bg-white/[0.04] hover:bg-white/[0.07] border border-white/[0.08] text-xs text-slate-400 w-64 lg:w-80 transition cursor-text text-left"
          >
            <Search className="w-3.5 h-3.5 text-slate-400 shrink-0" />
            <span className="truncate flex-1">Buscar filme, série, plataforma...</span>
            <kbd className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-white/[0.06] text-slate-500 border border-white/[0.08]">
              /
            </kbd>
          </button>

          {/* Top Actions */}
          <div className="flex items-center gap-2">
            {/* Assistente */}
            <button
              type="button"
              onClick={onOpenWizard}
              className="h-8 px-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/40 text-purple-300 hover:text-white text-xs font-semibold transition flex items-center gap-1.5 active:scale-95 shadow-sm shadow-purple-600/20"
            >
              <Compass className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Assistente</span>
            </button>

            {/* Filtros Drawer Trigger */}
            <button
              type="button"
              onClick={onOpenFilters}
              className="h-8 px-2.5 sm:px-3 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-slate-300 hover:text-white text-xs font-medium transition flex items-center gap-1.5 active:scale-95 relative"
              title="Filtros avançados"
            >
              <SlidersHorizontal className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Filtros</span>
              {activeFilterCount > 0 && (
                <span className="w-4 h-4 rounded-full bg-purple-600 text-[10px] font-bold text-white flex items-center justify-center -ml-0.5">
                  {activeFilterCount}
                </span>
              )}
            </button>

            {/* Sortear */}
            <button
              type="button"
              onClick={onOpenRandomizer}
              className="h-8 w-8 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-slate-400 hover:text-white flex items-center justify-center transition active:scale-95"
              title="Sortear obra"
            >
              <Dices className="w-3.5 h-3.5" />
            </button>

            {/* Add Nova Obra */}
            <button
              type="button"
              onClick={onOpenAdd}
              className="h-8 w-8 sm:w-auto sm:px-3 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-slate-300 hover:text-white text-xs font-medium flex items-center justify-center gap-1.5 transition active:scale-95"
              title="Adicionar obra"
            >
              <Plus className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Nova Obra</span>
            </button>

            {/* View Mode Toggle (Grid vs Table) */}
            <div className="hidden sm:flex items-center p-0.5 rounded-xl bg-white/[0.04] border border-white/[0.08]">
              <button
                type="button"
                onClick={() => setState(prev => ({ ...prev, view: 'grid' }))}
                className={`p-1.5 rounded-lg transition ${state.view === 'grid' ? 'bg-white/[0.12] text-white' : 'text-slate-400 hover:text-white'}`}
                title="Visualização em Grade"
              >
                <LayoutGrid className="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                onClick={() => setState(prev => ({ ...prev, view: 'table' }))}
                className={`p-1.5 rounded-lg transition ${state.view === 'table' ? 'bg-white/[0.12] text-white' : 'text-slate-400 hover:text-white'}`}
                title="Visualização em Lista"
              >
                <List className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Backup / Export */}
            <button
              type="button"
              onClick={onOpenExport}
              className="h-8 w-8 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-slate-400 hover:text-white flex items-center justify-center transition active:scale-95"
              title="Backup / Exportar"
            >
              <Download className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Telemetry Progress Bar */}
        <div className="w-full bg-white/[0.04] h-1 rounded-full overflow-hidden mt-3">
          <div
            className="bg-gradient-to-r from-purple-500 to-emerald-400 h-full transition-all duration-500"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>
    </header>
  );
}
