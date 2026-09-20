from scrapling import StealthyFetcher
import json, os

SEASON_ID = 21053
URL = f'https://www.fotmob.com/leagues/87/stats/season/{SEASON_ID}/players/laliga'

f = StealthyFetcher()
def action(page):
    # extract table rows
    data = page.evaluate("""
    () => {
        const rows = [];
        // FotMob stats table is rendered dynamically; try to get all links with metric data
        const anchors = Array.from(document.querySelectorAll('a')).filter(a=>a.href.includes('/stats/season/') && a.href.includes('/laliga'));
        return anchors.slice(0,200).map(a=>({href:a.href, text:a.innerText.trim()}));
    }
    """)
    print(json.dumps(data[:10], indent=2))

f.fetch(URL, network_idle=True, wait=10000, page_action=action)
