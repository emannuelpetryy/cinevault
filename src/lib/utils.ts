import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getPlatformBadgeClass(platform: string): string {
  switch (platform) {
    case 'Netflix':
      return 'bg-red-500/15 text-red-400 border border-red-500/30';
    case 'Max':
      return 'bg-blue-600/15 text-blue-400 border border-blue-600/30';
    case 'Prime Video':
      return 'bg-sky-500/15 text-sky-300 border border-sky-500/30';
    case 'Disney+':
      return 'bg-indigo-600/15 text-indigo-300 border border-indigo-500/30';
    case 'Apple TV+':
      return 'bg-slate-200/15 text-slate-200 border border-slate-300/30';
    case 'Paramount+':
      return 'bg-blue-500/15 text-blue-300 border border-blue-400/30';
    default:
      return 'bg-purple-500/15 text-purple-300 border border-purple-500/30';
  }
}
