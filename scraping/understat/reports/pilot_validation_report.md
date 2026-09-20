# Pilot Validation Report – Understat LaLiga 2023-24

## Status
- Playwright browsers installed via `patchright install`. ✅
- Dynamic rendering validated with `StealthyFetcher` for `https://understat.com/league/La%20liga/2023`. ✅
- HTML snapshot saved to `data/raw/laliga_2023_snapshot_*.html` and snippet. ✅
- Column headers identified via table options:
  - Player table columns: №, Player, Team, Apps, Min, G, NPG, A, xG, NPxG, xA, xGChain, xGBuildup, xG90, NPxG90, xA90, xG90 + xA90, NPxG90 + xA90, xGChain90, xGBuildup90
- Extraction scaffold created in `src/extractors/player_extractor.py`.
- Pilot extraction validated with `network_idle=True, wait=5000`.

## Findings
- League code for LaLiga is `La liga` → URL encoded as `La%20liga`.
- Season 2023-24 URL: `https://understat.com/league/La%20liga/2023`
- With `network_idle` and `wait_selector='div.jTable'` player rows are now present in the rendered DOM.
- Player table found as second `div.jTable`. Header extracted: №, Player, Team, Apps, Min, G, A, xG, xA, xG90, xA90
- Sample players extracted successfully:
  - Artem Dovbyk – Girona – xG 23.31 – xA 6.51
  - Jude Bellingham – Real Madrid – xG 12.97 – xA 5.89
  - Robert Lewandowski – Barcelona – xG 17.91 – xA 5.10
- xG/xA cells contain newline with delta value; parser splits into value + delta.
- Current view returns top 10 players + total row. Full league list may require pagination/scroll or filter change.

## Files Created
- `src/save_understat_snapshot.py`
- `src/fetch_with_wait.py`
- `src/extract_and_save_players.py`
- `src/extractors/player_extractor.py`
- `data/raw/laliga_2023_waited_*.html`
- `data/processed/laliga_2023_players_*.json`

## Next Steps
1. ✅ Full player list captured via Understat AJAX API via `understatapi`. 598 players for LaLiga 2023-24 extracted.
2. Normalize xG/xA parsing and persist to `data/processed/` with schema player, team, season, apps, mins, gls, ast, xg, xa.
3. Scale extraction to seasons 2014-2026 per config.
4. Add logging and rate limiting.
