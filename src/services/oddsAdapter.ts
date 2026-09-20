export interface OddsMatch {
  id: string;
  sport_key: string;
  sport_title: string;
  league: string;
  commence_time: string;
  home_team: string;
  away_team: string;
  bookmakers: {
    key: string;
    title: string;
    markets: {
      key: string;
      outcomes: { name: string; price: number }[];
    }[];
  }[];
  status: 'upcoming' | 'live' | 'finished';
}

const BASE = 'https://api.the-odds-api.com/v4';

import { getApiKeyPool } from './apiKeyPool';

async function fetchWithPool(url: string, key: string) {
  return fetch(url, { headers: { 'Ocp-Apim-Subscription-Key': key } });
}

export async function getLiveMatches(sportKey = 'soccer_epl'): Promise<OddsMatch[]> {
  const keys = getApiKeyPool('odds');
  if (keys.length === 0) {
    const { getMatches } = await import('./mockApi');
    const matches = await getMatches('live');
    return matches.map(m => ({
      id: m.id,
      sport_key: sportKey,
      sport_title: 'Soccer',
      league: m.league,
      commence_time: m.date,
      home_team: m.homeTeam,
      away_team: m.awayTeam,
      bookmakers: [],
      status: m.status as any,
    }));
  }

  for (const key of keys) {
    const url = `${BASE}/sports/${sportKey}/odds?apiKey=${key}&markets=h2h,spreads,totals&live=true`;
    try {
      const res = await fetch(url);
      if (res.status === 429) continue;
      if (!res.ok) continue;
      const data = await res.json();
      return data.map((d: any) => ({
        id: d.id,
        sport_key: d.sport_key,
        sport_title: d.sport_title,
        league: d.league,
        commence_time: d.commence_time,
        home_team: d.home_team,
        away_team: d.away_team,
        bookmakers: d.bookmakers ?? [],
        status: d.status ?? 'live',
      }));
    } catch {}
  }
  // fallback mock
  const { getMatches } = await import('./mockApi');
  const matches = await getMatches('live');
  return matches.map(m => ({
    id: m.id,
    sport_key: sportKey,
    sport_title: 'Soccer',
    league: m.league,
    commence_time: m.date,
    home_team: m.homeTeam,
    away_team: m.awayTeam,
    bookmakers: [],
    status: m.status as any,
  }));
}

export function isOddsConfigured() {
  return getApiKeyPool('odds').length > 0;
}
