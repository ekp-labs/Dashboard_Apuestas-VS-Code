"""
Extractor LaLiga.com API para estadísticas de jugadores
Usa API pública de LaLiga con subscription-key
"""
import requests, json, os
from datetime import datetime

SUBSCRIPTION_KEY = "c13c3a8e2f6b46da9c5c425cf61fab3e"
SEASON = "laliga-easports-2023"
SUBSCRIPTION_ID = 329
BASE_URL = "https://apim.laliga.com/public-service/api/v1"

def fetch_subscription():
    url = f"{BASE_URL}/subscriptions/{SEASON}?contentLanguage=en&subscription-key={SUBSCRIPTION_KEY}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()['subscription']

def fetch_players(page=1, page_size=100):
    url = f"{BASE_URL}/players?subscriptionId={SUBSCRIPTION_ID}&contentLanguage=en&subscription-key={SUBSCRIPTION_KEY}&page={page}&pageSize={page_size}"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def main():
    sub = fetch_subscription()
    print('Subscription', sub['name'], sub['season'])
    all_players = []
    page = 1
    while True:
        data = fetch_players(page=page)
        players = data.get('players', [])
        if not players:
            break
        all_players.extend(players)
        print(f'Page {page} -> {len(players)} players, total {len(all_players)}')
        if len(players) < 100:
            break
        page += 1
    # Save
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(out_dir, f'players_api_{SEASON}_{ts}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'source':'laliga_com','season':SEASON,'subscription':sub,'players':all_players}, f, ensure_ascii=False)
    print('Saved', out_path, 'players', len(all_players))

if __name__ == '__main__':
    main()
