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

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:4000';

export async function getLiveMatches(sportKey = 'soccer_epl'): Promise<OddsMatch[]> {
  try {
    const url = new URL(`${API_BASE}/api/odds`);
    url.searchParams.set('sportKey', sportKey);
    url.searchParams.set('markets', 'h2h,spreads,totals');
    url.searchParams.set('live', 'true');
    const res = await fetch(url.toString());
    if (!res.ok) throw new Error(`Backend responded ${res.status}`);
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
  } catch (e) {
    console.warn('[oddsAdapter] fallback to mock', e);
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
}

export function isOddsConfigured() {
  // Configuración ahora se gestiona en el backend
  return true;
}
