# Dashboard Apuestas

Dashboard LaLiga 2023-24 con integración Understat xG/xA, LaLiga.com y FotMob.

## Seguridad de API keys

Las keys de API-Football y Odds ahora se gestionan en el backend `server/`. Nunca se exponen al navegador.

### Variables de entorno

Copia `.env.example` a `.env` y completa las keys del servidor:

```
API_FOOTBALL_KEY_1=
API_FOOTBALL_KEY_2=
API_FOOTBALL_KEY_3=
ODDS_API_KEY_1=
ODDS_API_KEY_2=
ODDS_API_KEY_3=
PORT=4000
VITE_API_BASE=http://localhost:4000
```

El `.env` del proyecto está ignorado por Git.

## Desarrollo

Instala dependencias:
```bash
npm install
```

Levantar frontend + backend juntos:
```bash
npm run dev:all
```

Alternativa por separado:
```bash
npm run dev          # Vite en http://localhost:5173
npm run server       # Express en http://localhost:4000
```

### Build de producción

```bash
npm run build
npm run preview
```

El build de producción no contiene keys en el bundle.
