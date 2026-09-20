import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';

export default function RadarChartCard({ title, data }: { title: string; data: { subject: string; A: number; B: number }[] }) {
  return (
    <div className="bg-[#0b1422] rounded-xl p-5 border border-slate-800">
      <h3 className="font-semibold mb-3">{title}</h3>
      <div className="h-56 bg-slate-900/40 rounded-lg border border-slate-800 p-2">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart outerRadius={90} data={data}>
            <PolarGrid stroke="#1e293b" />
            <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#64748b' }} />
            <Radar name="Local" dataKey="A" stroke="#22d3ee" fill="#22d3ee" fillOpacity={0.3} />
            <Radar name="Visitante" dataKey="B" stroke="#a78bfa" fill="#a78bfa" fillOpacity={0.3} />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
