# -*- coding: utf-8 -*-
"""
Clean, minimalist, high-end redesign of Cinevault.
Inspired by useplanes.com, landdding.com, metalforge.xyz, sceneai.art and iconly.design.
Fixes popup closing bug completely and eliminates visual clutter.
"""

import json
import re
from metadata_cinevault import METADATA

# Load items from git HEAD as valid JSON
import subprocess
raw = subprocess.check_output(['git', 'show', 'HEAD:index.html'], encoding='utf-8')
start = raw.find('const INITIAL_DATA = [')
end = raw.find('];', start)
data_text = raw[start + len('const INITIAL_DATA = '):end + 1]

items = json.loads(data_text)
print(f"Clean builder: Loaded {len(items)} items from JSON.")
js_items = json.dumps(items, ensure_ascii=False, indent=8)

clean_html = f'''<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#090A0F">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Cinevault">
    <title>Cinevault — Emannuel Petry</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    }},
                    colors: {{
                        canvas: '#090A0F',
                        surface: {{
                            DEFAULT: '#0F1118',
                            hover: '#141722',
                            border: 'rgba(255, 255, 255, 0.07)',
                            borderHover: 'rgba(255, 255, 255, 0.16)',
                        }},
                        accent: {{
                            DEFAULT: '#820AD1',
                            light: '#A855F7',
                            glow: 'rgba(130, 10, 209, 0.25)',
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        * {{
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            -webkit-tap-highlight-color: transparent;
        }}
        html, body {{
            background-color: #090A0F;
            color: #F8FAFC;
            overflow-x: hidden;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11";
        }}
        /* Minimalist Card & Borders */
        .card-clean {{
            background: #0E1017;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        @media (hover: hover) and (pointer: fine) {{
            .card-clean:hover {{
                border-color: rgba(255, 255, 255, 0.14);
                background: #121520;
                transform: translateY(-2px);
                box-shadow: 0 16px 32px -12px rgba(0, 0, 0, 0.6), 0 0 24px -10px rgba(130, 10, 209, 0.15);
            }}
        }}
        .card-clean:active {{
            transform: scale(0.995);
        }}
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 5px;
            height: 5px;
        }}
        ::-webkit-scrollbar-track {{
            background: #090A0F;
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.12);
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.2);
        }}
        .no-scrollbar::-webkit-scrollbar {{
            display: none;
        }}
        .no-scrollbar {{
            -ms-overflow-style: none;
            scrollbar-width: none;
        }}
        /* Safe Areas */
        .pb-safe {{
            padding-bottom: calc(5rem + env(safe-area-inset-bottom, 0px));
        }}
        .bottom-nav-safe {{
            padding-bottom: env(safe-area-inset-bottom, 0px);
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col bg-canvas text-slate-100 selection:bg-accent selection:text-white">

    <!-- ================= MINIMALIST TOP NAVIGATION BAR ================= -->
    <header class="sticky top-0 z-30 bg-[#090A0F]/85 backdrop-blur-xl border-b border-white/[0.06]">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="h-16 flex items-center justify-between gap-3">
                
                <!-- Brand -->
                <div class="flex items-center gap-3 shrink-0">
                    <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-[#820AD1] to-[#6D28D9] flex items-center justify-center shadow-md border border-white/20">
                        <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
                            <line x1="7" y1="2" x2="7" y2="22"></line>
                            <line x1="17" y1="2" x2="17" y2="22"></line>
                            <line x1="2" y1="12" x2="22" y2="12"></line>
                        </svg>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="font-bold text-sm tracking-tight text-white">Cinevault</span>
                        <span class="hidden sm:inline-block text-[11px] text-slate-400 font-normal">/ Emannuel Petry</span>
                    </div>
                </div>

                <!-- Minimalist Search Input (Linear / Raycast aesthetic) -->
                <div class="flex-1 max-w-md relative">
                    <svg class="w-3.5 h-3.5 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input 
                        type="text" 
                        id="search-input"
                        oninput="handleSearch(this.value)"
                        placeholder="Buscar filme, série, nota, ano..." 
                        class="w-full pl-9 pr-8 py-1.5 sm:py-2 bg-white/[0.04] hover:bg-white/[0.06] focus:bg-white/[0.07] border border-white/[0.08] focus:border-purple-500/60 rounded-xl text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none transition shadow-inner"
                    >
                    <button id="clear-search-btn" onclick="clearSearch()" class="hidden absolute right-2.5 top-1/2 -translate-y-1/2 p-0.5 text-slate-400 hover:text-white" aria-label="Limpar busca">
                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                    </button>
                </div>

                <!-- Header Actions -->
                <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
                    <!-- Filter Button with active indicator -->
                    <button onclick="openFilterModal()" class="relative h-9 px-3 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-xs font-medium text-slate-200 transition flex items-center gap-2">
                        <svg class="w-3.5 h-3.5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                        <span class="hidden sm:inline">Filtros</span>
                        <span id="header-filter-badge" class="hidden w-2 h-2 rounded-full bg-purple-500 shadow-[0_0_8px_#A855F7]"></span>
                    </button>

                    <!-- Randomizer Button -->
                    <button onclick="openRandomizerModal()" class="h-9 px-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-xs font-medium text-purple-200 transition flex items-center gap-1.5" title="Sortear título">
                        <svg class="w-3.5 h-3.5 text-purple-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
                        <span class="hidden md:inline">Sortear</span>
                    </button>

                    <!-- Add New -->
                    <button onclick="openAddModal()" class="h-9 px-3 rounded-xl bg-white/[0.08] hover:bg-white/[0.14] text-xs font-medium text-white transition flex items-center gap-1.5">
                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                        <span class="hidden sm:inline">Novo</span>
                    </button>

                    <!-- View Mode Toggle -->
                    <div class="hidden sm:inline-flex rounded-xl bg-white/[0.04] p-0.5 border border-white/[0.08]">
                        <button onclick="setViewMode('grid')" id="view-btn-grid" class="p-1.5 rounded-lg text-white transition" aria-label="Grade">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                        </button>
                        <button onclick="setViewMode('table')" id="view-btn-table" class="p-1.5 rounded-lg text-slate-400 hover:text-white transition" aria-label="Lista">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
                        </button>
                    </div>

                    <!-- Backup / Export -->
                    <button onclick="openExportModal()" class="h-9 w-9 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-slate-400 hover:text-white flex items-center justify-center transition" title="Exportar / Backup">
                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                    </button>
                </div>
            </div>

            <!-- Clean Sub-Navigation Tabs & Quiet Telemetry -->
            <div class="py-2.5 flex items-center justify-between gap-3 overflow-x-auto no-scrollbar border-t border-white/[0.04]">
                <!-- Clean View Tabs (Pills) -->
                <div class="flex items-center gap-1.5 text-xs font-medium shrink-0">
                    <button onclick="setStatusFilter('all')" data-tab="all" class="tab-pill px-3 py-1.5 rounded-full text-slate-300 hover:text-white transition">
                        Todos <span data-tab-count="all" class="text-slate-500 font-mono text-[11px] ml-1">0</span>
                    </button>
                    <button onclick="setStatusFilter('priority')" data-tab="priority" class="tab-pill px-3 py-1.5 rounded-full text-slate-300 hover:text-white transition flex items-center gap-1.5">
                        <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                        <span>Prioridades</span>
                        <span data-tab-count="priority" class="text-amber-400/80 font-mono text-[11px]">0</span>
                    </button>
                    <button onclick="setStatusFilter('queue')" data-tab="queue" class="tab-pill px-3 py-1.5 rounded-full text-slate-300 hover:text-white transition">
                        Na Fila <span data-tab-count="queue" class="text-slate-500 font-mono text-[11px] ml-1">0</span>
                    </button>
                    <button onclick="setStatusFilter('watched')" data-tab="watched" class="tab-pill px-3 py-1.5 rounded-full text-slate-300 hover:text-white transition flex items-center gap-1.5">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                        <span>Concluídos</span>
                        <span data-tab-count="watched" class="text-emerald-400/80 font-mono text-[11px]">0</span>
                    </button>
                    <button onclick="setTypeFilter('series')" data-tab="series" class="tab-pill px-3 py-1.5 rounded-full text-slate-300 hover:text-white transition">
                        Séries <span data-tab-count="series" class="text-purple-400/80 font-mono text-[11px] ml-1">0</span>
                    </button>
                </div>

                <!-- Quiet Status & Sort -->
                <div class="flex items-center gap-3 shrink-0 text-xs">
                    <div class="hidden md:flex items-center gap-2 text-slate-400 text-[11px]">
                        <span id="telemetry-text">0 assistidos</span>
                        <div class="w-20 h-1 bg-white/[0.08] rounded-full overflow-hidden">
                            <div id="telemetry-bar" class="h-full bg-gradient-to-r from-purple-500 to-emerald-400" style="width: 0%"></div>
                        </div>
                    </div>

                    <select id="sort-select" onchange="setSortOrder(this.value)" class="bg-white/[0.04] border border-white/[0.08] rounded-lg px-2.5 py-1 text-xs text-slate-300 focus:outline-none focus:border-purple-500 cursor-pointer">
                        <option value="status">Ordenar: Prioridade</option>
                        <option value="imdb_desc">Maior IMDb ★</option>
                        <option value="critics_desc">Maior Crítica 🍅</option>
                        <option value="audience_desc">Maior Público 🍿</option>
                        <option value="year_desc">Mais Recentes</option>
                        <option value="alpha_asc">Nome (A — Z)</option>
                    </select>
                </div>
            </div>
        </div>
    </header>

    <!-- ================= MAIN CONTENT ================= -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-5 pb-safe">

        <!-- Active Filter Indicator (Only shown if filters are active) -->
        <div id="active-filters-bar" class="hidden mb-4 p-2.5 rounded-xl bg-white/[0.02] border border-white/[0.06] flex items-center justify-between text-xs">
            <div class="flex items-center gap-2 flex-wrap" id="active-chips-container">
                <!-- Injected dynamically -->
            </div>
            <button onclick="resetAllFilters()" class="text-[11px] text-purple-400 hover:text-purple-300 font-medium ml-2 shrink-0">
                Limpar todos
            </button>
        </div>

        <!-- 1. Grid View (Ultra Clean Cards) -->
        <div id="catalog-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3.5">
            <!-- Rendered dynamically -->
        </div>

        <!-- 2. Compact List View -->
        <div id="catalog-table-wrapper" class="hidden card-clean rounded-2xl overflow-hidden divide-y divide-white/[0.06]">
            <!-- Rendered dynamically -->
        </div>

        <!-- Empty State -->
        <div id="empty-state" class="hidden py-20 text-center">
            <div class="w-12 h-12 rounded-2xl bg-white/[0.04] border border-white/[0.08] flex items-center justify-center mx-auto mb-3 text-slate-400">
                <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </div>
            <h3 class="text-sm font-semibold text-white mb-1">Nenhum título encontrado</h3>
            <p class="text-xs text-slate-400 max-w-xs mx-auto mb-4">Nenhum filme ou série corresponde aos critérios selecionados.</p>
            <button onclick="resetAllFilters()" class="px-4 py-2 rounded-xl bg-white/[0.08] hover:bg-white/[0.12] text-xs font-medium text-white transition">
                Redefinir Filtros
            </button>
        </div>

    </main>

    <!-- ================= MOBILE BOTTOM DOCK (< 1024px) ================= -->
    <nav class="lg:hidden fixed bottom-0 inset-x-0 z-30 bg-[#090A0F]/90 backdrop-blur-xl border-t border-white/[0.06] bottom-nav-safe">
        <div class="grid grid-cols-5 h-14 max-w-md mx-auto items-center">
            <button onclick="setStatusFilter('all')" data-bnav="all" class="flex flex-col items-center justify-center gap-1 text-slate-400 transition">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                <span class="text-[10px]">Início</span>
            </button>
            <button onclick="setStatusFilter('priority')" data-bnav="priority" class="flex flex-col items-center justify-center gap-1 text-slate-400 transition">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                <span class="text-[10px]">Prioridade</span>
            </button>
            <!-- Center Sorteador Button -->
            <button onclick="openRandomizerModal()" class="flex flex-col items-center justify-center gap-1 text-purple-300">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-[#820AD1] to-[#6D28D9] text-white flex items-center justify-center shadow-md border border-white/20 -mt-3">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
                </div>
                <span class="text-[10px] font-semibold text-purple-300">Sortear</span>
            </button>
            <button onclick="openFilterModal()" class="relative flex flex-col items-center justify-center gap-1 text-slate-400 transition">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                <span class="text-[10px]">Filtros</span>
                <span id="bnav-filter-dot" class="hidden absolute top-2 right-4 w-1.5 h-1.5 rounded-full bg-purple-500 shadow-[0_0_6px_#A855F7]"></span>
            </button>
            <button onclick="setStatusFilter('watched')" data-bnav="watched" class="flex flex-col items-center justify-center gap-1 text-slate-400 transition">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                <span class="text-[10px]">Vistos</span>
            </button>
        </div>
    </nav>

    <!-- ================= CLEAN FILTER MODAL (BUG-FREE CLOSE) ================= -->
    <div id="filter-modal" onclick="if(event.target === this) closeFilterModal()" class="fixed inset-0 z-50 hidden items-center justify-center p-3 sm:p-5 bg-black/80 backdrop-blur-md transition-opacity">
        <div class="bg-[#0E1017] border border-white/[0.08] rounded-2xl w-full max-w-lg shadow-2xl flex flex-col max-h-[88vh] overflow-hidden">
            
            <!-- Modal Header -->
            <div class="px-5 py-3.5 border-b border-white/[0.06] flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                    <h3 class="text-sm font-semibold text-white">Filtros Avançados</h3>
                </div>
                <button type="button" onclick="closeFilterModal()" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition" aria-label="Fechar">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <!-- Modal Body (Clean grouped pills) -->
            <div class="px-5 py-4 overflow-y-auto space-y-4 no-scrollbar text-xs">
                <!-- 1. Formato & Status -->
                <div>
                    <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Status</label>
                    <div class="flex flex-wrap gap-1.5">
                        <button onclick="setStatusFilter('all')" data-m-status="all" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Todos</button>
                        <button onclick="setStatusFilter('pending')" data-m-status="pending" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Pendentes</button>
                        <button onclick="setStatusFilter('priority')" data-m-status="priority" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition text-amber-300">Prioridade ★</button>
                        <button onclick="setStatusFilter('queue')" data-m-status="queue" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Na Fila</button>
                        <button onclick="setStatusFilter('watched')" data-m-status="watched" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition text-emerald-400">Concluídos ✓</button>
                    </div>
                </div>

                <!-- 2. Gêneros -->
                <div>
                    <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Gênero</label>
                    <div class="flex flex-wrap gap-1.5">
                        <button onclick="setGenreFilter('all')" data-m-genre="all" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Todos</button>
                        <button onclick="setGenreFilter('Suspense & Thriller')" data-m-genre="Suspense & Thriller" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Suspense & Thriller</button>
                        <button onclick="setGenreFilter('Drama & Biografia')" data-m-genre="Drama & Biografia" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Drama & Biografia</button>
                        <button onclick="setGenreFilter('Ação & Ficção')" data-m-genre="Ação & Ficção" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Ação & Ficção</button>
                        <button onclick="setGenreFilter('Terror')" data-m-genre="Terror" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Terror</button>
                        <button onclick="setGenreFilter('Comédia')" data-m-genre="Comédia" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Comédia</button>
                        <button onclick="setGenreFilter('Série / Doc')" data-m-genre="Série / Doc" class="m-pill px-3 py-1.5 rounded-lg border text-xs transition">Séries & Docs</button>
                    </div>
                </div>

                <!-- 3. Nota IMDb Mínima -->
                <div>
                    <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Nota Mínima IMDb</label>
                    <div class="grid grid-cols-4 gap-1.5">
                        <button onclick="setMinImdb(0)" data-m-imdb="0" class="m-pill py-1.5 rounded-lg border text-center transition">Qualquer</button>
                        <button onclick="setMinImdb(7.0)" data-m-imdb="7.0" class="m-pill py-1.5 rounded-lg border text-center transition">★ 7.0+</button>
                        <button onclick="setMinImdb(7.5)" data-m-imdb="7.5" class="m-pill py-1.5 rounded-lg border text-center transition">★ 7.5+</button>
                        <button onclick="setMinImdb(8.0)" data-m-imdb="8.0" class="m-pill py-1.5 rounded-lg border text-center transition text-amber-300">★ 8.0+</button>
                    </div>
                </div>

                <!-- 4. Rotten Tomatoes -->
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">🍅 Tomatometer</label>
                        <div class="flex flex-col gap-1">
                            <button onclick="setRtCritics('all')" data-m-rtcritics="all" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">Qualquer</button>
                            <button onclick="setRtCritics('certified')" data-m-rtcritics="certified" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition text-rose-300">Certified (≥75%)</button>
                            <button onclick="setRtCritics('top')" data-m-rtcritics="top" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition text-rose-300">Top Tier (≥90%)</button>
                        </div>
                    </div>
                    <div>
                        <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">🍿 Popcornmeter</label>
                        <div class="flex flex-col gap-1">
                            <button onclick="setRtAudience('all')" data-m-rtaudience="all" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">Qualquer</button>
                            <button onclick="setRtAudience('fresh')" data-m-rtaudience="fresh" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition text-amber-200">Aprovado (≥60%)</button>
                            <button onclick="setRtAudience('high')" data-m-rtaudience="high" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition text-amber-200">Favorito (≥85%)</button>
                        </div>
                    </div>
                </div>

                <!-- 5. Origem & Décadas -->
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Origem</label>
                        <div class="flex flex-col gap-1">
                            <button onclick="setOriginFilter('all')" data-m-origin="all" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">Todas</button>
                            <button onclick="setOriginFilter('user')" data-m-origin="user" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">Manu (Pessoal)</button>
                            <button onclick="setOriginFilter('brother')" data-m-origin="brother" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">Irmão</button>
                            <button onclick="setOriginFilter('both')" data-m-origin="both" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">Ambos</button>
                        </div>
                    </div>
                    <div>
                        <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Época</label>
                        <div class="flex flex-col gap-1">
                            <button onclick="setDecadeFilter('all')" data-m-decade="all" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">Todas</button>
                            <button onclick="setDecadeFilter('2020s')" data-m-decade="2020s" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">2020+</button>
                            <button onclick="setDecadeFilter('2010s')" data-m-decade="2010s" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">2010s</button>
                            <button onclick="setDecadeFilter('classic')" data-m-decade="classic" class="m-pill py-1.5 px-2.5 rounded-lg border text-left transition">Clássicos</button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Modal Footer -->
            <div class="px-5 py-3 border-t border-white/[0.06] bg-[#0A0C11] flex items-center justify-between gap-3">
                <button type="button" onclick="resetAllFilters()" class="text-xs text-slate-400 hover:text-white transition">Limpar Filtros</button>
                <button type="button" onclick="closeFilterModal()" class="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs shadow-md transition flex items-center gap-1.5">
                    <span>Ver Resultados</span>
                    <span id="modal-counter-badge" class="px-1.5 py-0.2 rounded-full bg-white/20 font-mono text-[10px]">0</span>
                </button>
            </div>
        </div>
    </div>

    <!-- ================= RANDOMIZER MODAL ================= -->
    <div id="randomizer-modal" onclick="if(event.target === this) closeRandomizerModal()" class="fixed inset-0 z-50 hidden items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <div class="bg-[#0E1017] border border-white/[0.08] rounded-2xl w-full max-w-sm shadow-2xl p-5 text-center flex flex-col items-center">
            <div class="w-10 h-10 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-300 mb-3">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
            </div>
            <h3 class="text-sm font-semibold text-white mb-0.5">Sorteador</h3>
            <p class="text-[11px] text-slate-400 mb-4">Escolha aleatória entre os seus pendentes</p>

            <div class="w-full bg-white/[0.03] border border-white/[0.06] rounded-xl p-4 min-h-[110px] flex flex-col items-center justify-center mb-4">
                <span id="rand-tag" class="text-[10px] font-mono uppercase tracking-wider text-slate-500 mb-1">Pronto</span>
                <h4 id="rand-title" class="text-base font-bold text-white mb-1">Gire para sortear</h4>
                <div id="rand-ratings" class="hidden text-xs font-mono text-slate-300 my-1"></div>
                <p id="rand-meta" class="text-xs text-slate-400"></p>
            </div>

            <div class="w-full flex flex-col gap-2">
                <button onclick="runRandomizer()" class="w-full h-11 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs transition shadow-md">
                    Sortear Obra
                </button>
                <button onclick="closeRandomizerModal()" class="w-full h-9 rounded-xl text-slate-400 hover:text-white text-xs transition">
                    Fechar
                </button>
            </div>
        </div>
    </div>

    <!-- ================= EDIT / ADD MODAL ================= -->
    <div id="entry-modal" onclick="if(event.target === this) closeAddModal()" class="fixed inset-0 z-50 hidden items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <div class="bg-[#0E1017] border border-white/[0.08] rounded-2xl w-full max-w-md shadow-2xl p-5 overflow-y-auto max-h-[90vh]">
            <div class="flex items-center justify-between pb-3 border-b border-white/[0.06] mb-4">
                <h3 id="entry-modal-title" class="text-sm font-semibold text-white">Editar Obra</h3>
                <button onclick="closeAddModal()" class="p-1 rounded-lg text-slate-400 hover:text-white">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <form id="entry-form" onsubmit="saveEntryForm(event)" class="space-y-3 text-xs">
                <input type="hidden" id="entry-id">
                <div>
                    <label class="text-[11px] text-slate-400 block mb-1">Título</label>
                    <input type="text" id="entry-title" required class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-2 text-white focus:outline-none focus:border-purple-500">
                </div>
                <div class="grid grid-cols-3 gap-2">
                    <div>
                        <label class="text-[11px] text-slate-400 block mb-1">Ano</label>
                        <input type="number" id="entry-year" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-2 text-white font-mono focus:outline-none focus:border-purple-500">
                    </div>
                    <div>
                        <label class="text-[11px] text-slate-400 block mb-1">Formato</label>
                        <select id="entry-type" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-2.5 py-2 text-white focus:outline-none focus:border-purple-500">
                            <option value="movie">Filme</option>
                            <option value="series">Série / Doc</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-[11px] text-slate-400 block mb-1">Status</label>
                        <select id="entry-status" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-2.5 py-2 text-white focus:outline-none focus:border-purple-500">
                            <option value="priority">Prioridade</option>
                            <option value="queue">Na Fila</option>
                            <option value="watched">Concluído</option>
                        </select>
                    </div>
                </div>

                <!-- Ratings row in edit -->
                <div class="grid grid-cols-3 gap-2 p-2.5 rounded-xl bg-white/[0.02] border border-white/[0.04]">
                    <div>
                        <label class="text-[10px] text-amber-300 font-mono block mb-1">IMDb (0-10)</label>
                        <input type="number" step="0.1" id="entry-imdb" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-lg px-2 py-1 text-white font-mono">
                    </div>
                    <div>
                        <label class="text-[10px] text-rose-300 font-mono block mb-1">🍅 Crítica (%)</label>
                        <input type="number" id="entry-rt-critics" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-lg px-2 py-1 text-white font-mono">
                    </div>
                    <div>
                        <label class="text-[10px] text-amber-200 font-mono block mb-1">🍿 Público (%)</label>
                        <input type="number" id="entry-rt-audience" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-lg px-2 py-1 text-white font-mono">
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label class="text-[11px] text-slate-400 block mb-1">Categoria</label>
                        <select id="entry-genre" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-2.5 py-2 text-white focus:outline-none focus:border-purple-500">
                            <option value="Suspense & Thriller">Suspense & Thriller</option>
                            <option value="Drama & Biografia">Drama & Biografia</option>
                            <option value="Ação & Ficção">Ação & Ficção</option>
                            <option value="Terror">Terror</option>
                            <option value="Comédia">Comédia</option>
                            <option value="Série / Doc">Série / Doc</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-[11px] text-slate-400 block mb-1">Origem</label>
                        <select id="entry-origin" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-2.5 py-2 text-white focus:outline-none focus:border-purple-500">
                            <option value="user">Manu (Pessoal)</option>
                            <option value="brother">Irmão</option>
                            <option value="both">Ambos</option>
                        </select>
                    </div>
                </div>

                <div>
                    <label class="text-[11px] text-slate-400 block mb-1">Subgênero / Plataforma</label>
                    <input type="text" id="entry-subgenre" placeholder="Ex: Thriller Psicológico • Max" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-2 text-white">
                </div>

                <div>
                    <label class="text-[11px] text-slate-400 block mb-1">Anotação</label>
                    <input type="text" id="entry-note" placeholder="Ex: Recomendo assistir com fone..." class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-2 text-white">
                </div>

                <div class="pt-3 border-t border-white/[0.06] flex items-center justify-between gap-2">
                    <button type="button" id="delete-entry-btn" onclick="deleteCurrentEntry()" class="text-rose-400 hover:text-rose-300 font-medium">
                        Excluir
                    </button>
                    <div class="flex gap-2 ml-auto">
                        <button type="button" onclick="closeAddModal()" class="px-4 py-2 rounded-xl text-slate-400 hover:text-white">Cancelar</button>
                        <button type="submit" class="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium shadow-md">Salvar</button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- ================= EXPORT / BACKUP MODAL ================= -->
    <div id="export-modal" onclick="if(event.target === this) closeExportModal()" class="fixed inset-0 z-50 hidden items-center justify-center p-4 bg-black/80 backdrop-blur-md">
        <div class="bg-[#0E1017] border border-white/[0.08] rounded-2xl w-full max-w-md shadow-2xl p-5">
            <div class="flex items-center justify-between pb-3 border-b border-white/[0.06] mb-3">
                <h3 class="text-sm font-semibold text-white">Backup & Exportação</h3>
                <button onclick="closeExportModal()" class="p-1 rounded-lg text-slate-400 hover:text-white">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
            <textarea id="export-textarea" readonly class="w-full h-36 bg-black/50 border border-white/[0.08] rounded-xl p-3 font-mono text-[11px] text-slate-300 mb-3 resize-none focus:outline-none"></textarea>
            <div class="flex items-center justify-between gap-2 text-xs">
                <button onclick="copyExportText()" class="px-3 py-2 rounded-xl bg-white/[0.06] hover:bg-white/[0.1] text-white">Copiar JSON</button>
                <button onclick="downloadJson()" class="px-3 py-2 rounded-xl bg-white/[0.06] hover:bg-white/[0.1] text-white">Baixar Arquivo</button>
                <label class="px-3 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white cursor-pointer font-medium">
                    Restaurar
                    <input type="file" accept=".json" onchange="importJson(event)" class="hidden">
                </label>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-20 sm:bottom-6 right-4 sm:right-6 z-50 hidden transform transition-all duration-200 translate-y-2 opacity-0 pointer-events-none">
        <div class="bg-[#141722]/95 backdrop-blur-md border border-white/10 text-white px-4 py-2.5 rounded-xl shadow-2xl text-xs flex items-center gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
            <span id="toast-text">Atualizado</span>
        </div>
    </div>

    <!-- ================= JAVASCRIPT LOGIC ================= -->
    <script>
        const STORAGE_KEY = 'cinevault_clean_v1';
        const LEGACY_KEYS = ['cinevault_v3_state', 'cinevault_v2_state', 'cinevault_emannuel_petry_v2'];

        const INITIAL_DATA = {js_items};

        let catalog = [];
        let state = {{
            search: '',
            status: 'all',
            type: 'all',
            genre: 'all',
            origin: 'all',
            minImdb: 0,
            rtCritics: 'all',
            rtAudience: 'all',
            decade: 'all',
            sort: 'status',
            view: 'grid'
        }};

        function init() {{
            try {{
                let raw = localStorage.getItem(STORAGE_KEY);
                if (!raw) {{
                    for (const k of LEGACY_KEYS) {{
                        const leg = localStorage.getItem(k);
                        if (leg) {{ raw = leg; break; }}
                    }}
                }}
                if (raw) {{
                    const parsed = JSON.parse(raw);
                    if (Array.isArray(parsed) && parsed.length > 0) {{
                        catalog = parsed.map(item => {{
                            const initItem = INITIAL_DATA.find(i => i.id === item.id) || {{}};
                            return {{
                                ...initItem,
                                ...item,
                                year: item.year || initItem.year || 2020,
                                imdb: item.imdb !== undefined ? item.imdb : (initItem.imdb || null),
                                rtCritics: item.rtCritics !== undefined ? item.rtCritics : (initItem.rtCritics || null),
                                rtAudience: item.rtAudience !== undefined ? item.rtAudience : (initItem.rtAudience || null),
                            }};
                        }});
                        // Ensure all 217 items exist
                        const setIds = new Set(catalog.map(c => c.id));
                        for (const it of INITIAL_DATA) {{
                            if (!setIds.has(it.id)) catalog.push(JSON.parse(JSON.stringify(it)));
                        }}
                        persist();
                    }} else {{
                        catalog = JSON.parse(JSON.stringify(INITIAL_DATA));
                        persist();
                    }}
                }} else {{
                    catalog = JSON.parse(JSON.stringify(INITIAL_DATA));
                    persist();
                }}
            }} catch (e) {{
                catalog = JSON.parse(JSON.stringify(INITIAL_DATA));
            }}

            // Keyboard shortcut '/'
            window.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') {{
                    closeFilterModal();
                    closeRandomizerModal();
                    closeAddModal();
                    closeExportModal();
                }}
                if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {{
                    e.preventDefault();
                    document.getElementById('search-input')?.focus();
                }}
            }});

            syncStyles();
            render();
        }}

        function persist() {{
            try {{
                localStorage.setItem(STORAGE_KEY, JSON.stringify(catalog));
            }} catch (e) {{}}
        }}

        function escapeHtml(str) {{
            if (!str) return '';
            return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
        }}

        function getFilteredCatalog() {{
            return catalog.filter(item => {{
                if (state.search) {{
                    const q = state.search.toLowerCase().trim();
                    const inTitle = (item.title || '').toLowerCase().includes(q);
                    const inSub = (item.subgenre || '').toLowerCase().includes(q);
                    const inGenre = (item.genre || '').toLowerCase().includes(q);
                    const inNote = (item.note || '').toLowerCase().includes(q);
                    const inYear = String(item.year || '').includes(q);
                    if (!inTitle && !inSub && !inGenre && !inNote && !inYear) return false;
                }}

                if (state.status === 'priority' && item.status !== 'priority') return false;
                if (state.status === 'queue' && item.status !== 'queue') return false;
                if (state.status === 'watched' && item.status !== 'watched') return false;
                if (state.status === 'pending' && (item.status !== 'priority' && item.status !== 'queue')) return false;

                if (state.type === 'movie' && item.type !== 'movie') return false;
                if (state.type === 'series' && item.type !== 'series') return false;

                if (state.genre !== 'all' && item.genre !== state.genre) return false;
                if (state.origin !== 'all' && item.origin !== state.origin) return false;

                if (state.minImdb > 0 && (!item.imdb || item.imdb < state.minImdb)) return false;
                if (state.rtCritics === 'certified' && (!item.rtCritics || item.rtCritics < 75)) return false;
                if (state.rtCritics === 'top' && (!item.rtCritics || item.rtCritics < 90)) return false;
                if (state.rtAudience === 'fresh' && (!item.rtAudience || item.rtAudience < 60)) return false;
                if (state.rtAudience === 'high' && (!item.rtAudience || item.rtAudience < 85)) return false;

                if (state.decade === '2020s' && (!item.year || item.year < 2020)) return false;
                if (state.decade === '2010s' && (!item.year || item.year < 2010 || item.year > 2019)) return false;
                if (state.decade === 'classic' && (!item.year || item.year >= 2010)) return false;

                return true;
            }}).sort((a, b) => {{
                if (state.sort === 'imdb_desc') return (b.imdb || 0) - (a.imdb || 0) || a.title.localeCompare(b.title, 'pt-BR');
                if (state.sort === 'critics_desc') return (b.rtCritics || 0) - (a.rtCritics || 0) || a.title.localeCompare(b.title, 'pt-BR');
                if (state.sort === 'audience_desc') return (b.rtAudience || 0) - (a.rtAudience || 0) || a.title.localeCompare(b.title, 'pt-BR');
                if (state.sort === 'year_desc') return (b.year || 0) - (a.year || 0) || a.title.localeCompare(b.title, 'pt-BR');
                if (state.sort === 'alpha_asc') return a.title.localeCompare(b.title, 'pt-BR');

                const rank = {{ priority: 1, queue: 2, watched: 3 }};
                if (rank[a.status] !== rank[b.status]) return rank[a.status] - rank[b.status];
                return a.title.localeCompare(b.title, 'pt-BR');
            }});
        }}

        function getActiveFilterCount() {{
            let c = 0;
            if (state.search.trim()) c++;
            if (state.status !== 'all') c++;
            if (state.type !== 'all') c++;
            if (state.genre !== 'all') c++;
            if (state.origin !== 'all') c++;
            if (state.minImdb > 0) c++;
            if (state.rtCritics !== 'all') c++;
            if (state.rtAudience !== 'all') c++;
            if (state.decade !== 'all') c++;
            return c;
        }}

        function render() {{
            const list = getFilteredCatalog();
            const total = catalog.length;
            const watched = catalog.filter(i => i.status === 'watched').length;
            const priority = catalog.filter(i => i.status === 'priority').length;
            const queue = catalog.filter(i => i.status === 'queue').length;
            const series = catalog.filter(i => i.type === 'series').length;
            const pct = total > 0 ? Math.round((watched / total) * 100) : 0;

            // Telemetry
            document.getElementById('telemetry-text').textContent = `${{watched}} de ${{total}} assistidos (${{pct}}%)`;
            document.getElementById('telemetry-bar').style.width = `${{pct}}%`;

            // Tab counts
            const countMap = {{ all: total, priority, queue, watched, series }};
            document.querySelectorAll('[data-tab-count]').forEach(el => {{
                const k = el.getAttribute('data-tab-count');
                if (countMap[k] !== undefined) el.textContent = countMap[k];
            }});

            const filterCount = getActiveFilterCount();
            document.getElementById('header-filter-badge').classList.toggle('hidden', filterCount === 0);
            document.getElementById('bnav-filter-dot').classList.toggle('hidden', filterCount === 0);
            document.getElementById('modal-counter-badge').textContent = list.length;

            // Active filters bar
            const bar = document.getElementById('active-filters-bar');
            const chips = document.getElementById('active-chips-container');
            if (filterCount > 0) {{
                bar.classList.remove('hidden');
                let html = '';
                if (state.search) html += `<span class="px-2 py-0.5 rounded-md bg-white/[0.06] text-slate-300">"${{escapeHtml(state.search)}}"</span>`;
                if (state.status !== 'all') html += `<span class="px-2 py-0.5 rounded-md bg-white/[0.06] text-slate-300">Status: ${{state.status}}</span>`;
                if (state.genre !== 'all') html += `<span class="px-2 py-0.5 rounded-md bg-white/[0.06] text-slate-300">${{state.genre}}</span>`;
                if (state.minImdb > 0) html += `<span class="px-2 py-0.5 rounded-md bg-amber-500/15 text-amber-300 font-mono">IMDb ${{state.minImdb}}+</span>`;
                if (state.rtCritics !== 'all') html += `<span class="px-2 py-0.5 rounded-md bg-rose-500/15 text-rose-300 font-mono">🍅 Crítica</span>`;
                if (state.rtAudience !== 'all') html += `<span class="px-2 py-0.5 rounded-md bg-amber-400/15 text-amber-200 font-mono">🍿 Público</span>`;
                chips.innerHTML = `<span class="text-slate-500 mr-1">Filtros ativos:</span> ` + html;
            }} else {{
                bar.classList.add('hidden');
            }}

            const gridEl = document.getElementById('catalog-grid');
            const tableWrapperEl = document.getElementById('catalog-table-wrapper');
            const emptyEl = document.getElementById('empty-state');

            if (list.length === 0) {{
                gridEl.classList.add('hidden');
                tableWrapperEl.classList.add('hidden');
                emptyEl.classList.remove('hidden');
                return;
            }}
            emptyEl.classList.add('hidden');

            if (state.view === 'grid') {{
                tableWrapperEl.classList.add('hidden');
                gridEl.classList.remove('hidden');

                gridEl.innerHTML = list.map(item => {{
                    const dotColor = item.status === 'priority' ? 'bg-amber-400 shadow-[0_0_6px_#F59E0B]' : (item.status === 'watched' ? 'bg-emerald-400 shadow-[0_0_6px_#10B981]' : 'bg-slate-500');
                    const statusText = item.status === 'priority' ? 'Prioridade' : (item.status === 'watched' ? 'Concluído' : 'Na Fila');
                    const statusClass = item.status === 'priority' ? 'text-amber-300' : (item.status === 'watched' ? 'text-emerald-400' : 'text-slate-400');

                    return `
                        <div class="card-clean rounded-2xl p-4 flex flex-col justify-between group">
                            <div>
                                <!-- Top Row: Status Dot + Year / Series -->
                                <div class="flex items-center justify-between text-xs mb-2">
                                    <button onclick="cycleItemStatus('${{item.id}}')" class="inline-flex items-center gap-1.5 font-medium ${{statusClass}} hover:opacity-80 transition" title="Clique para alternar status">
                                        <span class="w-1.5 h-1.5 rounded-full ${{dotColor}}"></span>
                                        <span>${{statusText}}</span>
                                    </button>
                                    <div class="flex items-center gap-1.5 font-mono text-[11px] text-slate-500">
                                        ${{item.year ? `<span>${{item.year}}</span>` : ''}}
                                        ${{item.type === 'series' ? `<span class="text-[9px] uppercase tracking-wider px-1 py-0.2 rounded bg-purple-500/15 text-purple-300 border border-purple-500/20">Série</span>` : ''}}
                                    </div>
                                </div>

                                <!-- Title -->
                                <h3 onclick="openEditModal('${{item.id}}')" class="font-bold text-[15px] text-white leading-snug tracking-tight group-hover:text-purple-300 transition cursor-pointer mb-1">
                                    ${{escapeHtml(item.title)}}
                                </h3>

                                <!-- Genre -->
                                <p class="text-xs text-slate-400 truncate mb-3">
                                    <span>${{escapeHtml(item.genre)}}</span>
                                    ${{item.subgenre ? `<span class="text-slate-600"> · </span><span class="text-slate-500">${{escapeHtml(item.subgenre)}}</span>` : ''}}
                                </p>

                                <!-- Quiet Ratings Row (Clean, subtle, high-end) -->
                                <div class="flex items-center gap-2.5 text-xs font-mono mb-3">
                                    <span class="inline-flex items-center gap-1 text-amber-400/95" title="Nota IMDb">
                                        <span class="font-bold text-[10px] bg-amber-400/15 text-amber-300 px-1 py-0.5 rounded leading-none">IMDb</span>
                                        <span>${{item.imdb ? item.imdb.toFixed(1) : '—'}}</span>
                                    </span>
                                    <span class="text-slate-700">·</span>
                                    <span class="inline-flex items-center gap-1 text-rose-300/90" title="Rotten Tomatoes Crítica">
                                        <span>🍅</span>
                                        <span>${{item.rtCritics ? item.rtCritics + '%' : '—'}}</span>
                                    </span>
                                    <span class="text-slate-700">·</span>
                                    <span class="inline-flex items-center gap-1 text-amber-200/90" title="Rotten Tomatoes Público">
                                        <span>🍿</span>
                                        <span>${{item.rtAudience ? item.rtAudience + '%' : '—'}}</span>
                                    </span>
                                </div>

                                <!-- Optional Note -->
                                ${{item.note ? `
                                    <p class="text-[11px] text-slate-400 italic bg-white/[0.02] border border-white/[0.04] rounded-lg px-2.5 py-1 mb-2.5 truncate">
                                        "${{escapeHtml(item.note)}}"
                                    </p>
                                ` : ''}}
                            </div>

                            <!-- Bottom Row: Quick Status Cycle & Star Rating -->
                            <div class="pt-2.5 border-t border-white/[0.04] flex items-center justify-between text-xs">
                                <button onclick="cycleItemStatus('${{item.id}}')" class="h-7 px-2.5 rounded-lg bg-white/[0.03] hover:bg-white/[0.08] text-slate-400 hover:text-white transition text-[11px] flex items-center gap-1">
                                    <span>Mudar status</span>
                                </button>
                                
                                <div class="flex items-center">
                                    ${{buildMinimalStars(item)}}
                                </div>
                            </div>
                        </div>
                    `;
                }}).join('');
            }} else {{
                // Compact List View
                gridEl.classList.add('hidden');
                tableWrapperEl.classList.remove('hidden');

                tableWrapperEl.innerHTML = list.map(item => {{
                    const dotColor = item.status === 'priority' ? 'bg-amber-400 shadow-[0_0_6px_#F59E0B]' : (item.status === 'watched' ? 'bg-emerald-400 shadow-[0_0_6px_#10B981]' : 'bg-slate-500');
                    const statusText = item.status === 'priority' ? 'Prioridade' : (item.status === 'watched' ? 'Concluído' : 'Na Fila');
                    const statusClass = item.status === 'priority' ? 'text-amber-300' : (item.status === 'watched' ? 'text-emerald-400' : 'text-slate-400');

                    return `
                        <div class="p-3 sm:px-4 flex items-center justify-between gap-3 hover:bg-white/[0.02] transition">
                            <div class="min-w-0 flex-1 cursor-pointer" onclick="openEditModal('${{item.id}}')">
                                <div class="flex items-center gap-2 mb-0.5">
                                    <span class="w-2 h-2 rounded-full shrink-0 ${{dotColor}}"></span>
                                    <h4 class="font-semibold text-xs sm:text-sm text-white truncate">${{escapeHtml(item.title)}}</h4>
                                    ${{item.year ? `<span class="font-mono text-[11px] text-slate-500">(${{item.year}})</span>` : ''}}
                                    ${{item.type === 'series' ? `<span class="font-mono text-[9px] uppercase px-1 rounded bg-purple-500/15 text-purple-300 shrink-0">Série</span>` : ''}}
                                </div>
                                <div class="flex items-center gap-3 text-xs text-slate-400 pl-4">
                                    <span class="truncate">${{escapeHtml(item.genre)}}</span>
                                    <span class="text-slate-700">·</span>
                                    <span class="font-mono text-amber-400/90">★ ${{item.imdb ? item.imdb.toFixed(1) : '—'}}</span>
                                    <span class="font-mono text-rose-300/90">🍅 ${{item.rtCritics ? item.rtCritics + '%' : '—'}}</span>
                                    <span class="font-mono text-amber-200/90">🍿 ${{item.rtAudience ? item.rtAudience + '%' : '—'}}</span>
                                </div>
                            </div>
                            <div class="flex items-center gap-2 shrink-0">
                                <button onclick="cycleItemStatus('${{item.id}}')" class="h-8 px-2.5 rounded-lg border border-white/[0.08] text-[11px] font-medium ${{statusClass}} hover:bg-white/[0.04] transition">
                                    ${{statusText}}
                                </button>
                                <button onclick="openEditModal('${{item.id}}')" class="h-8 w-8 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] flex items-center justify-center text-slate-400 hover:text-white transition">
                                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                                </button>
                            </div>
                        </div>
                    `;
                }}).join('');
            }}
        }}

        function buildMinimalStars(item) {{
            let h = '';
            for (let s = 1; s <= 5; s++) {{
                const active = (item.rating || 0) >= s;
                h += `
                    <button onclick="setRating('${{item.id}}', ${{s}})" class="p-0.5 text-xs transition ${{active ? 'text-purple-400' : 'text-slate-700 hover:text-slate-400'}}">
                        ★
                    </button>
                `;
            }}
            return h;
        }}

        // Cycle status
        function cycleItemStatus(id) {{
            const item = catalog.find(i => i.id === id);
            if (!item) return;
            const seq = ['queue', 'priority', 'watched'];
            item.status = seq[(seq.indexOf(item.status) + 1) % seq.length];
            persist();
            render();
            notify(`${{item.title}}: ${{item.status === 'watched' ? 'Concluído' : (item.status === 'priority' ? 'Prioridade' : 'Na Fila')}}`);
        }}

        function setRating(id, stars) {{
            const item = catalog.find(i => i.id === id);
            if (!item) return;
            item.rating = item.rating === stars ? 0 : stars;
            persist();
            render();
            notify(item.rating > 0 ? `Avaliado com ${{item.rating}} estrela(s)` : 'Avaliação removida');
        }}

        // Filters
        function setStatusFilter(status) {{
            state.status = status;
            if (status !== 'all') state.type = 'all';
            syncStyles();
            render();
        }}

        function setTypeFilter(type) {{
            state.type = type;
            if (type !== 'all') state.status = 'all';
            syncStyles();
            render();
        }}

        function setGenreFilter(genre) {{
            state.genre = genre;
            syncStyles();
            render();
        }}

        function setOriginFilter(origin) {{
            state.origin = origin;
            syncStyles();
            render();
        }}

        function setMinImdb(score) {{
            state.minImdb = score;
            syncStyles();
            render();
        }}

        function setRtCritics(val) {{
            state.rtCritics = val;
            syncStyles();
            render();
        }}

        function setRtAudience(val) {{
            state.rtAudience = val;
            syncStyles();
            render();
        }}

        function setDecadeFilter(dec) {{
            state.decade = dec;
            syncStyles();
            render();
        }}

        function setSortOrder(sort) {{
            state.sort = sort;
            syncStyles();
            render();
        }}

        function setViewMode(mode) {{
            state.view = mode;
            syncStyles();
            render();
        }}

        function handleSearch(val) {{
            state.search = val;
            document.getElementById('clear-search-btn')?.classList.toggle('hidden', !val);
            render();
        }}

        function clearSearch() {{
            state.search = '';
            const inp = document.getElementById('search-input');
            if (inp) inp.value = '';
            document.getElementById('clear-search-btn')?.classList.add('hidden');
            render();
        }}

        function resetAllFilters() {{
            state.search = '';
            state.status = 'all';
            state.type = 'all';
            state.genre = 'all';
            state.origin = 'all';
            state.minImdb = 0;
            state.rtCritics = 'all';
            state.rtAudience = 'all';
            state.decade = 'all';
            state.sort = 'status';
            const inp = document.getElementById('search-input');
            if (inp) inp.value = '';
            document.getElementById('clear-search-btn')?.classList.add('hidden');
            syncStyles();
            render();
            notify("Filtros redefinidos");
        }}

        // Sync visual active states on pills
        function syncStyles() {{
            // Tabs
            document.querySelectorAll('.tab-pill').forEach(el => {{
                const tab = el.getAttribute('data-tab');
                const active = (tab === 'series') ? state.type === 'series' : (state.status === tab && state.type === 'all');
                el.classList.toggle('bg-white/[0.12]', active);
                el.classList.toggle('text-white', active);
                el.classList.toggle('text-slate-300', !active);
            }});

            // Mobile bnav
            document.querySelectorAll('[data-bnav]').forEach(el => {{
                const b = el.getAttribute('data-bnav');
                const active = state.status === b;
                el.classList.toggle('text-purple-400', active);
                el.classList.toggle('text-slate-400', !active);
            }});

            // Modal Pills
            document.querySelectorAll('[data-m-status]').forEach(el => {{
                const active = state.status === el.getAttribute('data-m-status');
                el.classList.toggle('bg-purple-600/25', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            }});

            document.querySelectorAll('[data-m-genre]').forEach(el => {{
                const active = state.genre === el.getAttribute('data-m-genre');
                el.classList.toggle('bg-purple-600/25', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            }});

            document.querySelectorAll('[data-m-imdb]').forEach(el => {{
                const active = state.minImdb === parseFloat(el.getAttribute('data-m-imdb'));
                el.classList.toggle('bg-amber-500/25', active);
                el.classList.toggle('border-amber-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            }});

            document.querySelectorAll('[data-m-rtcritics]').forEach(el => {{
                const active = state.rtCritics === el.getAttribute('data-m-rtcritics');
                el.classList.toggle('bg-rose-500/25', active);
                el.classList.toggle('border-rose-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            }});

            document.querySelectorAll('[data-m-rtaudience]').forEach(el => {{
                const active = state.rtAudience === el.getAttribute('data-m-rtaudience');
                el.classList.toggle('bg-amber-400/25', active);
                el.classList.toggle('border-amber-400/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            }});

            document.querySelectorAll('[data-m-origin]').forEach(el => {{
                const active = state.origin === el.getAttribute('data-m-origin');
                el.classList.toggle('bg-purple-600/25', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            }});

            document.querySelectorAll('[data-m-decade]').forEach(el => {{
                const active = state.decade === el.getAttribute('data-m-decade');
                el.classList.toggle('bg-purple-600/25', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            }});

            // View modes
            const isGrid = state.view === 'grid';
            document.getElementById('view-btn-grid')?.classList.toggle('text-white', isGrid);
            document.getElementById('view-btn-grid')?.classList.toggle('bg-white/[0.08]', isGrid);
            document.getElementById('view-btn-table')?.classList.toggle('text-white', !isGrid);
            document.getElementById('view-btn-table')?.classList.toggle('bg-white/[0.08]', !isGrid);

            const sortSel = document.getElementById('sort-select');
            if (sortSel) sortSel.value = state.sort;
        }}

        // Robust, clean modal opener / closer
        function openFilterModal() {{
            const m = document.getElementById('filter-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }}

        function closeFilterModal() {{
            const m = document.getElementById('filter-modal');
            m.classList.add('hidden');
            m.classList.remove('flex');
        }}

        function openRandomizerModal() {{
            const m = document.getElementById('randomizer-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }}

        function closeRandomizerModal() {{
            const m = document.getElementById('randomizer-modal');
            m.classList.add('hidden');
            m.classList.remove('flex');
        }}

        function runRandomizer() {{
            const pool = catalog.filter(i => i.status !== 'watched');
            if (pool.length === 0) return;

            const t = document.getElementById('rand-title');
            const meta = document.getElementById('rand-meta');
            const tag = document.getElementById('rand-tag');
            const ratings = document.getElementById('rand-ratings');

            tag.textContent = "Sorteando...";
            ratings.classList.add('hidden');

            let count = 0;
            const timer = setInterval(() => {{
                const item = pool[Math.floor(Math.random() * pool.length)];
                t.textContent = item.title;
                meta.textContent = `${{item.genre}} · ${{item.year || ''}}`;
                count++;
                if (count >= 14) {{
                    clearInterval(timer);
                    tag.textContent = item.status === 'priority' ? '★ Prioridade' : 'Na Fila';
                    ratings.innerHTML = `IMDb ${{item.imdb ? item.imdb.toFixed(1) : '-'}} · 🍅 ${{item.rtCritics || '-'}}% · 🍿 ${{item.rtAudience || '-'}}%`;
                    ratings.classList.remove('hidden');
                }}
            }}, 60);
        }}

        function openAddModal() {{
            document.getElementById('entry-modal-title').textContent = 'Nova Obra';
            document.getElementById('entry-id').value = '';
            document.getElementById('entry-form').reset();
            document.getElementById('delete-entry-btn').classList.add('hidden');
            const m = document.getElementById('entry-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }}

        function openEditModal(id) {{
            const item = catalog.find(i => i.id === id);
            if (!item) return;

            document.getElementById('entry-modal-title').textContent = 'Editar Obra';
            document.getElementById('entry-id').value = item.id;
            document.getElementById('entry-title').value = item.title;
            document.getElementById('entry-year').value = item.year || '';
            document.getElementById('entry-imdb').value = item.imdb !== null ? item.imdb : '';
            document.getElementById('entry-rt-critics').value = item.rtCritics !== null ? item.rtCritics : '';
            document.getElementById('entry-rt-audience').value = item.rtAudience !== null ? item.rtAudience : '';
            document.getElementById('entry-type').value = item.type;
            document.getElementById('entry-status').value = item.status;
            document.getElementById('entry-genre').value = item.genre;
            document.getElementById('entry-origin').value = item.origin;
            document.getElementById('entry-subgenre').value = item.subgenre || '';
            document.getElementById('entry-note').value = item.note || '';

            document.getElementById('delete-entry-btn').classList.remove('hidden');
            const m = document.getElementById('entry-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }}

        function closeAddModal() {{
            const m = document.getElementById('entry-modal');
            m.classList.add('hidden');
            m.classList.remove('flex');
        }}

        function saveEntryForm(e) {{
            e.preventDefault();
            const id = document.getElementById('entry-id').value;
            const title = document.getElementById('entry-title').value.trim();
            const yearVal = parseInt(document.getElementById('entry-year').value);
            const imdbVal = parseFloat(document.getElementById('entry-imdb').value);
            const rtCritVal = parseInt(document.getElementById('entry-rt-critics').value);
            const rtAudVal = parseInt(document.getElementById('entry-rt-audience').value);

            const payload = {{
                title,
                year: isNaN(yearVal) ? null : yearVal,
                imdb: isNaN(imdbVal) ? null : imdbVal,
                rtCritics: isNaN(rtCritVal) ? null : rtCritVal,
                rtAudience: isNaN(rtAudVal) ? null : rtAudVal,
                type: document.getElementById('entry-type').value,
                status: document.getElementById('entry-status').value,
                genre: document.getElementById('entry-genre').value,
                origin: document.getElementById('entry-origin').value,
                subgenre: document.getElementById('entry-subgenre').value.trim(),
                note: document.getElementById('entry-note').value.trim()
            }};

            if (id) {{
                const item = catalog.find(i => i.id === id);
                if (item) Object.assign(item, payload);
                notify(`"${{title}}" atualizado`);
            }} else {{
                catalog.unshift({{ id: 'custom_' + Date.now(), ...payload, rating: 0 }});
                notify(`"${{title}}" adicionado`);
            }}
            persist();
            render();
            closeAddModal();
        }}

        function deleteCurrentEntry() {{
            const id = document.getElementById('entry-id').value;
            if (!id) return;
            const item = catalog.find(i => i.id === id);
            if (!item) return;

            if (confirm(`Remover "${{item.title}}"?`)) {{
                catalog = catalog.filter(i => i.id !== id);
                persist();
                render();
                closeAddModal();
                notify(`"${{item.title}}" removido`);
            }}
        }}

        function openExportModal() {{
            document.getElementById('export-textarea').value = JSON.stringify(catalog, null, 2);
            const m = document.getElementById('export-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }}

        function closeExportModal() {{
            const m = document.getElementById('export-modal');
            m.classList.add('hidden');
            m.classList.remove('flex');
        }}

        function copyExportText() {{
            const ta = document.getElementById('export-textarea');
            ta.select();
            navigator.clipboard.writeText(ta.value).then(() => notify("JSON copiado!"));
        }}

        function downloadJson() {{
            const blob = new Blob([JSON.stringify(catalog, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cinevault_backup_${{new Date().toISOString().slice(0, 10)}}.json`;
            a.click();
            URL.revokeObjectURL(url);
            notify("Arquivo baixado!");
        }}

        function importJson(event) {{
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {{
                try {{
                    const data = JSON.parse(e.target.result);
                    if (Array.isArray(data)) {{
                        catalog = data;
                        persist();
                        render();
                        closeExportModal();
                        notify(`${{data.length}} títulos restaurados!`);
                    }}
                }} catch (err) {{
                    alert("JSON inválido");
                }}
            }};
            reader.readAsText(file);
        }}

        let toastTimer;
        function notify(text) {{
            const t = document.getElementById('toast');
            const txt = document.getElementById('toast-text');
            txt.textContent = text;
            t.classList.remove('hidden');
            requestAnimationFrame(() => t.classList.remove('translate-y-2', 'opacity-0'));
            clearTimeout(toastTimer);
            toastTimer = setTimeout(() => {{
                t.classList.add('translate-y-2', 'opacity-0');
                setTimeout(() => t.classList.add('hidden'), 200);
            }}, 2400);
        }}

        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(clean_html)

with open('cinevault_emannuel_petry.html', 'w', encoding='utf-8') as f:
    f.write(clean_html)

print("Both index.html and cinevault_emannuel_petry.html updated with clean UI!")
