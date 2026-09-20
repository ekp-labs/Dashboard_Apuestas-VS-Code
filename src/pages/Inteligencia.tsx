import { useState } from 'react';
import FilterBar from '../components/FilterBar';
import DataTable from '../components/DataTable';
import RadarChartCard from '../components/RadarChartCard';

export default function Inteligencia() {
  const [filter, setFilter] = useState('todos');

  const insights = [
    { titulo: 'Value Bet del día', texto: 'Bayer Leverkusen H2H', metrica: 'Edge 8.3% · Kelly 2.1%' },
    { titulo: 'Modelo xG', texto: 'Over 2.5 Real Madrid vs Barcelona', metrica: 'Prob 62% · Valor +5.4%' },
    { titulo: 'Momentum', texto: 'Bayern 4W streak', metrica: 'Form Rating 8.7/10' },
    { titulo: 'Lesiones clave', texto: 'Arsenal sin Partey', metrica: 'Impact -12% xG' },
  ];

  const predicciones = [
    { partido: 'Man City vs Arsenal', mercado: 'Over 2.5', prob: '64%', cuota: 1.85, valor: '+7.2%' },
    { partido: 'Inter vs Napoli', mercado: 'BTTS', prob: '58%', cuota: 1.95, valor: '+4.8%' },
    { partido: 'Real Madrid vs Barcelona', mercado: '1X2', prob: '51%', cuota: 2.10, valor: '+3.1%' },
  ];

  const predColumns = [
    { key: 'partido', header: 'Partido' },
    { key: 'mercado', header: 'Mercado' },
    { key: 'prob', header: 'Prob Modelo', className: 'text-center', render: (r:any)=> <span className="text-emerald-400">{r.prob}</span> },
    { key: 'cuota', header: 'Cuota', className: 'text-center', render: (r:any)=> <span className="text-cyan-400">{r.cuota}</span> },
    { key: 'valor', header: 'Valor', className: 'text-center', render: (r:any)=> <span className="text-fuchsia-400">{r.valor}</span> },
  ];

  const filteredPred = filter === 'todos' ? predicciones : predicciones.filter(p=>p.mercado===filter);

  const radarData = [
    { subject: 'xG', A: 85, B: 70 },
    { subject: 'Posesión', A: 78, B: 65 },
    { subject: 'Tiros', A: 90, B: 75 },
    { subject: 'PPDA', A: 70, B: 80 },
    { subject: 'Presión', A: 80, B: 60 },
  ];

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Inteligencia</h2>
        <div className="text-sm text-gray-400">Modelos actualizados hace 10 min</div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {insights.map((i,idx)=>(
          <div key={idx} className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
            <div className="text-xs text-gray-400 mb-1">{i.titulo}</div>
            <div className="font-medium">{i.texto}</div>
            <div className="mt-2 text-sm text-cyan-400">{i.metrica}</div>
          </div>
        ))}
      </section>

      <FilterBar
        active={filter}
        onChange={setFilter}
        options={[
          { label: 'Todos', value: 'todos' },
          { label: 'Over 2.5', value: 'Over 2.5' },
          { label: 'BTTS', value: 'BTTS' },
          { label: '1X2', value: '1X2' },
        ]}
      />

      <section className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
        <h3 className="text-lg font-semibold mb-3 text-cyan-300">Predicciones modelo</h3>
        <DataTable columns={predColumns} data={filteredPred} />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <RadarChartCard title="Radar de forma" data={radarData} />
        </div>
        <div className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
          <h3 className="font-semibold mb-3">Alertas</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>• Cambio de entrenador en Valencia</li>
            <li>• Lluvia prevista en Londres</li>
            <li>• Suspensión de Rodri</li>
          </ul>
        </div>
      </section>
    </div>
  );
}
