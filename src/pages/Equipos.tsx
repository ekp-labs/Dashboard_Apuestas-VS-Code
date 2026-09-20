import { useState, useEffect } from 'react';
import DataTable from '../components/DataTable';
import { staticData } from '../services/staticDataService';

export default function Equipos() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [toast, setToast] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<string>('—');
  const [teams, setTeams] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ts = localStorage.getItem('ff_last_update_teams');
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
    Promise.all([staticData.teams(), staticData.venues(), staticData.managers()]).then(([t, v, m]) => {
      const enriched = t.map((team:any) => ({
        ...team,
        venueName: v.find((ve:any)=> ve.id===team.venueId)?.name,
        managerName: m.find((ma:any)=> ma.id===team.managerId)?.name
      }));
      setTeams(enriched);
      setLoading(false);
      setToast('Equipos: datos cargados');
      localStorage.setItem('ff_last_update_teams', Date.now().toString());
    });
  }, [refreshTrigger]);

  useEffect(() => {
    const interval = setInterval(() => {
      setToast('Verificando actualización equipos...');
      setRefreshTrigger(t => t + 1);
    }, 60 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const handleActualizarTodo = () => {
    localStorage.setItem('ff_last_update_teams', Date.now().toString());
    setRefreshTrigger(t => t + 1);
  };

  const columns = [
    { key: 'name', header: 'Equipo' },
    { key: 'city', header: 'Ciudad' },
    { key: 'founded', header: 'Fundación' },
    { key: 'venueName', header: 'Estadio' },
    { key: 'managerName', header: 'Manager' }
  ];

  const data = teams.map(t => ({
    name: t.name,
    city: t.city,
    founded: t.founded,
    venueName: t.venueName || '-',
    managerName: t.managerName || '-'
  }));

  return (
    <div className="space-y-6">
      {toast && <div className="fixed top-4 right-4 bg-slate-900 border border-cyan-700 text-cyan-300 text-sm px-4 py-2 rounded shadow-lg z-50">{toast}</div>}
      <header className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Equipos</h2>
        <div className="flex items-center gap-3">
          <span className="text-[10px] text-gray-500">Última actualización: {lastUpdated}</span>
          <button className="bg-slate-800 hover:bg-slate-700 text-white text-xs px-3 py-1.5 rounded" onClick={handleActualizarTodo}>Actualizar todo</button>
        </div>
      </header>
      <section className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
        <h3 className="text-lg font-semibold text-cyan-300 mb-3">Listado de equipos</h3>
        {loading ? <div>Cargando...</div> : <DataTable columns={columns} data={data} />}
      </section>
    </div>
  );
}