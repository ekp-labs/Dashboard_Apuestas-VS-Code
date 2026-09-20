export type MatchStatus = 'upcoming' | 'live' | 'finished';

export interface Match {
  id: string;
  league: string;
  homeTeam: string;
  awayTeam: string;
  date: string; // ISO or display
  status: MatchStatus;
  market?: string;
  odds?: number;
  score?: string;
}

export interface League {
  id: string;
  name: string;
  country: string;
  teams: number;
  logo?: string;
  matches?: number;
  roi?: string;
  active?: boolean;
}

export interface Team {
  id: string;
  name: string;
  league: string;
  points: number;
  form: string; // e.g. 'W W D W L'
}

export interface Player {
  id: string;
  name: string;
  team: string;
  position: string;
  goals: number;
  assists: number;
  value: string;
}

export interface StatsSnapshot {
  period: string;
  accuracy: number;
  yield: number;
  roi: number;
  avgOdds: number;
}

export interface MarketDistribution {
  name: string;
  value: number;
}

export interface BankrollPoint {
  date: string;
  value: number;
}

const MOCK_MATCHES: Match[] = [
  { id: 'm1', league: 'LaLiga', homeTeam: 'Real Madrid', awayTeam: 'Barcelona', date: '2026-09-19T21:00:00Z', status: 'upcoming', market: 'Over 2.5', odds: 2.10 },
  { id: 'm2', league: 'Premier League', homeTeam: 'Man City', awayTeam: 'Arsenal', date: '2026-09-20T18:30:00Z', status: 'upcoming', market: 'BTTS', odds: 1.95 },
  { id: 'm3', league: 'Bundesliga', homeTeam: 'Bayern', awayTeam: 'Dortmund', date: '2026-09-20T20:30:00Z', status: 'upcoming', market: '1X2', odds: 1.85 },
  { id: 'm4', league: 'Serie A', homeTeam: 'Inter', awayTeam: 'Napoli', date: '2026-09-21T19:45:00Z', status: 'upcoming', market: 'Over 2.5', odds: 1.90 },
  { id: 'm5', league: 'Champions League', homeTeam: 'PSG', awayTeam: 'Dortmund', date: '2026-09-22T21:00:00Z', status: 'upcoming', market: 'Both to Score', odds: 2.05 },
  { id: 'm6', league: 'LaLiga', homeTeam: 'Girona', awayTeam: 'Valencia', date: '2026-09-13T20:00:00Z', status: 'finished', score: '3-1' },
  { id: 'm7', league: 'Premier League', homeTeam: 'Liverpool', awayTeam: 'Brighton', date: '2026-09-13T18:00:00Z', status: 'finished', score: '2-1' },
  { id: 'm8', league: 'Bundesliga', homeTeam: 'Leverkusen', awayTeam: 'Union Berlin', date: '2026-09-12T20:30:00Z', status: 'finished', score: '2-0' },
  { id: 'm9', league: 'Serie A', homeTeam: 'Milan', awayTeam: 'Roma', date: '2026-09-12T20:45:00Z', status: 'finished', score: '1-1' },
  { id: 'm10', league: 'LaLiga', homeTeam: 'Atletico', awayTeam: 'Sevilla', date: '2026-09-18T19:00:00Z', status: 'live', score: '1-0' },
];

const MOCK_LEAGUES: League[] = [
  { id: 'l1', name: 'LaLiga', country: 'EspaÃ±a', teams: 20, matches: 210, roi: '+9.2%', active: true },
  { id: 'l2', name: 'Premier League', country: 'Inglaterra', teams: 20, matches: 380, roi: '+11.4%', active: true },
  { id: 'l3', name: 'Bundesliga', country: 'Alemania', teams: 18, matches: 306, roi: '+7.8%', active: true },
  { id: 'l4', name: 'Serie A', country: 'Italia', teams: 20, matches: 380, roi: '+5.1%', active: true },
  { id: 'l5', name: 'Ligue 1', country: 'Francia', teams: 20, matches: 306, roi: '+3.4%', active: false },
  { id: 'l6', name: 'Champions League', country: 'UEFA', teams: 32, matches: 125, roi: '+14.2%', active: true },
];

const MOCK_TEAMS: Team[] = [
  { id: 't1', name: 'Real Madrid', league: 'LaLiga', points: 78, form: 'W W D W L' },
  { id: 't2', name: 'Manchester City', league: 'Premier League', points: 82, form: 'W W W D W' },
  { id: 't3', name: 'Bayern Munich', league: 'Bundesliga', points: 74, form: 'W D W W W' },
  { id: 't4', name: 'Inter', league: 'Serie A', points: 71, form: 'D W W L W' },
  { id: 't5', name: 'PSG', league: 'Ligue 1', points: 68, form: 'W W D W W' },
  { id: 't6', name: 'Barcelona', league: 'LaLiga', points: 70, form: 'L W W W D' },
  { id: 't7', name: 'Girona', league: 'LaLiga', points: 67, form: 'W D L W W' },
  { id: 't8', name: 'Atletico Madrid', league: 'LaLiga', points: 65, form: 'D W W L D' },
  { id: 't9', name: 'Athletic Club', league: 'LaLiga', points: 61, form: 'W L W D W' },
];

const MOCK_PLAYERS: Player[] = [
  { id: 'p1', name: 'Kylian MbappÃ©', team: 'Real Madrid', position: 'Delantero', goals: 18, assists: 5, value: 'â‚¬180M' },
  { id: 'p2', name: 'Erling Haaland', team: 'Man City', position: 'Delantero', goals: 22, assists: 3, value: 'â‚¬190M' },
  { id: 'p3', name: 'Harry Kane', team: 'Bayern', position: 'Delantero', goals: 19, assists: 7, value: 'â‚¬110M' },
  { id: 'p4', name: 'Jude Bellingham', team: 'Real Madrid', position: 'Mediocentro', goals: 12, assists: 9, value: 'â‚¬130M' },
  { id: 'p5', name: 'Bukayo Saka', team: 'Arsenal', position: 'Extremo', goals: 11, assists: 12, value: 'â‚¬120M' },
  { id: 'p6', name: 'Lautaro MartÃ­nez', team: 'Inter', position: 'Delantero', goals: 16, assists: 4, value: 'â‚¬95M' },
];

const MOCK_STATS_SNAPSHOTS: Record<string, StatsSnapshot> = {
  '90d': { period: '90d', accuracy: 68, yield: 9.4, roi: 42.7, avgOdds: 1.94 },
  '30d': { period: '30d', accuracy: 71, yield: 11.2, roi: 12.3, avgOdds: 1.91 },
  '7d': { period: '7d', accuracy: 64, yield: 6.8, roi: 2.1, avgOdds: 1.98 },
};

const MOCK_MARKET_DISTRIBUTION: MarketDistribution[] = [
  { name: 'Over 2.5', value: 45 },
  { name: 'BTTS', value: 30 },
  { name: '1X2', value: 25 },
];

const MOCK_BANKROLL: BankrollPoint[] = [
  { date: 'Ago', value: 10000 },
  { date: 'Sep 01', value: 10350 },
  { date: 'Sep 08', value: 10820 },
  { date: 'Sep 15', value: 11240 },
  { date: 'Sep 22', value: 12340 },
];

export async function getMatches(filter: MatchStatus | 'all' = 'all'): Promise<Match[]> {
  await new Promise(r => setTimeout(r, 300));
  if (filter === 'all') return MOCK_MATCHES;
  return MOCK_MATCHES.filter(m => m.status === filter);
}

export async function getLeagues(filter: 'all' | 'active' = 'all'): Promise<League[]> {
  await new Promise(r => setTimeout(r, 200));
  // Load static leagues from public/data
  const res = await fetch('/data/leagues.json');
  if (!res.ok) throw new Error('Failed to load static leagues');
  const staticLeagues = await res.json();
  // Map static league to mock League shape for UI compatibility, merging mock stats
  const mapped: League[] = staticLeagues.map((l: any) => {
    const mock = MOCK_LEAGUES.find(m => m.name === l.name);
    return {
      id: l.id,
      name: l.name,
      country: l.country,
      teams: mock?.teams ?? 20,
      matches: mock?.matches ?? 0,
      roi: mock?.roi ?? '+0%',
      active: mock?.active ?? true,
    };
  });
  const result = filter === 'active' ? mapped.filter(l => l.active) : mapped;
  return result;
}

export async function getTeams(leagueFilter?: string): Promise<Team[]> {
  await new Promise(r => setTimeout(r, 200));
  if (!leagueFilter || leagueFilter === 'todos') return MOCK_TEAMS;
  return MOCK_TEAMS.filter(t => t.league === leagueFilter);
}

export async function getPlayers(positionFilter?: string): Promise<Player[]> {
  await new Promise(r => setTimeout(r, 200));
  if (!positionFilter || positionFilter === 'todos') return MOCK_PLAYERS;
  return MOCK_PLAYERS.filter(p => p.position === positionFilter);
}

export async function getStatsSnapshot(period: '90d' | '30d' | '7d'): Promise<StatsSnapshot> {
  await new Promise(r => setTimeout(r, 150));
  return MOCK_STATS_SNAPSHOTS[period];
}

export async function getMarketDistribution(): Promise<MarketDistribution[]> {
  await new Promise(r => setTimeout(r, 150));
  return MOCK_MARKET_DISTRIBUTION;
}

export async function getBankroll(): Promise<BankrollPoint[]> {
  await new Promise(r => setTimeout(r, 150));
  return MOCK_BANKROLL;
}

// Future extension for The Odds API / API-Football
export function getApiBase() {
  return import.meta.env.VITE_API_BASE ?? '';
}

