export type ApiProvider = 'apiFootball' | 'odds';

// Las keys se gestionan ahora en el backend. Este módulo queda como stub para compatibilidad.
export function getApiKeyPool(provider: ApiProvider): string[] {
  return [];
}

export function isPoolConfigured(provider: ApiProvider): boolean {
  return false;
}
