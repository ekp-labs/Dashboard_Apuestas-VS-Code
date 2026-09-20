from scrapling import StealthyFetcher
import re

f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
html = r.html_content

# Find all <th> texts
ths = re.findall(r'<th[^>]*>(.*?)</th>', html, re.S)
clean = [re.sub(r'<[^>]+>', '', t).strip() for t in ths]
# Print unique
seen=set()
uniq=[]
for c in clean:
    if c and c not in seen:
        seen.add(c)
        uniq.append(c)
print('All unique th texts:')
for u in uniq:
    print(u)

# Find player table rows? Look for <tr> containing Player column.
# Find a snippet around 'Player' header
idx = html.find('Player')
if idx!=-1:
    print('Snippet around Player header:')
    print(html[max(0,idx-500):idx+500])
