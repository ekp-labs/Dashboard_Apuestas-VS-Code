import { useState, useEffect } from 'react';
import FilterBar from '../components/FilterBar';
import DataTable from '../components/DataTable';
import { useLeagues } from '../hooks/useLeagues';
import { useFixtures } from '../hooks/useFixtures';

export default function Competiciones() {
  const [filter, setFilter] = useState<'todas' | 'activas'>('todas');
  const [leagueId, setLeagueId] = useState<number | undefined>(undefined);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [toast, setToast] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('—');

  useEffect(() => {
    const ts = localStorage.getItem('ff_last_update');
    if (ts) setLastUpdated(new Date(Number(ts)).toLocaleTimeString('es-HN', { hour: '2-digit', minute: '2-digit', hour12: true }));
  }, [refreshTrigger]);

  useEffect(() => {
    const interval = setInterval(() => {
      console.info('[Competiciones] background refresh tick', new Date().toISOString(), { leagueId, refreshTrigger: refreshTrigger + 1 });
      setToast('Verificando actualización en segundo plano...');
      setRefreshTrigger(t => t + 1);
    }, 60 * 60 * 1000);
    return () => clearInterval(interval);
  }, [leagueId]);

  useEffect(() => {
    if (toast) {
      const t = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(t);
    }
  }, [toast]);

  const leagueFilter = filter === 'activas' ? 'active' : 'all';
  const { data: leagues, loading } = useLeagues(leagueFilter);
  const { data: upcomingFixtures } = useFixtures({ status: 'NS', leagueId, refreshTrigger });
  const { data: recentFixtures } = useFixtures({ status: 'FT', leagueId, refreshTrigger });

  useEffect(() => {
    if (upcomingFixtures.length) {
      const season = new Date().getFullYear().toString();
      const key = `ff_cache:fixtures:${leagueId ?? 'all'}:NS:${season}`;
      const raw = localStorage.getItem(key);
      if (raw) {
        try {
          const entry = JSON.parse(raw);
          const ageHours = (Date.now() - entry.ts) / 3600000;
          setToast(ageHours < 24 ? 'Próximos partidos: datos desde caché' : 'Próximos partidos: actualizados desde API');
        } catch {}
      }
    }
  }, [upcomingFixtures, leagueId]);

  useEffect(() => {
    if (recentFixtures.length) {
      const season = new Date().getFullYear().toString();
      const key = `ff_cache:fixtures:${leagueId ?? 'all'}:FT:${season}`;
      const raw = localStorage.getItem(key);
      if (raw) {
        try {
          const entry = JSON.parse(raw);
          const ageHours = (Date.now() - entry.ts) / 3600000;
          setToast(ageHours < 24 ? 'Resultados: datos desde caché' : 'Resultados: actualizados desde API');
        } catch {}
      }
    }
  }, [recentFixtures, leagueId]);

  const upcomingColumns = [
    { key: 'league', header: 'Liga' },
    { key: 'match', header: 'Partido' },
    { key: 'time', header: 'Hora' },
    { key: 'odds', header: 'Cuota mejor' },
  ];

  const upcomingData = upcomingFixtures.map(f => ({
    league: f.league.name,
    match: `${f.teams.home.name} vs ${f.teams.away.name}`,
    time: new Date(f.fixture.date).toLocaleString('es-HN', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true }),
    odds: '-',
  }));

  const resultsColumns = [
    { key: 'league', header: 'Liga' },
    { key: 'match', header: 'Partido' },
    { key: 'score', header: 'Resultado' },
    { key: 'time', header: 'Fecha' },
  ];

  const resultsData = recentFixtures.slice(0, 20).map(f => ({
    league: f.league.name,
    match: `${f.teams.home.name} vs ${f.teams.away.name}`,
    score: `${f.goals?.home ?? '-'} - ${f.goals?.away ?? '-'}`,
    time: new Date(f.fixture.date).toLocaleString('es-HN', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true }),
  }));

  return (
    <div className="space-y-6">
      {toast && (
        <div className="fixed top-4 right-4 bg-slate-900 border border-cyan-700 text-cyan-300 text-sm px-4 py-2 rounded shadow-lg z-50">
          {toast}
        </div>
      )}
      <header className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Competiciones</h2>
        <div className="flex items-center gap-3">
          <div className="text-sm text-gray-400">{loading ? 'Cargando...' : 'Actualizado hace 2 min'}</div>
          <button
            className="bg-slate-800 hover:bg-slate-700 text-white text-xs px-3 py-1.5 rounded"
            onClick={() => {
              const season = new Date().getFullYear().toString();
              Object.keys(localStorage).forEach(k => {
                if (k.startsWith('ff_cache:fixtures:')) localStorage.removeItem(k);
              });
              localStorage.setItem('ff_last_update', Date.now().toString());
              window.location.reload();
            }}
          >
            Actualizar todo
          </button>
          <span className="text-[10px] text-gray-500">Última actualización: {lastUpdated}</span>
        </div>
      </header>

      <FilterBar
        active={filter}
        onChange={(v)=> setFilter(v as any)}
        options={[
          { label: 'Todas', value: 'todas' },
          { label: 'Activas', value: 'activas' },
        ]}
      />

      <section className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {leagues.length === 0 ? (
          <div className="col-span-full text-center text-gray-500 py-8">Ligas — Pendiente de integración real</div>
        ) : leagues.map(c => (
          <div key={c.id} className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
            <div className="flex items-start justify-between">
              <div>
                <div className="font-semibold text-lg">{c.name}</div>
                <div className="text-xs text-gray-400">{c.country}</div>
              </div>
              <span className={`text-xs px-2 py-0.5 rounded ${c.active ? 'bg-emerald-900/40 text-emerald-300' : 'bg-slate-800 text-gray-400'}`}>
                {c.active ? 'Activa' : 'Pausada'}
              </span>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
              <div className="bg-slate-900/40 rounded-lg p-3 border border-slate-800">
                <div className="text-gray-400 text-xs">Partidos</div>
                <div className="text-lg mt-1">{c.matches}</div>
              </div>
              <div className="bg-slate-900/40 rounded-lg p-3 border border-slate-800">
                <div className="text-gray-400 text-xs">ROI 30d</div>
                <div className="text-lg mt-1 text-emerald-400">{c.roi}</div>
              </div>
            </div>
          </div>
        ))}
      </section>

      <div className="flex items-center gap-3">
        <label className="text-sm text-gray-400">Filtrar liga real:</label>
        <select
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm"
          value={leagueId ?? ''}
          onChange={(e) => setLeagueId(e.target.value ? Number(e.target.value) : undefined)}
        >
          <option value="">Todas</option>
          <option value="39">Premier League</option>
          <option value="140">LaLiga</option>
          <option value="2">UEFA Champions League</option>
          <option value="3">UEFA Europa League</option>
        </select>
        <span className="text-xs text-gray-500">Temporada {new Date().getFullYear()} vía API-Football</span>
        <button
          className="ml-2 bg-cyan-700 hover:bg-cyan-600 text-white text-xs px-3 py-1.5 rounded"
          onClick={() => {
            const season = new Date().getFullYear().toString();
            const ids = leagueId ? [leagueId] : [39,140,2,3];
            ids.forEach(id => ['NS','FT'].forEach(s => {
              const key = `fixtures:${id}:${s}:${season}`;
              localStorage.removeItem('ff_cache:' + key);
            }));
            localStorage.setItem('ff_last_update', Date.now().toString());
            window.location.reload();
          }}
        >
          Actualizar liga
        </button>
      </div>

      <section className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-cyan-300">Próximos partidos</h3>
          <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-gray-400">Fuente: API-Football • Caché 24h • Actualización manual</span>
        </div>
        <DataTable columns={upcomingColumns} data={upcomingData} />
      </section>

      <section className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-cyan-300">Resultados recientes</h3>
          <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-gray-400">Fuente: API-Football • Caché 24h • Actualización manual</span>
        </div>
        <DataTable columns={resultsColumns} data={resultsData} />
      </section>
    </div>
  );
}
