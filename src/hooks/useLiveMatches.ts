import { useEffect, useState } from 'react';
import { getLiveMatches } from '../services/oddsAdapter';
import type { OddsMatch } from '../services/oddsAdapter';

export function useLiveMatches(sportKey = 'soccer_epl') {
  const [data, setData] = useState<OddsMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getLiveMatches(sportKey)
      .then(res => { if (mounted) setData(res); })
      .catch(e => { if (mounted) setError(String(e)); })
      .finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [sportKey]);

  return { data, loading, error };
}
