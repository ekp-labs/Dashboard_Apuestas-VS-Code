# LaLiga.com Scraper

Extractor educativo de estadísticas de jugadores de LaLiga.com. No expone xG/xA; se extraen métricas tradicionales: partidos, goles, asistencias, tiros, etc.

## Estructura
- `src/extract_players.py` – extracción piloto con Scrapling
- `data/raw/` – snapshots HTML
- `data/processed/` – JSON normalizado

## Estado
- Inspección inicial completada: estadísticas avanzadas disponibles sin xG/xA.
- Piloto en progreso.
