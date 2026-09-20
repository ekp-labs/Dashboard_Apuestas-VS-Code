from scrapling import StealthyFetcher
f = StealthyFetcher()
url = 'https://www.fotmob.com/players/19001'
def action(page):
    info = page.evaluate("""
    () => {
        const title = document.title;
        const name = document.querySelector('h1')?.innerText || '';
        const stats = Array.from(document.querySelectorAll('[class*="stat"]')).map(e=>e.innerText).slice(0,20);
        return {title, name, stats};
    }
    """)
    print(info)
f.fetch(url, network_idle=True, wait=5000, page_action=action)
