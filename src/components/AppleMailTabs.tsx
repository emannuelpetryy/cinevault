import React, { useLayoutEffect, useRef, useState } from "react";
import { motion, useReducedMotion } from "motion/react";
import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

export interface AppleMailTabItem<T extends string = string> {
  value: T;
  label: string;
  count?: number;
  icon?: LucideIcon;
  activeClassName?: string;
}

export interface AppleMailTabsProps<T extends string = string> {
  tabs: readonly AppleMailTabItem<T>[];
  value: T;
  onValueChange: (value: T) => void;
  className?: string;
  pillClassName?: string;
  size?: 'sm' | 'md';
}

const SPRING_TRANSITION = {
  type: "spring",
  stiffness: 420,
  damping: 36,
  mass: 0.8,
} as const;

export function AppleMailTabs<T extends string>({
  tabs,
  value,
  onValueChange,
  className,
  pillClassName,
  size = 'md',
}: AppleMailTabsProps<T>) {
  const shouldReduceMotion = useReducedMotion();
  const labelRefs = useRef<Map<T, HTMLSpanElement>>(new Map());
  const [labelWidths, setLabelWidths] = useState<Map<T, number>>(new Map());

  // Measure actual text widths cleanly
  useLayoutEffect(() => {
    const nextWidths = new Map<T, number>();
    labelRefs.current.forEach((el, k) => {
      if (el) {
        nextWidths.set(k, Math.ceil(el.getBoundingClientRect().width));
      }
    });
    setLabelWidths(nextWidths);
  }, [tabs]);

  const heightClass = size === 'sm' ? 'h-8 text-xs' : 'h-10 text-xs sm:text-sm';
  const iconSize = size === 'sm' ? 'w-3.5 h-3.5' : 'w-4 h-4';

  return (
    <div
      role="tablist"
      className={cn(
        "flex items-center gap-1.5 p-1 rounded-xl bg-white/[0.04] border border-white/[0.07] overflow-x-auto no-scrollbar",
        className
      )}
    >
      {tabs.map((tab) => {
        const isSelected = value === tab.value;
        const Icon = tab.icon;
        const textWidth = labelWidths.get(tab.value) ?? 0;

        return (
          <button
            key={tab.value}
            role="tab"
            aria-selected={isSelected}
            onClick={() => onValueChange(tab.value)}
            className={cn(
              "relative flex items-center justify-center rounded-lg transition-colors select-none font-medium shrink-0",
              heightClass,
              isSelected ? "text-white" : "text-slate-400 hover:text-slate-200 hover:bg-white/[0.03]",
              pillClassName
            )}
            style={{
              paddingLeft: isSelected ? '12px' : '10px',
              paddingRight: isSelected ? '12px' : '10px',
            }}
          >
            {/* Animated Pill Background */}
            {isSelected && (
              <motion.div
                layoutId="apple-mail-active-pill"
                transition={shouldReduceMotion ? { duration: 0 } : SPRING_TRANSITION}
                className={cn(
                  "absolute inset-0 rounded-lg shadow-sm border border-white/10",
                  tab.activeClassName || "bg-purple-600/80 text-white"
                )}
              />
            )}

            {/* Content: Icon + Label + Count */}
            <span className="relative z-10 flex items-center gap-1.5">
              {Icon && <Icon className={cn(iconSize, isSelected ? "opacity-100" : "opacity-70")} />}
              
              <span
                ref={(el) => {
                  if (el) labelRefs.current.set(tab.value, el);
                }}
                className={cn("whitespace-nowrap transition-opacity", isSelected ? "font-semibold" : "font-normal")}
              >
                {tab.label}
              </span>

              {tab.count !== undefined && (
                <span
                  className={cn(
                    "text-[10px] font-mono px-1.5 py-0.2 rounded-full",
                    isSelected ? "bg-white/20 text-white" : "bg-white/[0.06] text-slate-400"
                  )}
                >
                  {tab.count}
                </span>
              )}
            </span>
          </button>
        );
      })}
    </div>
  );
}
