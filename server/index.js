import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

const API_FOOTBALL_KEYS = [
  process.env.API_FOOTBALL_KEY_1,
  process.env.API_FOOTBALL_KEY_2,
  process.env.API_FOOTBALL_KEY_3,
].filter(Boolean);

const ODDS_KEYS = [
  process.env.ODDS_API_KEY_1,
  process.env.ODDS_API_KEY_2,
  process.env.ODDS_API_KEY_3,
].filter(Boolean);

const BASE_FOOTBALL = 'https://v3.football.api-sports.io';
const BASE_ODDS = 'https://api.the-odds-api.com/v4';

const cache = new Map();
const CACHE_TTL = 5 * 60 * 1000;

function getCache(key) {
  const entry = cache.get(key);
  if (!entry) return null;
  if (Date.now() - entry.ts > CACHE_TTL) {
    cache.delete(key);
    return null;
  }
  return entry.data;
}

function setCache(key, data) {
  cache.set(key, { data, ts: Date.now() });
}

async function fetchWithFootballPool(path, params = {}) {
  const url = new URL(`${BASE_FOOTBALL}${path}`);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== '') url.searchParams.set(k, v);
  });

  for (const key of API_FOOTBALL_KEYS) {
    try {
      const res = await fetch(url.toString(), {
        headers: { 'x-apisports-key': key }
      });
      if (res.status === 429) continue;
      if (!res.ok) continue;
      return await res.json();
    } catch {}
  }
  throw new Error('API-Football pool exhausted');
}

async function fetchWithOddsPool(sportKey, opts = {}) {
  const url = new URL(`${BASE_ODDS}/sports/${sportKey}/odds`);
  url.searchParams.set('markets', opts.markets || 'h2h,spreads,totals');
  if (opts.live) url.searchParams.set('live', 'true');

  for (const key of ODDS_KEYS) {
    try {
      const res = await fetch(url.toString(), {
        headers: { 'Ocp-Apim-Subscription-Key': key }
      });
      if (res.status === 429) continue;
      if (!res.ok) continue;
      return await res.json();
    } catch {}
  }
  throw new Error('Odds pool exhausted');
}

app.get('/api/fixtures', async (req, res) => {
  try {
    const { leagueId, status = 'NS', season } = req.query;
    const currentSeason = season ?? new Date().getFullYear().toString();
    const cacheKey = `fixtures:${leagueId ?? 'all'}:${status}:${currentSeason}`;
    const cached = getCache(cacheKey);
    if (cached) return res.json(cached);

    const data = await fetchWithFootballPool('/fixtures', {
      league: leagueId ?? '',
      season: currentSeason,
      status
    });
    setCache(cacheKey, data);
    res.json(data);
  } catch (err) {
    console.error('[server] /api/fixtures error', err.message);
    res.status(502).json({ error: 'Upstream API unavailable', message: err.message });
  }
});

app.get('/api/odds', async (req, res) => {
  try {
    const { sportKey = 'soccer_epl', markets, live } = req.query;
    const cacheKey = `odds:${sportKey}:${markets}:${live}`;
    const cached = getCache(cacheKey);
    if (cached) return res.json(cached);

    const data = await fetchWithOddsPool(sportKey, { markets, live });
    setCache(cacheKey, data);
    res.json(data);
  } catch (err) {
    console.error('[server] /api/odds error', err.message);
    res.status(502).json({ error: 'Upstream API unavailable', message: err.message });
  }
});

app.get('/health', (_, res) => res.json({ ok: true, keys: { football: API_FOOTBALL_KEYS.length, odds: ODDS_KEYS.length } }));

app.listen(PORT, () => {
  console.log(`[server] API proxy listening on http://localhost:${PORT}`);
  console.log(`[server] Football keys configured: ${API_FOOTBALL_KEYS.length}, Odds keys configured: ${ODDS_KEYS.length}`);
});
