import { useEffect, useState } from 'react';
import { getLeagues } from '../services/mockApi';
import type { League } from '../services/mockApi';

export function useLeagues(filter: 'all' | 'active' = 'all') {
  const [data, setData] = useState<League[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getLeagues(filter)
      .then(res => { if (mounted) setData(res); })
      .catch(e => { if (mounted) setError(String(e)); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [filter]);

  return { data, loading, error };
}
