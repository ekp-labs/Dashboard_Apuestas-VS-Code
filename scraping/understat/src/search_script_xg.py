from scrapling import StealthyFetcher
import re
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
html = r.html_content
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
count=0
for s in scripts:
    if 'xG' in s and 'player' in s.lower():
        count+=1
        print('--- script snippet ---')
        print(s[:800])
print('total scripts with xG and player:', count)
