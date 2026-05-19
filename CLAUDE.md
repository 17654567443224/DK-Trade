
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DK-project is a full-stack quantitative cryptocurrency trading platform for the OKX exchange. It consists of three components:

- **dkquantweb/dkquantweb/** — Vue 3 frontend (the active frontend app)
- **okx_quant/** — Python trading engine (Flask API + strategy execution)
- **RuoYi-Vue-master/** — Admin framework template (reference only)

## Commands

### Frontend (`dkquantweb/dkquantweb/`)
```bash
npm run dev       # Dev server at http://localhost:5173
npm run build     # Production build → dist/
npm run preview   # Preview production build
```

### Backend (`okx_quant/`)
```bash
# No build step — run directly with Python
python Quant_Engine/main_Engine.py   # Start Flask trading engine
python test.py                       # Run tests
python crawl_data.py                 # Fetch market data
```

Install Python dependencies:
```bash
pip install -r requirement.txt
```

## Architecture

### Frontend (Vue 3 + TypeScript)
- **Entry:** `src/main.ts` → `src/App.vue`
- **Routing:** `src/router/index.ts` — routes: `/`, `/login`, `/register`, `/user`, `/create-strategy`, `/strategy/:id`, `/update-plans`, `/about`
- **State:** Pinia stores in `src/stores/` (`user.ts`, `strategy.ts`)
- **API layer:** `src/api/` — one module per domain (`auth.ts`, `strategy.ts`, `quant.ts`, `orders.ts`, `report.ts`, etc.). All go through `src/api/request.ts` (Axios instance).
- **Axios config:** Base URL `http://127.0.0.1:8080`, Bearer token injected via interceptor, 10s timeout
- **Dev proxy:** `/dev-api` → `http://127.0.0.1:8080`
- **UI:** Element Plus (zh-cn locale), ECharts for charts, SCSS for styles

### Backend (Python / Flask)
- **`Quant_Engine/main_Engine.py`** — Flask app; orchestrates strategy loading, execution, and exposes REST endpoints
- **`Quant_Engine/simulation_Engine.py`** — Backtesting engine for historical simulation
- **`Quant_Engine/WebSocketManager.py`** — Real-time market data streaming via WebSocket
- **`Quant_Engine/Common/constants.py`** — Trading enums and interval definitions
- **`Quant_Engine/Common/object.py`** — Core data models
- **`okx/`** — OKX exchange SDK (15+ modules: `Account_api.py`, `Market_api.py`, `Trade_api.py`, etc.)
- **`functionns/`** — Strategy implementations (`one_symbol_trade` v1.0–v4.0, `multi_symbol_trade.py`, `algotrade.py`, `Hedge_arbitrage.py`)

### Data Flow
```
Vue 3 Frontend → HTTP/REST → Flask (main_Engine.py)
                                    ↓ WebSocket
                              Market Data Stream
                                    ↓
                          Strategy Execution Engine
                                    ↓
                              OKX Exchange API
```

## Key Conventions
- Frontend uses Vue 3 Composition API with `<script setup>` syntax throughout
- TypeScript strict mode enabled (`tsconfig.json`)
- Authentication state is managed in `src/stores/user.ts`; route guards check auth before protected routes
- Strategy components are modular: symbol selection, entry logic, exit/profit-loss logic, and fund management are separate configurable pieces
- Chinese localization (Element Plus zh-cn, Chinese UI text) — the platform targets Chinese users
