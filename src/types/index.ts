export type MediaType = 'movie' | 'series';
export type MediaStatus = 'priority' | 'queue' | 'watched';
export type StreamingPlatform = 'Netflix' | 'Max' | 'Prime Video' | 'Disney+' | 'Apple TV+' | 'Paramount+' | 'Outros';

export interface CatalogItem {
  id: string;
  title: string;
  type: MediaType;
  status: MediaStatus;
  genre: string;
  subgenre?: string;
  origin?: string;
  note?: string;
  rating?: number;
  year?: number | null;
  imdb?: number | null;
  rtCritics?: number | null;
  rtAudience?: number | null;
  platform: string;
}

export interface AppState {
  search: string;
  type: 'all' | 'movie' | 'series';
  status: 'all' | 'priority' | 'queue' | 'watched';
  genre: string;
  platform: string;
  minImdb: number;
  rtCritics: string;
  rtAudience: string;
  decade: string;
  sort: string;
  view: 'grid' | 'table';
  wizardOpen: boolean;
}
