from scrapling import StealthyFetcher
import json
f = StealthyFetcher()
url = 'https://www.fotmob.com/leagues/87/stats/laliga/players'
def action(page):
    data = page.evaluate("""
    () => {
        const rows = Array.from(document.querySelectorAll('table tbody tr')).slice(0,10);
        const out = [];
        for (const tr of rows) {
            const cells = Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim());
            if (cells.length>0) out.push(cells);
        }
        return out;
    }
    """)
    print(json.dumps(data, indent=2, ensure_ascii=False))
f.fetch(url, network_idle=True, wait=5000, page_action=action)
