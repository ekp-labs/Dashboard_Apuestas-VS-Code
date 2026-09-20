import { useEffect, useState } from 'react';
import { getFixtures } from '../services/apiFootballAdapter';
import type { ApiFootballFixture } from '../services/apiFootballAdapter';

export function useFixtures(params: { leagueId?: number; status?: 'NS' | 'FT' | 'LIVE'; season?: string; refreshTrigger?: number } = {}) {
  const [data, setData] = useState<ApiFootballFixture[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getFixtures(params)
      .then(res => { if (mounted) setData(res); })
      .catch(e => { if (mounted) setError(String(e)); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [params.leagueId, params.status, params.season, params.refreshTrigger]);

  return { data, loading, error };
}
