type Column<T> = {
  key: keyof T | string;
  header: string;
  className?: string;
  render?: (row: T) => React.ReactNode;
};

export default function DataTable<T extends Record<string, any>>({ columns, data, emptyText = 'Sin datos' }: { columns: Column<T>[]; data: T[]; emptyText?: string }) {
  return (
    <div className="overflow-hidden rounded-lg border border-slate-800">
      <table className="w-full text-sm">
        <thead className="bg-slate-900/60 text-gray-400">
          <tr>
            {columns.map(col => (
              <th key={String(col.key)} className={`p-3 text-left ${col.className || ''}`}>{col.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="p-4 text-center text-gray-500">{emptyText}</td>
            </tr>
          ) : (
            data.map((row, i) => (
              <tr key={i} className="border-t border-slate-800 hover:bg-slate-900/40">
                {columns.map(col => (
                  <td key={String(col.key)} className="p-3">
                    {col.render ? col.render(row) : String(row[col.key as keyof T] ?? '')}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
