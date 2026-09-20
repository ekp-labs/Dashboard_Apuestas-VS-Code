import { useEffect, useState } from 'react';
import { getPlayers } from '../services/mockApi';
import type { Player } from '../services/mockApi';

export function usePlayers(positionFilter?: string) {
  const [data, setData] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getPlayers(positionFilter)
      .then(res => { if (mounted) setData(res); })
      .catch(e => { if (mounted) setError(String(e)); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [positionFilter]);

  return { data, loading, error };
}
