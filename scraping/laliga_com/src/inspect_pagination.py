from scrapling import StealthyFetcher
def dump(page):
    info = page.evaluate("""
    () => {
        const table = document.querySelector('table');
        if (!table) return {found:false};
        const rows = table.querySelectorAll('tbody tr').length;
        const pagination = document.querySelectorAll('[aria-label="pagination"], .pagination, button[aria-label*="next"], button[aria-label*="siguiente"]').length;
        return {found:true, rows, pagination, html: table.outerHTML.slice(0,500)};
    }
    """)
    print(info)

f = StealthyFetcher()
f.fetch('https://www.laliga.com/en-ES/advanced-stats', network_idle=True, wait=5000, page_action=dump)
