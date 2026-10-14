import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { CatalogItem } from "@/types";
import { cn } from "@/lib/utils";
import {
  Film,
  Tv,
  Sparkles,
  ChevronLeft,
  ChevronRight,
  Star,
  CheckCircle2,
  X,
  Compass
} from "lucide-react";

interface WizardConciergeProps {
  catalog: CatalogItem[];
  onComplete: (filters: { type: 'all' | 'movie' | 'series'; genre: string; ratingFilter: string }) => void;
  onSkip: () => void;
  isOpen: boolean;
  onClose: () => void;
}

const WIZARD_GENRES = [
  { name: "all", label: "Qualquer Gênero", emoji: "✨", desc: "Explorar todos os gêneros" },
  { name: "Suspense & Mistério", label: "Suspense & Mistério", emoji: "🔍", desc: "Enigmas, reviravoltas e tensão contínua" },
  { name: "Thriller Psicológico", label: "Thriller Psicológico", emoji: "🧠", desc: "Jogos mentais, obsessão e suspense profundo" },
  { name: "Ficção Científica", label: "Ficção Científica", emoji: "🚀", desc: "Futurismo, cosmos e distopias fascinantes" },
  { name: "Drama", label: "Drama & Emoção", emoji: "🎭", desc: "Histórias intensas e atuações memoráveis" },
  { name: "Crime & Policial", label: "Crime & Policial", emoji: "💼", desc: "Máfia, investigações e submundo" },
  { name: "Terror", label: "Terror", emoji: "👻", desc: "Medo visceral e atmosferas sombrias" },
  { name: "Ação & Aventura", label: "Ação & Aventura", emoji: "💥", desc: "Adrenalina pura e ritmo acelerado" },
  { name: "Comédia", label: "Comédia", emoji: "😄", desc: "Humor inteligente e leveza" },
  { name: "Biografia & Histórico", label: "Biografia & História", emoji: "📜", desc: "Fatos reais que moldaram o mundo" },
  { name: "Romance", label: "Romance", emoji: "❤️", desc: "Relações marcantes e sentimentos" },
  { name: "Guerra", label: "Guerra", emoji: "⚔️", desc: "Conflitos históricos e sobrevivência" },
  { name: "Animação", label: "Animação", emoji: "🎨", desc: "Obras visuais criativas e cativantes" },
];

const WIZARD_RATINGS = [
  { id: "all", title: "Qualquer Avaliação", desc: "Sem corte de nota, ver todas as obras", badge: "✨ Sem filtro" },
  { id: "imdb_8", title: "Obras-Primas", desc: "Nota IMDb 8.0 ou superior", badge: "★ IMDb 8.0+" },
  { id: "rt_critics", title: "Aclamação da Crítica", desc: "Rotten Tomatoes Tomatometer 80%+", badge: "🍅 80%+ Crítica" },
  { id: "rt_audience", title: "Favoritos do Público", desc: "Rotten Tomatoes Popcornmeter 85%+", badge: "🍿 85%+ Público" },
];

export function WizardConcierge({
  catalog,
  onComplete,
  onSkip,
  isOpen,
  onClose,
}: WizardConciergeProps) {
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [selectedType, setSelectedType] = useState<'all' | 'movie' | 'series'>('all');
  const [selectedGenre, setSelectedGenre] = useState<string>('all');
  const [selectedRating, setSelectedRating] = useState<string>('all');
  const [direction, setDirection] = useState<number>(1);

  if (!isOpen) return null;

  // Calculate live matching count based on current wizard choices
  const getMatchCount = (t: 'all' | 'movie' | 'series', g: string, r: string) => {
    return catalog.filter(item => {
      if (t !== 'all' && item.type !== t) return false;
      if (g !== 'all' && item.genre !== g) return false;
      if (r === 'imdb_8' && (!item.imdb || item.imdb < 8.0)) return false;
      if (r === 'rt_critics' && (!item.rtCritics || item.rtCritics < 80)) return false;
      if (r === 'rt_audience' && (!item.rtAudience || item.rtAudience < 85)) return false;
      return true;
    }).length;
  };

  const currentMatchCount = getMatchCount(selectedType, selectedGenre, selectedRating);

  const nextStep = () => {
    if (step < 3) {
      setDirection(1);
      setStep((step + 1) as any);
    } else {
      onComplete({
        type: selectedType,
        genre: selectedGenre,
        ratingFilter: selectedRating,
      });
    }
  };

  const prevStep = () => {
    if (step > 1) {
      setDirection(-1);
      setStep((step - 1) as any);
    }
  };

  // Slide transition variants for 60fps mobile feel
  const variants = {
    enter: (dir: number) => ({
      x: dir > 0 ? 30 : -30,
      opacity: 0,
    }),
    center: {
      x: 0,
      opacity: 1,
      transition: {
        x: { type: "spring" as const, stiffness: 380, damping: 30 },
        opacity: { duration: 0.18 },
      },
    },
    exit: (dir: number) => ({
      x: dir > 0 ? -30 : 30,
      opacity: 0,
      transition: { duration: 0.15 },
    }),
  };

  return (
    <div className="fixed inset-0 z-50 bg-[#090A0F] text-white flex flex-col justify-between overflow-hidden animate-fade-in">
      {/* Top Bar: Progress Indicator & Escape Hatch */}
      <div className="px-4 pt-4 sm:px-6 sm:pt-6 pb-2 shrink-0 border-b border-white/[0.05]">
        <div className="max-w-2xl mx-auto flex items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-purple-600/20 border border-purple-500/30 flex items-center justify-center text-purple-400">
              <Compass className="w-4 h-4" />
            </div>
            <div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-purple-300">
                Assistente de Escolha
              </span>
              <p className="text-xs text-slate-400 font-medium">
                Etapa {step} de 3
              </p>
            </div>
          </div>

          {/* Escape Hatch Button */}
          <button
            type="button"
            onClick={onSkip}
            className="text-xs font-medium text-slate-400 hover:text-white px-3 py-1.5 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] transition flex items-center gap-1 active:scale-95"
          >
            <span>Ver tudo tranquilo</span>
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* 3-Segment Progress Bar */}
        <div className="max-w-2xl mx-auto grid grid-cols-3 gap-2 mt-3.5">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              onClick={() => {
                if (s < step) {
                  setDirection(-1);
                  setStep(s as any);
                }
              }}
              className={cn(
                "h-1.5 rounded-full transition-all duration-300",
                step >= s
                  ? "bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.5)]"
                  : "bg-white/[0.08]",
                s < step ? "cursor-pointer" : ""
              )}
            />
          ))}
        </div>
      </div>

      {/* Main Interactive Step Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6 no-scrollbar flex items-center justify-center">
        <div className="max-w-2xl w-full">
          <AnimatePresence mode="wait" custom={direction}>
            {step === 1 && (
              <motion.div
                key="step-1"
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                className="space-y-4"
              >
                <div className="text-center mb-6">
                  <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
                    O que você quer assistir hoje?
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-400 mt-1">
                    Escolha o formato ideal para a sua sessão
                  </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {[
                    {
                      type: 'movie' as const,
                      title: "Filmes",
                      desc: "Experiências completas em uma sessão",
                      icon: Film,
                      count: catalog.filter(i => i.type === 'movie').length,
                    },
                    {
                      type: 'series' as const,
                      title: "Séries",
                      desc: "Maratonas e narrativas estendidas",
                      icon: Tv,
                      count: catalog.filter(i => i.type === 'series').length,
                    },
                    {
                      type: 'all' as const,
                      title: "Tanto faz",
                      desc: "Explorar filmes e séries juntos",
                      icon: Sparkles,
                      count: catalog.length,
                    },
                  ].map((option) => {
                    const isSelected = selectedType === option.type;
                    const Icon = option.icon;
                    return (
                      <button
                        key={option.type}
                        type="button"
                        onClick={() => {
                          setSelectedType(option.type);
                          // Auto advance after micro delay for fluid feel
                          setTimeout(() => {
                            setDirection(1);
                            setStep(2);
                          }, 180);
                        }}
                        className={cn(
                          "p-5 rounded-2xl border text-left transition-all active:scale-98 flex flex-col justify-between h-40 group relative",
                          isSelected
                            ? "bg-purple-600/20 border-purple-500/60 shadow-lg shadow-purple-600/10"
                            : "bg-[#0E1017] border-white/[0.06] hover:border-white/[0.15] hover:bg-[#131622]"
                        )}
                      >
                        <div className="flex items-center justify-between w-full">
                          <div className={cn(
                            "w-10 h-10 rounded-xl flex items-center justify-center transition-colors",
                            isSelected ? "bg-purple-500 text-white" : "bg-white/[0.05] text-slate-400 group-hover:text-white"
                          )}>
                            <Icon className="w-5 h-5" />
                          </div>
                          <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-white/[0.06] text-slate-400">
                            {option.count} obras
                          </span>
                        </div>

                        <div>
                          <h3 className="font-semibold text-sm sm:text-base text-white">
                            {option.title}
                          </h3>
                          <p className="text-xs text-slate-400 mt-0.5 line-clamp-1">
                            {option.desc}
                          </p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </motion.div>
            )}

            {step === 2 && (
              <motion.div
                key="step-2"
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                className="space-y-4"
              >
                <div className="text-center mb-5">
                  <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
                    Qual gênero combina com seu humor?
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-400 mt-1">
                    Mostrando contagem para {selectedType === 'movie' ? 'filmes' : selectedType === 'series' ? 'séries' : 'todas as obras'}
                  </p>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 max-h-[50vh] overflow-y-auto no-scrollbar p-1">
                  {WIZARD_GENRES.map((g) => {
                    const isSelected = selectedGenre === g.name;
                    const count = getMatchCount(selectedType, g.name, 'all');
                    const isDisabled = count === 0;

                    return (
                      <button
                        key={g.name}
                        type="button"
                        disabled={isDisabled}
                        onClick={() => {
                          if (isDisabled) return;
                          setSelectedGenre(g.name);
                          setTimeout(() => {
                            setDirection(1);
                            setStep(3);
                          }, 180);
                        }}
                        className={cn(
                          "p-3.5 rounded-xl border text-left transition-all active:scale-98 flex flex-col justify-between h-28 relative group",
                          isSelected
                            ? "bg-purple-600/25 border-purple-500/70 shadow-md shadow-purple-600/15"
                            : isDisabled
                            ? "bg-white/[0.01] border-white/[0.02] opacity-40 cursor-not-allowed"
                            : "bg-[#0E1017] border-white/[0.06] hover:border-white/[0.15] hover:bg-[#131622]"
                        )}
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xl">{g.emoji}</span>
                          <span className={cn(
                            "text-[10px] font-mono px-1.5 py-0.2 rounded-md",
                            isSelected ? "bg-purple-500/40 text-purple-200" : "bg-white/[0.05] text-slate-400"
                          )}>
                            {count}
                          </span>
                        </div>

                        <div>
                          <h4 className="font-semibold text-xs sm:text-sm text-white truncate">
                            {g.label}
                          </h4>
                          <p className="text-[10px] text-slate-400 truncate mt-0.5">
                            {isDisabled ? "Nenhuma série neste gênero" : g.desc}
                          </p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </motion.div>
            )}

            {step === 3 && (
              <motion.div
                key="step-3"
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                className="space-y-4"
              >
                <div className="text-center mb-5">
                  <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
                    Qual o seu nível de exigência hoje?
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-400 mt-1">
                    Filtre pelo selo de qualidade ou explore livremente
                  </p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {WIZARD_RATINGS.map((r) => {
                    const isSelected = selectedRating === r.id;
                    const count = getMatchCount(selectedType, selectedGenre, r.id);

                    return (
                      <button
                        key={r.id}
                        type="button"
                        onClick={() => setSelectedRating(r.id)}
                        className={cn(
                          "p-4 rounded-2xl border text-left transition-all active:scale-98 flex items-start justify-between group",
                          isSelected
                            ? "bg-purple-600/20 border-purple-500/60 shadow-lg shadow-purple-600/10"
                            : "bg-[#0E1017] border-white/[0.06] hover:border-white/[0.15] hover:bg-[#131622]"
                        )}
                      >
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <h3 className="font-semibold text-sm sm:text-base text-white">
                              {r.title}
                            </h3>
                            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-white/[0.06] text-purple-300">
                              {r.badge}
                            </span>
                          </div>
                          <p className="text-xs text-slate-400">
                            {r.desc}
                          </p>
                        </div>

                        <span className={cn(
                          "text-xs font-mono px-2 py-1 rounded-lg shrink-0 ml-2 font-medium",
                          isSelected ? "bg-purple-500 text-white" : "bg-white/[0.05] text-slate-400"
                        )}>
                          {count}
                        </span>
                      </button>
                    );
                  })}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Bottom Sticky Action Bar */}
      <div className="px-4 py-4 sm:px-6 border-t border-white/[0.06] bg-[#0A0C12] shrink-0">
        <div className="max-w-2xl mx-auto flex items-center justify-between gap-3">
          {step > 1 ? (
            <button
              type="button"
              onClick={prevStep}
              className="h-11 px-4 rounded-xl border border-white/[0.08] text-xs font-medium text-slate-300 hover:text-white hover:bg-white/[0.05] flex items-center gap-1.5 transition active:scale-95"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Voltar</span>
            </button>
          ) : (
            <button
              type="button"
              onClick={onSkip}
              className="h-11 px-4 rounded-xl text-xs font-medium text-slate-400 hover:text-white transition"
            >
              Pular etapas
            </button>
          )}

          <button
            type="button"
            onClick={nextStep}
            className="flex-1 h-11 px-5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs sm:text-sm transition shadow-lg shadow-purple-600/25 flex items-center justify-center gap-2 active:scale-95"
          >
            <span>
              {step === 3
                ? `Explorar ${currentMatchCount} ${currentMatchCount === 1 ? 'Título' : 'Títulos'}`
                : "Continuar"}
            </span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
