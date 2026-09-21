from scrapling import StealthyFetcher
import json
url = "https://www.laliga.com/en-ES/advanced-stats"
f = StealthyFetcher()
def action(page):
    # try to find selector options
    opts = page.evaluate("""
    () => {
        const selects = Array.from(document.querySelectorAll('select'));
        const result = [];
        for (const s of selects){
            const options = Array.from(s.options).map(o=>({value:o.value, text:o.textContent.trim()}));
            result.push({id:s.id, name:s.name, options});
        }
        return result;
    }
    """)
    print(json.dumps(opts, indent=2, ensure_ascii=False))
f.fetch(url, network_idle=True, wait=5000, page_action=action)
