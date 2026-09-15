import { Link } from 'react-router-dom';

const routes = [
  { label: 'Inicio', path: '/' },
  { label: 'Competiciones', path: '/competiciones' },
  { label: 'Equipos', path: '/equipos' },
  { label: 'Jugadores', path: '/jugadores' },
  { label: 'Partidos', path: '/partidos' },
  { label: 'Apuestas', path: '/apuestas' },
  { label: 'Inteligencia', path: '/inteligencia' },
  { label: 'Estadísticas', path: '/estadisticas' },
];

export default function Sidebar({ active }: { active: string }) {
  return (
    <aside className="w-64 bg-[#0b1422] border-r border-slate-800 p-4 hidden md:flex flex-col">
      <h1 className="text-xl font-bold text-cyan-400 mb-6 tracking-wide">Football Analytics Center</h1>
      <nav className="space-y-1 text-sm">
        {routes.map(item=>(
          <Link
            key={item.label}
            to={item.path}
            className={`block px-3 py-2 rounded hover:bg-slate-800 ${active===item.label ? 'bg-slate-800 text-white' : 'text-gray-300'}`}
          >
            {item.label}
          </Link>
        ))}
      </nav>
      <div className="mt-auto text-xs text-gray-500">Apuestas · Inteligencia</div>
    </aside>
  );
}

