import { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';

const routeMap: Record<string, string> = {
  '/': 'Inicio',
  '/competiciones': 'Competiciones',
  '/equipos': 'Equipos',
  '/jugadores': 'Jugadores',
  '/partidos': 'Partidos',
  '/apuestas': 'Apuestas',
  '/inteligencia': 'Inteligencia',
  '/estadisticas': 'Estadísticas',
};

export default function Layout() {
  const location = useLocation();
  const active = routeMap[location.pathname] || 'Inicio';
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#040b14] text-gray-200 flex">
      <Sidebar active={active} />
      
      {mobileOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <div className="absolute inset-0 bg-black/60" onClick={()=>setMobileOpen(false)} />
          <div className="relative w-64 h-full bg-[#0b1422] border-r border-slate-800 p-4">
            <Sidebar active={active} />
          </div>
        </div>
      )}

      <div className="flex-1 flex flex-col">
        <header className="md:hidden flex items-center justify-between p-4 border-b border-slate-800 bg-[#0b1422]">
          <button onClick={()=>setMobileOpen(true)} className="text-cyan-400">☰</button>
          <span className="font-semibold">Football Analytics</span>
          <span />
        </header>
        <main className="flex-1 p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
