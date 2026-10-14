# -*- coding: utf-8 -*-
"""
Builder for Cinevault App Experience with:
- Step-by-Step Guided Discovery Wizard (Tipo -> Gênero -> Avaliação)
- Real-time live match counter in each step
- "Tranquilo" / "Sem Filtros" escape hatch to see full catalog with 1 click
- Concierge banner in catalog view with 1-click refazer or limpar
- Header & Mobile Bottom Dock with quick access to Assistente
- Direct status selection dropdown (Priority, Queue, Watched)
- 1-click instant 'Marcar como Visto' button
- Rich genres & intuitive separation
- Accurate Brazilian streaming platforms + 'Ver plataforma' button
- Full compatibility with all 217 items
"""

import json
import subprocess
from enrich_platforms_and_genres import PLATFORM_GENRE_MAP
from metadata_cinevault import METADATA

# Load items from index.html if present, else git HEAD
try:
    with open('index.html', 'r', encoding='utf-8') as f:
        raw = f.read()
except Exception:
    raw = subprocess.check_output(['git', 'show', 'HEAD:index.html'], encoding='utf-8')

start = raw.find('const INITIAL_DATA = [')
end = raw.find('];', start)
data_text = raw[start + len('const INITIAL_DATA = '):end + 1]

items = json.loads(data_text)
print(f"Loaded {len(items)} items.")

# Enrich with updated genres and platforms
for item in items:
    item_id = item['id']
    pg = PLATFORM_GENRE_MAP.get(item_id, {'platform': 'Netflix', 'genre': item.get('genre', 'Drama'), 'subgenre': item.get('subgenre', '')})
    item['genre'] = pg['genre']
    if pg.get('subgenre'):
        item['subgenre'] = pg['subgenre']
    item['platform'] = pg['platform']

print("Enriched all items with refined genres and platforms.")
js_items = json.dumps(items, ensure_ascii=False, indent=8)

HTML_PAGE = """<!DOCTYPE html>
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
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        canvas: '#090A0F',
                        surface: {
                            DEFAULT: '#0F1118',
                            hover: '#141722',
                            border: 'rgba(255, 255, 255, 0.06)',
                            borderHover: 'rgba(255, 255, 255, 0.16)',
                        },
                        accent: {
                            DEFAULT: '#820AD1',
                            light: '#A855F7',
                            glow: 'rgba(130, 10, 209, 0.25)',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        * {
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            -webkit-tap-highlight-color: transparent;
        }
        html, body {
            background-color: #090A0F;
            color: #F8FAFC;
            overflow-x: hidden;
            font-feature-settings: "cv02", "cv03", "cv04", "cv11";
        }
        .card-clean {
            background: #0E1017;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @media (hover: hover) and (pointer: fine) {
            .card-clean:hover {
                border-color: rgba(255, 255, 255, 0.14);
                background: #121520;
                transform: translateY(-2px);
                box-shadow: 0 16px 32px -12px rgba(0, 0, 0, 0.6), 0 0 24px -10px rgba(130, 10, 209, 0.15);
            }
        }
        .card-clean:active {
            transform: scale(0.995);
        }

        /* Wizard Discovery Cards */
        .wizard-card {
            background: #0E1017;
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 1rem;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            cursor: pointer;
            user-select: none;
            position: relative;
        }
        @media (hover: hover) and (pointer: fine) {
            .wizard-card:hover {
                border-color: rgba(168, 85, 247, 0.4);
                background: #131724;
                transform: translateY(-2px);
                box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.5), 0 0 20px -8px rgba(130, 10, 209, 0.25);
            }
        }
        .wizard-card:active {
            transform: scale(0.98);
        }
        .wizard-card.selected {
            border-color: #A855F7 !important;
            background: linear-gradient(135deg, rgba(130, 10, 209, 0.18) 0%, rgba(18, 22, 34, 0.96) 100%) !important;
            box-shadow: 0 0 24px -4px rgba(130, 10, 209, 0.4) !important;
        }

        /* Animation between steps */
        @keyframes stepFadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .step-fade-in {
            animation: stepFadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        ::-webkit-scrollbar-track {
            background: #090A0F;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.12);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }
        .no-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .no-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .pb-safe {
            padding-bottom: calc(5.5rem + env(safe-area-inset-bottom, 0px));
        }
        .bottom-nav-safe {
            padding-bottom: env(safe-area-inset-bottom, 0px);
        }
        /* Platform Badge Colors */
        .badge-netflix { background: rgba(229, 9, 20, 0.12); color: #FF4D4D; border: 1px solid rgba(229, 9, 20, 0.25); }
        .badge-max { background: rgba(0, 43, 231, 0.15); color: #809BFF; border: 1px solid rgba(0, 43, 231, 0.3); }
        .badge-prime { background: rgba(0, 168, 225, 0.12); color: #38BDF8; border: 1px solid rgba(0, 168, 225, 0.25); }
        .badge-disney { background: rgba(17, 60, 207, 0.15); color: #60A5FA; border: 1px solid rgba(17, 60, 207, 0.3); }
        .badge-apple { background: rgba(255, 255, 255, 0.1); color: #F1F5F9; border: 1px solid rgba(255, 255, 255, 0.2); }
        .badge-paramount { background: rgba(0, 100, 255, 0.12); color: #93C5FD; border: 1px solid rgba(0, 100, 255, 0.25); }
        .badge-mubi { background: rgba(235, 17, 56, 0.12); color: #FDA4AF; border: 1px solid rgba(235, 17, 56, 0.25); }
        .badge-globoplay { background: rgba(251, 146, 60, 0.12); color: #FB923C; border: 1px solid rgba(251, 146, 60, 0.25); }
    </style>
</head>
<body class="min-h-screen bg-canvas text-slate-100 selection:bg-accent selection:text-white" onclick="closeAllStatusDropdowns()">

    <!-- ================================================================ -->
    <!-- VIEW 1: STEP-BY-STEP GUIDED DISCOVERY WIZARD (ASSISTENTE)       -->
    <!-- ================================================================ -->
    <div id="wizard-view" class="min-h-screen flex flex-col justify-between">
        
        <!-- Wizard Top Header -->
        <header class="sticky top-0 z-30 bg-[#090A0F]/90 backdrop-blur-xl border-b border-white/[0.06]">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-3">
                
                <!-- Brand -->
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-[#820AD1] to-[#6D28D9] flex items-center justify-center shadow-md border border-white/20">
                        <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
                            <line x1="7" y1="2" x2="7" y2="22"></line>
                            <line x1="17" y1="2" x2="17" y2="22"></line>
                            <line x1="2" y1="12" x2="22" y2="12"></line>
                        </svg>
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="font-bold text-sm tracking-tight text-white">Cinevault</span>
                            <span class="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300 font-mono border border-purple-500/30">Assistente</span>
                        </div>
                        <span class="text-[11px] text-slate-400 block -mt-0.5">Encontre o que assistir em 3 passos</span>
                    </div>
                </div>

                <!-- Escape Hatch (Ver tudo sem filtros / tranquilo) -->
                <button onclick="skipWizard()" class="text-xs font-medium text-slate-300 hover:text-white px-3.5 py-1.5 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] transition active:scale-95 flex items-center gap-1.5" title="Abrir catálogo completo">
                    <span>Ver tudo sem filtros</span>
                    <svg class="w-3.5 h-3.5 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
                </button>
            </div>
        </header>

        <!-- Main Wizard Content -->
        <main class="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-6 pb-28">
            
            <!-- Step Progress Indicator -->
            <div class="max-w-xl mx-auto mb-6 sm:mb-8">
                <div class="flex items-center justify-between mb-2.5 text-xs font-mono">
                    <div class="flex items-center gap-2">
                        <span id="wizard-step-badge" class="px-2 py-0.5 rounded-md bg-purple-600/30 text-purple-300 font-mono text-[11px] border border-purple-500/40">1 / 3</span>
                        <span id="wizard-step-title-header" class="text-white font-semibold">Formato da Sessão</span>
                    </div>
                    <span id="wizard-progress-summary" class="text-[11px] font-mono text-slate-400">Passo 1: Tipo</span>
                </div>
                <!-- 3 Segmented Bars (Clickable to jump back) -->
                <div class="grid grid-cols-3 gap-2">
                    <div id="prog-bar-1" onclick="goToStep(1)" class="h-1.5 rounded-full bg-purple-500 transition-all duration-300 cursor-pointer" title="Passo 1: Formato"></div>
                    <div id="prog-bar-2" onclick="goToStep(2)" class="h-1.5 rounded-full bg-white/[0.08] transition-all duration-300 cursor-pointer" title="Passo 2: Gênero"></div>
                    <div id="prog-bar-3" onclick="goToStep(3)" class="h-1.5 rounded-full bg-white/[0.08] transition-all duration-300 cursor-pointer" title="Passo 3: Notas"></div>
                </div>
            </div>

            <!-- STEP 1: FORMATO / TIPO -->
            <div id="step-panel-1" class="step-fade-in max-w-xl mx-auto space-y-4">
                <div class="text-center sm:text-left mb-6">
                    <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight mb-1.5">O que você quer assistir hoje?</h2>
                    <p class="text-xs sm:text-sm text-slate-400">Escolha se prefere um filme, uma série para maratonar ou explorar o catálogo completo.</p>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <!-- Filmes -->
                    <div onclick="selectWizardType('movie')" data-w-type="movie" class="wizard-card p-4 flex flex-col justify-between">
                        <div>
                            <div class="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-300 flex items-center justify-center mb-3">
                                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect><line x1="7" y1="2" x2="7" y2="22"></line><line x1="17" y1="2" x2="17" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="2" y1="7" x2="7" y2="7"></line><line x1="2" y1="17" x2="7" y2="17"></line><line x1="17" y1="17" x2="22" y2="17"></line><line x1="17" y1="7" x2="22" y2="7"></line></svg>
                            </div>
                            <h3 class="font-bold text-base text-white mb-1">Filmes</h3>
                            <p class="text-xs text-slate-400 leading-relaxed">Longas-metragens para ver em uma única sessão.</p>
                        </div>
                        <div class="pt-4 mt-2 border-t border-white/[0.06] flex items-center justify-between text-xs font-mono">
                            <span class="text-slate-400" id="w-badge-count-movies">203 títulos</span>
                            <span class="w-2 h-2 rounded-full bg-purple-500/50"></span>
                        </div>
                    </div>

                    <!-- Séries -->
                    <div onclick="selectWizardType('series')" data-w-type="series" class="wizard-card p-4 flex flex-col justify-between">
                        <div>
                            <div class="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-300 flex items-center justify-center mb-3">
                                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="15" rx="2" ry="2"></rect><polyline points="17 2 12 7 7 2"></polyline></svg>
                            </div>
                            <h3 class="font-bold text-base text-white mb-1">Séries</h3>
                            <p class="text-xs text-slate-400 leading-relaxed">Séries e docs para acompanhar episódio a episódio.</p>
                        </div>
                        <div class="pt-4 mt-2 border-t border-white/[0.06] flex items-center justify-between text-xs font-mono">
                            <span class="text-slate-400" id="w-badge-count-series">14 títulos</span>
                            <span class="w-2 h-2 rounded-full bg-purple-500/50"></span>
                        </div>
                    </div>

                    <!-- Tanto Faz -->
                    <div onclick="selectWizardType('all')" data-w-type="all" class="wizard-card p-4 flex flex-col justify-between selected">
                        <div>
                            <div class="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-300 flex items-center justify-center mb-3">
                                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                            </div>
                            <h3 class="font-bold text-base text-white mb-1">Tanto Faz</h3>
                            <p class="text-xs text-slate-400 leading-relaxed">Sem restrição, quero ver o melhor de ambos.</p>
                        </div>
                        <div class="pt-4 mt-2 border-t border-white/[0.06] flex items-center justify-between text-xs font-mono">
                            <span class="text-slate-400" id="w-badge-count-all">217 títulos</span>
                            <span class="w-2 h-2 rounded-full bg-purple-500"></span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- STEP 2: GÊNERO / VIBE -->
            <div id="step-panel-2" class="step-fade-in max-w-3xl mx-auto space-y-4 hidden">
                <div class="text-center sm:text-left mb-6">
                    <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight mb-1.5">Qual clima você procura?</h2>
                    <p class="text-xs sm:text-sm text-slate-400">Selecione a atmosfera ou gênero que mais combina com seu momento.</p>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5" id="wizard-genre-grid">
                    <!-- Injected dynamically with live counts -->
                </div>
            </div>

            <!-- STEP 3: NOTAS / AVALIAÇÃO -->
            <div id="step-panel-3" class="step-fade-in max-w-2xl mx-auto space-y-4 hidden">
                <div class="text-center sm:text-left mb-6">
                    <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight mb-1.5">Qual o padrão de avaliação?</h2>
                    <p class="text-xs sm:text-sm text-slate-400">Filtre por aclamação crítica, avaliação da audiência ou explore tudo.</p>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3" id="wizard-ratings-grid">
                    <!-- Injected dynamically with live counts -->
                </div>
            </div>

        </main>

        <!-- Wizard Sticky Bottom Action Bar -->
        <div class="sticky bottom-0 z-30 bg-[#090A0F]/95 backdrop-blur-xl border-t border-white/[0.08] py-3 px-4 bottom-nav-safe">
            <div class="max-w-3xl mx-auto flex items-center justify-between gap-3">
                
                <!-- Back Button -->
                <button id="wizard-back-btn" onclick="wizardPrevStep()" class="hidden px-4 py-2.5 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] text-slate-300 hover:text-white border border-white/[0.08] text-xs font-semibold transition active:scale-95 flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
                    <span>Voltar</span>
                </button>
                <div id="wizard-back-spacer" class="w-16"></div>

                <!-- Live Match Counter Pill -->
                <div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/[0.04] border border-white/[0.08] text-xs font-mono">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span id="wizard-live-match-text" class="text-slate-300 font-medium">217 títulos combinam</span>
                </div>

                <!-- Next or Finish CTA Button -->
                <button id="wizard-next-btn" onclick="wizardNextStep()" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-[#820AD1] to-[#7C3AED] hover:from-[#9333EA] hover:to-[#6D28D9] text-white text-xs font-bold shadow-lg shadow-purple-900/30 transition active:scale-95 flex items-center gap-1.5">
                    <span id="wizard-next-text">Continuar</span>
                    <svg id="wizard-next-icon" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                </button>
            </div>
            
            <div class="text-center mt-2">
                <button onclick="skipWizard()" class="text-[11px] text-slate-500 hover:text-slate-300 transition">
                    Pular etapas e ver todo o catálogo sem filtros (tranquilo) ›
                </button>
            </div>
        </div>

    </div>


    <!-- ================================================================ -->
    <!-- VIEW 2: MAIN CATALOG VIEW (TELA PRINCIPAL COM FILTROS)          -->
    <!-- ================================================================ -->
    <div id="catalog-view" class="min-h-screen flex flex-col justify-between hidden">

        <!-- ================= TOP NAVIGATION BAR ================= -->
        <header class="sticky top-0 z-30 bg-[#090A0F]/85 backdrop-blur-xl border-b border-white/[0.06]">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="h-16 flex items-center justify-between gap-3">
                    
                    <!-- Brand -->
                    <div class="flex items-center gap-3 shrink-0 cursor-pointer" onclick="openWizard()">
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

                    <!-- Minimalist Search Input -->
                    <div class="flex-1 max-w-md relative">
                        <svg class="w-3.5 h-3.5 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                        <input 
                            type="text" 
                            id="search-input"
                            oninput="handleSearch(this.value)"
                            placeholder="Buscar filme, série, plataforma, nota..." 
                            class="w-full pl-9 pr-8 py-1.5 sm:py-2 bg-white/[0.04] hover:bg-white/[0.06] focus:bg-white/[0.07] border border-white/[0.08] focus:border-purple-500/60 rounded-xl text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none transition shadow-inner"
                        >
                        <button id="clear-search-btn" onclick="clearSearch()" class="hidden absolute right-2.5 top-1/2 -translate-y-1/2 p-0.5 text-slate-400 hover:text-white" aria-label="Limpar busca">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                        </button>
                    </div>

                    <!-- Actions -->
                    <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
                        
                        <!-- NEW: Assistente de Etapas Button -->
                        <button onclick="openWizard()" class="h-9 px-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-xs font-semibold text-purple-200 transition flex items-center gap-1.5 shadow-sm active:scale-95" title="Assistente de Escolha em Etapas">
                            <svg class="w-3.5 h-3.5 text-purple-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                            <span class="hidden md:inline">Assistente</span>
                        </button>

                        <button onclick="openFilterModal()" class="relative h-9 px-3 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-xs font-medium text-slate-200 transition flex items-center gap-2">
                            <svg class="w-3.5 h-3.5 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                            <span class="hidden sm:inline">Filtros</span>
                            <span id="header-filter-badge" class="hidden w-2 h-2 rounded-full bg-purple-500 shadow-[0_0_8px_#A855F7]"></span>
                        </button>

                        <button onclick="openRandomizerModal()" class="h-9 px-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-xs font-medium text-purple-200 transition flex items-center gap-1.5" title="Sortear título">
                            <svg class="w-3.5 h-3.5 text-purple-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
                            <span class="hidden md:inline">Sortear</span>
                        </button>

                        <button onclick="openAddModal()" class="h-9 px-3 rounded-xl bg-white/[0.08] hover:bg-white/[0.14] text-xs font-medium text-white transition flex items-center gap-1.5">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                            <span class="hidden sm:inline">Novo</span>
                        </button>

                        <!-- View Toggle -->
                        <div class="hidden sm:inline-flex rounded-xl bg-white/[0.04] p-0.5 border border-white/[0.08]">
                            <button onclick="setViewMode('grid')" id="view-btn-grid" class="p-1.5 rounded-lg text-white transition" aria-label="Grade">
                                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                            </button>
                            <button onclick="setViewMode('table')" id="view-btn-table" class="p-1.5 rounded-lg text-slate-400 hover:text-white transition" aria-label="Lista">
                                <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
                            </button>
                        </div>

                        <!-- Backup -->
                        <button onclick="openExportModal()" class="h-9 w-9 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-slate-400 hover:text-white flex items-center justify-center transition" title="Exportar / Backup">
                            <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                        </button>
                    </div>
                </div>

                <!-- Sub-Navigation: Primary Status Tabs & Quiet Progress -->
                <div class="py-2.5 flex items-center justify-between gap-3 overflow-x-auto no-scrollbar border-t border-white/[0.04]">
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

                <!-- Enhanced Interactive Genre Strip (Horizontal Scroll) -->
                <div class="py-2 border-t border-white/[0.04] flex items-center gap-1.5 overflow-x-auto no-scrollbar -mx-1 px-1 text-xs" id="genre-scroll-bar">
                    <button onclick="setGenreFilter('all')" data-genre-chip="all" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Todos os Gêneros
                    </button>
                    <button onclick="setGenreFilter('Suspense & Mistério')" data-genre-chip="Suspense & Mistério" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Suspense & Mistério
                    </button>
                    <button onclick="setGenreFilter('Thriller Psicológico')" data-genre-chip="Thriller Psicológico" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Thriller Psicológico
                    </button>
                    <button onclick="setGenreFilter('Ficção Científica')" data-genre-chip="Ficção Científica" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Ficção Científica
                    </button>
                    <button onclick="setGenreFilter('Drama')" data-genre-chip="Drama" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Drama
                    </button>
                    <button onclick="setGenreFilter('Crime & Policial')" data-genre-chip="Crime & Policial" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Crime & Policial
                    </button>
                    <button onclick="setGenreFilter('Terror')" data-genre-chip="Terror" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Terror
                    </button>
                    <button onclick="setGenreFilter('Ação & Aventura')" data-genre-chip="Ação & Aventura" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Ação & Aventura
                    </button>
                    <button onclick="setGenreFilter('Comédia')" data-genre-chip="Comédia" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Comédia
                    </button>
                    <button onclick="setGenreFilter('Biografia & Histórico')" data-genre-chip="Biografia & Histórico" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Biografia & Histórico
                    </button>
                    <button onclick="setGenreFilter('Romance')" data-genre-chip="Romance" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Romance
                    </button>
                    <button onclick="setGenreFilter('Guerra')" data-genre-chip="Guerra" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Guerra
                    </button>
                    <button onclick="setGenreFilter('Fantasia')" data-genre-chip="Fantasia" class="genre-chip px-2.5 py-1 rounded-lg text-slate-400 hover:text-white whitespace-nowrap transition bg-white/[0.02] border border-white/[0.05]">
                        Fantasia
                    </button>
                </div>
            </div>
        </header>

        <!-- ================= MAIN CATALOG CONTENT ================= -->
        <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-5 pb-safe">

            <!-- Concierge Active Banner -->
            <div id="wizard-active-banner" class="hidden mb-4 p-3.5 rounded-2xl bg-gradient-to-r from-purple-950/40 via-[#0F1118] to-[#0F1118] border border-purple-500/25 flex flex-wrap items-center justify-between gap-3 shadow-lg shadow-purple-950/20">
                <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-300 shrink-0">
                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-bold text-white">Assistente de Escolha Ativo</span>
                            <span id="wizard-banner-count" class="text-[11px] font-mono px-1.5 py-0.2 rounded bg-purple-500/20 text-purple-300">0 obras</span>
                        </div>
                        <span id="wizard-banner-desc" class="text-xs text-slate-400">Filtros aplicados em etapas</span>
                    </div>
                </div>
                <div class="flex items-center gap-2 ml-auto">
                    <button onclick="openWizard()" class="h-8 px-3 rounded-xl bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/30 text-xs font-medium text-purple-200 transition active:scale-95 flex items-center gap-1.5">
                        <svg class="w-3 h-3 text-purple-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
                        <span>Refazer etapas</span>
                    </button>
                    <button onclick="resetAllFilters()" class="h-8 px-3 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-xs font-medium text-slate-300 hover:text-white transition active:scale-95">
                        Ver tudo sem filtros ✕
                    </button>
                </div>
            </div>

            <!-- Active Filter Indicator -->
            <div id="active-filters-bar" class="hidden mb-4 p-2.5 rounded-xl bg-white/[0.02] border border-white/[0.06] flex items-center justify-between text-xs">
                <div class="flex items-center gap-2 flex-wrap" id="active-chips-container">
                    <!-- Injected dynamically -->
                </div>
                <button onclick="resetAllFilters()" class="text-[11px] text-purple-400 hover:text-purple-300 font-medium ml-2 shrink-0">
                    Limpar todos
                </button>
            </div>

            <!-- 1. Grid View (Clean Cards) -->
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
                <div class="flex items-center justify-center gap-2">
                    <button onclick="openWizard()" class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-xs font-medium text-white transition active:scale-95">
                        Refazer no Assistente
                    </button>
                    <button onclick="resetAllFilters()" class="px-4 py-2 rounded-xl bg-white/[0.08] hover:bg-white/[0.12] text-xs font-medium text-white transition">
                        Ver Catálogo Completo
                    </button>
                </div>
            </div>

        </main>

        <!-- ================= MOBILE BOTTOM DOCK (< 1024px) ================= -->
        <nav class="lg:hidden fixed bottom-0 inset-x-0 z-30 bg-[#090A0F]/90 backdrop-blur-xl border-t border-white/[0.06] bottom-nav-safe">
            <div class="grid grid-cols-5 h-14 max-w-md mx-auto items-center">
                <!-- Assistente -->
                <button onclick="openWizard()" data-bnav="wizard" class="flex flex-col items-center justify-center gap-1 text-purple-300 transition">
                    <svg class="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                    <span class="text-[10px] font-semibold text-purple-300">Assistente</span>
                </button>
                <!-- Catálogo -->
                <button onclick="showCatalog(); setStatusFilter('all');" data-bnav="catalog" class="flex flex-col items-center justify-center gap-1 text-slate-400 transition">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                    <span class="text-[10px]">Catálogo</span>
                </button>
                <!-- Center Sorteador Button -->
                <button onclick="openRandomizerModal()" class="flex flex-col items-center justify-center gap-1 text-purple-300">
                    <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-[#820AD1] to-[#6D28D9] text-white flex items-center justify-center shadow-md border border-white/20 -mt-3 active:scale-95 transition">
                        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>
                    </div>
                    <span class="text-[10px] font-semibold text-purple-300">Sortear</span>
                </button>
                <!-- Filtros -->
                <button onclick="openFilterModal()" class="relative flex flex-col items-center justify-center gap-1 text-slate-400 transition">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                    <span class="text-[10px]">Filtros</span>
                    <span id="bnav-filter-dot" class="hidden absolute top-2 right-4 w-1.5 h-1.5 rounded-full bg-purple-500 shadow-[0_0_6px_#A855F7]"></span>
                </button>
                <!-- Vistos -->
                <button onclick="showCatalog(); setStatusFilter('watched');" data-bnav="watched" class="flex flex-col items-center justify-center gap-1 text-slate-400 transition">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                    <span class="text-[10px]">Vistos</span>
                </button>
            </div>
        </nav>

    </div>

    <!-- ================= CLEAN FILTER MODAL ================= -->
    <div id="filter-modal" onclick="if(event.target === this) closeFilterModal()" class="fixed inset-0 z-50 hidden items-center justify-center p-3 sm:p-5 bg-black/80 backdrop-blur-md transition-opacity">
        <div class="bg-[#0E1017] border border-white/[0.08] rounded-2xl w-full max-w-lg shadow-2xl flex flex-col max-h-[88vh] overflow-hidden">
            
            <div class="px-5 py-3.5 border-b border-white/[0.06] flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                    <h3 class="text-sm font-semibold text-white">Filtros Avançados</h3>
                </div>
                <button type="button" onclick="closeFilterModal()" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/[0.06] transition" aria-label="Fechar">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>

            <div class="px-5 py-4 overflow-y-auto space-y-4 no-scrollbar text-xs">
                <!-- Status -->
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

                <!-- Gêneros detalhados -->
                <div>
                    <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Gênero</label>
                    <div class="flex flex-wrap gap-1.5">
                        <button onclick="setGenreFilter('all')" data-m-genre="all" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Todos</button>
                        <button onclick="setGenreFilter('Suspense & Mistério')" data-m-genre="Suspense & Mistério" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Suspense & Mistério</button>
                        <button onclick="setGenreFilter('Thriller Psicológico')" data-m-genre="Thriller Psicológico" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Thriller Psicológico</button>
                        <button onclick="setGenreFilter('Ficção Científica')" data-m-genre="Ficção Científica" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Ficção Científica</button>
                        <button onclick="setGenreFilter('Drama')" data-m-genre="Drama" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Drama</button>
                        <button onclick="setGenreFilter('Crime & Policial')" data-m-genre="Crime & Policial" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Crime & Policial</button>
                        <button onclick="setGenreFilter('Terror')" data-m-genre="Terror" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Terror</button>
                        <button onclick="setGenreFilter('Ação & Aventura')" data-m-genre="Ação & Aventura" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Ação & Aventura</button>
                        <button onclick="setGenreFilter('Comédia')" data-m-genre="Comédia" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Comédia</button>
                        <button onclick="setGenreFilter('Biografia & Histórico')" data-m-genre="Biografia & Histórico" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Biografia & Histórico</button>
                        <button onclick="setGenreFilter('Romance')" data-m-genre="Romance" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Romance</button>
                        <button onclick="setGenreFilter('Guerra')" data-m-genre="Guerra" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Guerra</button>
                        <button onclick="setGenreFilter('Fantasia')" data-m-genre="Fantasia" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Fantasia</button>
                    </div>
                </div>

                <!-- Plataformas de Streaming -->
                <div>
                    <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Plataforma de Streaming</label>
                    <div class="flex flex-wrap gap-1.5">
                        <button onclick="setPlatformFilter('all')" data-m-platform="all" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Todas</button>
                        <button onclick="setPlatformFilter('Netflix')" data-m-platform="Netflix" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition text-red-400">Netflix</button>
                        <button onclick="setPlatformFilter('Max')" data-m-platform="Max" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition text-blue-400">Max</button>
                        <button onclick="setPlatformFilter('Prime Video')" data-m-platform="Prime Video" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition text-sky-400">Prime Video</button>
                        <button onclick="setPlatformFilter('Disney+')" data-m-platform="Disney+" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition text-indigo-400">Disney+</button>
                        <button onclick="setPlatformFilter('Apple TV+')" data-m-platform="Apple TV+" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition">Apple TV+</button>
                        <button onclick="setPlatformFilter('Paramount+')" data-m-platform="Paramount+" class="m-pill px-2.5 py-1.5 rounded-lg border text-xs transition text-blue-300">Paramount+</button>
                    </div>
                </div>

                <!-- IMDb -->
                <div>
                    <label class="text-[11px] font-mono uppercase tracking-wider text-slate-400 block mb-2">Nota Mínima IMDb</label>
                    <div class="grid grid-cols-4 gap-1.5">
                        <button onclick="setMinImdb(0)" data-m-imdb="0" class="m-pill py-1.5 rounded-lg border text-center transition">Qualquer</button>
                        <button onclick="setMinImdb(7.0)" data-m-imdb="7.0" class="m-pill py-1.5 rounded-lg border text-center transition">★ 7.0+</button>
                        <button onclick="setMinImdb(7.5)" data-m-imdb="7.5" class="m-pill py-1.5 rounded-lg border text-center transition">★ 7.5+</button>
                        <button onclick="setMinImdb(8.0)" data-m-imdb="8.0" class="m-pill py-1.5 rounded-lg border text-center transition text-amber-300">★ 8.0+</button>
                    </div>
                </div>

                <!-- Rotten Tomatoes -->
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
            </div>

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

            <div class="w-full bg-white/[0.03] border border-white/[0.06] rounded-xl p-4 min-h-[120px] flex flex-col items-center justify-center mb-4">
                <span id="rand-tag" class="text-[10px] font-mono uppercase tracking-wider text-slate-500 mb-1">Pronto</span>
                <h4 id="rand-title" class="text-base font-bold text-white mb-1">Gire para sortear</h4>
                <div id="rand-ratings" class="hidden text-xs font-mono text-slate-300 my-1"></div>
                <div id="rand-platform" class="hidden my-1"></div>
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

                <!-- Platform select -->
                <div class="grid grid-cols-2 gap-2">
                    <div>
                        <label class="text-[11px] text-slate-400 block mb-1">Plataforma</label>
                        <select id="entry-platform" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-2.5 py-2 text-white focus:outline-none focus:border-purple-500">
                            <option value="Netflix">Netflix</option>
                            <option value="Max">Max</option>
                            <option value="Prime Video">Prime Video</option>
                            <option value="Disney+">Disney+</option>
                            <option value="Apple TV+">Apple TV+</option>
                            <option value="Paramount+">Paramount+</option>
                            <option value="Globoplay">Globoplay</option>
                            <option value="Mubi">Mubi</option>
                            <option value="Telecine">Telecine</option>
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

                <div>
                    <label class="text-[11px] text-slate-400 block mb-1">Categoria Principal</label>
                    <select id="entry-genre" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-2.5 py-2 text-white focus:outline-none focus:border-purple-500">
                        <option value="Suspense & Mistério">Suspense & Mistério</option>
                        <option value="Thriller Psicológico">Thriller Psicológico</option>
                        <option value="Ficção Científica">Ficção Científica</option>
                        <option value="Drama">Drama</option>
                        <option value="Crime & Policial">Crime & Policial</option>
                        <option value="Terror">Terror</option>
                        <option value="Ação & Aventura">Ação & Aventura</option>
                        <option value="Comédia">Comédia</option>
                        <option value="Biografia & Histórico">Biografia & Histórico</option>
                        <option value="Romance">Romance</option>
                        <option value="Guerra">Guerra</option>
                        <option value="Fantasia">Fantasia</option>
                    </select>
                </div>

                <div>
                    <label class="text-[11px] text-slate-400 block mb-1">Subgênero / Detalhes</label>
                    <input type="text" id="entry-subgenre" placeholder="Ex: Viagem no Tempo / Cult" class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-2 text-white">
                </div>

                <div>
                    <label class="text-[11px] text-slate-400 block mb-1">Anotação</label>
                    <input type="text" id="entry-note" placeholder="Ex: Assistir no fim de semana..." class="w-full bg-white/[0.04] border border-white/[0.08] rounded-xl px-3 py-2 text-white">
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
        const STORAGE_KEY = 'cinevault_clean_v2';
        const LEGACY_KEYS = ['cinevault_clean_v1', 'cinevault_v3_state', 'cinevault_v2_state', 'cinevault_emannuel_petry_v2'];

        const INITIAL_DATA = __INITIAL_DATA__;

        let catalog = [];
        let state = {
            search: '',
            status: 'all',
            type: 'all',
            genre: 'all',
            platform: 'all',
            origin: 'all',
            minImdb: 0,
            rtCritics: 'all',
            rtAudience: 'all',
            decade: 'all',
            sort: 'status',
            view: 'grid'
        };

        // Wizard State
        let wizardState = {
            step: 1,
            type: 'all',
            genre: 'all',
            ratingChoice: 'all'
        };

        const WIZARD_GENRES = [
            { id: 'Suspense & Mistério', label: 'Suspense & Mistério', icon: '🔍', desc: 'Reviravoltas e enigmas' },
            { id: 'Thriller Psicológico', label: 'Thriller Psicológico', icon: '🧠', desc: 'Tensão e paranoia' },
            { id: 'Ficção Científica', label: 'Ficção Científica', icon: '🚀', desc: 'Futuro e distopias' },
            { id: 'Drama', label: 'Drama', icon: '🎭', desc: 'Histórias profundas' },
            { id: 'Crime & Policial', label: 'Crime & Policial', icon: '🚨', desc: 'Máfia e investigações' },
            { id: 'Terror', label: 'Terror', icon: '👁️', desc: 'Medo e atmosfera' },
            { id: 'Ação & Aventura', label: 'Ação & Aventura', icon: '💥', desc: 'Adrenalina e ritmo' },
            { id: 'Comédia', label: 'Comédia', icon: '😂', desc: 'Humor e descontração' },
            { id: 'Biografia & Histórico', label: 'Biografia & Histórico', icon: '📜', desc: 'Fatos reais' },
            { id: 'Romance', label: 'Romance', icon: '❤️', desc: 'Paixão e conexões' },
            { id: 'Guerra', label: 'Guerra', icon: '⚔️', desc: 'Batalhas e sobrevivência' },
            { id: 'Fantasia', label: 'Fantasia', icon: '🪄', desc: 'Mundos mágicos' },
            { id: 'all', label: 'Qualquer Gênero', icon: '✨', desc: 'Surpreenda-me' }
        ];

        const WIZARD_RATINGS = [
            {
                id: 'imdb_8',
                title: 'Obras-Primas Absolutas',
                tag: 'IMDb ★ 8.0+',
                tagClass: 'bg-amber-400/15 text-amber-300 border-amber-400/30',
                desc: 'O mais alto padrão do cinema e da TV mundial.',
                icon: '🏆'
            },
            {
                id: 'imdb_75',
                title: 'Muito Bem Avaliados',
                tag: 'IMDb ★ 7.5+',
                tagClass: 'bg-amber-400/15 text-amber-300 border-amber-400/30',
                desc: 'Qualidade narrativa comprovada e alto padrão.',
                icon: '⭐'
            },
            {
                id: 'rt_critics',
                title: 'Aclamados pela Crítica',
                tag: '🍅 Rotten ≥ 75%',
                tagClass: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
                desc: 'Selo Certified Fresh do consenso internacional.',
                icon: '🍅'
            },
            {
                id: 'rt_audience',
                title: 'Favoritos do Público',
                tag: '🍿 Popcorn ≥ 80%',
                tagClass: 'bg-amber-300/15 text-amber-200 border-amber-300/30',
                desc: 'Aprovados com honras pelas grandes multidões.',
                icon: '🍿'
            },
            {
                id: 'imdb_7',
                title: 'Recomendados Gerais',
                tag: 'IMDb ★ 7.0+',
                tagClass: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
                desc: 'Histórias sólidas com avaliação consistente.',
                icon: '🎯'
            },
            {
                id: 'all',
                title: 'Qualquer Avaliação',
                tag: 'Sem filtro',
                tagClass: 'bg-white/10 text-slate-300 border-white/20',
                desc: 'Ver todas as obras do gênero sem restrição de nota.',
                icon: '🎬'
            }
        ];

        function init() {
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
                        catalog = parsed.map(item => {
                            const initItem = INITIAL_DATA.find(i => i.id === item.id) || {};
                            return {
                                ...initItem,
                                ...item,
                                genre: initItem.genre || item.genre || 'Drama',
                                platform: initItem.platform || item.platform || 'Netflix',
                                year: item.year || initItem.year || 2020,
                                imdb: item.imdb !== undefined ? item.imdb : (initItem.imdb || null),
                                rtCritics: item.rtCritics !== undefined ? item.rtCritics : (initItem.rtCritics || null),
                                rtAudience: item.rtAudience !== undefined ? item.rtAudience : (initItem.rtAudience || null),
                            };
                        });
                        const setIds = new Set(catalog.map(c => c.id));
                        for (const it of INITIAL_DATA) {
                            if (!setIds.has(it.id)) catalog.push(JSON.parse(JSON.stringify(it)));
                        }
                        persist();
                    } else {
                        catalog = JSON.parse(JSON.stringify(INITIAL_DATA));
                        persist();
                    }
                } else {
                    catalog = JSON.parse(JSON.stringify(INITIAL_DATA));
                    persist();
                }
            } catch (e) {
                catalog = JSON.parse(JSON.stringify(INITIAL_DATA));
            }

            window.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    closeFilterModal();
                    closeRandomizerModal();
                    closeAddModal();
                    closeExportModal();
                    closeAllStatusDropdowns();
                }
                if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
                    e.preventDefault();
                    if (document.getElementById('catalog-view').classList.contains('hidden')) {
                        switchView('catalog');
                    }
                    setTimeout(() => document.getElementById('search-input')?.focus(), 50);
                }
            });

            document.addEventListener('click', () => closeAllStatusDropdowns());

            // Check view routing
            const hash = window.location.hash;
            const savedView = sessionStorage.getItem('cinevault_view');
            if (hash === '#catalog' || savedView === 'catalog') {
                switchView('catalog', false);
            } else {
                switchView('wizard', false);
            }

            syncStyles();
            render();
            updateWizardUI();
        }

        function persist() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(catalog));
            } catch (e) {}
        }

        function escapeHtml(str) {
            if (!str) return '';
            return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
        }

        function getPlatformBadgeClass(p) {
            if (!p) return 'badge-netflix';
            const pl = p.toLowerCase();
            if (pl.includes('netflix')) return 'badge-netflix';
            if (pl.includes('max') || pl.includes('hbo')) return 'badge-max';
            if (pl.includes('prime') || pl.includes('amazon')) return 'badge-prime';
            if (pl.includes('disney') || pl.includes('star+')) return 'badge-disney';
            if (pl.includes('apple')) return 'badge-apple';
            if (pl.includes('paramount')) return 'badge-paramount';
            if (pl.includes('mubi')) return 'badge-mubi';
            if (pl.includes('globoplay')) return 'badge-globoplay';
            return 'badge-prime';
        }

        // ================= WIZARD CONTROLLER =================
        function getLiveMatchCount(wType, wGenre, wRating) {
            return catalog.filter(item => {
                if (wType === 'movie' && item.type !== 'movie') return false;
                if (wType === 'series' && item.type !== 'series') return false;
                if (wGenre !== 'all' && item.genre !== wGenre) return false;
                if (wRating === 'imdb_8' && (!item.imdb || item.imdb < 8.0)) return false;
                if (wRating === 'imdb_75' && (!item.imdb || item.imdb < 7.5)) return false;
                if (wRating === 'imdb_7' && (!item.imdb || item.imdb < 7.0)) return false;
                if (wRating === 'rt_critics' && (!item.rtCritics || item.rtCritics < 75)) return false;
                if (wRating === 'rt_audience' && (!item.rtAudience || item.rtAudience < 80)) return false;
                return true;
            }).length;
        }

        function renderWizardGenres() {
            const grid = document.getElementById('wizard-genre-grid');
            if (!grid) return;
            const formatLabel = wizardState.type === 'movie' ? 'filmes' : (wizardState.type === 'series' ? 'séries' : 'obras');
            grid.innerHTML = WIZARD_GENRES.map(g => {
                const count = getLiveMatchCount(wizardState.type, g.id, 'all');
                const isSelected = wizardState.genre === g.id;
                const selectedClass = isSelected ? 'selected' : '';
                const countClass = count > 0 ? 'text-purple-300' : 'text-slate-600';
                return `
                    <div onclick="selectWizardGenre('${g.id}')" data-w-genre="${g.id}" class="wizard-card p-3 sm:p-3.5 flex flex-col justify-between ${selectedClass}">
                        <div>
                            <div class="flex items-center justify-between gap-1 mb-1.5">
                                <span class="text-xl sm:text-2xl">${g.icon}</span>
                                ${isSelected ? '<span class="w-4 h-4 rounded-full bg-purple-500 text-white flex items-center justify-center text-[10px] font-bold">✓</span>' : ''}
                            </div>
                            <h4 class="font-bold text-xs sm:text-sm text-white leading-tight mb-0.5">${escapeHtml(g.label)}</h4>
                            <p class="text-[11px] text-slate-400 leading-snug line-clamp-1">${escapeHtml(g.desc)}</p>
                        </div>
                        <div class="mt-2.5 pt-2 border-t border-white/[0.04] flex items-center justify-between text-[11px] font-mono">
                            <span class="${countClass}">${count} ${formatLabel}</span>
                            <span class="w-1.5 h-1.5 rounded-full ${count > 0 ? 'bg-purple-500/60' : 'bg-slate-700'}"></span>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function renderWizardRatings() {
            const grid = document.getElementById('wizard-ratings-grid');
            if (!grid) return;
            const formatLabel = wizardState.type === 'movie' ? 'filmes' : (wizardState.type === 'series' ? 'séries' : 'obras');
            grid.innerHTML = WIZARD_RATINGS.map(r => {
                const count = getLiveMatchCount(wizardState.type, wizardState.genre, r.id);
                const isSelected = wizardState.ratingChoice === r.id;
                const selectedClass = isSelected ? 'selected' : '';
                const countClass = count > 0 ? 'text-purple-300' : 'text-slate-600';
                return `
                    <div onclick="selectWizardRating('${r.id}')" data-w-rating="${r.id}" class="wizard-card p-4 flex flex-col justify-between ${selectedClass}">
                        <div>
                            <div class="flex items-start justify-between gap-2 mb-2">
                                <div class="flex items-center gap-2">
                                    <span class="text-2xl">${r.icon}</span>
                                    <span class="px-2 py-0.5 rounded-lg text-[10px] font-mono border ${r.tagClass}">${r.tag}</span>
                                </div>
                                ${isSelected ? '<span class="w-4 h-4 rounded-full bg-purple-500 text-white flex items-center justify-center text-[10px] font-bold">✓</span>' : ''}
                            </div>
                            <h4 class="font-bold text-sm text-white mb-1">${escapeHtml(r.title)}</h4>
                            <p class="text-xs text-slate-400 leading-relaxed">${escapeHtml(r.desc)}</p>
                        </div>
                        <div class="mt-3 pt-2.5 border-t border-white/[0.04] flex items-center justify-between text-xs font-mono">
                            <span class="${countClass}">${count} ${formatLabel} disponíveis</span>
                            <span class="w-1.5 h-1.5 rounded-full ${count > 0 ? 'bg-emerald-400' : 'bg-slate-700'}"></span>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function updateWizardUI() {
            const p1 = document.getElementById('step-panel-1');
            const p2 = document.getElementById('step-panel-2');
            const p3 = document.getElementById('step-panel-3');
            if (!p1 || !p2 || !p3) return;

            p1.classList.toggle('hidden', wizardState.step !== 1);
            p2.classList.toggle('hidden', wizardState.step !== 2);
            p3.classList.toggle('hidden', wizardState.step !== 3);

            const titles = ["Formato da Sessão", "Gênero & Atmosfera", "Nível de Avaliação"];
            const summaries = ["Passo 1: Tipo", "Passo 2: Gênero", "Passo 3: Notas"];
            const sb = document.getElementById('wizard-step-badge');
            const th = document.getElementById('wizard-step-title-header');
            const ps = document.getElementById('wizard-progress-summary');
            if (sb) sb.textContent = `${wizardState.step} / 3`;
            if (th) th.textContent = titles[wizardState.step - 1];
            if (ps) ps.textContent = summaries[wizardState.step - 1];

            for (let i = 1; i <= 3; i++) {
                const bar = document.getElementById(`prog-bar-${i}`);
                if (bar) {
                    bar.classList.toggle('bg-purple-500', i <= wizardState.step);
                    bar.classList.toggle('bg-white/[0.08]', i > wizardState.step);
                }
            }

            const backBtn = document.getElementById('wizard-back-btn');
            const backSpacer = document.getElementById('wizard-back-spacer');
            if (backBtn && backSpacer) {
                if (wizardState.step > 1) {
                    backBtn.classList.remove('hidden');
                    backSpacer.classList.add('hidden');
                } else {
                    backBtn.classList.add('hidden');
                    backSpacer.classList.remove('hidden');
                }
            }

            const movieCount = catalog.filter(i => i.type === 'movie').length;
            const seriesCount = catalog.filter(i => i.type === 'series').length;
            const allCount = catalog.length;
            const mb = document.getElementById('w-badge-count-movies');
            if (mb) mb.textContent = `${movieCount} títulos`;
            const sbx = document.getElementById('w-badge-count-series');
            if (sbx) sbx.textContent = `${seriesCount} títulos`;
            const ab = document.getElementById('w-badge-count-all');
            if (ab) ab.textContent = `${allCount} títulos`;

            document.querySelectorAll('[data-w-type]').forEach(el => {
                el.classList.toggle('selected', el.getAttribute('data-w-type') === wizardState.type);
            });

            if (wizardState.step === 2) {
                renderWizardGenres();
            } else if (wizardState.step === 3) {
                renderWizardRatings();
            }

            const currentRating = wizardState.step === 3 ? wizardState.ratingChoice : 'all';
            const currentGenre = wizardState.step >= 2 ? wizardState.genre : 'all';
            const liveCount = getLiveMatchCount(wizardState.type, currentGenre, currentRating);

            const liveText = document.getElementById('wizard-live-match-text');
            if (liveText) {
                if (liveCount === 0) {
                    liveText.textContent = '0 obras com este filtro restrito';
                    liveText.classList.add('text-amber-300');
                } else {
                    liveText.textContent = `${liveCount} títulos combinam`;
                    liveText.classList.remove('text-amber-300');
                }
            }

            const nextText = document.getElementById('wizard-next-text');
            if (nextText) {
                if (wizardState.step === 3) {
                    if (liveCount > 0) {
                        nextText.textContent = `Ver ${liveCount} Obras`;
                    } else {
                        nextText.textContent = 'Ver Obras do Gênero';
                    }
                } else {
                    nextText.textContent = 'Continuar';
                }
            }
        }

        function goToStep(s) {
            if (s >= 1 && s <= 3) {
                wizardState.step = s;
                updateWizardUI();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }

        function selectWizardType(type) {
            wizardState.type = type;
            updateWizardUI();
        }

        function selectWizardGenre(genre) {
            wizardState.genre = genre;
            updateWizardUI();
        }

        function selectWizardRating(ratingChoice) {
            wizardState.ratingChoice = ratingChoice;
            updateWizardUI();
        }

        function wizardNextStep() {
            if (wizardState.step < 3) {
                wizardState.step++;
                updateWizardUI();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                const liveCount = getLiveMatchCount(wizardState.type, wizardState.genre, wizardState.ratingChoice);
                if (liveCount === 0) {
                    wizardState.ratingChoice = 'all';
                }
                applyWizardToCatalog();
            }
        }

        function wizardPrevStep() {
            if (wizardState.step > 1) {
                wizardState.step--;
                updateWizardUI();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }

        function applyWizardToCatalog() {
            state.search = '';
            state.status = 'all';
            state.origin = 'all';
            state.decade = 'all';
            state.type = wizardState.type;
            state.genre = wizardState.genre;

            state.minImdb = 0;
            state.rtCritics = 'all';
            state.rtAudience = 'all';

            if (wizardState.ratingChoice === 'imdb_8') {
                state.minImdb = 8.0;
            } else if (wizardState.ratingChoice === 'imdb_75') {
                state.minImdb = 7.5;
            } else if (wizardState.ratingChoice === 'imdb_7') {
                state.minImdb = 7.0;
            } else if (wizardState.ratingChoice === 'rt_critics') {
                state.rtCritics = 'certified';
            } else if (wizardState.ratingChoice === 'rt_audience') {
                state.rtAudience = 'high';
            }

            switchView('catalog');
            syncStyles();
            render();

            const count = getFilteredCatalog().length;
            notify(`Assistente: ${count} títulos encontrados!`);
        }

        function skipWizard() {
            resetAllFilters();
            switchView('catalog');
            notify("Exibindo catálogo completo sem filtros (217 títulos)");
        }

        function openWizard() {
            switchView('wizard');
            updateWizardUI();
        }

        function showCatalog() {
            switchView('catalog');
        }

        function switchView(viewName, updateHash = true) {
            const wView = document.getElementById('wizard-view');
            const cView = document.getElementById('catalog-view');
            if (!wView || !cView) return;

            if (viewName === 'wizard') {
                wView.classList.remove('hidden');
                cView.classList.add('hidden');
                if (updateHash) {
                    try { history.replaceState(null, '', '#assistente'); } catch (e) {}
                }
                sessionStorage.setItem('cinevault_view', 'wizard');
                updateWizardUI();
                window.scrollTo({ top: 0, behavior: 'instant' });
            } else {
                wView.classList.add('hidden');
                cView.classList.remove('hidden');
                if (updateHash) {
                    try { history.replaceState(null, '', '#catalog'); } catch (e) {}
                }
                sessionStorage.setItem('cinevault_view', 'catalog');
                syncStyles();
                render();
                window.scrollTo({ top: 0, behavior: 'instant' });
            }
        }

        // ================= CATALOG LOGIC =================
        function getFilteredCatalog() {
            return catalog.filter(item => {
                if (state.search) {
                    const q = state.search.toLowerCase().trim();
                    const inTitle = (item.title || '').toLowerCase().includes(q);
                    const inSub = (item.subgenre || '').toLowerCase().includes(q);
                    const inGenre = (item.genre || '').toLowerCase().includes(q);
                    const inPlatform = (item.platform || '').toLowerCase().includes(q);
                    const inNote = (item.note || '').toLowerCase().includes(q);
                    const inYear = String(item.year || '').includes(q);
                    if (!inTitle && !inSub && !inGenre && !inPlatform && !inNote && !inYear) return false;
                }

                if (state.status === 'priority' && item.status !== 'priority') return false;
                if (state.status === 'queue' && item.status !== 'queue') return false;
                if (state.status === 'watched' && item.status !== 'watched') return false;
                if (state.status === 'pending' && (item.status !== 'priority' && item.status !== 'queue')) return false;

                if (state.type === 'movie' && item.type !== 'movie') return false;
                if (state.type === 'series' && item.type !== 'series') return false;

                if (state.genre !== 'all' && item.genre !== state.genre) return false;
                if (state.platform !== 'all' && item.platform !== state.platform) return false;
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
            }).sort((a, b) => {
                if (state.sort === 'imdb_desc') return (b.imdb || 0) - (a.imdb || 0) || a.title.localeCompare(b.title, 'pt-BR');
                if (state.sort === 'critics_desc') return (b.rtCritics || 0) - (a.rtCritics || 0) || a.title.localeCompare(b.title, 'pt-BR');
                if (state.sort === 'audience_desc') return (b.rtAudience || 0) - (a.rtAudience || 0) || a.title.localeCompare(b.title, 'pt-BR');
                if (state.sort === 'year_desc') return (b.year || 0) - (a.year || 0) || a.title.localeCompare(b.title, 'pt-BR');
                if (state.sort === 'alpha_asc') return a.title.localeCompare(b.title, 'pt-BR');

                const rank = { priority: 1, queue: 2, watched: 3 };
                if (rank[a.status] !== rank[b.status]) return rank[a.status] - rank[b.status];
                return a.title.localeCompare(b.title, 'pt-BR');
            });
        }

        function getActiveFilterCount() {
            let c = 0;
            if (state.search.trim()) c++;
            if (state.status !== 'all') c++;
            if (state.type !== 'all') c++;
            if (state.genre !== 'all') c++;
            if (state.platform !== 'all') c++;
            if (state.origin !== 'all') c++;
            if (state.minImdb > 0) c++;
            if (state.rtCritics !== 'all') c++;
            if (state.rtAudience !== 'all') c++;
            if (state.decade !== 'all') c++;
            return c;
        }

        function closeAllStatusDropdowns() {
            document.querySelectorAll('.status-dropdown-menu').forEach(el => el.classList.add('hidden'));
        }

        function toggleStatusDropdown(id, e) {
            e.stopPropagation();
            const menu = document.getElementById(`status-dropdown-${id}`);
            if (!menu) return;
            const isHidden = menu.classList.contains('hidden');
            closeAllStatusDropdowns();
            if (isHidden) menu.classList.remove('hidden');
        }

        function render() {
            const list = getFilteredCatalog();
            const total = catalog.length;
            const watched = catalog.filter(i => i.status === 'watched').length;
            const priority = catalog.filter(i => i.status === 'priority').length;
            const queue = catalog.filter(i => i.status === 'queue').length;
            const series = catalog.filter(i => i.type === 'series').length;
            const pct = total > 0 ? Math.round((watched / total) * 100) : 0;

            const telText = document.getElementById('telemetry-text');
            const telBar = document.getElementById('telemetry-bar');
            if (telText) telText.textContent = `${watched} de ${total} assistidos (${pct}%)`;
            if (telBar) telBar.style.width = `${pct}%`;

            const countMap = { all: total, priority, queue, watched, series };
            document.querySelectorAll('[data-tab-count]').forEach(el => {
                const k = el.getAttribute('data-tab-count');
                if (countMap[k] !== undefined) el.textContent = countMap[k];
            });

            const filterCount = getActiveFilterCount();
            document.getElementById('header-filter-badge')?.classList.toggle('hidden', filterCount === 0);
            document.getElementById('bnav-filter-dot')?.classList.toggle('hidden', filterCount === 0);
            const mCount = document.getElementById('modal-counter-badge');
            if (mCount) mCount.textContent = list.length;

            // Concierge Active Banner
            const banner = document.getElementById('wizard-active-banner');
            const bannerCount = document.getElementById('wizard-banner-count');
            const bannerDesc = document.getElementById('wizard-banner-desc');
            const isWizardActive = (state.type !== 'all' || state.genre !== 'all' || state.minImdb > 0 || state.rtCritics !== 'all' || state.rtAudience !== 'all');

            if (banner) {
                if (isWizardActive) {
                    banner.classList.remove('hidden');
                    if (bannerCount) bannerCount.textContent = `${list.length} obras`;
                    const parts = [];
                    if (state.type === 'movie') parts.push('🎬 Filmes');
                    else if (state.type === 'series') parts.push('📺 Séries');
                    else parts.push('🍿 Filmes & Séries');

                    if (state.genre !== 'all') parts.push(state.genre);
                    else parts.push('Todos os gêneros');

                    if (state.minImdb >= 8.0) parts.push('★ IMDb 8.0+');
                    else if (state.minImdb >= 7.5) parts.push('★ IMDb 7.5+');
                    else if (state.minImdb >= 7.0) parts.push('★ IMDb 7.0+');
                    else if (state.rtCritics === 'certified') parts.push('🍅 Certified Fresh (≥75%)');
                    else if (state.rtAudience === 'high') parts.push('🍿 Favoritos Público (≥85%)');

                    if (bannerDesc) bannerDesc.textContent = parts.join(' · ');
                } else {
                    banner.classList.add('hidden');
                }
            }

            // Standard Active Filters Bar
            const bar = document.getElementById('active-filters-bar');
            const chips = document.getElementById('active-chips-container');
            if (filterCount > 0 && !isWizardActive) {
                bar.classList.remove('hidden');
                let html = '';
                if (state.search) html += `<span class="px-2 py-0.5 rounded-md bg-white/[0.06] text-slate-300">"${escapeHtml(state.search)}"</span>`;
                if (state.status !== 'all') html += `<span class="px-2 py-0.5 rounded-md bg-white/[0.06] text-slate-300">Status: ${state.status}</span>`;
                if (state.genre !== 'all') html += `<span class="px-2 py-0.5 rounded-md bg-white/[0.06] text-purple-300">${state.genre}</span>`;
                if (state.platform !== 'all') html += `<span class="px-2 py-0.5 rounded-md bg-blue-500/15 text-blue-300 font-mono">${state.platform}</span>`;
                chips.innerHTML = `<span class="text-slate-500 mr-1">Filtros ativos:</span> ` + html;
            } else {
                bar.classList.add('hidden');
            }

            const gridEl = document.getElementById('catalog-grid');
            const tableWrapperEl = document.getElementById('catalog-table-wrapper');
            const emptyEl = document.getElementById('empty-state');

            if (list.length === 0) {
                gridEl.classList.add('hidden');
                tableWrapperEl.classList.add('hidden');
                emptyEl.classList.remove('hidden');
                return;
            }
            emptyEl.classList.add('hidden');

            if (state.view === 'grid') {
                tableWrapperEl.classList.add('hidden');
                gridEl.classList.remove('hidden');

                gridEl.innerHTML = list.map(item => {
                    const isWatched = item.status === 'watched';
                    const isPriority = item.status === 'priority';
                    const dotColor = isPriority ? 'bg-amber-400 shadow-[0_0_6px_#F59E0B]' : (isWatched ? 'bg-emerald-400 shadow-[0_0_6px_#10B981]' : 'bg-slate-500');
                    const statusText = isPriority ? 'Prioridade' : (isWatched ? 'Concluído' : 'Na Fila');
                    const statusColor = isPriority ? 'text-amber-300' : (isWatched ? 'text-emerald-400' : 'text-slate-400');
                    const pBadgeClass = getPlatformBadgeClass(item.platform);

                    return `
                        <div class="card-clean rounded-2xl p-4 flex flex-col justify-between group relative">
                            <div>
                                <!-- Top Row: Status Button + Platform + Year -->
                                <div class="flex items-center justify-between text-xs mb-2">
                                    <div class="relative inline-block text-left">
                                        <button onclick="toggleStatusDropdown('${item.id}', event)" class="inline-flex items-center gap-1.5 font-medium ${statusColor} hover:opacity-80 transition bg-white/[0.03] px-2 py-0.5 rounded-lg border border-white/[0.05]" title="Clique para escolher o status">
                                            <span class="w-1.5 h-1.5 rounded-full ${dotColor}"></span>
                                            <span>${statusText}</span>
                                            <svg class="w-2.5 h-2.5 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"></polyline></svg>
                                        </button>

                                        <!-- Direct Choice Status Dropdown -->
                                        <div id="status-dropdown-${item.id}" onclick="event.stopPropagation()" class="status-dropdown-menu hidden absolute left-0 top-7 z-40 w-36 rounded-xl bg-[#141722] border border-white/10 shadow-2xl py-1 text-xs">
                                            <button onclick="setItemStatus('${item.id}', 'priority'); closeAllStatusDropdowns();" class="w-full text-left px-3 py-1.5 hover:bg-white/[0.06] flex items-center gap-2 text-amber-300 font-medium">
                                                <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span> Prioridade ★
                                            </button>
                                            <button onclick="setItemStatus('${item.id}', 'queue'); closeAllStatusDropdowns();" class="w-full text-left px-3 py-1.5 hover:bg-white/[0.06] flex items-center gap-2 text-slate-300">
                                                <span class="w-1.5 h-1.5 rounded-full bg-slate-500"></span> Na Fila
                                            </button>
                                            <button onclick="setItemStatus('${item.id}', 'watched'); closeAllStatusDropdowns();" class="w-full text-left px-3 py-1.5 hover:bg-white/[0.06] flex items-center gap-2 text-emerald-400 font-medium">
                                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Concluído ✓
                                            </button>
                                        </div>
                                    </div>

                                    <div class="flex items-center gap-1.5 font-mono text-[11px] text-slate-500">
                                        ${item.year ? `<span>${item.year}</span>` : ''}
                                        ${item.type === 'series' ? `<span class="text-[9px] uppercase tracking-wider px-1 py-0.2 rounded bg-purple-500/15 text-purple-300 border border-purple-500/20">Série</span>` : ''}
                                    </div>
                                </div>

                                <!-- Title -->
                                <h3 onclick="openEditModal('${item.id}')" class="font-bold text-[15px] text-white leading-snug tracking-tight group-hover:text-purple-300 transition cursor-pointer mb-1">
                                    ${escapeHtml(item.title)}
                                </h3>

                                <!-- Genre & Subgenre -->
                                <p class="text-xs text-slate-400 truncate mb-2.5">
                                    <span class="text-purple-300/90 font-medium">${escapeHtml(item.genre)}</span>
                                    ${item.subgenre ? `<span class="text-slate-600"> · </span><span class="text-slate-500">${escapeHtml(item.subgenre)}</span>` : ''}
                                </p>

                                <!-- Quiet Ratings Row -->
                                <div class="flex items-center gap-2.5 text-xs font-mono mb-3">
                                    <span class="inline-flex items-center gap-1 text-amber-400/95" title="Nota IMDb">
                                        <span class="font-bold text-[10px] bg-amber-400/15 text-amber-300 px-1 py-0.5 rounded leading-none">IMDb</span>
                                        <span>${item.imdb ? item.imdb.toFixed(1) : '—'}</span>
                                    </span>
                                    <span class="text-slate-700">·</span>
                                    <span class="inline-flex items-center gap-1 text-rose-300/90" title="Rotten Tomatoes Crítica">
                                        <span>🍅</span>
                                        <span>${item.rtCritics ? item.rtCritics + '%' : '—'}</span>
                                    </span>
                                    <span class="text-slate-700">·</span>
                                    <span class="inline-flex items-center gap-1 text-amber-200/90" title="Rotten Tomatoes Público">
                                        <span>🍿</span>
                                        <span>${item.rtAudience ? item.rtAudience + '%' : '—'}</span>
                                    </span>
                                </div>

                                <!-- Optional Note -->
                                ${item.note ? `
                                    <p class="text-[11px] text-slate-400 italic bg-white/[0.02] border border-white/[0.04] rounded-lg px-2.5 py-1 mb-2.5 truncate">
                                        "${escapeHtml(item.note)}"
                                    </p>
                                ` : ''}
                            </div>

                            <!-- Bottom Action Bar: Easy 1-Click 'Visto' + Platform Button -->
                            <div class="pt-2.5 border-t border-white/[0.04] flex items-center justify-between gap-2 text-xs">
                                
                                <!-- Platform Button / Link -->
                                <a href="https://www.justwatch.com/br/busca?q=${encodeURIComponent(item.title)}" target="_blank" rel="noopener noreferrer" class="h-7 px-2.5 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.08] text-slate-300 hover:text-white text-[11px] font-medium transition inline-flex items-center gap-1.5 shrink-0" title="Ver onde assistir no streaming">
                                    <svg class="w-3 h-3 text-slate-400 group-hover:text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polygon points="10 8 16 12 10 16 10 8"></polygon></svg>
                                    <span>Ver plataforma</span>
                                    <svg class="w-2.5 h-2.5 opacity-60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                                </a>

                                <div class="flex items-center gap-1.5 ml-auto">
                                    <!-- 1-CLICK EASY MARCAR COMO VISTO BUTTON -->
                                    ${!isWatched ? `
                                        <button onclick="setItemStatus('${item.id}', 'watched')" class="h-7 px-2.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 active:scale-95 text-emerald-400 border border-emerald-500/25 text-[11px] font-semibold transition flex items-center gap-1" title="Marcar como Concluído em 1 clique">
                                            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                            <span>Visto</span>
                                        </button>
                                    ` : `
                                        <button onclick="setItemStatus('${item.id}', 'queue')" class="h-7 px-2.5 rounded-lg bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 text-[11px] font-semibold transition flex items-center gap-1" title="Já concluído (clique para voltar para a fila)">
                                            <svg class="w-3 h-3 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                            <span>Concluído</span>
                                        </button>
                                    `}

                                    <!-- Minimal star / edit -->
                                    <button onclick="openEditModal('${item.id}')" class="h-7 w-7 rounded-lg bg-white/[0.03] hover:bg-white/[0.08] flex items-center justify-center text-slate-400 hover:text-white" title="Editar / Detalhes">
                                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                }).join('');
            } else {
                // Compact List View
                gridEl.classList.add('hidden');
                tableWrapperEl.classList.remove('hidden');

                tableWrapperEl.innerHTML = list.map(item => {
                    const isWatched = item.status === 'watched';
                    const isPriority = item.status === 'priority';
                    const dotColor = isPriority ? 'bg-amber-400 shadow-[0_0_6px_#F59E0B]' : (isWatched ? 'bg-emerald-400 shadow-[0_0_6px_#10B981]' : 'bg-slate-500');
                    const statusText = isPriority ? 'Prioridade' : (isWatched ? 'Concluído' : 'Na Fila');
                    const statusColor = isPriority ? 'text-amber-300' : (isWatched ? 'text-emerald-400' : 'text-slate-400');
                    const pBadgeClass = getPlatformBadgeClass(item.platform);

                    return `
                        <div class="p-3 sm:px-4 flex items-center justify-between gap-3 hover:bg-white/[0.02] transition">
                            <div class="min-w-0 flex-1 cursor-pointer" onclick="openEditModal('${item.id}')">
                                <div class="flex items-center gap-2 mb-0.5">
                                    <span class="w-2 h-2 rounded-full shrink-0 ${dotColor}"></span>
                                    <h4 class="font-semibold text-xs sm:text-sm text-white truncate">${escapeHtml(item.title)}</h4>
                                    ${item.year ? `<span class="font-mono text-[11px] text-slate-500">(${item.year})</span>` : ''}
                                    <span class="text-[10px] px-1.5 py-0.2 rounded font-medium ${pBadgeClass}">${escapeHtml(item.platform)}</span>
                                </div>
                                <div class="flex items-center gap-2.5 text-xs text-slate-400 pl-4">
                                    <span class="text-purple-300/80 truncate">${escapeHtml(item.genre)}</span>
                                    <span class="text-slate-700">·</span>
                                    <span class="font-mono text-amber-400/90">★ ${item.imdb ? item.imdb.toFixed(1) : '—'}</span>
                                    <span class="font-mono text-rose-300/90">🍅 ${item.rtCritics ? item.rtCritics + '%' : '—'}</span>
                                    <span class="font-mono text-amber-200/90">🍿 ${item.rtAudience ? item.rtAudience + '%' : '—'}</span>
                                </div>
                            </div>
                            <div class="flex items-center gap-2 shrink-0">
                                <a href="https://www.justwatch.com/br/busca?q=${encodeURIComponent(item.title)}" target="_blank" rel="noopener noreferrer" class="h-8 px-2.5 rounded-lg border border-white/[0.08] text-[11px] font-medium text-slate-300 hover:text-white flex items-center gap-1.5" title="Ver onde assistir no streaming">
                                    <span>Ver plataforma</span>
                                    <svg class="w-3 h-3 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                                </a>
                                
                                ${!isWatched ? `
                                    <button onclick="setItemStatus('${item.id}', 'watched')" class="h-8 px-2.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/25 text-[11px] font-semibold transition flex items-center gap-1" title="Marcar como Concluído em 1 clique">
                                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                        <span>Visto</span>
                                    </button>
                                ` : `
                                    <button onclick="setItemStatus('${item.id}', 'queue')" class="h-8 px-2.5 rounded-lg bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 text-[11px] font-semibold transition">
                                        ✓ Visto
                                    </button>
                                `}
                            </div>
                        </div>
                    `;
                }).join('');
            }
        }

        function setItemStatus(id, newStatus) {
            const item = catalog.find(i => i.id === id);
            if (!item) return;
            item.status = newStatus;
            persist();
            render();
            const labels = { priority: 'marcado como Prioridade ★', queue: 'colocado Na Fila', watched: 'marcado como Concluído! 🎉' };
            notify(`"${item.title}" ${labels[newStatus] || 'atualizado'}`);
        }

        function setStatusFilter(status) {
            state.status = status;
            if (status !== 'all') state.type = 'all';
            syncStyles();
            render();
        }

        function setTypeFilter(type) {
            state.type = type;
            if (type !== 'all') state.status = 'all';
            syncStyles();
            render();
        }

        function setGenreFilter(genre) {
            state.genre = genre;
            syncStyles();
            render();
        }

        function setPlatformFilter(p) {
            state.platform = p;
            syncStyles();
            render();
        }

        function setMinImdb(score) {
            state.minImdb = score;
            syncStyles();
            render();
        }

        function setRtCritics(val) {
            state.rtCritics = val;
            syncStyles();
            render();
        }

        function setRtAudience(val) {
            state.rtAudience = val;
            syncStyles();
            render();
        }

        function setDecadeFilter(dec) {
            state.decade = dec;
            syncStyles();
            render();
        }

        function setSortOrder(sort) {
            state.sort = sort;
            syncStyles();
            render();
        }

        function setViewMode(mode) {
            state.view = mode;
            syncStyles();
            render();
        }

        function handleSearch(val) {
            state.search = val;
            document.getElementById('clear-search-btn')?.classList.toggle('hidden', !val);
            render();
        }

        function clearSearch() {
            state.search = '';
            const inp = document.getElementById('search-input');
            if (inp) inp.value = '';
            document.getElementById('clear-search-btn')?.classList.add('hidden');
            render();
        }

        function resetAllFilters() {
            state.search = '';
            state.status = 'all';
            state.type = 'all';
            state.genre = 'all';
            state.platform = 'all';
            state.origin = 'all';
            state.minImdb = 0;
            state.rtCritics = 'all';
            state.rtAudience = 'all';
            state.decade = 'all';
            state.sort = 'status';

            wizardState.type = 'all';
            wizardState.genre = 'all';
            wizardState.ratingChoice = 'all';
            wizardState.step = 1;

            const inp = document.getElementById('search-input');
            if (inp) inp.value = '';
            document.getElementById('clear-search-btn')?.classList.add('hidden');
            syncStyles();
            render();
            notify("Filtros redefinidos");
        }

        function syncStyles() {
            document.querySelectorAll('.tab-pill').forEach(el => {
                const tab = el.getAttribute('data-tab');
                const active = (tab === 'series') ? state.type === 'series' : (state.status === tab && state.type === 'all');
                el.classList.toggle('bg-white/[0.12]', active);
                el.classList.toggle('text-white', active);
                el.classList.toggle('text-slate-300', !active);
            });

            document.querySelectorAll('.genre-chip').forEach(el => {
                const g = el.getAttribute('data-genre-chip');
                const active = state.genre === g;
                el.classList.toggle('bg-purple-600/30', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('text-purple-200', active);
                el.classList.toggle('text-slate-400', !active);
            });

            const isWView = !document.getElementById('wizard-view')?.classList.contains('hidden');
            document.querySelectorAll('[data-bnav]').forEach(el => {
                const b = el.getAttribute('data-bnav');
                let active = false;
                if (b === 'wizard') active = isWView;
                else if (b === 'catalog') active = !isWView && state.status === 'all';
                else if (b === 'watched') active = !isWView && state.status === 'watched';
                el.classList.toggle('text-purple-400', active);
                el.classList.toggle('text-slate-400', !active);
            });

            document.querySelectorAll('[data-m-status]').forEach(el => {
                const active = state.status === el.getAttribute('data-m-status');
                el.classList.toggle('bg-purple-600/25', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            });

            document.querySelectorAll('[data-m-genre]').forEach(el => {
                const active = state.genre === el.getAttribute('data-m-genre');
                el.classList.toggle('bg-purple-600/25', active);
                el.classList.toggle('border-purple-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            });

            document.querySelectorAll('[data-m-platform]').forEach(el => {
                const active = state.platform === el.getAttribute('data-m-platform');
                el.classList.toggle('bg-blue-600/25', active);
                el.classList.toggle('border-blue-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            });

            document.querySelectorAll('[data-m-imdb]').forEach(el => {
                const active = state.minImdb === parseFloat(el.getAttribute('data-m-imdb'));
                el.classList.toggle('bg-amber-500/25', active);
                el.classList.toggle('border-amber-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            });

            document.querySelectorAll('[data-m-rtcritics]').forEach(el => {
                const active = state.rtCritics === el.getAttribute('data-m-rtcritics');
                el.classList.toggle('bg-rose-500/25', active);
                el.classList.toggle('border-rose-500/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            });

            document.querySelectorAll('[data-m-rtaudience]').forEach(el => {
                const active = state.rtAudience === el.getAttribute('data-m-rtaudience');
                el.classList.toggle('bg-amber-400/25', active);
                el.classList.toggle('border-amber-400/50', active);
                el.classList.toggle('border-white/[0.08]', !active);
            });

            const isGrid = state.view === 'grid';
            document.getElementById('view-btn-grid')?.classList.toggle('text-white', isGrid);
            document.getElementById('view-btn-grid')?.classList.toggle('bg-white/[0.08]', isGrid);
            document.getElementById('view-btn-table')?.classList.toggle('text-white', !isGrid);
            document.getElementById('view-btn-table')?.classList.toggle('bg-white/[0.08]', !isGrid);

            const sortSel = document.getElementById('sort-select');
            if (sortSel) sortSel.value = state.sort;
        }

        function openFilterModal() {
            const m = document.getElementById('filter-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }

        function closeFilterModal() {
            const m = document.getElementById('filter-modal');
            m.classList.add('hidden');
            m.classList.remove('flex');
        }

        function openRandomizerModal() {
            const m = document.getElementById('randomizer-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }

        function closeRandomizerModal() {
            const m = document.getElementById('randomizer-modal');
            m.classList.add('hidden');
            m.classList.remove('flex');
        }

        function runRandomizer() {
            const pool = catalog.filter(i => i.status !== 'watched');
            if (pool.length === 0) return;

            const t = document.getElementById('rand-title');
            const meta = document.getElementById('rand-meta');
            const tag = document.getElementById('rand-tag');
            const ratings = document.getElementById('rand-ratings');
            const plat = document.getElementById('rand-platform');

            tag.textContent = "Sorteando...";
            ratings.classList.add('hidden');
            plat.classList.add('hidden');

            let count = 0;
            const timer = setInterval(() => {
                const item = pool[Math.floor(Math.random() * pool.length)];
                t.textContent = item.title;
                meta.textContent = `${item.genre} · ${item.year || ''}`;
                count++;
                if (count >= 14) {
                    clearInterval(timer);
                    tag.textContent = item.status === 'priority' ? '★ Prioridade' : 'Na Fila';
                    ratings.innerHTML = `IMDb ${item.imdb ? item.imdb.toFixed(1) : '-'} · 🍅 ${item.rtCritics || '-'}% · 🍿 ${item.rtAudience || '-'}%`;
                    ratings.classList.remove('hidden');

                    plat.innerHTML = `<span class="px-2 py-0.5 rounded text-[11px] font-medium ${getPlatformBadgeClass(item.platform)}">${item.platform}</span>`;
                    plat.classList.remove('hidden');
                }
            }, 60);
        }

        function openAddModal() {
            document.getElementById('entry-modal-title').textContent = 'Nova Obra';
            document.getElementById('entry-id').value = '';
            document.getElementById('entry-form').reset();
            document.getElementById('delete-entry-btn').classList.add('hidden');
            const m = document.getElementById('entry-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }

        function openEditModal(id) {
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
            document.getElementById('entry-platform').value = item.platform || 'Netflix';
            document.getElementById('entry-genre').value = item.genre;
            document.getElementById('entry-origin').value = item.origin;
            document.getElementById('entry-subgenre').value = item.subgenre || '';
            document.getElementById('entry-note').value = item.note || '';

            document.getElementById('delete-entry-btn').classList.remove('hidden');
            const m = document.getElementById('entry-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }

        function closeAddModal() {
            const m = document.getElementById('entry-modal');
            m.classList.add('hidden');
            m.classList.remove('flex');
        }

        function saveEntryForm(e) {
            e.preventDefault();
            const id = document.getElementById('entry-id').value;
            const title = document.getElementById('entry-title').value.trim();
            const yearVal = parseInt(document.getElementById('entry-year').value);
            const imdbVal = parseFloat(document.getElementById('entry-imdb').value);
            const rtCritVal = parseInt(document.getElementById('entry-rt-critics').value);
            const rtAudVal = parseInt(document.getElementById('entry-rt-audience').value);

            const payload = {
                title,
                year: isNaN(yearVal) ? null : yearVal,
                imdb: isNaN(imdbVal) ? null : imdbVal,
                rtCritics: isNaN(rtCritVal) ? null : rtCritVal,
                rtAudience: isNaN(rtAudVal) ? null : rtAudVal,
                type: document.getElementById('entry-type').value,
                status: document.getElementById('entry-status').value,
                platform: document.getElementById('entry-platform').value,
                genre: document.getElementById('entry-genre').value,
                origin: document.getElementById('entry-origin').value,
                subgenre: document.getElementById('entry-subgenre').value.trim(),
                note: document.getElementById('entry-note').value.trim()
            };

            if (id) {
                const item = catalog.find(i => i.id === id);
                if (item) Object.assign(item, payload);
                notify(`"${title}" atualizado`);
            } else {
                catalog.unshift({ id: 'custom_' + Date.now(), ...payload, rating: 0 });
                notify(`"${title}" adicionado`);
            }
            persist();
            render();
            closeAddModal();
        }

        function deleteCurrentEntry() {
            const id = document.getElementById('entry-id').value;
            if (!id) return;
            const item = catalog.find(i => i.id === id);
            if (!item) return;

            if (confirm(`Remover "${item.title}"?`)) {
                catalog = catalog.filter(i => i.id !== id);
                persist();
                render();
                closeAddModal();
                notify(`"${item.title}" removido`);
            }
        }

        function openExportModal() {
            document.getElementById('export-textarea').value = JSON.stringify(catalog, null, 2);
            const m = document.getElementById('export-modal');
            m.classList.remove('hidden');
            m.classList.add('flex');
        }

        function closeExportModal() {
            const m = document.getElementById('export-modal');
            m.classList.add('hidden');
            m.classList.remove('flex');
        }

        function copyExportText() {
            const ta = document.getElementById('export-textarea');
            ta.select();
            navigator.clipboard.writeText(ta.value).then(() => notify("JSON copiado!"));
        }

        function downloadJson() {
            const blob = new Blob([JSON.stringify(catalog, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cinevault_backup_${new Date().toISOString().slice(0, 10)}.json`;
            a.click();
            URL.revokeObjectURL(url);
            notify("Arquivo baixado!");
        }

        function importJson(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    if (Array.isArray(data)) {
                        catalog = data;
                        persist();
                        render();
                        closeExportModal();
                        notify(`${data.length} títulos restaurados!`);
                    }
                } catch (err) {
                    alert("JSON inválido");
                }
            };
            reader.readAsText(file);
        }

        let toastTimer;
        function notify(text) {
            const t = document.getElementById('toast');
            const txt = document.getElementById('toast-text');
            txt.textContent = text;
            t.classList.remove('hidden');
            requestAnimationFrame(() => t.classList.remove('translate-y-2', 'opacity-0'));
            clearTimeout(toastTimer);
            toastTimer = setTimeout(() => {
                t.classList.add('translate-y-2', 'opacity-0');
                setTimeout(() => t.classList.add('hidden'), 200);
            }, 2400);
        }

        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
"""

final_html = HTML_PAGE.replace('__INITIAL_DATA__', js_items)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

with open('cinevault_emannuel_petry.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("SUCCESS: index.html and cinevault_emannuel_petry.html updated with Discovery Flow (Etapas)!")
