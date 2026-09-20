from scrapling import StealthyFetcher
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/EPL/2023')
print(r.status, len(r.html_content))
# search for La liga
if 'La liga' in r.html_content:
    print('found')
else:
    print('not found')
# print snippet around 'La liga'
import re
m = re.search(r'La liga.{0,200}', r.html_content)
if m:
    print(m.group(0))
