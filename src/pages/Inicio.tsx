import KPICard from '../components/KPICard';

export default function Inicio() {
  const kpis = [
    { label: 'ROI 30d', value: '+12.4%', color: 'text-emerald-400' },
    { label: 'Aciertos', value: '68%', color: 'text-cyan-400' },
    { label: 'Value Bets', value: '23', color: 'text-fuchsia-400' },
    { label: 'Bankroll', value: '$12,340', color: 'text-emerald-400' },
  ];
  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Inicio</h2>
        <div className="text-sm text-gray-400">Actualizado hace 2 min</div>
      </header>

      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {kpis.map(k=><KPICard key={k.label} {...k} />)}
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 bg-[#0b1422] rounded-xl p-5 border border-slate-800">
          <h3 className="text-lg font-semibold mb-3 text-cyan-300">Partido Destacado</h3>
          <div className="flex items-center justify-between bg-slate-900/50 rounded-lg p-4 border border-slate-800">
            <div>
              <div className="font-medium">Real Madrid vs Barcelona</div>
              <div className="text-xs text-gray-400 mt-1">LaLiga · 24 Sep 21:00</div>
            </div>
            <div className="text-right">
              <div className="text-cyan-400 font-semibold">2.10</div>
              <div className="text-xs text-gray-400">Over 2.5</div>
            </div>
          </div>
        </div>
        <div className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
          <h3 className="font-semibold mb-2">Value Bet del día</h3>
          <p className="text-sm text-gray-300">Bayer Leverkusen H2H</p>
          <p className="text-fuchsia-400 mt-1 font-medium">Edge 8.3% · Kelly 2.1%</p>
        </div>
      </section>

      <section className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
        <h3 className="text-lg font-semibold mb-3">Gestión Bankroll</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="bg-slate-900/40 rounded-lg p-4 border border-slate-800">
            <div className="text-gray-400">Stake sugerido</div>
            <div className="text-xl mt-1">$185</div>
          </div>
          <div className="bg-slate-900/40 rounded-lg p-4 border border-slate-800">
            <div className="text-gray-400">Drawdown máx</div>
            <div className="text-xl mt-1">-6.2%</div>
          </div>
          <div className="bg-slate-900/40 rounded-lg p-4 border border-slate-800">
            <div className="text-gray-400">Próxima liquidación</div>
            <div className="text-xl mt-1">Viernes</div>
          </div>
        </div>
      </section>
    </div>
  );
}
