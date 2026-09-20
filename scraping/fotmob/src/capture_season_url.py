from scrapling import StealthyFetcher
import json

f = StealthyFetcher()
def action(page):
    # click season 2023/2024
    page.evaluate("""
    () => {
        const els = Array.from(document.querySelectorAll('*')).filter(e=>e.innerText && e.innerText.includes('2023/2024'));
        if(els.length>0) els[0].click();
    }
    """)
    # wait for navigation
    page.wait_for_timeout(5000)
    url = page.url()
    print('URL after click:', url)
    # extract season id from url
    import re
    m = re.search(r'/stats/season/(\\d+)/', url)
    if m:
        print('season_id:', m.group(1))
    else:
        print('season_id not found in url')
    # get page title
    title = page.title()
    print('title:', title)

f.fetch('https://www.fotmob.com/leagues/87/stats/players/laliga', network_idle=True, wait=8000, page_action=action)
