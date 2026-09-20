import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

type PieData = { name: string; value: number };

export default function PieChartCard({ title, data, colors = ['#22d3ee', '#a78bfa', '#34d399'] }: { title: string; data: PieData[]; colors?: string[] }) {
  return (
    <div className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
      <h3 className="font-semibold mb-3">{title}</h3>
      <div className="h-56 bg-slate-900/40 rounded-lg border border-slate-800 p-2">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" outerRadius={80} label>
              {data.map((_, i) => (
                <Cell key={i} fill={colors[i % colors.length]} />
              ))}
            </Pie>
            <Tooltip contentStyle={{ backgroundColor: '#0b1422', border: '1px solid #1e293b', color: '#e2e8f0' }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
