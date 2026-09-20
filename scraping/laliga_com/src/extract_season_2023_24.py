from scrapling import StealthyFetcher
import json

URL = "https://www.laliga.com/en-ES/advanced-stats"

f = StealthyFetcher()
extracted = None

def action(page):
    global extracted
    extracted = page.evaluate("""
    () => {
        // Buscar selector de temporada
        const selects = Array.from(document.querySelectorAll('select'));
        const seasons = [];
        for (const s of selects) {
            const opts = Array.from(s.options).map(o=>({value:o.value, text:o.textContent.trim()}));
            seasons.push({id:s.id, name:s.name, options:opts});
        }
        // Intentar encontrar botón con texto 2023-2024
        const links = Array.from(document.querySelectorAll('a')).map(a=>({href:a.href, text:a.innerText.trim()})).filter(l=>l.text.includes('2023'));
        return {seasons, links};
    }
    """)

f.fetch(URL, network_idle=True, wait=5000, page_action=action)
print(json.dumps(extracted, indent=2, ensure_ascii=False))
