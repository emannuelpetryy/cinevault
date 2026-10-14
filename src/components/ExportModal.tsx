import React, { useState } from "react";
import { CatalogItem } from "@/types";
import { X, Copy, Download, Upload, Check } from "lucide-react";

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  catalog: CatalogItem[];
  onImport: (data: CatalogItem[]) => void;
}

export function ExportModal({
  isOpen,
  onClose,
  catalog,
  onImport,
}: ExportModalProps) {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const jsonString = JSON.stringify(catalog, null, 2);

  const handleCopy = () => {
    navigator.clipboard.writeText(jsonString).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handleDownload = () => {
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `cinevault_backup_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const parsed = JSON.parse(event.target?.result as string);
        if (Array.isArray(parsed) && parsed.length > 0) {
          onImport(parsed);
          onClose();
        } else {
          alert("Arquivo JSON inválido.");
        }
      } catch (err) {
        alert("Erro ao ler o arquivo JSON.");
      }
    };
    reader.readAsText(file);
  };

  return (
    <div
      onClick={onClose}
      className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-lg bg-[#0E1017] border border-white/[0.1] rounded-3xl p-6 shadow-2xl text-white flex flex-col max-h-[85vh]"
      >
        <div className="flex items-center justify-between pb-3 border-b border-white/[0.06]">
          <div>
            <h3 className="font-semibold text-sm">Backup e Exportação</h3>
            <p className="text-[11px] text-slate-400">
              {catalog.length} títulos no seu cofre
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="py-4 space-y-4 flex-1 overflow-y-auto no-scrollbar">
          <textarea
            readOnly
            value={jsonString}
            className="w-full h-44 p-3 rounded-xl bg-black/40 border border-white/[0.08] text-xs font-mono text-slate-300 focus:outline-none resize-none no-scrollbar"
          />

          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={handleCopy}
              className="py-2.5 px-3 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-xs font-medium text-slate-200 transition flex items-center justify-center gap-1.5 active:scale-95"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? "Copiado!" : "Copiar JSON"}</span>
            </button>

            <button
              type="button"
              onClick={handleDownload}
              className="py-2.5 px-3 rounded-xl bg-purple-600/30 hover:bg-purple-600/40 border border-purple-500/40 text-xs font-medium text-purple-200 transition flex items-center justify-center gap-1.5 active:scale-95"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Baixar Arquivo</span>
            </button>
          </div>

          <div className="pt-3 border-t border-white/[0.06]">
            <label className="text-[11px] font-mono uppercase text-slate-400 block mb-2">
              Restaurar Backup
            </label>
            <label className="w-full py-3 rounded-xl border border-dashed border-white/20 hover:border-purple-500/60 hover:bg-white/[0.02] flex items-center justify-center gap-2 cursor-pointer transition text-xs text-slate-300">
              <Upload className="w-4 h-4 text-purple-400" />
              <span>Selecionar arquivo .json para restaurar</span>
              <input
                type="file"
                accept=".json"
                onChange={handleFileChange}
                className="hidden"
              />
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}
