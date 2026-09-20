export interface ApiFootballFixture {
  fixture: { id: number; date: string; status: { long: string; short: string } };
  league: { id: number; name: string; country: string };
  teams: { home: { name: string }; away: { name: string } };
  goals?: { home: number | null; away: number | null };
}

const BASE = 'https://v3.football.api-sports.io';

import { getApiKeyPool } from './apiKeyPool';
import { getCached, setCached } from './fixtureCacheService';

const cache = new Map<string, { data: any; ts: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 min

async function fetchWithPool(path: string, params: Record<string,string> = {}): Promise<any> {
  const keys = getApiKeyPool('apiFootball');
  if (keys.length === 0) throw new Error('API-Football keys not configured');
  
  for (const key of keys) {
    const url = new URL(`${BASE}${path}`);
    Object.entries(params).forEach(([k,v]) => url.searchParams.set(k, v));
    const res = await fetch(url.toString(), {
      headers: { 'x-apisports-key': key },
    });
    if (res.status === 429) continue; // rotate
    if (!res.ok) continue; // try next key
    return res.json();
  }
  throw new Error('API-Football pool exhausted');
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
    const res = await fetchWithPool(`/fixtures`, { league: String(leagueId ?? ''), season: currentSeason, status });
    if (res?.errors && Object.keys(res.errors).length > 0) {
      const errMsg = `API-Football error: ${JSON.stringify(res.errors)}`;
      console.error('[apiFootballAdapter] getFixtures error', res.errors);
      throw new Error(errMsg);
    }
    const data = res.response || [];
    cache.set(inMemKey, { data, ts: now });
    setCached(cacheKey, data, 24 * 60 * 60 * 1000);
    if (typeof window !== 'undefined') {
      localStorage.setItem('ff_last_update', Date.now().toString());
    }
    console.info('[apiFootballAdapter] getFixtures OK', { leagueId, status, season: currentSeason, count: data.length });
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
  return getApiKeyPool('apiFootball').length > 0;
}
