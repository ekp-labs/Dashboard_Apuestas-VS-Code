from scrapling import StealthyFetcher
import re
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
html = r.html_content

# Find all <th> with title attribute
rows = re.findall(r'<div class="row-title"><span[^>]*>(.*?)</span></div>', html, re.S)
clean = [re.sub(r'<[^>]+>', '', t).strip() for t in rows]
print('Row titles from table options:')
for c in clean:
    print(c)
