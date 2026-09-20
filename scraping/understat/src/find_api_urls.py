from scrapling import StealthyFetcher
import re
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
html = r.html_content

# Find URLs in JS
urls = re.findall(r'https://understat\.com/api/[^"\']+', html)
print('API URLs found:', set(urls))
