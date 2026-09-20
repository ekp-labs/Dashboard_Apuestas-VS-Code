import { useState } from 'react';
import FilterBar from '../components/FilterBar';
import DataTable from '../components/DataTable';
import { useMatches } from '../hooks/useMatches';
import { useLiveMatches } from '../hooks/useLiveMatches';

export default function Partidos() {
  const [filter, setFilter] = useState<'proximos' | 'vivo' | 'finalizados'>('proximos');

  const statusMap = {
    proximos: 'upcoming' as const,
    vivo: 'live' as const,
    finalizados: 'finished' as const,
  };

  const { data: matches, loading } = useMatches(statusMap[filter]);
  const { data: liveMatches } = useLiveMatches('soccer_epl');

  const displayMatches = filter === 'vivo' ? liveMatches.map(l => ({
    id: l.id,
    league: l.league,
    homeTeam: l.home_team,
    awayTeam: l.away_team,
    date: l.commence_time,
    status: 'live' as const,
    market: 'Live',
    odds: l.bookmakers?.[0]?.markets?.[0]?.outcomes?.[0]?.price,
  })) : matches;

  const upcoming = displayMatches.filter(m => m.status === 'upcoming' || m.status === 'live');
  const results = displayMatches.filter(m => m.status === 'finished');

  const resultColumns = [
    { key: 'liga', header: 'Liga' },
    { key: 'partido', header: 'Partido', render: (r:any)=> `${r.homeTeam} - ${r.awayTeam}` },
    { key: 'resultado', header: 'Resultado', className: 'text-center', render: (r:any)=> <span className="font-semibold text-emerald-400">{r.score ?? '-'}</span> },
    { key: 'fecha', header: 'Fecha', className: 'text-center', render: (r:any)=> new Date(r.date).toLocaleDateString() },
  ];

  const formatDate = (iso: string) => {
    const d = new Date(iso);
    return `${d.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' })} ${d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}`;
  };

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Partidos</h2>
        <div className="text-sm text-gray-400">{loading ? 'Cargando...' : 'Actualizado hace 1 min'}</div>
      </header>

      <FilterBar
        active={filter}
        onChange={(v)=> setFilter(v as any)}
        options={[
          { label: 'Próximos', value: 'proximos' },
          { label: 'En vivo', value: 'vivo' },
          { label: 'Finalizados', value: 'finalizados' },
        ]}
      />

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {upcoming.map((p:any)=>(
          <div key={p.id} className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
            <div className="flex items-center justify-between text-xs text-gray-400 mb-3">
              <span>{p.league}</span>
              <span>{formatDate(p.date)}</span>
            </div>
            <div className="flex items-center justify-between">
              <div className="text-center flex-1">
                <div className="font-semibold">{p.homeTeam || p.home_team}</div>
              </div>
              <div className="text-gray-500 mx-2">vs</div>
              <div className="text-center flex-1">
                <div className="font-semibold">{p.awayTeam || p.away_team}</div>
              </div>
            </div>
            <div className="mt-4 flex items-center justify-between bg-slate-900/50 rounded-lg p-3 border border-slate-800">
              <div className="text-sm text-gray-300">{p.market}</div>
              <div className="text-cyan-400 font-semibold">{p.odds?.toFixed?.(2) ?? p.odds}</div>
            </div>
          </div>
        ))}
        {upcoming.length === 0 && !loading && (
          <div className="text-gray-400 text-sm">Sin partidos para este filtro.</div>
        )}
      </section>

      <section className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
        <h3 className="text-lg font-semibold mb-3 text-cyan-300">Resultados recientes</h3>
        <DataTable columns={resultColumns} data={results} />
      </section>
    </div>
  );
}
