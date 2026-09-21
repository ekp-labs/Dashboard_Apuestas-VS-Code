from scrapling import StealthyFetcher
f = StealthyFetcher()
url = 'https://www.fotmob.com/leagues/87/stats/season/21053/players/expected_goals_per_90/laliga'
extracted = None
def action(page):
    global extracted
    extracted = page.evaluate("() => document.body.innerText")
f.fetch(url, network_idle=True, wait=10000, page_action=action)
if extracted:
    lines = [l.strip() for l in extracted.splitlines() if l.strip()]
    for i,l in enumerate(lines[:120]):
        print(i,l)
