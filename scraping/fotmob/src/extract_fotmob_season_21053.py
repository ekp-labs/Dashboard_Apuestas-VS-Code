from playwright.sync_api import sync_playwright
import json, os

SEASON_ID = 21053
LEAGUE_ID = 87
LEAGUE_SLUG = "laliga"
OUTPUT_PATH = r"f:\- APP DEV -\2. VS Code\Dashboard Apuestas\DashboardApuestas\scraping\fotmob\data\processed\fotmob_laliga_2023_24_normalized.json"

METRICS = [
    "expected_goals",
    "expected_assists",
    "expected_goals_per_90",
    "expected_assists_per_90"
]

def extract():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for metric in METRICS:
            url = f"https://www.fotmob.com/leagues/{LEAGUE_ID}/stats/season/{SEASON_ID}/players/{metric}/{LEAGUE_SLUG}"
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                # Extraer filas de la tabla - simplificado
                # Aquí iría la lógica real de parseo de la tabla
                # Por ahora placeholder
                results.append({
                    "source": "fotmob",
                    "league": "laliga",
                    "league_id": LEAGUE_ID,
                    "season": "2023/2024",
                    "metric": metric,
                    "player_name": "PLACEHOLDER",
                    "team": "PLACEHOLDER",
                    "value": 0
                })
            except Exception as e:
                print(f"Error metric {metric}: {e}")
        browser.close()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(results)} records to {OUTPUT_PATH}")

if __name__ == "__main__":
    extract()
