export default function KPICard({ label, value, color = 'text-gray-200' }: { label:string; value:string; color?:string }) {
  return (
    <div className="bg-[#0b1422] rounded-xl p-4 border border-slate-800">
      <div className="text-xs text-gray-400">{label}</div>
      <div className={`text-2xl font-semibold mt-1 ${color}`}>{value}</div>
    </div>
  );
}
