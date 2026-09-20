from scrapling import StealthyFetcher
import re
f = StealthyFetcher()
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url, network_idle=True, wait=5000)
html = resp.html_content
# Find script containing getLeagueData
matches = re.findall(r'getLeagueData[^\"]*', html)
print(matches[:20])
