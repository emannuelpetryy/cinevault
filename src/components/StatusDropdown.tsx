import React, { useState, useRef, useEffect } from "react";
import { MediaStatus } from "@/types";
import { cn } from "@/lib/utils";
import { Check, Clock, Star, ChevronDown } from "lucide-react";

interface StatusDropdownProps {
  status: MediaStatus;
  onChange: (newStatus: MediaStatus) => void;
  className?: string;
}

export function StatusDropdown({ status, onChange, className }: StatusDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isOpen]);

  const isPriority = status === "priority";
  const isWatched = status === "watched";

  const dotColor = isPriority
    ? "bg-amber-400 shadow-[0_0_6px_#F59E0B]"
    : isWatched
    ? "bg-emerald-400 shadow-[0_0_6px_#10B981]"
    : "bg-slate-500";

  const statusLabel = isPriority ? "Prioridade" : isWatched ? "Concluído" : "Na Fila";
  const statusColor = isPriority ? "text-amber-300" : isWatched ? "text-emerald-400" : "text-slate-400";

  return (
    <div className={cn("relative inline-block text-left", className)} ref={containerRef}>
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          setIsOpen(!isOpen);
        }}
        className={cn(
          "inline-flex items-center gap-1.5 font-medium px-2 py-0.5 rounded-lg border transition text-xs",
          "bg-white/[0.03] border-white/[0.06] hover:bg-white/[0.06] active:scale-95",
          statusColor
        )}
        title="Clique para escolher o status diretamente"
      >
        <span className={cn("w-1.5 h-1.5 rounded-full shrink-0", dotColor)} />
        <span>{statusLabel}</span>
        <ChevronDown className="w-2.5 h-2.5 text-slate-500 opacity-80" />
      </button>

      {isOpen && (
        <div
          onClick={(e) => e.stopPropagation()}
          className="absolute left-0 top-7 z-50 w-36 rounded-xl bg-[#141722] border border-white/10 shadow-2xl py-1 text-xs animate-fade-in backdrop-blur-md"
        >
          <button
            type="button"
            onClick={() => {
              onChange("priority");
              setIsOpen(false);
            }}
            className="w-full text-left px-3 py-1.5 hover:bg-white/[0.06] flex items-center gap-2 text-amber-300 font-medium transition-colors"
          >
            <Star className="w-3 h-3 text-amber-400 fill-amber-400/30" />
            <span>Prioridade ★</span>
          </button>
          <button
            type="button"
            onClick={() => {
              onChange("queue");
              setIsOpen(false);
            }}
            className="w-full text-left px-3 py-1.5 hover:bg-white/[0.06] flex items-center gap-2 text-slate-300 transition-colors"
          >
            <Clock className="w-3 h-3 text-slate-400" />
            <span>Na Fila ⏳</span>
          </button>
          <button
            type="button"
            onClick={() => {
              onChange("watched");
              setIsOpen(false);
            }}
            className="w-full text-left px-3 py-1.5 hover:bg-white/[0.06] flex items-center gap-2 text-emerald-400 font-medium transition-colors"
          >
            <Check className="w-3 h-3 text-emerald-400" />
            <span>Concluído ✓</span>
          </button>
        </div>
      )}
    </div>
  );
}
