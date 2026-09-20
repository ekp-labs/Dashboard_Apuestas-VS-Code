"""
Extractor FotMob LaLiga player stats
Normaliza a esquema común
"""
import json, os
from datetime import datetime
from scrapling import StealthyFetcher

URL = "https://www.fotmob.com/leagues/87/stats/laliga/players"
SEASON = "2026/2027"  # FotMob muestra temporada actual por defecto

f = StealthyFetcher()
extracted = None

def action(page):
    global extracted
    extracted = page.evaluate("""
    () => {
        const players = [];
        // FotMob muestra secciones con headings y listas
        const sections = document.querySelectorAll('div[class*="stat"], section');
        // Fallback: extraer texto visible
        const text = document.body.innerText;
        return {text};
    }
    """)

f.fetch(URL, network_idle=True, wait=8000, page_action=action)

if extracted:
    # Simple parsing de top stats visibles
    text = extracted['text']
    # Extraer bloque Expected goals (xG)
    players = []
    # Para piloto, extraer primeras menciones de xG
    lines = text.split('\\n')
    in_xg = False
    for line in lines:
        if 'Expected goals' in line or 'Expected goals (xG)' in line:
            in_xg = True
            continue
        if in_xg:
            # esperar formato Nombre\\nEquipo\\nvalor
            pass
    # Guardar raw text para inspección
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    out_path = os.path.join(out_dir, f'fotmob_laliga_players_raw_{ts}.txt')
    with open(out_path, 'w', encoding='utf-8') as f_out:
        f_out.write(text)
    print('Saved raw text to', out_path)
    # Guardar metadata
    meta = {
        'source':'fotmob',
        'league':'laliga',
        'league_id':87,
        'url':URL,
        'season':SEASON,
        'extracted_at':ts
    }
    with open(os.path.join(out_dir, f'fotmob_laliga_metadata_{ts}.json'), 'w', encoding='utf-8') as f_meta:
        json.dump(meta, f_meta, ensure_ascii=False, indent=2)
    print('Metadata saved')
else:
    print('No extraction')
