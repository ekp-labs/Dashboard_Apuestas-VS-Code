import { useEffect, useState } from 'react';
import { getStatsSnapshot, getMarketDistribution, getBankroll } from '../services/mockApi';
import type { StatsSnapshot, MarketDistribution, BankrollPoint } from '../services/mockApi';

export function useStats(period: '90d' | '30d' | '7d') {
  const [snapshot, setSnapshot] = useState<StatsSnapshot | null>(null);
  const [market, setMarket] = useState<MarketDistribution[]>([]);
  const [bankroll, setBankroll] = useState<BankrollPoint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    Promise.all([
      getStatsSnapshot(period),
      getMarketDistribution(),
      getBankroll(),
    ]).then(([snap, mkt, br]) => {
      if (mounted) {
        setSnapshot(snap);
        setMarket(mkt);
        setBankroll(br);
      }
    }).finally(() => { if (mounted) setLoading(false); });
    return () => { mounted = false; };
  }, [period]);

  return { snapshot, market, bankroll, loading };
}
