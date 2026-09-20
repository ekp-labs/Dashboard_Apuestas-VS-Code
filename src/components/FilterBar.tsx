export default function FilterBar({ options, active, onChange }: { options: { label: string; value: string }[]; active: string; onChange?: (v: string) => void }) {
  return (
    <div className="flex items-center gap-2 text-sm">
      {options.map(opt => {
        const isActive = active === opt.value;
        return (
          <button
            key={opt.value}
            onClick={() => onChange?.(opt.value)}
            className={`px-3 py-1.5 rounded-lg transition ${isActive ? 'bg-slate-800 text-white' : 'hover:bg-slate-800 text-gray-300'}`}
          >
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
