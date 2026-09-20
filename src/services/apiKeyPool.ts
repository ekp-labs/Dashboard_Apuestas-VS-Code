export type ApiProvider = 'apiFootball' | 'odds';

export function getApiKeyPool(provider: ApiProvider): string[] {
  const map: Record<ApiProvider, string[]> = {
    apiFootball: [
      import.meta.env.VITE_API_FOOTBALL_KEY_1,
      import.meta.env.VITE_API_FOOTBALL_KEY_2,
      import.meta.env.VITE_API_FOOTBALL_KEY_3,
    ].filter(Boolean) as string[],
    odds: [
      import.meta.env.VITE_ODDS_API_KEY_1,
      import.meta.env.VITE_ODDS_API_KEY_2,
      import.meta.env.VITE_ODDS_API_KEY_3,
    ].filter(Boolean) as string[],
  };
  return map[provider];
}

export function isPoolConfigured(provider: ApiProvider): boolean {
  return getApiKeyPool(provider).length > 0;
}
