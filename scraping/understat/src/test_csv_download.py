from scrapling import StealthyFetcher
f = StealthyFetcher()
# Configure fetch with custom headers? StealthyFetcher may not allow.
url = "https://understat.com/league/La%20liga/2023"
resp = f.fetch(url)
# Try to find download links
import re
links = re.findall(r'href="([^"]+csv[^"]*)"', resp.html_content)
print('CSV links found:', links[:10])
