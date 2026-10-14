# -*- coding: utf-8 -*-
"""
Build script to generate the enhanced Cinevault application.
Extremely optimized for mobile, rich multi-dimensional filters,
and subtle yet delightful IMDb and Rotten Tomatoes (Critics & Audience) ratings.
"""

import json
import re
from metadata_cinevault import METADATA

# 1. Parse raw items from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('const INITIAL_DATA = [')
end = text.find('];', start)
data_text = text[start:end]

items = []
pattern = re.compile(
    r"\{\s*id:\s*'([^']+)',\s*title:\s*'([^']+)',\s*type:\s*'([^']+)',\s*status:\s*'([^']+)',\s*genre:\s*'([^']+)',\s*subgenre:\s*'([^']*)',\s*origin:\s*'([^']+)',\s*note:\s*'([^']*)',\s*rating:\s*(\d+)\s*\}"
)

for line in data_text.splitlines():
    m = pattern.search(line)
    if m:
        item_id = m.group(1)
        meta = METADATA.get(item_id, {'year': 2020, 'imdb': 7.0, 'rtCritics': 80, 'rtAudience': 80})
        items.append({
            'id': item_id,
            'title': m.group(2),
            'type': m.group(3),
            'status': m.group(4),
            'genre': m.group(5),
            'subgenre': m.group(6),
            'origin': m.group(7),
            'note': m.group(8),
            'rating': int(m.group(9)),
            'year': meta['year'],
            'imdb': meta['imdb'],
            'rtCritics': meta['rtCritics'],
            'rtAudience': meta['rtAudience'],
        })

print(f"Loaded and enriched {len(items)} items.")

# Convert items to formatted JS array
js_items = json.dumps(items, ensure_ascii=False, indent=12)

# Build the complete HTML
html_content = f'''<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#07080D">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Cinevault">
    <title>Cinevault — Emannuel Petry</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    }},
                    colors: {{
                        surface: {{
                            950: '#07080D',
                            900: '#0E1017',
                            850: '#141722',
                            800: '#1B1E2B',
                            700: '#252A3C',
                            600: '#343B52'
                        }},
                        brand: {{
                            DEFAULT: '#820AD1',
                            light: '#9B30FF',
                            glow: 'rgba(130, 10, 209, 0.28)',
                            subtle: 'rgba(130, 10, 209, 0.12)'
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
            background-color: #07080D;
            color: #F8FAFC;
            overflow-x: hidden;
            overscroll-behavior-y: none;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11";
        }}
        /* Crisp 1px Borders & Elevated Surfaces */
        .border-subtle {{
            border-color: #1C202F;
        }}
        .border-subtle-light {{
            border-color: rgba(255, 255, 255, 0.08);
        }}
        .surface-card {{
            background-color: #0E1017;
            border: 1px solid #1C202F;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        @media (hover: hover) and (pointer: fine) {{
            .surface-card:hover {{
                border-color: #2F374E;
                background-color: #12151F;
                box-shadow: 0 16px 36px -12px rgba(0, 0, 0, 0.75), 0 0 20px -8px rgba(130, 10, 209, 0.18);
                transform: translateY(-2px);
            }}
        }}
        .surface-card:active {{
            transform: scale(0.995);
        }}
        /* Touch Targets & Safe Area */
        .touch-target {{
            min-height: 44px;
            min-width: 44px;
        }}
        .pb-safe {{
            padding-bottom: calc(5rem + env(safe-area-inset-bottom, 0px));
        }}
        .bottom-nav-safe {{
            padding-bottom: env(safe-area-inset-bottom, 0px);
        }}
        .sheet-safe {{
            padding-bottom: calc(1.75rem + env(safe-area-inset-bottom, 0px));
        }}
        /* Sleek Ambient Lighting */
        .header-gradient {{
            background: radial-gradient(circle at 18% 0%, rgba(130, 10, 209, 0.22) 0%, rgba(14, 16, 23, 0) 65%),
                        rgba(7, 8, 13, 0.92);
        }}
        /* Custom Scrollbars */
        ::-webkit-scrollbar {{
            width: 5px;
            height: 5px;
        }}
        ::-webkit-scrollbar-track {{
            background: #07080D;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #1C202F;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #2D354B;
        }}
        .no-scrollbar::-webkit-scrollbar {{
            display: none;
        }}
        .no-scrollbar {{
            -ms-overflow-style: none;
            scrollbar-width: none;
            -webkit-overflow-scrolling: touch;
        }}
        /* Active Filter Chip Pulse */
        .filter-chip-active {{
            background: linear-gradient(135deg, rgba(130, 10, 209, 0.25), rgba(155, 48, 255, 0.15));
            border-color: rgba(168, 85, 247, 0.45);
            color: #E9D5FF;
            box-shadow: 0 0 12px -2px rgba(130, 10, 209, 0.35);
        }}
        /* Ratings Micro Badge Badges */
        .rating-badge-imdb {{
            background: rgba(245, 197, 24, 0.10);
            border: 1px solid rgba(245, 197, 24, 0.26);
            color: #FACC15;
        }}
        .rating-badge-critics {{
            background: rgba(239, 68, 68, 0.10);
            border: 1px solid rgba(239, 68, 68, 0.26);
            color: #FCA5A5;
        }}
        .rating-badge-audience {{
            background: rgba(245, 158, 11, 0.10);
            border: 1px solid rgba(245, 158, 11, 0.26);
            color: #FDE68A;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col lg:flex-row selection:bg-brand selection:text-white">

    <!-- ================= DESKTOP SIDEBAR (HIDDEN ON MOBILE) ================= -->
    <aside class="hidden lg:flex lg:w-64 lg:fixed lg:inset-y-0 lg:left-0 bg-surface-900 border-r border-subtle flex-col justify-between z-30">
        <div class="overflow-y-auto no-scrollbar">
            <!-- Brand Header -->
            <div class="h-16 px-5 flex items-center justify-between border-b border-subtle">
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#820AD1] to-[#6D28D9] flex items-center justify-center shadow-lg border border-white/20">
                        <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
                            <line x1="7" y1="2" x2="7" y2="22"></line>
                            <line x1="17" y1="2" x2="17" y2="22"></line>
                            <line x1="2" y1="12" x2="22" y2="12"></line>
                            <line x1="2" y1="7" x2="7" y2="7"></line>
                            <line x1="2" y1="17" x2="7" y2="17"></line>
                            <line x1="17" y1="17" x2="22" y2="17"></line>
                            <line x1="17" y1="7" x2="22" y2="7"></line>
                        </svg>
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="font-bold text-sm tracking-tight text-white">Cinevault</span>
                            <span class="font-mono text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded bg-brand/20 text-purple-300 border border-purple-500/30">PRO</span>
                        </div>
                        <p class="text-[11px] text-slate-400">Emannuel Petry</p>
                    </div>
                </div>
            </div>

            <!-- Primary Views -->
            <div class="p-3">
                <div class="text-[10px] font-mono uppercase tracking-widest text-slate-500 px-2.5 mb-2">Visualizações</div>
                <nav class="flex flex-col gap-1">
                    <button onclick="setStatusFilter('all')" data-nav="all" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition">
                        <div class="flex items-center gap-2.5">
                            <svg class="w-4 h-4 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                            <span>Catálogo Completo</span>
                        </div>
                        <span data-count="all" class="font-mono text-[11px] text-slate-500">0</span>
                    </button>

                    <button onclick="setStatusFilter('pending')" data-nav="pending" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition">
                        <div class="flex items-center gap-2.5">
                            <svg class="w-4 h-4 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                            <span>Pendentes</span>
                        </div>
                        <span data-count="pending" class="font-mono text-[11px] text-slate-500">0</span>
                    </button>

                    <button onclick="setStatusFilter('priority')" data-nav="priority" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition">
                        <div class="flex items-center gap-2.5">
                            <span class="w-2 h-2 rounded-full bg-amber-400 shadow-[0_0_8px_#F59E0B]"></span>
                            <span>Prioridade</span>
                        </div>
                        <span data-count="priority" class="font-mono text-[11px] text-amber-400 font-semibold">0</span>
                    </button>

                    <button onclick="setStatusFilter('queue')" data-nav="queue" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition">
                        <div class="flex items-center gap-2.5">
                            <span class="w-2 h-2 rounded-full bg-slate-400"></span>
                            <span>Na Fila</span>
                        </div>
                        <span data-count="queue" class="font-mono text-[11px] text-slate-500">0</span>
                    </button>

                    <button onclick="setStatusFilter('watched')" data-nav="watched" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition">
                        <div class="flex items-center gap-2.5">
                            <span class="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#10B981]"></span>
                            <span>Concluídos</span>
                        </div>
                        <span data-count="watched" class="font-mono text-[11px] text-emerald-400 font-semibold">0</span>
                    </button>

                    <button onclick="setTypeFilter('series')" data-nav-type="series" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition">
                        <div class="flex items-center gap-2.5">
                            <svg class="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"></rect><polyline points="17 2 12 7 7 2"></polyline></svg>
                            <span>Séries e Docs</span>
                        </div>
                        <span data-count="series" class="font-mono text-[11px] text-purple-300 font-semibold">0</span>
                    </button>
                </nav>

                <!-- Filters Section -->
                <div class="mt-5 pt-4 border-t border-subtle">
                    <div class="flex items-center justify-between px-2.5 mb-2">
                        <span class="text-[10px] font-mono uppercase tracking-widest text-slate-500">Classificação Crítica</span>
                        <button onclick="clearRatingFilters()" class="text-[10px] text-purple-400 hover:underline">Limpar</button>
                    </div>
                    <div class="space-y-1">
                        <button onclick="setMinImdb(8.0)" data-filter-imdb="8.0" class="w-full flex items-center justify-between px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white transition">
                            <div class="flex items-center gap-2">
                                <span class="text-amber-400 font-bold">★</span>
                                <span>IMDb 8.0+ (Obras-primas)</span>
                            </div>
                            <span data-count-imdb="8" class="font-mono text-[10px] text-slate-500">0</span>
                        </button>
                        <button onclick="setMinImdb(7.5)" data-filter-imdb="7.5" class="w-full flex items-center justify-between px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white transition">
                            <div class="flex items-center gap-2">
                                <span class="text-amber-400">★</span>
                                <span>IMDb 7.5+ (Excelentes)</span>
                            </div>
                            <span data-count-imdb="7.5" class="font-mono text-[10px] text-slate-500">0</span>
                        </button>
                        <button onclick="setRtCritics('certified')" data-filter-rtcritics="certified" class="w-full flex items-center justify-between px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white transition">
                            <div class="flex items-center gap-2">
                                <span>🍅</span>
                                <span>Certified Fresh (≥75%)</span>
                            </div>
                            <span data-count-rtcritics="certified" class="font-mono text-[10px] text-slate-500">0</span>
                        </button>
                        <button onclick="setRtAudience('high')" data-filter-rtaudience="high" class="w-full flex items-center justify-between px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white transition">
                            <div class="flex items-center gap-2">
                                <span>🍿</span>
                                <span>Aprovado Público (≥85%)</span>
                            </div>
                            <span data-count-rtaudience="high" class="font-mono text-[10px] text-slate-500">0</span>
                        </button>
                    </div>
                </div>

                <!-- Origin Filter -->
                <div class="mt-5 pt-4 border-t border-subtle">
                    <div class="text-[10px] font-mono uppercase tracking-widest text-slate-500 px-2.5 mb-2">Origem da Curadoria</div>
                    <div class="flex flex-col gap-1">
                        <button onclick="setOriginFilter('all')" data-origin="all" class="origin-item flex items-center justify-between px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white transition">
                            <span>Todas as Origens</span>
                        </button>
                        <button onclick="setOriginFilter('user')" data-origin="user" class="origin-item flex items-center justify-between px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white transition">
                            <span>Catálogo Pessoal (Manu)</span>
                        </button>
                        <button onclick="setOriginFilter('brother')" data-origin="brother" class="origin-item flex items-center justify-between px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white transition">
                            <span>Indicação Irmão</span>
                        </button>
                        <button onclick="setOriginFilter('both')" data-origin="both" class="origin-item flex items-center justify-between px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-white transition">
                            <span>Em Ambos</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bottom Completion Progress -->
        <div class="p-4 border-t border-subtle bg-surface-950/80">
            <div class="mb-3">
                <div class="flex items-center justify-between text-xs mb-1.5">
                    <span class="text-slate-400 font-medium">Índice de Conclusão</span>
                    <span id="sidebar-percent" class="font-mono text-xs text-emerald-400 font-semibold">0%</span>
                </div>
                <div class="w-full h-1.5 bg-surface-800 rounded-full overflow-hidden">
                    <div id="sidebar-progress" class="h-full bg-gradient-to-r from-[#820AD1] via-purple-500 to-emerald-400 transition-all duration-500" style="width: 0%"></div>
                </div>
            </div>
            <div class="flex items-center justify-between pt-2 border-t border-subtle text-[11px] text-slate-500">
                <span>Persistência Local</span>
                <button onclick="openResetModal()" class="text-slate-400 hover:text-white underline transition">Restaurar</button>
            </div>
        </div>
    </aside>

    <!-- ================= SLIDE-OVER MOBILE DRAWER ================= -->
    <div id="mobile-drawer-backdrop" onclick="closeMobileDrawer()" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-sm transition-opacity lg:hidden"></div>
    <aside id="mobile-drawer" class="fixed inset-y-0 left-0 z-50 w-72 max-w-[85vw] bg-surface-900 border-r border-subtle flex flex-col justify-between transform -translate-x-full transition-transform duration-200 ease-out lg:hidden">
        <div class="overflow-y-auto no-scrollbar">
            <!-- Drawer Header -->
            <div class="h-16 px-4 flex items-center justify-between border-b border-subtle">
                <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-[#820AD1] to-[#6D28D9] flex items-center justify-center border border-white/20">
                        <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line></svg>
                    </div>
                    <div>
                        <span class="font-bold text-sm text-white block leading-none">Cinevault</span>
                        <span class="text-[10px] text-slate-400">Emannuel Petry</span>
                    </div>
                </div>
                <button onclick="closeMobileDrawer()" class="p-2 rounded-lg text-slate-400 hover:text-white bg-surface-800 border border-subtle" aria-label="Fechar menu">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <!-- Drawer Navigation -->
            <div class="p-3">
                <div class="text-[10px] font-mono uppercase tracking-widest text-slate-500 px-2.5 mb-2">Visualizações</div>
                <nav class="flex flex-col gap-1">
                    <button onclick="setStatusFilter('all'); closeMobileDrawer();" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium">
                        <span>Catálogo Completo</span>
                        <span data-count="all" class="font-mono text-[11px] text-slate-500">0</span>
                    </button>
                    <button onclick="setStatusFilter('pending'); closeMobileDrawer();" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium">
                        <span>Pendentes</span>
                        <span data-count="pending" class="font-mono text-[11px] text-slate-500">0</span>
                    </button>
                    <button onclick="setStatusFilter('priority'); closeMobileDrawer();" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium">
                        <span class="text-amber-300">★ Prioridade</span>
                        <span data-count="priority" class="font-mono text-[11px] text-amber-400">0</span>
                    </button>
                    <button onclick="setStatusFilter('queue'); closeMobileDrawer();" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium">
                        <span>Na Fila</span>
                        <span data-count="queue" class="font-mono text-[11px] text-slate-500">0</span>
                    </button>
                    <button onclick="setStatusFilter('watched'); closeMobileDrawer();" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium">
                        <span class="text-emerald-300">✓ Concluídos</span>
                        <span data-count="watched" class="font-mono text-[11px] text-emerald-400">0</span>
                    </button>
                    <button onclick="setTypeFilter('series'); closeMobileDrawer();" class="nav-item flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium">
                        <span class="text-purple-300">📺 Séries e Docs</span>
                        <span data-count="series" class="font-mono text-[11px] text-purple-300">0</span>
                    </button>
                </nav>

                <div class="mt-4 pt-3 border-t border-subtle">
                    <button onclick="openFilterSheet(); closeMobileDrawer();" class="w-full py-2.5 px-3 rounded-xl bg-surface-800 hover:bg-surface-700 border border-subtle text-xs font-medium text-purple-300 flex items-center justify-between">
                        <span class="flex items-center gap-2">
                            <svg class="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line></svg>
                            <span>Filtros Completos</span>
                        </span>
                        <span id="drawer-filter-badge" class="px-1.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 text-[10px] font-mono">0</span>
                    </button>
                </div>

                <div class="mt-4 pt-3 border-t border-subtle flex flex-col gap-2">
                    <button onclick="openRandomizerModal(); closeMobileDrawer();" class="w-full py-2 px-3 rounded-lg bg-brand/20 border border-purple-500/30 text-purple-200 text-xs font-medium text-left flex items-center gap-2">
                        <span>🎲</span> <span>Sortear Filme/Série</span>
                    </button>
                    <button onclick="openExportModal(); closeMobileDrawer();" class="w-full py-2 px-3 rounded-lg bg-surface-800 text-slate-300 text-xs font-medium text-left flex items-center gap-2">
                        <span>📦</span> <span>Exportar / Backup</span>
                    </button>
                </div>
            </div>
        </div>

        <div class="p-4 border-t border-subtle bg-surface-950/80">
            <div class="flex items-center justify-between text-xs mb-1.5">
                <span class="text-slate-400">Progresso</span>
                <span id="drawer-percent" class="font-mono text-emerald-400 font-semibold">0%</span>
            </div>
            <div class="w-full h-1.5 bg-surface-800 rounded-full overflow-hidden">
                <div id="drawer-progress" class="h-full bg-gradient-to-r from-[#820AD1] to-emerald-400" style="width: 0%"></div>
            </div>
        </div>
    </aside>

    <!-- ================= MAIN WRAPPER ================= -->
    <div class="flex-1 lg:pl-64 flex flex-col min-h-screen">

        <!-- ================= STICKY TOP HEADER ================= -->
        <header class="header-gradient border-b border-subtle sticky top-0 z-20 backdrop-blur-xl">
            <div class="max-w-7xl mx-auto px-3.5 sm:px-6 lg:px-8 pt-3 pb-2.5 sm:py-3.5">

                <!-- Mobile Top Brand Bar (< 1024px) -->
                <div class="flex lg:hidden items-center justify-between mb-2.5">
                    <div class="flex items-center gap-2">
                        <button onclick="openMobileDrawer()" class="p-2 -ml-1 rounded-lg text-slate-300 hover:text-white active:bg-surface-800 touch-target flex items-center justify-center" aria-label="Abrir Menu">
                            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
                        </button>
                        <div class="flex items-center gap-2">
                            <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-[#820AD1] to-[#6D28D9] flex items-center justify-center border border-white/20 shadow-md">
                                <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line></svg>
                            </div>
                            <span class="font-bold text-sm tracking-tight text-white">Cinevault</span>
                            <span class="font-mono text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded bg-brand/20 text-purple-300 border border-purple-500/30">PRO</span>
                        </div>
                    </div>

                    <div class="flex items-center gap-1.5">
                        <!-- View Toggle (Grid / Compact) -->
                        <div class="inline-flex rounded-lg bg-surface-900 p-0.5 border border-subtle">
                            <button onclick="setViewMode('grid')" id="mobile-view-grid" class="p-1.5 rounded-md text-slate-400 transition" aria-label="Visualização em Grade">
                                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                            </button>
                            <button onclick="setViewMode('table')" id="mobile-view-table" class="p-1.5 rounded-md text-slate-400 transition" aria-label="Visualização em Lista">
                                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
                            </button>
                        </div>

                        <!-- Filter Bottom Sheet Trigger -->
                        <button onclick="openFilterSheet()" class="relative p-2 rounded-lg bg-surface-900 border border-subtle text-slate-300 active:bg-surface-800 touch-target flex items-center justify-center" aria-label="Abrir Filtros">
                            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                            <span id="mobile-filter-badge" class="hidden absolute -top-1 -right-1 w-4 h-4 rounded-full bg-purple-600 text-white text-[9px] font-bold font-mono flex items-center justify-center shadow-md">0</span>
                        </button>

                        <button onclick="openAddModal()" class="h-8 px-2.5 rounded-lg bg-[#820AD1] active:bg-[#9B30FF] text-white text-xs font-medium flex items-center gap-1 shadow-sm">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                            <span>Novo</span>
                        </button>
                    </div>
                </div>

                <!-- Search & Action Bar -->
                <div class="flex items-center justify-between gap-2.5">
                    <div class="relative flex-1 max-w-xl">
                        <svg class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                        <input 
                            type="text" 
                            id="search-input"
                            oninput="handleSearch(this.value)"
                            placeholder="Buscar título, gênero, ano, plataforma, nota..." 
                            class="w-full pl-10 pr-12 py-2 sm:py-2.5 bg-surface-900 border border-subtle rounded-xl text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 transition shadow-inner"
                        >
                        <div class="absolute right-2.5 top-1/2 -translate-y-1/2 flex items-center gap-1">
                            <button id="clear-search-btn" onclick="clearSearch()" class="hidden p-1 text-slate-400 hover:text-white" aria-label="Limpar busca">
                                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                            </button>
                            <kbd class="hidden sm:inline-block font-mono text-[10px] text-slate-500 bg-surface-800 border border-subtle px-1.5 py-0.5 rounded">/</kbd>
                        </div>
                    </div>

                    <!-- Desktop Actions -->
                    <div class="hidden lg:flex items-center gap-2">
                        <button onclick="openFilterSheet()" class="relative inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-surface-900 hover:bg-surface-800 border border-subtle text-slate-200 text-xs font-medium transition">
                            <svg class="w-3.5 h-3.5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                            <span>Filtros Avançados</span>
                            <span id="desktop-filter-count" class="hidden px-1.5 py-0.2 rounded-full bg-purple-500/20 text-purple-300 font-mono text-[10px]">0</span>
                        </button>

                        <button onclick="openRandomizerModal()" class="inline-flex items-center gap-2 px-3.5 py-2 rounded-lg bg-[#820AD1] hover:bg-[#9B30FF] text-white text-xs font-medium shadow-md transition">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
                            <span>Sortear</span>
                        </button>

                        <button onclick="openAddModal()" class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-surface-800 hover:bg-surface-700 border border-subtle text-slate-200 text-xs font-medium transition">
                            <svg class="w-3.5 h-3.5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                            <span>Novo</span>
                        </button>

                        <button onclick="openExportModal()" class="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-surface-800 hover:bg-surface-700 border border-subtle text-slate-200 text-xs font-medium transition">
                            <svg class="w-3.5 h-3.5 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            <span>Exportar</span>
                        </button>
                    </div>
                </div>

                <!-- Fast Horizontal Quick Filter Chips (Momentum Scrolling) -->
                <div class="mt-2.5 pt-2 border-t border-subtle flex items-center justify-between gap-2">
                    <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5 -mx-1 px-1 flex-1" id="quick-filter-bar">
                        <button onclick="setStatusFilter('all')" data-quick="status:all" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-slate-300 hover:text-white transition">
                            Todos
                        </button>
                        <button onclick="toggleQuickFilter('status', 'priority')" data-quick="status:priority" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-amber-300/90 hover:text-amber-300 transition flex items-center gap-1.5">
                            <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
                            <span>Prioridades</span>
                        </button>
                        <button onclick="toggleQuickFilter('minImdb', 8.0)" data-quick="minImdb:8.0" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-yellow-300/90 hover:text-yellow-300 transition flex items-center gap-1">
                            <span class="text-amber-400 font-bold">★</span>
                            <span>IMDb 8.0+</span>
                        </button>
                        <button onclick="toggleQuickFilter('rtCritics', 'top')" data-quick="rtCritics:top" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-rose-300 hover:text-rose-200 transition flex items-center gap-1">
                            <span>🍅</span>
                            <span>Top Crítica 90%+</span>
                        </button>
                        <button onclick="toggleQuickFilter('rtAudience', 'high')" data-quick="rtAudience:high" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-amber-200 hover:text-white transition flex items-center gap-1">
                            <span>🍿</span>
                            <span>Aprovados Público 85%+</span>
                        </button>
                        <button onclick="toggleQuickFilter('status', 'pending')" data-quick="status:pending" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-slate-300 hover:text-white transition">
                            Pendentes
                        </button>
                        <button onclick="toggleQuickFilter('type', 'movie')" data-quick="type:movie" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-slate-300 hover:text-white transition">
                            Filmes
                        </button>
                        <button onclick="toggleQuickFilter('type', 'series')" data-quick="type:series" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-purple-300 hover:text-purple-200 transition">
                            Séries
                        </button>
                        <button onclick="toggleQuickFilter('status', 'watched')" data-quick="status:watched" class="quick-chip px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap bg-surface-900 border border-subtle text-emerald-300/90 hover:text-emerald-300 transition flex items-center gap-1.5">
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                            <span>Concluídos</span>
                        </button>
                    </div>

                    <!-- Desktop Sort & View Toggle -->
                    <div class="hidden lg:flex items-center gap-2 shrink-0">
                        <select id="desktop-sort-select" onchange="setSortOrder(this.value)" class="bg-surface-900 border border-subtle rounded-lg px-2.5 py-1.5 text-xs text-slate-300 focus:outline-none focus:border-purple-500">
                            <option value="status">Ordenar: Prioridade</option>
                            <option value="imdb_desc">Ordenar: Maior IMDb ★</option>
                            <option value="critics_desc">Ordenar: Maior Crítica 🍅</option>
                            <option value="audience_desc">Ordenar: Maior Público 🍿</option>
                            <option value="year_desc">Ordenar: Mais Recentes</option>
                            <option value="alpha_asc">Ordenar: A — Z</option>
                            <option value="rating_desc">Ordenar: Minha Avaliação</option>
                        </select>

                        <div class="inline-flex rounded-lg bg-surface-900 p-0.5 border border-subtle">
                            <button onclick="setViewMode('grid')" id="view-btn-grid" class="p-1.5 rounded-md text-slate-400 hover:text-white transition" title="Grade">
                                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                            </button>
                            <button onclick="setViewMode('table')" id="view-btn-table" class="p-1.5 rounded-md text-slate-400 hover:text-white transition" title="Lista Compacta">
                                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </header>

        <!-- ================= MAIN WORKSPACE ================= -->
        <main class="flex-1 max-w-7xl w-full mx-auto px-3.5 sm:px-6 lg:px-8 py-3.5 sm:py-5 pb-safe">

            <!-- Compact KPI Bar -->
            <div class="grid grid-cols-4 gap-2 sm:gap-3 mb-3.5 sm:mb-5">
                <div onclick="setStatusFilter('all')" class="cursor-pointer surface-card rounded-xl p-2.5 sm:p-3 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] sm:text-[11px] font-medium text-slate-400 block truncate">Total</span>
                        <span id="kpi-total" class="font-mono text-sm sm:text-lg font-bold text-white block">0</span>
                    </div>
                    <span class="text-xs text-slate-500 font-mono">100%</span>
                </div>

                <div onclick="setStatusFilter('priority')" class="cursor-pointer surface-card rounded-xl p-2.5 sm:p-3 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] sm:text-[11px] font-medium text-amber-300/90 block truncate">Prioridade</span>
                        <span id="kpi-priority" class="font-mono text-sm sm:text-lg font-bold text-amber-400 block">0</span>
                    </div>
                    <span class="w-2 h-2 rounded-full bg-amber-400 shadow-[0_0_8px_#F59E0B]"></span>
                </div>

                <div onclick="setStatusFilter('queue')" class="cursor-pointer surface-card rounded-xl p-2.5 sm:p-3 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] sm:text-[11px] font-medium text-slate-400 block truncate">Na Fila</span>
                        <span id="kpi-queue" class="font-mono text-sm sm:text-lg font-bold text-slate-300 block">0</span>
                    </div>
                    <span class="w-2 h-2 rounded-full bg-slate-500"></span>
                </div>

                <div onclick="setStatusFilter('watched')" class="cursor-pointer surface-card rounded-xl p-2.5 sm:p-3 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] sm:text-[11px] font-medium text-emerald-300/90 block truncate">Concluídos</span>
                        <span id="kpi-watched" class="font-mono text-sm sm:text-lg font-bold text-emerald-400 block">0</span>
                    </div>
                    <span id="kpi-watched-pct" class="font-mono text-xs text-emerald-400 font-semibold">0%</span>
                </div>
            </div>

            <!-- Active Filters Indicators & Results Summary -->
            <div class="mb-3.5 flex flex-wrap items-center justify-between gap-2 text-xs">
                <div class="flex items-center gap-1.5 flex-wrap" id="active-filter-tags">
                    <!-- Injected dynamically -->
                </div>
                <div class="flex items-center gap-2 ml-auto">
                    <span id="results-counter" class="text-[11px] font-mono text-slate-400">Exibindo 0 registros</span>
                    <button id="clear-all-filters-btn" onclick="resetAllFilters()" class="hidden text-[11px] text-purple-400 hover:text-purple-300 underline font-medium">
                        Limpar todos
                    </button>
                </div>
            </div>

            <!-- 1. Catalog Grid View -->
            <div id="catalog-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-3.5">
                <!-- Injected dynamically via render() -->
            </div>

            <!-- 2. Catalog Table / Compact List View -->
            <div id="catalog-table-wrapper" class="hidden">
                <!-- Mobile Compact Spotify-style List -->
                <div id="catalog-mobile-list" class="lg:hidden divide-y divide-subtle surface-card rounded-xl overflow-hidden">
                    <!-- Injected dynamically via render() -->
                </div>

                <!-- Desktop Multi-column Table -->
                <div class="hidden lg:block surface-card rounded-xl overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-xs">
                            <thead class="bg-surface-950/90 text-slate-400 font-mono text-[10px] uppercase tracking-wider border-b border-subtle">
                                <tr>
                                    <th class="py-3 px-4">Título & Formato</th>
                                    <th class="py-3 px-3">Gênero / Plataforma</th>
                                    <th class="py-3 px-3 text-center">Ano</th>
                                    <th class="py-3 px-3 text-center">Avaliações (IMDb • 🍅 • 🍿)</th>
                                    <th class="py-3 px-3">Origem</th>
                                    <th class="py-3 px-3">Minha Avaliação</th>
                                    <th class="py-3 px-4 text-right">Status / Ações</th>
                                </tr>
                            </thead>
                            <tbody id="catalog-table-body" class="divide-y divide-subtle">
                                <!-- Injected dynamically via render() -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div id="empty-state" class="hidden py-16 text-center">
                <div class="w-14 h-14 rounded-2xl bg-surface-850 border border-subtle flex items-center justify-center mx-auto mb-3 text-slate-500">
                    <svg class="w-7 h-7" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                </div>
                <h3 class="text-sm font-semibold text-white mb-1">Nenhum título encontrado</h3>
                <p class="text-xs text-slate-400 max-w-xs mx-auto mb-4">Nenhum registro corresponde aos filtros ou termo de busca atuais.</p>
                <button onclick="resetAllFilters()" class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-medium transition shadow-md">
                    Limpar todos os filtros
                </button>
            </div>

        </main>
    </div>

    <!-- ================= FIXED MOBILE BOTTOM NAVIGATION BAR (< 1024px) ================= -->
    <nav class="lg:hidden fixed bottom-0 inset-x-0 z-30 bg-[#07080D]/95 backdrop-blur-xl border-t border-subtle bottom-nav-safe">
        <div class="grid grid-cols-5 h-16 max-w-md mx-auto px-1">
            <button onclick="setStatusFilter('all')" data-bnav="all" class="bnav-item flex flex-col items-center justify-center gap-1 text-slate-400 transition active:scale-95 touch-target">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                <span class="text-[10px] font-medium tracking-tight">Catálogo</span>
            </button>

            <button onclick="setStatusFilter('priority')" data-bnav="priority" class="bnav-item flex flex-col items-center justify-center gap-1 text-slate-400 transition active:scale-95 touch-target">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                <span class="text-[10px] font-medium tracking-tight">Prioridade</span>
            </button>

            <!-- Elevated Central Randomizer Action -->
            <button onclick="openRandomizerModal()" class="flex flex-col items-center justify-center gap-1 text-purple-300 active:scale-90 transition touch-target">
                <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#820AD1] to-[#6D28D9] text-white flex items-center justify-center shadow-lg border border-purple-400/40 -mt-3.5">
                    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
                </div>
                <span class="text-[10px] font-semibold tracking-tight text-purple-300">Sortear</span>
            </button>

            <button onclick="openFilterSheet()" class="relative flex flex-col items-center justify-center gap-1 text-slate-400 hover:text-white transition active:scale-95 touch-target">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                <span class="text-[10px] font-medium tracking-tight">Filtros</span>
                <span id="bnav-filter-dot" class="hidden absolute top-2 right-4 w-2 h-2 rounded-full bg-purple-500 shadow-[0_0_6px_#A855F7]"></span>
            </button>

            <button onclick="setStatusFilter('watched')" data-bnav="watched" class="bnav-item flex flex-col items-center justify-center gap-1 text-slate-400 transition active:scale-95 touch-target">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                <span class="text-[10px] font-medium tracking-tight">Vistos</span>
            </button>
        </div>
    </nav>

    <!-- ================= ADVANCED FILTER BOTTOM SHEET (MOBILE & DESKTOP) ================= -->
    <div id="filter-sheet-backdrop" onclick="closeFilterSheet()" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-sm transition-opacity"></div>
    <div id="filter-sheet" class="fixed inset-x-0 bottom-0 z-50 transform translate-y-full transition-transform duration-200 ease-out max-h-[88vh] bg-surface-900 border-t border-subtle rounded-t-3xl flex flex-col sheet-safe sm:max-w-xl sm:mx-auto sm:rounded-2xl sm:bottom-auto sm:top-1/2 sm:-translate-y-1/2 sm:translate-x-0 shadow-2xl overflow-hidden">
        
        <!-- Sheet Handle for Mobile Touch -->
        <div class="pt-3 pb-1 flex justify-center sm:hidden">
            <div class="w-12 h-1.5 bg-surface-700 rounded-full"></div>
        </div>

        <!-- Sheet Header -->
        <div class="px-5 py-3.5 border-b border-subtle flex items-center justify-between">
            <div class="flex items-center gap-2.5">
                <div class="w-7 h-7 rounded-lg bg-brand/20 border border-purple-500/30 flex items-center justify-center text-purple-300">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                </div>
                <div>
                    <h2 class="text-sm font-semibold text-white">Filtros & Ordenação</h2>
                    <p class="text-[11px] text-slate-400">Refine por nota, status, gênero e métricas</p>
                </div>
            </div>
            <button onclick="closeFilterSheet()" class="p-2 rounded-lg text-slate-400 hover:text-white bg-surface-800 border border-subtle touch-target flex items-center justify-center">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
        </div>

        <!-- Sheet Content (Scrollable) -->
        <div class="px-5 py-4 overflow-y-auto space-y-4 no-scrollbar flex-1 text-xs">

            <!-- 1. Ordenação Principal -->
            <div>
                <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Critério de Ordenação</label>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-1.5">
                    <button onclick="setSortOrder('status')" data-sheet-sort="status" class="sheet-sort-btn px-3 py-2 rounded-xl border text-left font-medium transition">
                        Prioridade (Padrão)
                    </button>
                    <button onclick="setSortOrder('imdb_desc')" data-sheet-sort="imdb_desc" class="sheet-sort-btn px-3 py-2 rounded-xl border text-left font-medium transition text-amber-300/90">
                        Maior Nota IMDb ★
                    </button>
                    <button onclick="setSortOrder('critics_desc')" data-sheet-sort="critics_desc" class="sheet-sort-btn px-3 py-2 rounded-xl border text-left font-medium transition text-rose-300">
                        Maior Tomatometer 🍅
                    </button>
                    <button onclick="setSortOrder('audience_desc')" data-sheet-sort="audience_desc" class="sheet-sort-btn px-3 py-2 rounded-xl border text-left font-medium transition text-amber-200">
                        Maior Popcornmeter 🍿
                    </button>
                    <button onclick="setSortOrder('year_desc')" data-sheet-sort="year_desc" class="sheet-sort-btn px-3 py-2 rounded-xl border text-left font-medium transition">
                        Mais Recentes (Ano)
                    </button>
                    <button onclick="setSortOrder('alpha_asc')" data-sheet-sort="alpha_asc" class="sheet-sort-btn px-3 py-2 rounded-xl border text-left font-medium transition">
                        Título (A — Z)
                    </button>
                </div>
            </div>

            <!-- 2. Status de Visualização -->
            <div>
                <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Status</label>
                <div class="grid grid-cols-3 sm:grid-cols-5 gap-1.5">
                    <button onclick="setStatusFilter('all')" data-sheet-status="all" class="sheet-status-btn px-2.5 py-2 rounded-xl border font-medium text-center transition">
                        Todos
                    </button>
                    <button onclick="setStatusFilter('pending')" data-sheet-status="pending" class="sheet-status-btn px-2.5 py-2 rounded-xl border font-medium text-center transition">
                        Pendentes
                    </button>
                    <button onclick="setStatusFilter('priority')" data-sheet-status="priority" class="sheet-status-btn px-2.5 py-2 rounded-xl border font-medium text-center transition text-amber-300">
                        ★ Prioridade
                    </button>
                    <button onclick="setStatusFilter('queue')" data-sheet-status="queue" class="sheet-status-btn px-2.5 py-2 rounded-xl border font-medium text-center transition">
                        Na Fila
                    </button>
                    <button onclick="setStatusFilter('watched')" data-sheet-status="watched" class="sheet-status-btn px-2.5 py-2 rounded-xl border font-medium text-center transition text-emerald-400">
                        ✓ Concluídos
                    </button>
                </div>
            </div>

            <!-- 3. Nota IMDb Mínima -->
            <div>
                <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2 flex items-center justify-between">
                    <span>Nota Mínima no IMDb</span>
                    <span id="sheet-imdb-display" class="text-amber-400 font-mono font-bold">Qualquer</span>
                </label>
                <div class="grid grid-cols-4 gap-1.5">
                    <button onclick="setMinImdb(0)" data-sheet-imdb="0" class="sheet-imdb-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Todas
                    </button>
                    <button onclick="setMinImdb(7.0)" data-sheet-imdb="7.0" class="sheet-imdb-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        ★ 7.0+
                    </button>
                    <button onclick="setMinImdb(7.5)" data-sheet-imdb="7.5" class="sheet-imdb-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        ★ 7.5+
                    </button>
                    <button onclick="setMinImdb(8.0)" data-sheet-imdb="8.0" class="sheet-imdb-btn px-2 py-2 rounded-xl border text-center font-medium transition text-amber-300">
                        ★ 8.0+
                    </button>
                </div>
            </div>

            <!-- 4. Rotten Tomatoes (Crítica / Tomatometer) -->
            <div>
                <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Rotten Tomatoes — Crítica (Tomatometer 🍅)</label>
                <div class="grid grid-cols-3 gap-1.5">
                    <button onclick="setRtCritics('all')" data-sheet-rtcritics="all" class="sheet-rtcritics-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Qualquer
                    </button>
                    <button onclick="setRtCritics('certified')" data-sheet-rtcritics="certified" class="sheet-rtcritics-btn px-2 py-2 rounded-xl border text-center font-medium transition text-rose-300">
                        🍅 Certified (≥75%)
                    </button>
                    <button onclick="setRtCritics('top')" data-sheet-rtcritics="top" class="sheet-rtcritics-btn px-2 py-2 rounded-xl border text-center font-medium transition text-rose-300">
                        🍅 Top Tier (≥90%)
                    </button>
                </div>
            </div>

            <!-- 5. Rotten Tomatoes (Público / Popcornmeter) -->
            <div>
                <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Rotten Tomatoes — Público (Popcornmeter 🍿)</label>
                <div class="grid grid-cols-3 gap-1.5">
                    <button onclick="setRtAudience('all')" data-sheet-rtaudience="all" class="sheet-rtaudience-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Qualquer
                    </button>
                    <button onclick="setRtAudience('fresh')" data-sheet-rtaudience="fresh" class="sheet-rtaudience-btn px-2 py-2 rounded-xl border text-center font-medium transition text-amber-200">
                        🍿 Aprovado (≥60%)
                    </button>
                    <button onclick="setRtAudience('high')" data-sheet-rtaudience="high" class="sheet-rtaudience-btn px-2 py-2 rounded-xl border text-center font-medium transition text-amber-200">
                        🍿 Favorito (≥85%)
                    </button>
                </div>
            </div>

            <!-- 6. Gêneros & Categorias -->
            <div>
                <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Gênero Principal</label>
                <div class="flex flex-wrap gap-1.5" id="sheet-genre-pills">
                    <button onclick="setGenreFilter('all')" data-sheet-genre="all" class="sheet-genre-btn px-3 py-1.5 rounded-full border text-xs font-medium transition">
                        Todos os Gêneros
                    </button>
                    <button onclick="setGenreFilter('Suspense & Thriller')" data-sheet-genre="Suspense & Thriller" class="sheet-genre-btn px-3 py-1.5 rounded-full border text-xs font-medium transition">
                        Suspense & Thriller
                    </button>
                    <button onclick="setGenreFilter('Drama & Biografia')" data-sheet-genre="Drama & Biografia" class="sheet-genre-btn px-3 py-1.5 rounded-full border text-xs font-medium transition">
                        Drama & Biografia
                    </button>
                    <button onclick="setGenreFilter('Ação & Ficção')" data-sheet-genre="Ação & Ficção" class="sheet-genre-btn px-3 py-1.5 rounded-full border text-xs font-medium transition">
                        Ação & Ficção
                    </button>
                    <button onclick="setGenreFilter('Terror')" data-sheet-genre="Terror" class="sheet-genre-btn px-3 py-1.5 rounded-full border text-xs font-medium transition">
                        Terror
                    </button>
                    <button onclick="setGenreFilter('Comédia')" data-sheet-genre="Comédia" class="sheet-genre-btn px-3 py-1.5 rounded-full border text-xs font-medium transition">
                        Comédia
                    </button>
                    <button onclick="setGenreFilter('Série / Doc')" data-sheet-genre="Série / Doc" class="sheet-genre-btn px-3 py-1.5 rounded-full border text-xs font-medium transition">
                        Série / Doc
                    </button>
                </div>
            </div>

            <!-- 7. Década / Época -->
            <div>
                <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Década de Lançamento</label>
                <div class="grid grid-cols-5 gap-1.5">
                    <button onclick="setDecadeFilter('all')" data-sheet-decade="all" class="sheet-decade-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Todas
                    </button>
                    <button onclick="setDecadeFilter('2020s')" data-sheet-decade="2020s" class="sheet-decade-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        2020+
                    </button>
                    <button onclick="setDecadeFilter('2010s')" data-sheet-decade="2010s" class="sheet-decade-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        2010s
                    </button>
                    <button onclick="setDecadeFilter('2000s')" data-sheet-decade="2000s" class="sheet-decade-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        2000s
                    </button>
                    <button onclick="setDecadeFilter('classic')" data-sheet-decade="classic" class="sheet-decade-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Clássicos
                    </button>
                </div>
            </div>

            <!-- 8. Origem da Curadoria -->
            <div>
                <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Origem da Curadoria</label>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-1.5">
                    <button onclick="setOriginFilter('all')" data-sheet-origin="all" class="sheet-origin-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Todas
                    </button>
                    <button onclick="setOriginFilter('user')" data-sheet-origin="user" class="sheet-origin-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Manu (Pessoal)
                    </button>
                    <button onclick="setOriginFilter('brother')" data-sheet-origin="brother" class="sheet-origin-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Irmão
                    </button>
                    <button onclick="setOriginFilter('both')" data-sheet-origin="both" class="sheet-origin-btn px-2 py-2 rounded-xl border text-center font-medium transition">
                        Ambos
                    </button>
                </div>
            </div>
        </div>

        <!-- Sheet Sticky Footer Actions -->
        <div class="px-5 py-3 border-t border-subtle bg-surface-950 flex items-center justify-between gap-3">
            <button onclick="resetAllFilters()" class="h-11 px-4 rounded-xl bg-surface-800 hover:bg-surface-700 text-slate-300 font-medium text-xs transition">
                Limpar Tudo
            </button>
            <button onclick="closeFilterSheet()" class="flex-1 h-11 px-5 rounded-xl bg-[#820AD1] hover:bg-[#9B30FF] active:scale-[0.99] text-white font-semibold text-xs transition shadow-lg flex items-center justify-center gap-2">
                <span>Ver Resultados</span>
                <span id="sheet-apply-counter" class="px-2 py-0.5 rounded-full bg-white/20 text-[11px] font-mono">0</span>
            </button>
        </div>
    </div>

    <!-- ================= MODALS ================= -->

    <!-- 1. RANDOMIZER MODAL (ENHANCED WITH RATINGS POOL) -->
    <div id="randomizer-modal" class="fixed inset-0 z-50 hidden flex items-end sm:items-center justify-center sm:p-4 bg-black/80 backdrop-blur-sm">
        <div class="bg-surface-900 border-t sm:border border-subtle rounded-t-3xl sm:rounded-2xl max-w-md w-full p-5 sm:p-6 sheet-safe sm:pb-6 shadow-2xl">
            <div class="w-10 h-1 bg-surface-700 rounded-full mx-auto mb-3 sm:hidden"></div>
            <div class="flex items-center justify-between pb-3.5 border-b border-subtle mb-4">
                <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-xl bg-brand/20 border border-purple-500/30 flex items-center justify-center text-purple-300 shadow-inner">
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
                    </div>
                    <div>
                        <h2 class="text-sm font-semibold text-white">Sorteador Cinematográfico</h2>
                        <p class="text-[11px] text-slate-400">Escolha com critérios inteligentes</p>
                    </div>
                </div>
                <button onclick="closeRandomizerModal()" class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-surface-800 transition">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <div class="grid grid-cols-2 gap-3 mb-4">
                <div>
                    <label class="text-[11px] font-medium text-slate-400 block mb-1">Escopo</label>
                    <select id="rand-pool" class="w-full bg-surface-950 border border-subtle rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500">
                        <option value="pending">Todos Pendentes</option>
                        <option value="priority">Apenas Prioridade ★</option>
                        <option value="queue">Apenas Na Fila</option>
                        <option value="series">Apenas Séries</option>
                        <option value="top_rated">Top Rated (IMDb 7.5+)</option>
                    </select>
                </div>
                <div>
                    <label class="text-[11px] font-medium text-slate-400 block mb-1">Categoria</label>
                    <select id="rand-genre" class="w-full bg-surface-950 border border-subtle rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500">
                        <option value="all">Todas</option>
                        <option value="Suspense & Thriller">Suspense & Thriller</option>
                        <option value="Drama & Biografia">Drama & Biografia</option>
                        <option value="Ação & Ficção">Ação & Ficção</option>
                        <option value="Terror">Terror</option>
                        <option value="Comédia">Comédia</option>
                    </select>
                </div>
            </div>

            <div class="bg-surface-950 border border-subtle rounded-2xl p-5 text-center min-h-[160px] flex flex-col items-center justify-center mb-4 transition-all">
                <span id="rand-status-tag" class="font-mono text-[10px] uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-surface-800 text-slate-400 border border-subtle mb-2">
                    Pronto para Sorteio
                </span>
                <h3 id="rand-title" class="text-base font-bold text-white mb-1.5">
                    Defina o filtro e sortear
                </h3>
                
                <!-- Ratings display on randomizer winner -->
                <div id="rand-ratings" class="hidden flex items-center justify-center gap-2 mb-2"></div>

                <p id="rand-meta" class="text-xs text-slate-400"></p>

                <div id="rand-actions" class="hidden mt-3 pt-3 border-t border-subtle w-full flex justify-center gap-2">
                    <button id="rand-mark-watched" class="px-4 py-2 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/30 text-emerald-300 text-xs font-semibold flex items-center gap-1.5 transition">
                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <span>Marcar como Concluído</span>
                    </button>
                </div>
            </div>

            <button onclick="runRandomizer()" class="w-full h-12 rounded-xl bg-[#820AD1] hover:bg-[#9B30FF] active:scale-[0.99] text-white font-semibold text-xs transition flex items-center justify-center gap-2 shadow-lg">
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline></svg>
                <span>Girar Roleta Cinematográfica</span>
            </button>
        </div>
    </div>

    <!-- 2. ADD / EDIT MODAL -->
    <div id="entry-modal" class="fixed inset-0 z-50 hidden flex items-end sm:items-center justify-center sm:p-4 bg-black/80 backdrop-blur-sm">
        <div class="bg-surface-900 border-t sm:border border-subtle rounded-t-3xl sm:rounded-2xl max-w-md w-full p-5 sm:p-6 sheet-safe sm:pb-6 shadow-2xl max-h-[92vh] overflow-y-auto no-scrollbar">
            <div class="w-10 h-1 bg-surface-700 rounded-full mx-auto mb-3 sm:hidden"></div>
            <div class="flex items-center justify-between pb-3.5 border-b border-subtle mb-4">
                <h2 id="entry-modal-title" class="text-sm font-semibold text-white">Editar Obra</h2>
                <button onclick="closeAddModal()" class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-surface-800 transition">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <form id="entry-form" onsubmit="saveEntryForm(event)" class="space-y-3.5">
                <input type="hidden" id="entry-id">

                <div>
                    <label class="text-[11px] font-medium text-slate-400 block mb-1">Título da Obra *</label>
                    <input type="text" id="entry-title" required placeholder="Ex: Oppenheimer" class="w-full bg-surface-950 border border-subtle rounded-xl px-3 py-2.5 text-xs text-white focus:outline-none focus:border-purple-500">
                </div>

                <div class="grid grid-cols-3 gap-2.5">
                    <div>
                        <label class="text-[11px] font-medium text-slate-400 block mb-1">Ano</label>
                        <input type="number" id="entry-year" placeholder="2024" class="w-full bg-surface-950 border border-subtle rounded-xl px-2.5 py-2 text-xs text-white focus:outline-none focus:border-purple-500 font-mono">
                    </div>
                    <div>
                        <label class="text-[11px] font-medium text-slate-400 block mb-1">Formato</label>
                        <select id="entry-type" class="w-full bg-surface-950 border border-subtle rounded-xl px-2.5 py-2 text-xs text-white focus:outline-none focus:border-purple-500">
                            <option value="movie">Filme</option>
                            <option value="series">Série / Doc</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-[11px] font-medium text-slate-400 block mb-1">Status</label>
                        <select id="entry-status" class="w-full bg-surface-950 border border-subtle rounded-xl px-2.5 py-2 text-xs text-white focus:outline-none focus:border-purple-500">
                            <option value="priority">Prioridade</option>
                            <option value="queue">Na Fila</option>
                            <option value="watched">Concluído</option>
                        </select>
                    </div>
                </div>

                <!-- Subtle Ratings Input Row -->
                <div class="p-3 rounded-xl bg-surface-950 border border-subtle">
                    <span class="text-[10px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Avaliações Públicas</span>
                    <div class="grid grid-cols-3 gap-2">
                        <div>
                            <label class="text-[10px] text-amber-300 font-medium block mb-1">IMDb (0-10)</label>
                            <input type="number" step="0.1" min="0" max="10" id="entry-imdb" placeholder="8.2" class="w-full bg-surface-900 border border-subtle rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-amber-400 font-mono">
                        </div>
                        <div>
                            <label class="text-[10px] text-rose-300 font-medium block mb-1">🍅 Crítica (%)</label>
                            <input type="number" min="0" max="100" id="entry-rt-critics" placeholder="92" class="w-full bg-surface-900 border border-subtle rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-rose-400 font-mono">
                        </div>
                        <div>
                            <label class="text-[10px] text-amber-200 font-medium block mb-1">🍿 Público (%)</label>
                            <input type="number" min="0" max="100" id="entry-rt-audience" placeholder="88" class="w-full bg-surface-900 border border-subtle rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-amber-400 font-mono">
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="text-[11px] font-medium text-slate-400 block mb-1">Categoria</label>
                        <select id="entry-genre" class="w-full bg-surface-950 border border-subtle rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500">
                            <option value="Suspense & Thriller">Suspense & Thriller</option>
                            <option value="Drama & Biografia">Drama & Biografia</option>
                            <option value="Ação & Ficção">Ação & Ficção</option>
                            <option value="Terror">Terror</option>
                            <option value="Comédia">Comédia</option>
                            <option value="Série / Doc">Série / Doc</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-[11px] font-medium text-slate-400 block mb-1">Origem</label>
                        <select id="entry-origin" class="w-full bg-surface-950 border border-subtle rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500">
                            <option value="user">Manu (Pessoal)</option>
                            <option value="brother">Irmão</option>
                            <option value="both">Ambos</option>
                        </select>
                    </div>
                </div>

                <div>
                    <label class="text-[11px] font-medium text-slate-400 block mb-1">Subgênero / Plataforma</label>
                    <input type="text" id="entry-subgenre" placeholder="Ex: Thriller Psicológico • Max" class="w-full bg-surface-950 border border-subtle rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500">
                </div>

                <div>
                    <label class="text-[11px] font-medium text-slate-400 block mb-1">Anotação Pessoal</label>
                    <input type="text" id="entry-note" placeholder="Ex: Assistir no fim de semana..." class="w-full bg-surface-950 border border-subtle rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500">
                </div>

                <div class="pt-3 border-t border-subtle flex justify-between items-center gap-2">
                    <button type="button" id="delete-entry-btn" onclick="deleteCurrentEntry()" class="hidden h-10 px-3.5 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/20 text-xs font-medium transition">
                        Excluir
                    </button>
                    <div class="flex gap-2 ml-auto">
                        <button type="button" onclick="closeAddModal()" class="h-10 px-4 rounded-xl bg-surface-800 hover:bg-surface-700 text-xs font-medium text-slate-300 transition">
                            Cancelar
                        </button>
                        <button type="submit" class="h-10 px-5 rounded-xl bg-[#820AD1] hover:bg-[#9B30FF] text-xs font-medium text-white transition shadow-md">
                            Salvar
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- 3. EXPORT / BACKUP MODAL -->
    <div id="export-modal" class="fixed inset-0 z-50 hidden flex items-end sm:items-center justify-center sm:p-4 bg-black/80 backdrop-blur-sm">
        <div class="bg-surface-900 border-t sm:border border-subtle rounded-t-3xl sm:rounded-2xl max-w-lg w-full p-5 sm:p-6 sheet-safe sm:pb-6 shadow-2xl">
            <div class="w-10 h-1 bg-surface-700 rounded-full mx-auto mb-3 sm:hidden"></div>
            <div class="flex items-center justify-between pb-3.5 border-b border-subtle mb-4">
                <div>
                    <h3 class="text-sm font-semibold text-white">Exportação e Backup</h3>
                    <p class="text-[11px] text-slate-400">Guarde seus status e notas em formato JSON</p>
                </div>
                <button onclick="closeExportModal()" class="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-surface-800 transition">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <textarea id="export-textarea" readonly class="w-full h-40 bg-surface-950 border border-subtle rounded-xl p-3 font-mono text-[11px] text-slate-300 focus:outline-none mb-3 resize-none"></textarea>

            <div class="flex flex-wrap gap-2 justify-between">
                <div class="flex gap-2">
                    <button onclick="copyExportText()" class="h-10 px-3.5 rounded-xl bg-surface-800 hover:bg-surface-700 border border-subtle text-xs font-medium text-slate-200 transition flex items-center gap-1.5">
                        <svg class="w-3.5 h-3.5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        <span>Copiar JSON</span>
                    </button>
                    <button onclick="downloadJson()" class="h-10 px-3.5 rounded-xl bg-surface-800 hover:bg-surface-700 border border-subtle text-xs font-medium text-slate-200 transition flex items-center gap-1.5">
                        <svg class="w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                        <span>Baixar Arquivo</span>
                    </button>
                </div>
                <label class="h-10 px-3.5 rounded-xl bg-[#820AD1] hover:bg-[#9B30FF] text-white text-xs font-medium transition cursor-pointer flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
                    <span>Restaurar Backup</span>
                    <input type="file" accept=".json" onchange="importJson(event)" class="hidden">
                </label>
            </div>
        </div>
    </div>

    <!-- 4. RESET MODAL -->
    <div id="reset-modal" class="fixed inset-0 z-50 hidden flex items-end sm:items-center justify-center sm:p-4 bg-black/80 backdrop-blur-sm">
        <div class="bg-surface-900 border-t sm:border border-subtle rounded-t-3xl sm:rounded-2xl max-w-sm w-full p-5 sm:p-6 sheet-safe sm:pb-6 shadow-2xl">
            <h3 class="text-sm font-semibold text-white mb-1">Restaurar Base Original</h3>
            <p class="text-xs text-slate-400 mb-5 leading-relaxed">Esta ação redefinirá todos os status, avaliações e notas para a lista original de 217 registros com todas as notas IMDb e Rotten Tomatoes.</p>
            <div class="flex justify-end gap-2">
                <button onclick="closeResetModal()" class="h-10 px-4 rounded-xl bg-surface-800 hover:bg-surface-700 text-xs font-medium text-slate-300 transition">
                    Cancelar
                </button>
                <button onclick="confirmFactoryReset()" class="h-10 px-4 rounded-xl bg-rose-600 hover:bg-rose-500 text-xs font-medium text-white transition shadow-md">
                    Confirmar Restauração
                </button>
            </div>
        </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div id="toast" class="fixed bottom-20 lg:bottom-6 right-4 lg:right-6 z-50 hidden transform transition-all duration-200 translate-y-2 opacity-0 pointer-events-none">
        <div class="bg-surface-800/95 backdrop-blur-md border border-white/15 text-slate-100 px-4 py-2.5 rounded-xl shadow-2xl flex items-center gap-2.5 text-xs font-medium">
            <span class="w-2 h-2 rounded-full bg-purple-400 shadow-[0_0_8px_#A855F7]"></span>
            <span id="toast-text">Alteração registrada</span>
        </div>
    </div>

    <!-- ================= JAVASCRIPT LOGIC ================= -->
    <script>
        const STORAGE_KEY = 'cinevault_v3_state';
        const LEGACY_KEYS = ['cinevault_v2_state', 'cinevault_emannuel_petry_v2', 'cinevault_v1'];

        // Complete Enriched Dataset (217 items with IMDb, RT Critics, RT Audience, Year)
        const INITIAL_DATA = {js_items};

        let catalog = [];
        let state = {{
            search: '',
            status: 'all',        // all | pending | priority | queue | watched
            type: 'all',          // all | movie | series
            genre: 'all',         // all | 'Suspense & Thriller' | 'Drama & Biografia' | etc.
            origin: 'all',        // all | user | brother | both
            minImdb: 0,           // 0 | 7.0 | 7.5 | 8.0
            rtCritics: 'all',     // all | certified (>=75%) | top (>=90%)
            rtAudience: 'all',    // all | fresh (>=60%) | high (>=85%)
            decade: 'all',        // all | 2020s | 2010s | 2000s | classic
            sort: 'status',       // status | imdb_desc | critics_desc | audience_desc | year_desc | alpha_asc | rating_desc
            view: 'grid'          // grid | table
        }};

        // Initialization with seamless migration of existing saved user data
        function init() {{
            try {{
                let raw = localStorage.getItem(STORAGE_KEY);
                if (!raw) {{
                    for (const legacyKey of LEGACY_KEYS) {{
                        const legacyData = localStorage.getItem(legacyKey);
                        if (legacyData) {{
                            raw = legacyData;
                            break;
                        }}
                    }}
                }}

                if (raw) {{
                    const parsed = JSON.parse(raw);
                    if (Array.isArray(parsed) && parsed.length > 0) {{
                        // Merge with INITIAL_DATA to ensure all items have imdb, rtCritics, rtAudience, year
                        catalog = parsed.map(item => {{
                            const initial = INITIAL_DATA.find(i => i.id === item.id) || {{}};
                            return {{
                                ...initial,
                                ...item,
                                year: item.year || initial.year || 2020,
                                imdb: item.imdb !== undefined ? item.imdb : (initial.imdb || null),
                                rtCritics: item.rtCritics !== undefined ? item.rtCritics : (initial.rtCritics || null),
                                rtAudience: item.rtAudience !== undefined ? item.rtAudience : (initial.rtAudience || null),
                            }};
                        }});

                        // If new entries exist in INITIAL_DATA that weren't in parsed
                        const existingIds = new Set(catalog.map(c => c.id));
                        for (const initItem of INITIAL_DATA) {{
                            if (!existingIds.has(initItem.id)) {{
                                catalog.push(JSON.parse(JSON.stringify(initItem)));
                            }}
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
                console.error("Init fallback to INITIAL_DATA:", e);
                catalog = JSON.parse(JSON.stringify(INITIAL_DATA));
            }}

            // Desktop search keyboard shortcut '/'
            window.addEventListener('keydown', (e) => {{
                if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {{
                    e.preventDefault();
                    document.getElementById('search-input').focus();
                }}
            }});

            syncNavigationStyles();
            render();
        }}

        function persist() {{
            try {{
                localStorage.setItem(STORAGE_KEY, JSON.stringify(catalog));
            }} catch (err) {{
                console.error('Storage persistence failed:', err);
            }}
        }}

        // Helper string escapes
        function escapeHtml(str) {{
            if (!str) return '';
            return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
        }}

        function getOriginLabel(code) {{
            if (code === 'user') return 'Manu';
            if (code === 'both') return 'Ambos';
            return 'Irmão';
        }}

        // Telemetry Counters Update
        function updateCounters() {{
            const total = catalog.length;
            const priority = catalog.filter(i => i.status === 'priority').length;
            const queue = catalog.filter(i => i.status === 'queue').length;
            const watched = catalog.filter(i => i.status === 'watched').length;
            const pending = priority + queue;
            const series = catalog.filter(i => i.type === 'series').length;
            const pct = total > 0 ? Math.round((watched / total) * 100) : 0;

            const imdb8 = catalog.filter(i => (i.imdb || 0) >= 8.0).length;
            const imdb75 = catalog.filter(i => (i.imdb || 0) >= 7.5).length;
            const rtCritCert = catalog.filter(i => (i.rtCritics || 0) >= 75).length;
            const rtAudHigh = catalog.filter(i => (i.rtAudience || 0) >= 85).length;

            document.getElementById('kpi-total').textContent = total;
            document.getElementById('kpi-priority').textContent = priority;
            document.getElementById('kpi-queue').textContent = queue;
            document.getElementById('kpi-watched').textContent = watched;
            document.getElementById('kpi-watched-pct').textContent = `${{pct}}%`;

            // Sidebar & Drawer counts
            const countMap = {{
                all: total,
                pending,
                priority,
                queue,
                watched,
                series
            }};
            document.querySelectorAll('[data-count]').forEach(el => {{
                const key = el.getAttribute('data-count');
                if (countMap[key] !== undefined) el.textContent = countMap[key];
            }});

            const imdbCountMap = {{ '8': imdb8, '7.5': imdb75 }};
            document.querySelectorAll('[data-count-imdb]').forEach(el => {{
                const key = el.getAttribute('data-count-imdb');
                if (imdbCountMap[key] !== undefined) el.textContent = imdbCountMap[key];
            }});

            const rtCritEl = document.querySelector('[data-count-rtcritics="certified"]');
            if (rtCritEl) rtCritEl.textContent = rtCritCert;
            const rtAudEl = document.querySelector('[data-count-rtaudience="high"]');
            if (rtAudEl) rtAudEl.textContent = rtAudHigh;

            // Progress bars
            document.getElementById('sidebar-percent').textContent = `${{pct}}%`;
            document.getElementById('sidebar-progress').style.width = `${{pct}}%`;
            document.getElementById('drawer-percent').textContent = `${{pct}}%`;
            document.getElementById('drawer-progress').style.width = `${{pct}}%`;
        }}

        // Active Filter Count
        function getActiveFilterCount() {{
            let count = 0;
            if (state.search.trim() !== '') count++;
            if (state.status !== 'all') count++;
            if (state.type !== 'all') count++;
            if (state.genre !== 'all') count++;
            if (state.origin !== 'all') count++;
            if (state.minImdb > 0) count++;
            if (state.rtCritics !== 'all') count++;
            if (state.rtAudience !== 'all') count++;
            if (state.decade !== 'all') count++;
            return count;
        }}

        // Filter and Sort Engine
        function getFilteredCatalog() {{
            return catalog.filter(item => {{
                // Search query
                if (state.search) {{
                    const q = state.search.toLowerCase().trim();
                    const inTitle = (item.title || '').toLowerCase().includes(q);
                    const inSub = (item.subgenre || '').toLowerCase().includes(q);
                    const inGenre = (item.genre || '').toLowerCase().includes(q);
                    const inNote = (item.note || '').toLowerCase().includes(q);
                    const inYear = String(item.year || '').includes(q);
                    if (!inTitle && !inSub && !inGenre && !inNote && !inYear) return false;
                }}

                // Status
                if (state.status === 'priority' && item.status !== 'priority') return false;
                if (state.status === 'queue' && item.status !== 'queue') return false;
                if (state.status === 'watched' && item.status !== 'watched') return false;
                if (state.status === 'pending' && (item.status !== 'priority' && item.status !== 'queue')) return false;

                // Type (movie vs series)
                if (state.type === 'movie' && item.type !== 'movie') return false;
                if (state.type === 'series' && item.type !== 'series') return false;

                // Genre
                if (state.genre !== 'all' && item.genre !== state.genre) return false;

                // Origin
                if (state.origin !== 'all' && item.origin !== state.origin) return false;

                // IMDb minimum rating
                if (state.minImdb > 0 && (!item.imdb || item.imdb < state.minImdb)) return false;

                // Rotten Critics (Tomatometer)
                if (state.rtCritics === 'certified' && (!item.rtCritics || item.rtCritics < 75)) return false;
                if (state.rtCritics === 'top' && (!item.rtCritics || item.rtCritics < 90)) return false;
                if (state.rtCritics === 'fresh' && (!item.rtCritics || item.rtCritics < 60)) return false;

                // Rotten Audience (Popcornmeter)
                if (state.rtAudience === 'fresh' && (!item.rtAudience || item.rtAudience < 60)) return false;
                if (state.rtAudience === 'high' && (!item.rtAudience || item.rtAudience < 85)) return false;

                // Decade
                if (state.decade === '2020s' && (!item.year || item.year < 2020)) return false;
                if (state.decade === '2010s' && (!item.year || item.year < 2010 || item.year > 2019)) return false;
                if (state.decade === '2000s' && (!item.year || item.year < 2000 || item.year > 2009)) return false;
                if (state.decade === 'classic' && (!item.year || item.year >= 2000)) return false;

                return true;
            }}).sort((a, b) => {{
                // Sorting orders
                if (state.sort === 'imdb_desc') {{
                    return (b.imdb || 0) - (a.imdb || 0) || a.title.localeCompare(b.title, 'pt-BR');
                }}
                if (state.sort === 'critics_desc') {{
                    return (b.rtCritics || 0) - (a.rtCritics || 0) || a.title.localeCompare(b.title, 'pt-BR');
                }}
                if (state.sort === 'audience_desc') {{
                    return (b.rtAudience || 0) - (a.rtAudience || 0) || a.title.localeCompare(b.title, 'pt-BR');
                }}
                if (state.sort === 'year_desc') {{
                    return (b.year || 0) - (a.year || 0) || a.title.localeCompare(b.title, 'pt-BR');
                }}
                if (state.sort === 'alpha_asc') {{
                    return a.title.localeCompare(b.title, 'pt-BR');
                }}
                if (state.sort === 'rating_desc') {{
                    return (b.rating || 0) - (a.rating || 0) || a.title.localeCompare(b.title, 'pt-BR');
                }}
                
                // Default: Priority -> Queue -> Watched -> Alphabetical
                const rank = {{ priority: 1, queue: 2, watched: 3 }};
                if (rank[a.status] !== rank[b.status]) {{
                    return rank[a.status] - rank[b.status];
                }}
                return a.title.localeCompare(b.title, 'pt-BR');
            }});
        }}

        // Subtle Ratings Micro-Row Generator
        function buildRatingsRow(item, isCompact = false) {{
            let html = '';
            
            // IMDb
            if (item.imdb) {{
                html += `
                    <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-md rating-badge-imdb text-[11px] font-mono font-semibold" title="Nota IMDb: ${{item.imdb}}">
                        <span class="bg-[#F5C518] text-black font-sans font-black text-[9px] px-1 py-0.2 rounded-sm leading-none">IMDb</span>
                        <span>${{item.imdb.toFixed(1)}}</span>
                    </span>
                `;
            }}

            // Rotten Tomatoes Critics (Tomatometer)
            if (item.rtCritics !== undefined && item.rtCritics !== null) {{
                const icon = item.rtCritics >= 75 ? '🍅' : (item.rtCritics >= 60 ? '🍅' : '🟢');
                html += `
                    <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-md rating-badge-critics text-[11px] font-mono font-medium" title="Rotten Tomatoes Crítica (Tomatometer): ${{item.rtCritics}}%">
                        <span>${{icon}}</span>
                        <span>${{item.rtCritics}}%</span>
                    </span>
                `;
            }}

            // Rotten Tomatoes Audience (Popcornmeter)
            if (item.rtAudience !== undefined && item.rtAudience !== null) {{
                const icon = item.rtAudience >= 60 ? '🍿' : '🍿';
                html += `
                    <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-md rating-badge-audience text-[11px] font-mono font-medium" title="Rotten Tomatoes Público (Popcornmeter): ${{item.rtAudience}}%">
                        <span>${{icon}}</span>
                        <span>${{item.rtAudience}}%</span>
                    </span>
                `;
            }}

            // Release Year Badge
            if (item.year && !isCompact) {{
                html += `
                    <span class="inline-flex items-center px-1.5 py-0.5 rounded-md bg-surface-800 text-slate-400 border border-subtle text-[10px] font-mono">
                        ${{item.year}}
                    </span>
                `;
            }}

            return html;
        }}

        // Star Rating Generator
        function buildStarsHtml(item) {{
            let html = '';
            for (let s = 1; s <= 5; s++) {{
                const active = (item.rating || 0) >= s;
                html += `
                    <button onclick="setRating('${{item.id}}', ${{s}})" title="Avaliar ${{s}}/5" class="p-1 touch-target flex items-center justify-center transition ${{active ? 'text-purple-400 scale-105' : 'text-slate-700 hover:text-slate-400'}}">
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="${{active ? 'currentColor' : 'none'}}" stroke="currentColor" stroke-width="1.75">
                            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                        </svg>
                    </button>
                `;
            }}
            return html;
        }}

        // Status Badge Generator
        function buildStatusBadge(status) {{
            if (status === 'priority') {{
                return `<span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11px] font-medium bg-amber-500/15 text-amber-300 border border-amber-500/30">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-400 shadow-[0_0_6px_#F59E0B]"></span>Prioridade
                </span>`;
            }}
            if (status === 'watched') {{
                return `<span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11px] font-medium bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_6px_#10B981]"></span>Concluído
                </span>`;
            }}
            return `<span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md text-[11px] font-medium bg-surface-800 text-slate-300 border border-subtle">
                <span class="w-1.5 h-1.5 rounded-full bg-slate-400"></span>Na Fila
            </span>`;
        }}

        // Cycle Status on 1-tap
        function cycleItemStatus(id) {{
            const item = catalog.find(i => i.id === id);
            if (!item) return;
            const order = ['queue', 'priority', 'watched'];
            const next = order[(order.indexOf(item.status) + 1) % order.length];
            setItemStatus(id, next);
        }}

        // Main Render Function
        function render() {{
            updateCounters();
            const list = getFilteredCatalog();

            const gridEl = document.getElementById('catalog-grid');
            const tableWrapperEl = document.getElementById('catalog-table-wrapper');
            const mobileListEl = document.getElementById('catalog-mobile-list');
            const tableBodyEl = document.getElementById('catalog-table-body');
            const emptyEl = document.getElementById('empty-state');
            const counterEl = document.getElementById('results-counter');
            const clearAllBtn = document.getElementById('clear-all-filters-btn');
            const activeFilterTagsEl = document.getElementById('active-filter-tags');

            const filterCount = getActiveFilterCount();
            clearAllBtn.classList.toggle('hidden', filterCount === 0);
            counterEl.textContent = `Exibindo ${{list.length}} de ${{catalog.length}} registros`;
            document.getElementById('sheet-apply-counter').textContent = list.length;

            // Badges on filter buttons
            const mobileFilterBadge = document.getElementById('mobile-filter-badge');
            const desktopFilterCount = document.getElementById('desktop-filter-count');
            const drawerFilterBadge = document.getElementById('drawer-filter-badge');
            const bnavFilterDot = document.getElementById('bnav-filter-dot');

            if (filterCount > 0) {{
                mobileFilterBadge.classList.remove('hidden');
                mobileFilterBadge.textContent = filterCount;
                desktopFilterCount.classList.remove('hidden');
                desktopFilterCount.textContent = filterCount;
                drawerFilterBadge.textContent = filterCount;
                bnavFilterDot.classList.remove('hidden');
            }} else {{
                mobileFilterBadge.classList.add('hidden');
                desktopFilterCount.classList.add('hidden');
                drawerFilterBadge.textContent = '0';
                bnavFilterDot.classList.add('hidden');
            }}

            // Render Active Filter Chips
            let activeChipsHtml = '';
            if (state.search) {{
                activeChipsHtml += `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-200 text-xs">Busca: "${{escapeHtml(state.search)}}" <button onclick="clearSearch()" class="hover:text-white ml-0.5">✕</button></span>`;
            }}
            if (state.status !== 'all') {{
                const labels = {{ priority: 'Prioridade', queue: 'Na Fila', watched: 'Concluídos', pending: 'Pendentes' }};
                activeChipsHtml += `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-800 border border-subtle text-slate-200 text-xs">${{labels[state.status] || state.status}} <button onclick="setStatusFilter('all')" class="hover:text-white ml-0.5">✕</button></span>`;
            }}
            if (state.type !== 'all') {{
                activeChipsHtml += `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-800 border border-subtle text-slate-200 text-xs">${{state.type === 'movie' ? 'Filmes' : 'Séries'}} <button onclick="setTypeFilter('all')" class="hover:text-white ml-0.5">✕</button></span>`;
            }}
            if (state.genre !== 'all') {{
                activeChipsHtml += `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-800 border border-subtle text-slate-200 text-xs">${{state.genre}} <button onclick="setGenreFilter('all')" class="hover:text-white ml-0.5">✕</button></span>`;
            }}
            if (state.minImdb > 0) {{
                activeChipsHtml += `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-300 text-xs">★ IMDb ${{state.minImdb}}+ <button onclick="setMinImdb(0)" class="hover:text-white ml-0.5">✕</button></span>`;
            }}
            if (state.rtCritics !== 'all') {{
                const label = state.rtCritics === 'top' ? 'Tomatometer ≥90%' : 'Certified Fresh ≥75%';
                activeChipsHtml += `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs">🍅 ${{label}} <button onclick="setRtCritics('all')" class="hover:text-white ml-0.5">✕</button></span>`;
            }}
            if (state.rtAudience !== 'all') {{
                const label = state.rtAudience === 'high' ? 'Público ≥85%' : 'Público ≥60%';
                activeChipsHtml += `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-400/15 border border-amber-400/30 text-amber-200 text-xs">🍿 ${{label}} <button onclick="setRtAudience('all')" class="hover:text-white ml-0.5">✕</button></span>`;
            }}
            if (state.decade !== 'all') {{
                const decLabels = {{ '2020s': '2020+', '2010s': 'Anos 2010', '2000s': 'Anos 2000', 'classic': 'Clássicos' }};
                activeChipsHtml += `<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-800 border border-subtle text-slate-200 text-xs">${{decLabels[state.decade]}} <button onclick="setDecadeFilter('all')" class="hover:text-white ml-0.5">✕</button></span>`;
            }}
            activeFilterTagsEl.innerHTML = activeChipsHtml;

            // Empty state check
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

                gridEl.innerHTML = list.map(item => `
                    <div class="surface-card rounded-2xl p-4 flex flex-col justify-between group">
                        <div>
                            <!-- Header Meta Pill Row -->
                            <div class="flex items-center justify-between gap-1.5 mb-2.5">
                                ${{buildStatusBadge(item.status)}}
                                <div class="flex items-center gap-1.5">
                                    <span class="font-mono text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-md bg-surface-800 text-slate-400 border border-subtle">
                                        ${{getOriginLabel(item.origin)}}
                                    </span>
                                    <button onclick="openEditModal('${{item.id}}')" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-surface-800 transition" title="Editar registro">
                                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                                    </button>
                                </div>
                            </div>

                            <!-- Title & Type -->
                            <div class="flex items-start justify-between gap-2 mb-1">
                                <h3 class="font-bold text-sm text-white leading-snug group-hover:text-purple-300 transition">
                                    ${{escapeHtml(item.title)}}
                                </h3>
                                ${{item.type === 'series' ? `<span class="shrink-0 font-mono text-[9px] uppercase tracking-widest px-1.5 py-0.5 rounded bg-purple-500/15 text-purple-300 border border-purple-500/30">Série</span>` : ''}}
                            </div>

                            <!-- Genre & Subgenre -->
                            <p class="text-xs text-slate-400 mb-2 truncate">
                                <span class="text-slate-300 font-medium">${{escapeHtml(item.genre)}}</span>
                                ${{item.subgenre ? `<span class="text-slate-500"> • ${{escapeHtml(item.subgenre)}}</span>` : ''}}
                            </p>

                            <!-- Subtle Ratings Row (IMDb, Rotten Critics, Rotten Audience, Year) -->
                            <div class="flex items-center gap-1.5 flex-wrap my-2.5">
                                ${{buildRatingsRow(item)}}
                            </div>

                            <!-- Personal Note -->
                            ${{item.note ? `
                                <div class="my-2.5 px-2.5 py-1.5 rounded-xl bg-surface-950 border border-subtle text-[11px] text-slate-300 flex items-center gap-2">
                                    <svg class="w-3.5 h-3.5 text-purple-400 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
                                    <span class="truncate">${{escapeHtml(item.note)}}</span>
                                </div>
                            ` : ''}}
                        </div>

                        <!-- Card Footer: Personal Rating & 42px Touch-Optimized Segmented Selector -->
                        <div class="pt-3 border-t border-subtle mt-2">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-[11px] text-slate-500 font-medium">Minha Avaliação</span>
                                <div class="flex items-center -mr-1">
                                    ${{buildStarsHtml(item)}}
                                </div>
                            </div>

                            <!-- 3-Segment Touch Control -->
                            <div class="grid grid-cols-3 gap-1 bg-surface-950 p-1 rounded-xl border border-subtle">
                                <button onclick="setItemStatus('${{item.id}}', 'priority')" class="h-9 rounded-lg text-[11px] font-semibold transition ${{item.status === 'priority' ? 'bg-amber-500/25 text-amber-300 border border-amber-500/50 shadow-sm' : 'text-slate-400 hover:text-white'}}">
                                    Prioridade
                                </button>
                                <button onclick="setItemStatus('${{item.id}}', 'queue')" class="h-9 rounded-lg text-[11px] font-semibold transition ${{item.status === 'queue' ? 'bg-surface-700 text-white border border-white/10 shadow-sm' : 'text-slate-400 hover:text-white'}}">
                                    Na Fila
                                </button>
                                <button onclick="setItemStatus('${{item.id}}', 'watched')" class="h-9 rounded-lg text-[11px] font-semibold transition ${{item.status === 'watched' ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'}}">
                                    Concluído
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('');
            }} else {{
                // COMPACT LIST / TABLE VIEW
                gridEl.classList.add('hidden');
                tableWrapperEl.classList.remove('hidden');

                // Mobile Spotify-style rows (super dense & touch-friendly)
                mobileListEl.innerHTML = list.map(item => {{
                    const dotColor = item.status === 'priority' ? 'bg-amber-400' : (item.status === 'watched' ? 'bg-emerald-400' : 'bg-slate-500');
                    const statusLabel = item.status === 'priority' ? 'Prioridade' : (item.status === 'watched' ? 'Concluído' : 'Na Fila');
                    const statusBtnStyle = item.status === 'priority'
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                        : (item.status === 'watched' ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' : 'bg-surface-800 text-slate-300 border-subtle');

                    return `
                        <div class="p-3 sm:p-3.5 flex items-center justify-between gap-3 active:bg-surface-800/60 transition">
                            <div class="min-w-0 flex-1" onclick="openEditModal('${{item.id}}')">
                                <div class="flex items-center gap-2 mb-1">
                                    <span class="w-2 h-2 rounded-full shrink-0 ${{dotColor}}"></span>
                                    <h4 class="font-bold text-xs text-white truncate">${{escapeHtml(item.title)}}</h4>
                                    ${{item.year ? `<span class="font-mono text-[10px] text-slate-500">(${{item.year}})</span>` : ''}}
                                    ${{item.type === 'series' ? `<span class="font-mono text-[9px] uppercase px-1 py-0.2 rounded bg-purple-500/15 text-purple-300 border border-purple-500/20 shrink-0">Série</span>` : ''}}
                                </div>
                                
                                <!-- Ratings in compact list -->
                                <div class="flex items-center gap-1.5 flex-wrap pl-4 mb-1">
                                    ${{buildRatingsRow(item, true)}}
                                </div>

                                <div class="text-[11px] text-slate-400 truncate pl-4">
                                    <span>${{escapeHtml(item.genre)}}</span>
                                    <span class="text-slate-600"> • </span>
                                    <span class="font-mono text-[10px] text-slate-500">${{getOriginLabel(item.origin)}}</span>
                                    ${{item.note ? `<span class="text-purple-300"> • ${{escapeHtml(item.note)}}</span>` : ''}}
                                </div>
                            </div>

                            <div class="flex items-center gap-2 shrink-0">
                                <button onclick="cycleItemStatus('${{item.id}}')" class="h-8 px-2.5 rounded-lg border text-[11px] font-semibold transition ${{statusBtnStyle}} touch-target flex items-center justify-center">
                                    ${{statusLabel}}
                                </button>
                                <button onclick="openEditModal('${{item.id}}')" class="h-8 w-8 rounded-lg bg-surface-800 border border-subtle flex items-center justify-center text-slate-400 hover:text-white">
                                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                                </button>
                            </div>
                        </div>
                    `;
                }}).join('');

                // Desktop Table rows
                tableBodyEl.innerHTML = list.map(item => `
                    <tr class="hover:bg-surface-850/60 transition group">
                        <td class="py-3 px-4">
                            <div class="flex items-center gap-2.5">
                                <span class="w-2 h-2 rounded-full shrink-0 ${{item.status === 'priority' ? 'bg-amber-400 shadow-[0_0_6px_#F59E0B]' : (item.status === 'watched' ? 'bg-emerald-400 shadow-[0_0_6px_#10B981]' : 'bg-slate-500')}}"></span>
                                <div>
                                    <div class="font-bold text-white flex items-center gap-2">
                                        <span>${{escapeHtml(item.title)}}</span>
                                        ${{item.type === 'series' ? `<span class="font-mono text-[9px] uppercase px-1.5 py-0.2 rounded bg-purple-500/15 text-purple-300 border border-purple-500/20">Série</span>` : ''}}
                                        ${{item.note ? `<span class="text-[11px] text-purple-300 bg-brand/15 px-1.5 py-0.2 rounded border border-purple-500/20">${{escapeHtml(item.note)}}</span>` : ''}}
                                    </div>
                                </div>
                            </div>
                        </td>
                        <td class="py-3 px-3 text-slate-300">
                            <div>${{escapeHtml(item.genre)}}</div>
                            <div class="text-[11px] text-slate-500">${{escapeHtml(item.subgenre || '—')}}</div>
                        </td>
                        <td class="py-3 px-3 text-center font-mono text-slate-400">
                            ${{item.year || '—'}}
                        </td>
                        <td class="py-3 px-3 text-center">
                            <div class="flex items-center justify-center gap-1.5 flex-wrap">
                                ${{buildRatingsRow(item, true)}}
                            </div>
                        </td>
                        <td class="py-3 px-3">
                            <span class="font-mono text-[10px] uppercase tracking-wider px-2 py-0.5 rounded bg-surface-800 text-slate-400 border border-subtle">
                                ${{getOriginLabel(item.origin)}}
                            </span>
                        </td>
                        <td class="py-3 px-3">
                            <div class="flex items-center">${{buildStarsHtml(item)}}</div>
                        </td>
                        <td class="py-3 px-4 text-right">
                            <div class="inline-flex items-center justify-end gap-1.5">
                                <select onchange="setItemStatus('${{item.id}}', this.value)" class="bg-surface-950 border border-subtle rounded-lg px-2 py-1.5 text-[11px] text-slate-200 focus:outline-none focus:border-purple-500">
                                    <option value="priority" ${{item.status === 'priority' ? 'selected' : ''}}>Prioridade</option>
                                    <option value="queue" ${{item.status === 'queue' ? 'selected' : ''}}>Na Fila</option>
                                    <option value="watched" ${{item.status === 'watched' ? 'selected' : ''}}>Concluído</option>
                                </select>
                                <button onclick="openEditModal('${{item.id}}')" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-surface-700 transition" title="Editar">
                                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                                </button>
                            </div>
                        </td>
                    </tr>
                `).join('');
            }}
        }}

        // State Mutations
        function setItemStatus(id, newStatus) {{
            const item = catalog.find(i => i.id === id);
            if (!item) return;
            item.status = newStatus;
            persist();
            render();
            const labels = {{ priority: 'marcado como Prioridade ★', queue: 'colocado Na Fila', watched: 'concluído! 🎉' }};
            notify(`"${{item.title}}" ${{labels[newStatus] || 'atualizado'}}`);
        }}

        function setRating(id, stars) {{
            const item = catalog.find(i => i.id === id);
            if (!item) return;
            item.rating = item.rating === stars ? 0 : stars;
            persist();
            render();
            notify(item.rating > 0 ? `Avaliado com ${{item.rating}} estrela(s)` : 'Avaliação removida');
        }}

        // Filter Actions
        function handleSearch(val) {{
            state.search = val;
            document.getElementById('clear-search-btn').classList.toggle('hidden', val.length === 0);
            render();
        }}

        function clearSearch() {{
            state.search = '';
            document.getElementById('search-input').value = '';
            document.getElementById('clear-search-btn').classList.add('hidden');
            render();
        }}

        function setStatusFilter(status) {{
            state.status = status;
            syncNavigationStyles();
            render();
        }}

        function setTypeFilter(type) {{
            state.type = type;
            syncNavigationStyles();
            render();
        }}

        function setGenreFilter(genre) {{
            state.genre = genre;
            syncNavigationStyles();
            render();
        }}

        function setOriginFilter(origin) {{
            state.origin = origin;
            syncNavigationStyles();
            render();
        }}

        function setMinImdb(score) {{
            state.minImdb = score;
            syncNavigationStyles();
            render();
        }}

        function setRtCritics(val) {{
            state.rtCritics = val;
            syncNavigationStyles();
            render();
        }}

        function setRtAudience(val) {{
            state.rtAudience = val;
            syncNavigationStyles();
            render();
        }}

        function setDecadeFilter(decade) {{
            state.decade = decade;
            syncNavigationStyles();
            render();
        }}

        function setSortOrder(sort) {{
            state.sort = sort;
            syncNavigationStyles();
            render();
        }}

        function setViewMode(mode) {{
            state.view = mode;
            syncNavigationStyles();
            render();
        }}

        function toggleQuickFilter(field, value) {{
            if (state[field] === value) {{
                state[field] = (field === 'minImdb' ? 0 : 'all');
            }} else {{
                state[field] = value;
            }}
            syncNavigationStyles();
            render();
        }}

        function clearRatingFilters() {{
            state.minImdb = 0;
            state.rtCritics = 'all';
            state.rtAudience = 'all';
            syncNavigationStyles();
            render();
            notify("Filtros de nota limpos");
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
            document.getElementById('search-input').value = '';
            document.getElementById('clear-search-btn').classList.add('hidden');
            syncNavigationStyles();
            render();
            notify("Todos os filtros foram redefinidos");
        }}

        // Style Synchronizer for all UI states
        function syncNavigationStyles() {{
            // Desktop Sidebar & Drawer items
            document.querySelectorAll('[data-nav]').forEach(el => {{
                const val = el.getAttribute('data-nav');
                const active = state.status === val && state.type === 'all';
                el.classList.toggle('bg-surface-800', active);
                el.classList.toggle('text-white', active);
                el.classList.toggle('text-slate-400', !active);
            }});

            document.querySelectorAll('[data-nav-type]').forEach(el => {{
                const val = el.getAttribute('data-nav-type');
                const active = state.type === val;
                el.classList.toggle('bg-surface-800', active);
                el.classList.toggle('text-white', active);
                el.classList.toggle('text-slate-400', !active);
            }});

            // Mobile Bottom Nav Active States
            document.querySelectorAll('[data-bnav]').forEach(el => {{
                const val = el.getAttribute('data-bnav');
                const active = state.status === val;
                el.classList.toggle('text-purple-400', active);
                el.classList.toggle('text-slate-400', !active);
            }});

            // Quick Chips
            document.querySelectorAll('.quick-chip').forEach(el => {{
                const val = el.getAttribute('data-quick');
                let active = false;
                if (val === 'status:all') active = state.status === 'all' && state.type === 'all' && state.minImdb === 0 && state.rtCritics === 'all' && state.rtAudience === 'all';
                else if (val === 'status:priority') active = state.status === 'priority';
                else if (val === 'minImdb:8.0') active = state.minImdb === 8.0;
                else if (val === 'rtCritics:top') active = state.rtCritics === 'top';
                else if (val === 'rtAudience:high') active = state.rtAudience === 'high';
                else if (val === 'status:pending') active = state.status === 'pending';
                else if (val === 'type:movie') active = state.type === 'movie';
                else if (val === 'type:series') active = state.type === 'series';
                else if (val === 'status:watched') active = state.status === 'watched';

                el.classList.toggle('filter-chip-active', active);
                el.classList.toggle('bg-surface-900', !active);
            }});

            // Sheet Filter Buttons Styling
            document.querySelectorAll('[data-sheet-sort]').forEach(el => {{
                const active = state.sort === el.getAttribute('data-sheet-sort');
                el.classList.toggle('bg-purple-600/20', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-subtle', !active);
            }});

            document.querySelectorAll('[data-sheet-status]').forEach(el => {{
                const active = state.status === el.getAttribute('data-sheet-status');
                el.classList.toggle('bg-purple-600/20', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-subtle', !active);
            }});

            document.querySelectorAll('[data-sheet-imdb]').forEach(el => {{
                const val = parseFloat(el.getAttribute('data-sheet-imdb'));
                const active = state.minImdb === val;
                el.classList.toggle('bg-amber-500/20', active);
                el.classList.toggle('border-amber-500/50', active);
                el.classList.toggle('border-subtle', !active);
            }});
            document.getElementById('sheet-imdb-display').textContent = state.minImdb > 0 ? `★ ${{state.minImdb}}+` : 'Qualquer';

            document.querySelectorAll('[data-sheet-rtcritics]').forEach(el => {{
                const active = state.rtCritics === el.getAttribute('data-sheet-rtcritics');
                el.classList.toggle('bg-rose-500/20', active);
                el.classList.toggle('border-rose-500/50', active);
                el.classList.toggle('border-subtle', !active);
            }});

            document.querySelectorAll('[data-sheet-rtaudience]').forEach(el => {{
                const active = state.rtAudience === el.getAttribute('data-sheet-rtaudience');
                el.classList.toggle('bg-amber-400/20', active);
                el.classList.toggle('border-amber-400/50', active);
                el.classList.toggle('border-subtle', !active);
            }});

            document.querySelectorAll('[data-sheet-genre]').forEach(el => {{
                const active = state.genre === el.getAttribute('data-sheet-genre');
                el.classList.toggle('bg-purple-600/20', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-subtle', !active);
            }});

            document.querySelectorAll('[data-sheet-decade]').forEach(el => {{
                const active = state.decade === el.getAttribute('data-sheet-decade');
                el.classList.toggle('bg-purple-600/20', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-subtle', !active);
            }});

            document.querySelectorAll('[data-sheet-origin]').forEach(el => {{
                const active = state.origin === el.getAttribute('data-sheet-origin');
                el.classList.toggle('bg-purple-600/20', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-subtle', !active);
            }});

            // View Mode button styles
            const isGrid = state.view === 'grid';
            document.getElementById('view-btn-grid')?.classList.toggle('text-white', isGrid);
            document.getElementById('view-btn-grid')?.classList.toggle('bg-surface-800', isGrid);
            document.getElementById('view-btn-table')?.classList.toggle('text-white', !isGrid);
            document.getElementById('view-btn-table')?.classList.toggle('bg-surface-800', !isGrid);

            document.getElementById('mobile-view-grid')?.classList.toggle('text-white', isGrid);
            document.getElementById('mobile-view-grid')?.classList.toggle('bg-surface-800', isGrid);
            document.getElementById('mobile-view-table')?.classList.toggle('text-white', !isGrid);
            document.getElementById('mobile-view-table')?.classList.toggle('bg-surface-800', !isGrid);

            const desktopSortSelect = document.getElementById('desktop-sort-select');
            if (desktopSortSelect) desktopSortSelect.value = state.sort;
        }}

        // Filter Bottom Sheet Controller
        function openFilterSheet() {{
            const sheet = document.getElementById('filter-sheet');
            const backdrop = document.getElementById('filter-sheet-backdrop');
            backdrop.classList.remove('hidden');
            requestAnimationFrame(() => {{
                sheet.classList.remove('translate-y-full');
            }});
        }}

        function closeFilterSheet() {{
            const sheet = document.getElementById('filter-sheet');
            const backdrop = document.getElementById('filter-sheet-backdrop');
            sheet.classList.add('translate-y-full');
            setTimeout(() => {{
                backdrop.classList.add('hidden');
            }}, 200);
        }}

        // Mobile Drawer Controller
        function openMobileDrawer() {{
            const drawer = document.getElementById('mobile-drawer');
            const backdrop = document.getElementById('mobile-drawer-backdrop');
            backdrop.classList.remove('hidden');
            requestAnimationFrame(() => {{
                drawer.classList.remove('-translate-x-full');
            }});
        }}

        function closeMobileDrawer() {{
            const drawer = document.getElementById('mobile-drawer');
            const backdrop = document.getElementById('mobile-drawer-backdrop');
            drawer.classList.add('-translate-x-full');
            setTimeout(() => {{
                backdrop.classList.add('hidden');
            }}, 200);
        }}

        // Randomizer Controller
        function openRandomizerModal() {{
            document.getElementById('randomizer-modal').classList.remove('hidden');
        }}

        function closeRandomizerModal() {{
            document.getElementById('randomizer-modal').classList.add('hidden');
        }}

        function runRandomizer() {{
            const poolType = document.getElementById('rand-pool').value;
            const genre = document.getElementById('rand-genre').value;

            let pool = catalog.filter(i => {{
                if (poolType === 'pending' && i.status === 'watched') return false;
                if (poolType === 'priority' && i.status !== 'priority') return false;
                if (poolType === 'queue' && i.status !== 'queue') return false;
                if (poolType === 'series' && i.type !== 'series') return false;
                if (poolType === 'top_rated' && (i.status === 'watched' || (i.imdb || 0) < 7.5)) return false;

                if (genre !== 'all' && i.genre !== genre) return false;
                return true;
            }});

            if (pool.length === 0) {{
                document.getElementById('rand-title').textContent = "Nenhum título no escopo";
                document.getElementById('rand-meta').textContent = "Tente alterar os critérios de seleção acima.";
                document.getElementById('rand-status-tag').textContent = "Vazio";
                document.getElementById('rand-ratings').classList.add('hidden');
                document.getElementById('rand-actions').classList.add('hidden');
                return;
            }}

            const titleEl = document.getElementById('rand-title');
            const metaEl = document.getElementById('rand-meta');
            const tagEl = document.getElementById('rand-status-tag');
            const ratingsEl = document.getElementById('rand-ratings');
            const actionsEl = document.getElementById('rand-actions');

            tagEl.textContent = "Sorteando...";
            ratingsEl.classList.add('hidden');
            actionsEl.classList.add('hidden');

            let spins = 0;
            const maxSpins = 16;
            const interval = setInterval(() => {{
                const temp = pool[Math.floor(Math.random() * pool.length)];
                titleEl.textContent = temp.title;
                metaEl.textContent = `${{temp.genre}} • ${{temp.year || ''}}`;
                spins++;

                if (spins >= maxSpins) {{
                    clearInterval(interval);
                    const winner = pool[Math.floor(Math.random() * pool.length)];
                    titleEl.textContent = winner.title;
                    metaEl.textContent = `${{winner.genre}} ${{winner.subgenre ? '— ' + winner.subgenre : ''}} • ${{getOriginLabel(winner.origin)}}`;
                    tagEl.textContent = winner.status === 'priority' ? '★ Prioridade' : 'Na Fila';
                    
                    ratingsEl.innerHTML = buildRatingsRow(winner);
                    ratingsEl.classList.remove('hidden');

                    const btnWatched = document.getElementById('rand-mark-watched');
                    btnWatched.onclick = () => {{
                        setItemStatus(winner.id, 'watched');
                        closeRandomizerModal();
                    }};
                    actionsEl.classList.remove('hidden');
                }}
            }}, 65);
        }}

        // Entry Modal Controller (Add & Edit)
        function openAddModal() {{
            document.getElementById('entry-modal-title').textContent = 'Novo Registro';
            document.getElementById('entry-id').value = '';
            document.getElementById('entry-form').reset();
            document.getElementById('delete-entry-btn').classList.add('hidden');
            document.getElementById('entry-modal').classList.remove('hidden');
        }}

        function openEditModal(id) {{
            const item = catalog.find(i => i.id === id);
            if (!item) return;

            document.getElementById('entry-modal-title').textContent = 'Editar Registro';
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
            document.getElementById('entry-modal').classList.remove('hidden');
        }}

        function closeAddModal() {{
            document.getElementById('entry-modal').classList.add('hidden');
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
                const newItem = {{
                    id: 'custom_' + Date.now(),
                    ...payload,
                    rating: 0
                }};
                catalog.unshift(newItem);
                notify(`"${{title}}" adicionado ao catálogo`);
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

            if (confirm(`Deseja realmente remover "${{item.title}}"?`)) {{
                catalog = catalog.filter(i => i.id !== id);
                persist();
                render();
                closeAddModal();
                notify(`"${{item.title}}" removido`);
            }}
        }}

        // Export & Import Controller
        function openExportModal() {{
            document.getElementById('export-textarea').value = JSON.stringify(catalog, null, 2);
            document.getElementById('export-modal').classList.remove('hidden');
        }}

        function closeExportModal() {{
            document.getElementById('export-modal').classList.add('hidden');
        }}

        function copyExportText() {{
            const ta = document.getElementById('export-textarea');
            ta.select();
            navigator.clipboard.writeText(ta.value).then(() => {{
                notify("JSON copiado para a área de transferência!");
            }});
        }}

        function downloadJson() {{
            const blob = new Blob([JSON.stringify(catalog, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cinevault_backup_${{new Date().toISOString().slice(0, 10)}}.json`;
            a.click();
            URL.revokeObjectURL(url);
            notify("Arquivo de backup baixado!");
        }}

        function importJson(event) {{
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {{
                try {{
                    const data = JSON.parse(e.target.result);
                    if (Array.isArray(data) && data.length > 0) {{
                        catalog = data;
                        persist();
                        render();
                        closeExportModal();
                        notify(`${{data.length}} registros restaurados com sucesso!`);
                    }} else {{
                        alert("Arquivo de backup inválido.");
                    }}
                }} catch (err) {{
                    alert("Erro ao ler JSON: " + err.message);
                }}
            }};
            reader.readAsText(file);
        }}

        // Reset Controller
        function openResetModal() {{
            document.getElementById('reset-modal').classList.remove('hidden');
        }}

        function closeResetModal() {{
            document.getElementById('reset-modal').classList.add('hidden');
        }}

        function confirmFactoryReset() {{
            catalog = JSON.parse(JSON.stringify(INITIAL_DATA));
            persist();
            render();
            closeResetModal();
            notify("Catálogo original restaurado com sucesso!");
        }}

        // Interactive Toast Notification
        let toastTimeout;
        function notify(text) {{
            const toast = document.getElementById('toast');
            const toastText = document.getElementById('toast-text');
            toastText.textContent = text;

            toast.classList.remove('hidden');
            requestAnimationFrame(() => {{
                toast.classList.remove('translate-y-2', 'opacity-0');
            }});

            clearTimeout(toastTimeout);
            toastTimeout = setTimeout(() => {{
                toast.classList.add('translate-y-2', 'opacity-0');
                setTimeout(() => toast.classList.add('hidden'), 200);
            }}, 2600);
        }}

        // Run on DOM load
        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('cinevault_emannuel_petry.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Both index.html and cinevault_emannuel_petry.html updated successfully!")
