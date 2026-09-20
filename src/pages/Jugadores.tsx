import { useState, useEffect } from 'react';
import DataTable from '../components/DataTable';
import { staticData } from '../services/staticDataService';

export default function Jugadores() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [toast, setToast] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('—');
  const [players, setPlayers] = useState<any[]>([]);
  const [teams, setTeams] = useState<any[]>([]);
  const [filterTeam, setFilterTeam] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ts = localStorage.getItem('ff_last_update_players');
    if (ts) setLastUpdated(new Date(Number(ts)).toLocaleTimeString('es-HN', { hour: '2-digit', minute: '2-digit', hour12: true }));
  }, [refreshTrigger]);

  useEffect(() => {
    if (toast) {
      const t = setTimeout(() => setToast(null), 3000);
      return () => clearTimeout(t);
    }
  }, [toast]);

  useEffect(() => {
    setLoading(true);
    Promise.all([staticData.players(), staticData.teams()]).then(([p, t]) => {
      setPlayers(p);
      setTeams(t);
      setLoading(false);
      setToast('Jugadores: datos cargados');
      localStorage.setItem('ff_last_update_players', Date.now().toString());
    });
  }, [refreshTrigger]);

  useEffect(() => {
    const interval = setInterval(() => {
      setToast('Verificando actualización jugadores...');
      setRefreshTrigger(t => t + 1);
    }, 60 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const handleActualizarTodo = () => {
    localStorage.setItem('ff_last_update_players', Date.now().toString());
    setRefreshTrigger(t => t + 1);
  };

  const filtered = filterTeam ? players.filter(p => p.currentTeamId === filterTeam) : players;

  const columns = [
    { key: 'name', header: 'Jugador' },
    { key: 'position', header: 'Posición' },
    { key: 'nationality', header: 'Nacionalidad' },
    { key: 'teamName', header: 'Equipo' },
    { key: 'birthYear', header: 'Año nac.' }
  ];

  const data = filtered.map(p => ({
    name: p.name,
    position: p.position,
    nationality: p.nationality,
    teamName: teams.find(t => t.id === p.currentTeamId)?.name || '-',
    birthYear: p.id.split('-').pop() || '-'
  }));

  return (
    <div className="space-y-6">
      {toast && <div className="fixed top-4 right-4 bg-slate-900 border border-cyan-700 text-cyan-300 text-sm px-4 py-2 rounded shadow-lg z-50">{toast}</div>}
      <header className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Jugadores</h2>
        <div className="flex items-center gap-3">
          <span className="text-[10px] text-gray-500">Última actualización: {lastUpdated}</span>
          <button className="bg-slate-800 hover:bg-slate-700 text-white text-xs px-3 py-1.5 rounded" onClick={handleActualizarTodo}>Actualizar todo</button>
        </div>
      </header>
      <div className="flex items-center gap-3">
        <label className="text-sm text-gray-400">Filtrar por equipo:</label>
        <select className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm" value={filterTeam} onChange={e => setFilterTeam(e.target.value)}>
          <option value="">Todos</option>
          {teams.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
        </select>
      </div>
      <section className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
        <h3 className="text-lg font-semibold text-cyan-300 mb-3">Listado de jugadores</h3>
        {loading ? <div>Cargando...</div> : <DataTable columns={columns} data={data} />}
      </section>
    </div>
  );
}
