import { useEffect, useState } from 'react';
import { getMatches } from '../services/mockApi';
import type { Match, MatchStatus } from '../services/mockApi';

export function useMatches(filter: MatchStatus | 'all' = 'all') {
  const [data, setData] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getMatches(filter)
      .then(res => { if (mounted) setData(res); })
      .catch(e => { if (mounted) setError(String(e)); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [filter]);

  return { data, loading, error };
}
