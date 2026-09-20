import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

type LineData = Record<string, any>;

export default function LineChartCard({ title, data, dataKey = 'value', stroke = '#22d3ee', xKey = 'date' }: { title: string; data: LineData[]; dataKey?: string; stroke?: string; xKey?: string }) {
  return (
    <div className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
      <h3 className="font-semibold mb-3">{title}</h3>
      <div className="h-56 bg-slate-900/40 rounded-lg border border-slate-800 p-2">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ left: 0, right: 10, top: 10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey={xKey} stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip contentStyle={{ backgroundColor: '#0b1422', border: '1px solid #1e293b', color: '#e2e8f0' }} />
            <Line type="monotone" dataKey={dataKey} stroke={stroke} strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
