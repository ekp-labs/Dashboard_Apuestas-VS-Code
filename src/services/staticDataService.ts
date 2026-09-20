export interface StaticLeague {
  id: string;
  name: string;
  country: string;
  confederation: string;
  season: string;
  leagueId: number;
}

export interface StaticTeam {
  id: string;
  name: string;
  leagueId?: string;
  venueId: string;
  founded: number;
  city?: string;
  countryCode?: string;
  managerId?: string;
}

export interface StaticPlayer {
  id: string;
  name: string;
  position: string;
  nationality: string;
  currentTeamId: string;
  career?: { teamId: string; season: string }[];
}

export interface StaticVenue {
  id: string;
  name: string;
  city: string;
  capacity: number;
}

export interface StaticClub {
  id: string;
  name: string;
  founded: number;
}

export interface StaticCompetition {
  id: string;
  name: string;
  confederation: string;
  country: string;
  season: string;
}

export interface StaticSeason {
  id: string;
  year: string;
  startDate: string;
  endDate: string;
}

export interface StaticManager {
  id: string;
  name: string;
  nationality: string;
  currentTeamId: string;
}

export interface StaticReferee {
  id: string;
  name: string;
  nationality: string;
  category: string;
}

export interface StaticTransfer {
  id: string;
  playerId: string;
  fromTeamId: string;
  toTeamId: string;
  date: string;
  fee: string;
}

export interface StaticInjury {
  id: string;
  playerId: string;
  type: string;
  startDate: string;
  expectedReturn: string;
}

export interface StaticTrainingGround {
  id: string;
  name: string;
  teamId: string;
  city: string;
}

async function loadJson<T>(path: string): Promise<T[]> {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to load ${path}`);
  return res.json();
}

export const staticData = {
  leagues: () => loadJson<StaticLeague>('/data/leagues.json'),
  teams: () => loadJson<StaticTeam>('/data/teams.json'),
  players: () => loadJson<StaticPlayer>('/data/players.json'),
  venues: () => loadJson<StaticVenue>('/data/venues.json'),
  clubs: () => loadJson<StaticClub>('/data/clubs.json'),
  competitions: () => loadJson<StaticCompetition>('/data/competitions.json'),
  seasons: () => loadJson<StaticSeason>('/data/seasons.json'),
  managers: () => loadJson<StaticManager>('/data/managers.json'),
  referees: () => loadJson<StaticReferee>('/data/referees.json'),
  transfers: () => loadJson<StaticTransfer>('/data/transfers.json'),
  injuries: () => loadJson<StaticInjury>('/data/injuries.json'),
  trainingGrounds: () => loadJson<StaticTrainingGround>('/data/training_grounds.json'),
  manifest: async () => {
    const res = await fetch('/data/manifest.json');
    if (!res.ok) throw new Error('Failed to load manifest');
    return res.json();
  }
};
