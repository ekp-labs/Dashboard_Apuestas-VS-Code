from scrapling import StealthyFetcher
import json, re
f = StealthyFetcher()
def action(page):
    links = page.evaluate("""
    () => {
        const anchors = Array.from(document.querySelectorAll('a'));
        const seasons = new Set();
        anchors.forEach(a=>{
            const m = a.href.match(/\\/stats\\/season\\/(\\d+)\\/players\\/[^/]+\\/laliga/);
            if(m) seasons.add(m[1]);
        });
        return Array.from(seasons);
    }
    """)
    print(links)
f.fetch('https://www.fotmob.com/leagues/87/stats/players/laliga', network_idle=True, wait=8000, page_action=action)
