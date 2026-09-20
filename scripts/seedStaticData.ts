import { apiFootballAdapter } from '../src/services/apiFootballAdapter';
import { writeFileSync, readFileSync, existsSync } from 'fs';
import { join } from 'path';

const DATA_DIR = join(process.cwd(), 'public', 'data');

function save(file: string, data: any) {
  writeFileSync(join(DATA_DIR, file), JSON.stringify(data, null, 2));
}

function load<T>(file: string): T[] {
  const path = join(DATA_DIR, file);
  if (!existsSync(path)) return [];
  return JSON.parse(readFileSync(path, 'utf-8'));
}

async function seedRealMadridAndBarca() {
  const leagueId = 140;
  const teams = await apiFootballAdapter.getTeams({ league: leagueId });
  const rm = teams.find(t => t.name === 'Real Madrid CF');
  const bar = teams.find(t => t.name === 'FC Barcelona');
  if (!rm || !bar) throw new Error('Teams not found');

  const [rmPlayers, barPlayers] = await Promise.all([
    apiFootballAdapter.getPlayers({ team: rm.id }),
    apiFootballAdapter.getPlayers({ team: bar.id })
  ]);

  const teamsStatic = [
    {
      id: 'team-ES-RM-1902',
      name: 'Real Madrid CF',
      countryCode: 'ES',
      city: rm.city || 'Madrid',
      founded: 1902,
      venueId: 'venue-ES-MAD-BERNABEU',
      managerId: 'manager-IT-ANCELOTTI',
      apiId: rm.id
    },
    {
      id: 'team-ES-BAR-1899',
      name: 'FC Barcelona',
      countryCode: 'ES',
      city: bar.city || 'Barcelona',
      founded: 1899,
      venueId: 'venue-ES-BCN-CAMPNOU',
      managerId: 'manager-DE-FLIK',
      apiId: bar.id
    }
  ];

  const venuesStatic = [
    {
      id: 'venue-ES-MAD-BERNABEU',
      name: rm.venue?.name || 'Santiago Bernabéu',
      city: 'Madrid',
      capacity: rm.venue?.capacity || 81044
    },
    {
      id: 'venue-ES-BCN-CAMPNOU',
      name: bar.venue?.name || 'Estadi Olímpic Lluís Companys',
      city: 'Barcelona',
      capacity: bar.venue?.capacity || 55000
    }
  ];

  const managersStatic = [
    {
      id: 'manager-IT-ANCELOTTI',
      name: 'Carlo Ancelotti',
      nationality: 'IT',
      currentTeamId: 'team-ES-RM-1902'
    },
    {
      id: 'manager-DE-FLIK',
      name: 'Hansi Flick',
      nationality: 'DE',
      currentTeamId: 'team-ES-BAR-1899'
    }
  ];

  const playersStatic = [...rmPlayers, ...barPlayers].map(p => ({
    id: `player-${p.nationality?.substring(0,2).toUpperCase()}-${p.firstname?.replace(/\s+/g,'').toUpperCase()}-${p.birth?.date?.slice(0,4) || '2000'}`,
    name: `${p.firstname} ${p.lastname}`,
    position: p.position || 'Unknown',
    nationality: p.nationality,
    currentTeamId: p.team?.id === rm.id ? 'team-ES-RM-1902' : 'team-ES-BAR-1899',
    apiId: p.id
  }));

  save('teams.json', teamsStatic);
  save('venues.json', venuesStatic);
  save('managers.json', managersStatic);
  save('players.json', playersStatic);
  console.log('Seeded teams, venues, managers and players for RM and BAR');
}

seedRealMadridAndBarca().catch(console.error);

