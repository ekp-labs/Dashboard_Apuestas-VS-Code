from scrapling import StealthyFetcher
import re

f = StealthyFetcher()
url = 'https://www.fotmob.com/leagues/87/stats/season/21053/players/expected_goals/laliga'
extracted = None
def action(page):
    global extracted
    extracted = page.evaluate("() => document.body.innerText")
f.fetch(url, network_idle=True, wait=10000, page_action=action)
if extracted:
    lines = extracted.splitlines()
    # print first 200 lines
    for i,line in enumerate(lines[:200]):
        print(i, repr(line))
else:
    print('no')
