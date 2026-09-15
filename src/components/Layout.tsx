import { useState } from 'react';
import Sidebar from './Sidebar';

export default function Layout({ children }: { children: React.ReactNode }) {
  const [active, setActive] = useState('Inicio');
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#040b14] text-gray-200 flex">
      <Sidebar active={active} onSelect={(i)=>{ setActive(i); setMobileOpen(false); }} />
      
      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <div className="absolute inset-0 bg-black/60" onClick={()=>setMobileOpen(false)} />
          <div className="relative w-64 h-full bg-[#0b1422] border-r border-slate-800 p-4">
            <Sidebar active={active} onSelect={(i)=>{ setActive(i); setMobileOpen(false); }} />
          </div>
        </div>
      )}

      <div className="flex-1 flex flex-col">
        <header className="md:hidden flex items-center justify-between p-4 border-b border-slate-800 bg-[#0b1422]">
          <button onClick={()=>setMobileOpen(true)} className="text-cyan-400">☰</button>
          <span className="font-semibold">Football Analytics</span>
          <span />
        </header>
        <main className="flex-1 p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
