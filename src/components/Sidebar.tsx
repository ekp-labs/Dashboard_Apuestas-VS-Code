export default function Sidebar({ active, onSelect }: { active: string; onSelect: (i:string)=>void }) {
  const items = ['Inicio','Competiciones','Equipos','Jugadores','Partidos','Apuestas','Inteligencia','Estadísticas'];
  return (
    <aside className="w-64 bg-[#0b1422] border-r border-slate-800 p-4 hidden md:flex flex-col">
      <h1 className="text-xl font-bold text-cyan-400 mb-6 tracking-wide">Football Analytics Center</h1>
      <nav className="space-y-1 text-sm">
        {items.map(item=>(
          <button
            key={item}
            onClick={()=>onSelect(item)}
            className={`w-full text-left px-3 py-2 rounded hover:bg-slate-800 ${active===item ? 'bg-slate-800 text-white' : 'text-gray-300'}`}
          >
            {item}
          </button>
        ))}
      </nav>
      <div className="mt-auto text-xs text-gray-500">Apuestas · Inteligencia</div>
    </aside>
  );
}
