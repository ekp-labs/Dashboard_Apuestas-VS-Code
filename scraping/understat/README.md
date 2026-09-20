# Understat Scraper - LaLiga

Proyecto educativo para extracción de métricas xG/xA de Understat.com con Scrapling.

## Estructura
- config/ : configuración de temporadas y parámetros
- src/ : scripts de extracción y normalización
- data/raw/ : datos descargados sin procesar
- data/processed/ : datos normalizados
- logs/ : registros de ejecución
- reports/ : informes de validación

## Entorno
Python 3.10+ con entorno virtual en `venv/`.
Scrapling + fetchers instalados. Playwright browsers instalados vía `patchright install`.

## Uso
Pilot inicial: LaLiga 2023-24, todos los jugadores.
Respetar robots.txt y límites de tasa.

## Estado actual
- ✅ Playwright browsers instalados
- ✅ URL de LaLiga 2023-24 validada: `https://understat.com/league/La%20liga/2023`
- ✅ Snapshot HTML guardado en `data/raw/`
- ✅ Selectores adaptativos identificados para columnas xG/xA
- ✅ Extracción piloto validada con `network_idle` y `wait_selector`. Ejemplo: Dovbyk 23.31 xG / 6.51 xA, Bellingham 12.97 xG / 5.89 xA
- 📄 Datos piloto guardados en `data/processed/laliga_2023_players_*.json`
- ✅ Extracción completa vía API Understat `getLeagueData`. 598 jugadores LaLiga 2023-24 en `data/processed/laliga_2023_players_api_*.json`
- Informe: `reports/pilot_validation_report.md`
