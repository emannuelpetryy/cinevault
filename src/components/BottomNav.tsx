import React from "react";
import { Compass, SlidersHorizontal, Dices, Search, Plus } from "lucide-react";
import { cn } from "@/lib/utils";

interface BottomNavProps {
  onOpenWizard: () => void;
  onOpenFilters: () => void;
  onOpenRandomizer: () => void;
  onOpenSearch: () => void;
  onOpenAdd: () => void;
  activeFilterCount: number;
}

export function BottomNav({
  onOpenWizard,
  onOpenFilters,
  onOpenRandomizer,
  onOpenSearch,
  onOpenAdd,
  activeFilterCount,
}: BottomNavProps) {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 bg-[#0E1017]/95 backdrop-blur-xl border-t border-white/[0.08] lg:hidden pb-[env(safe-area-inset-bottom,0px)] shadow-2xl">
      <div className="grid grid-cols-5 h-14 max-w-lg mx-auto">
        {/* Assistente */}
        <button
          type="button"
          onClick={onOpenWizard}
          className="flex flex-col items-center justify-center text-slate-400 hover:text-purple-400 transition active:scale-95 group"
        >
          <Compass className="w-5 h-5 group-hover:text-purple-400 transition-colors" />
          <span className="text-[10px] mt-0.5 font-medium tracking-tight">Assistente</span>
        </button>

        {/* Filtros */}
        <button
          type="button"
          onClick={onOpenFilters}
          className="flex flex-col items-center justify-center text-slate-400 hover:text-white transition relative active:scale-95 group"
        >
          <div className="relative">
            <SlidersHorizontal className="w-5 h-5 group-hover:text-white transition-colors" />
            {activeFilterCount > 0 && (
              <span className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-purple-500 ring-2 ring-[#0E1017]" />
            )}
          </div>
          <span className="text-[10px] mt-0.5 font-medium tracking-tight">Filtros</span>
        </button>

        {/* Adicionar (+) Center Action */}
        <button
          type="button"
          onClick={onOpenAdd}
          className="flex flex-col items-center justify-center -mt-3.5 group active:scale-90 transition-transform"
        >
          <div className="w-11 h-11 rounded-2xl bg-purple-600 hover:bg-purple-500 text-white flex items-center justify-center shadow-lg shadow-purple-600/30 border border-purple-400/30">
            <Plus className="w-5 h-5 stroke-[2.5]" />
          </div>
          <span className="text-[9px] mt-1 font-medium text-purple-300">Novo</span>
        </button>

        {/* Sortear */}
        <button
          type="button"
          onClick={onOpenRandomizer}
          className="flex flex-col items-center justify-center text-slate-400 hover:text-white transition active:scale-95 group"
        >
          <Dices className="w-5 h-5 group-hover:text-white transition-colors" />
          <span className="text-[10px] mt-0.5 font-medium tracking-tight">Sortear</span>
        </button>

        {/* Buscar */}
        <button
          type="button"
          onClick={onOpenSearch}
          className="flex flex-col items-center justify-center text-slate-400 hover:text-white transition active:scale-95 group"
        >
          <Search className="w-5 h-5 group-hover:text-white transition-colors" />
          <span className="text-[10px] mt-0.5 font-medium tracking-tight">Buscar</span>
        </button>
      </div>
    </nav>
  );
}
