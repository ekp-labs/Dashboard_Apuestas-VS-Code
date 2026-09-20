import { useEffect, useState } from 'react';
import { getTeams } from '../services/mockApi';
import type { Team } from '../services/mockApi';

export function useTeams(leagueFilter?: string) {
  const [data, setData] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getTeams(leagueFilter)
      .then(res => { if (mounted) setData(res); })
      .catch(e => { if (mounted) setError(String(e)); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [leagueFilter]);

  return { data, loading, error };
}
