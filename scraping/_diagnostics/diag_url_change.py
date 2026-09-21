from scrapling import StealthyFetcher
URL = "https://www.laliga.com/en-ES/advanced-stats"
f = StealthyFetcher()
def action(page):
    # wait a bit
    import time
    time.sleep(3)
    # try to find selector for season
    # we can evaluate JS to click first option containing 2023
    page.evaluate("""
    () => {
        const opts = Array.from(document.querySelectorAll('select option, [role=option], li, a'));
        const target = opts.find(el => /2023[\\-/]2024/.test(el.textContent));
        if (target) {
            const parent = target.closest('select') || target.closest('div');
            if (parent) {
                parent.dispatchEvent(new Event('click', {bubbles:true}));
                target.click();
            }
        }
        // fallback: try URL change with param
        window._seasonClicked = true;
    }
    """)
    time.sleep(4)
    loc = page.evaluate("() => location.href")
    print('Location after attempt:', loc)
    # list resource names
    resources = page.evaluate("() => performance.getEntriesByType('resource').map(r=>r.name)")
    nextdata = [r for r in resources if '/_next/data/' in r]
    print('Next data count:', len(nextdata))
    for r in nextdata:
        print(r)
f.fetch(URL, network_idle=True, wait=10000, page_action=action)
