from scrapling import StealthyFetcher
import re
f = StealthyFetcher()
r = f.fetch('https://understat.com/league/EPL/2023')
html = r.html_content
# Find all option tags
opts = re.findall(r'<option value="([^"]+)">([^<]+)</option>', html)
league_opts = [(v,t) for v,t in opts if t.strip().lower() in ['epl','la liga','bundesliga','serie a','ligue 1','rfpl']]
print(league_opts)
