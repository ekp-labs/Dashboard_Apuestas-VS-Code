import { useState } from 'react';
import StatCard from '../components/StatCard';
import DataTable from '../components/DataTable';
import FilterBar from '../components/FilterBar';
import PieChartCard from '../components/PieChartCard';
import LineChartCard from '../components/LineChartCard';
import { useStats } from '../hooks/useStats';
import { useLeagues } from '../hooks/useLeagues';

export default function Estadisticas() {
  const [period, setPeriod] = useState<'90d' | '30d' | '7d'>('90d');
  const { snapshot, market, bankroll, loading } = useStats(period);
  const { data: leagues } = useLeagues('all');

  const kpis = snapshot ? [
    { label: 'Aciertos 30d', value: `${snapshot.accuracy}%`, color: 'text-emerald-400' },
    { label: 'Yield', value: `+${snapshot.yield}%`, color: 'text-cyan-400' },
    { label: 'ROI acumulado', value: `+${snapshot.roi}%`, color: 'text-fuchsia-400' },
    { label: 'Promedio cuota', value: snapshot.avgOdds.toFixed(2), color: 'text-gray-200' },
  ] : [];

  const ligaStats = leagues.map(l => ({
    liga: l.name,
    partidos: l.matches ?? 0,
    aciertos: 65,
    roi: l.roi ?? '+0%',
  }));

  const columns = [
    { key: 'liga', header: 'Liga' },
    { key: 'partidos', header: 'Partidos', className: 'text-center', render: (r:any)=> r.partidos },
    { key: 'aciertos', header: 'Aciertos', className: 'text-center', render: (r:any)=> <span className="text-emerald-400">{r.aciertos}%</span> },
    { key: 'roi', header: 'ROI', className: 'text-center', render: (r:any)=> <span className="text-cyan-400">{r.roi}</span> },
  ];

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Estadísticas</h2>
        <div className="text-sm text-gray-400">Periodo: últimos {period} {loading ? '· cargando' : ''}</div>
      </header>

      <FilterBar
        active={period}
        onChange={setPeriod}
        options={[
          { label: '90 días', value: '90d' },
          { label: '30 días', value: '30d' },
          { label: '7 días', value: '7d' },
        ]}
      />

      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {kpis.map(k=>(
          <StatCard key={k.label} label={k.label} value={k.value} color={k.color} />
        ))}
      </section>

      <section className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
        <h3 className="text-lg font-semibold mb-3 text-cyan-300">Rendimiento por liga</h3>
        <DataTable columns={columns} data={ligaStats} />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <PieChartCard title="Distribución por mercado" data={market} />
        <LineChartCard title="Evolución bankroll" data={bankroll} />
      </section>
    </div>
  );
}
