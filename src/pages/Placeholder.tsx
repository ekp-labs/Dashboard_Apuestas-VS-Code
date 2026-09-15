export default function Placeholder({ title }: { title: string }) {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      <div className="bg-[#0b1422] rounded-xl p-6 border border-slate-800 text-gray-400">
        Contenido estático en construcción. Próximamente integraciones con The Odds API y API-Football.
      </div>
    </div>
  );
}
