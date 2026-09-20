from scrapling import StealthyFetcher
import re
f = StealthyFetcher()
url = "https://www.laliga.com/en-ES/laliga-easports"
resp = f.fetch(url, network_idle=True, wait=3000)
html = resp.html_content
links = re.findall(r'href=\"([^\"]*statistics[^\"]*)\"', html, re.I)
print('stats links found:', set(links))
