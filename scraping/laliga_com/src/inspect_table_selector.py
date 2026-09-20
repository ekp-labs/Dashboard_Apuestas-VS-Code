from scrapling import StealthyFetcher
def dump_table(page):
    rows = page.evaluate("""
    () => {
        const tables = Array.from(document.querySelectorAll('table'));
        return tables.map(t => {
            const headers = Array.from(t.querySelectorAll('th')).map(th => th.innerText.trim()).slice(0,20);
            const firstRows = Array.from(t.querySelectorAll('tbody tr')).slice(0,3).map(tr => Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim()));
            return {headers, firstRows};
        });
    }
    """)
    print('tables found:', len(rows))
    for i,t in enumerate(rows):
        print('Table', i, 'headers', t['headers'][:10])
        print('rows sample', t['firstRows'])

f = StealthyFetcher()
resp = f.fetch('https://www.laliga.com/en-ES/advanced-stats', network_idle=True, wait=5000, page_action=dump_table)
