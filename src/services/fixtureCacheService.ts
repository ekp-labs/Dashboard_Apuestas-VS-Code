const CACHE_PREFIX = 'ff_cache:';
const DEFAULT_TTL = 24 * 60 * 60 * 1000; // 24h

function safeParse(str: string) {
  try { return JSON.parse(str); } catch { return null; }
}

export function getCached(key: string) {
  const raw = localStorage.getItem(CACHE_PREFIX + key);
  if (!raw) return null;
  const entry = safeParse(raw);
  if (!entry || !entry.ts || !entry.data) return null;
  if (Date.now() - entry.ts > entry.ttl) {
    localStorage.removeItem(CACHE_PREFIX + key);
    return null;
  }
  return entry.data;
}

export function setCached(key: string, data: any, ttl = DEFAULT_TTL) {
  const entry = { ts: Date.now(), ttl, data };
  try {
    localStorage.setItem(CACHE_PREFIX + key, JSON.stringify(entry));
  } catch { /* ignore quota */ }
}

export function invalidateCache(key?: string) {
  if (key) {
    localStorage.removeItem(CACHE_PREFIX + key);
  } else {
    Object.keys(localStorage).forEach(k => {
      if (k.startsWith(CACHE_PREFIX)) localStorage.removeItem(k);
    });
  }
}
