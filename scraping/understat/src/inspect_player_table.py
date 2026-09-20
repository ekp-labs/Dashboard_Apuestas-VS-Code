from scrapling import StealthyFetcher
import re

f = StealthyFetcher()
r = f.fetch('https://understat.com/league/La%20liga/2023')
html = r.html_content

# Find sections containing 'player'
matches = [m.start() for m in re.finditer('player', html, re.I)]
print('Occurrences of player:', len(matches))

# Find table headers
# Look for <th> containing xG or xA
ths = re.findall(r'<th[^>]*>(.*?)</th>', html, re.S)
clean = [re.sub(r'<[^>]+>', '', t).strip() for t in ths]
uniq = []
for c in clean:
    if c and c not in uniq:
        uniq.append(c)
print('Headers snippet:', uniq[:100])

# Find JSON data embedded
json_matches = re.findall(r'window\.__data__|window\.__players__|data-player', html, re.I)
print('JSON markers:', json_matches)

# Look for script tags containing player data
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
# Print scripts containing 'xG'
for i, s in enumerate(scripts):
    if 'xG' in s and 'player' in s.lower():
        print(f'--- script {i} snippet ---')
        print(s[:500])
        break
