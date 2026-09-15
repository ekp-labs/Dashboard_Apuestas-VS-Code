export default function Apuestas() {
  const bets = [
    { match: 'Real Madrid vs Barcelona', market: 'Over 2.5', odds: 2.10, edge: 7.2, kelly: '2.1%' },
    { match: 'Bayern vs Dortmund', market: '1X2', odds: 1.95, edge: 5.8, kelly: '1.6%' },
    { match: 'Man City vs Arsenal', market: 'BTTS', odds: 1.85, edge: 4.3, kelly: '1.2%' },
  ];
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Apuestas</h2>
        <span className="text-sm text-gray-400">Value bets filtrados</span>
      </div>

      <div className="bg-[#0b1422] rounded-xl border border-slate-800 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-900/60 text-gray-400">
            <tr>
              <th className="text-left p-3">Partido</th>
              <th className="text-left p-3">Mercado</th>
              <th className="text-left p-3">Cuota</th>
              <th className="text-left p-3">Edge</th>
              <th className="text-left p-3">Kelly</th>
            </tr>
          </thead>
          <tbody>
            {bets.map((b,i)=>(
              <tr key={i} className="border-t border-slate-800 hover:bg-slate-900/40">
                <td className="p-3">{b.match}</td>
                <td className="p-3">{b.market}</td>
                <td className="p-3 text-cyan-400">{b.odds.toFixed(2)}</td>
                <td className="p-3 text-emerald-400">{b.edge}%</td>
                <td className="p-3">{b.kelly}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
