export interface ApiFootballFixture {
  fixture: { id: number; date: string; status: { long: string; short: string } };
  league: { id: number; name: string; country: string };
  teams: { home: { name: string }; away: { name: string } };
  goals?: { home: number | null; away: number | null };
}

import { getCached, setCached } from './fixtureCacheService';

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:4000';

const cache = new Map<string, { data: any; ts: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 min

async function fetchFromBackend(path: string, params: Record<string,string> = {}): Promise<any> {
  const url = new URL(`${API_BASE}${path}`);
  Object.entries(params).forEach(([k,v]) => {
    if (v !== undefined && v !== '') url.searchParams.set(k, v);
  });
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`Backend responded ${res.status}`);
  return res.json();
}

export async function getFixtures({ leagueId, status = 'NS', season } = {}): Promise<ApiFootballFixture[]> {
  const currentSeason = season ?? new Date().getFullYear().toString();
  const cacheKey = `fixtures:${leagueId ?? 'all'}:${status}:${currentSeason}`;
  const cached = getCached(cacheKey);
  if (cached) {
    console.info('[apiFootballAdapter] getFixtures cache hit persistent', { leagueId, status, season: currentSeason });
    return cached;
  }

  const now = Date.now();
  const inMemKey = `fixtures:${leagueId ?? 'all'}:${status}:${currentSeason}`;
  const inMemCached = cache.get(inMemKey);
  if (inMemCached && now - inMemCached.ts < CACHE_TTL) {
    console.info('[apiFootballAdapter] getFixtures cache hit memory', { leagueId, status, season: currentSeason });
    return inMemCached.data;
  }

  try {
    const res = await fetchFromBackend(`/api/fixtures`, { leagueId: String(leagueId ?? ''), season: currentSeason, status });
    const data = res?.response || res || [];
    cache.set(inMemKey, { data, ts: now });
    setCached(cacheKey, data, 24 * 60 * 60 * 1000);
    if (typeof window !== 'undefined') {
      localStorage.setItem('ff_last_update', Date.now().toString());
    }
    console.info('[apiFootballAdapter] getFixtures OK via backend', { leagueId, status, season: currentSeason, count: data.length });
    return data;
  } catch (e) {
    console.warn('[apiFootballAdapter] getFixtures fallback to mock', e);
    const { getMatches } = await import('./mockApi');
    let matches = await getMatches(status === 'FT' ? 'finished' : 'upcoming');
    // Filter by leagueId if provided
    if (leagueId) {
      const leagueMap: Record<number, string> = {
        39: 'Premier League',
        140: 'LaLiga',
        2: 'Champions League',
        3: 'Europa League',
      };
      const leagueName = leagueMap[leagueId];
      if (leagueName) {
        matches = matches.filter(m => m.league === leagueName);
      }
    }
    const fallback = matches.map(m => ({
      fixture: { id: Number(m.id), date: m.date, status: { long: m.status, short: m.status } },
      league: { id: 0, name: m.league, country: '' },
      teams: { home: { name: m.homeTeam }, away: { name: m.awayTeam } },
      goals: m.score ? (() => { const [h,a]=m.score.split('-'); return { home: Number(h), away: Number(a) }; })() : undefined,
    }));
    cache.set(inMemKey, { data: fallback, ts: now });
    setCached(cacheKey, fallback, 24 * 60 * 60 * 1000);
    if (typeof window !== 'undefined') {
      localStorage.setItem('ff_last_update', Date.now().toString());
    }
    return fallback;
  }
}

export function isApiFootballConfigured() {
  // Configuración ahora se gestiona en el backend
  return true;
}
