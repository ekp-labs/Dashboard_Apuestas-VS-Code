"""
Extrae los season IDs de una liga en FotMob automatizando un navegador
headless con Playwright. No requiere intervención manual: Playwright
genera el header x-mas por sí solo al correr JS real.

Uso:
    python fotmob_season_ids.py <league_id> <league_slug>
    python fotmob_season_ids.py 87 laliga
"""

import sys
import json
from playwright.sync_api import sync_playwright


def get_season_ids(league_id: str, league_slug: str) -> list[dict]:
    url = f"https://www.fotmob.com/leagues/{league_id}/stats/players/{league_slug}"
    captured = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Intercepta toda petición que vaya al API interno de FotMob
        def handle_response(response):
            req_url = response.url
            if "apigw.fotmob.com" in req_url or "/api/" in req_url:
                try:
                    body = response.json()
                except Exception:
                    return
                captured.append({"url": req_url, "body": body})

        page.on("response", handle_response)
        page.goto(url, wait_until="networkidle")

        # Abre el selector de temporada - primero intenta hacer click en el control visible asociado al label
        # Busca el elemento con id que empieza por seasons-dropdown-
        selector = page.locator("select, button, div").filter(has=page.locator("text=Select season")).first
        if selector.count() == 0:
            # Fallback: hacer click en el label y luego en el control cercano
            page.locator("label:has-text('Select season')").click()
        else:
            selector.click()
        page.wait_for_timeout(800)

        # Lee las opciones visibles del dropdown
        options = page.locator("li, [role='option']").all_text_contents()
        season_names = [o.strip() for o in options if "/" in o]

        for season_name in season_names:
            try:
                page.click(f"text='{season_name}'", timeout=3000)
                page.wait_for_timeout(800)  # deja que dispare la petición
            except Exception:
                continue

        browser.close()

    return captured


if __name__ == "__main__":
    league_id = sys.argv[1] if len(sys.argv) > 1 else "87"
    league_slug = sys.argv[2] if len(sys.argv) > 2 else "laliga"

    results = get_season_ids(league_id, league_slug)
    print(json.dumps(results, indent=2, ensure_ascii=False))
