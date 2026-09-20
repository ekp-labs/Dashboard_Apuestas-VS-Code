import { useEffect, useState } from 'react';
import { staticData, StaticTeam, StaticPlayer } from '../services/staticDataService';

export function useStaticTeams(refreshTrigger = 0) {
  const [data, setData] = useState<StaticTeam[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    staticData.teams().then(list => {
      if (mounted) {
        setData(list);
        setLoading(false);
      }
    });
    return () => { mounted = false; };
  }, [refreshTrigger]);

  return { data, loading };
}

export function useStaticPlayers(refreshTrigger = 0) {
  const [data, setData] = useState<StaticPlayer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    staticData.players().then(list => {
      if (mounted) {
        setData(list);
        setLoading(false);
      }
    });
    return () => { mounted = false; };
  }, [refreshTrigger]);

  return { data, loading };
}
