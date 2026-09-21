from scrapling import StealthyFetcher
import json
URL = "https://www.laliga.com/en-ES/advanced-stats"
f = StealthyFetcher()
def action(page):
    # try to change season via JS
    page.evaluate("""
    () => {
        const selects = Array.from(document.querySelectorAll('select'));
        for (const s of selects) {
            const opt = Array.from(s.options).find(o => o.textContent.includes('2023') && o.textContent.includes('2024'));
            if (opt) { s.value = opt.value; s.dispatchEvent(new Event('change', {bubbles:true})); }
        }
        const links = Array.from(document.querySelectorAll('a'));
        for (const a of links) {
            if (a.innerText.includes('2023-2024') || a.innerText.includes('2023/2024')) { a.click(); break; }
        }
    }
    """)
    import time
    time.sleep(3)
    # capture resources
    resources = page.evaluate("""
    () => performance.getEntriesByType('resource').map(r => r.name)
    """)
    print('--- Resources containing _next/data ---')
    for r in resources:
        if '/_next/data/' in r:
            print(r)
    # current URL
    current = page.evaluate("() => location.href")
    print('Current URL:', current)
    # try to fetch _next data via fetch API inside page
    # just print first 500 chars of page
    html = page.evaluate("() => document.documentElement.outerHTML.slice(0,2000)")
    print('HTML start:', html[:500])
f.fetch(URL, network_idle=True, wait=8000, page_action=action)
