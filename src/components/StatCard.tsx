export default function StatCard({ label, value, sublabel, color = 'text-gray-200' }: { label: string; value: string; sublabel?: string; color?: string }) {
  return (
    <div className="bg-[#0b1422] rounded-xl p-4 border border-slate-800">
      <div className="text-xs text-gray-400">{label}</div>
      <div className={`text-2xl font-semibold mt-1 ${color}`}>{value}</div>
      {sublabel && <div className="text-xs text-gray-500 mt-1">{sublabel}</div>}
    </div>
  );
}
