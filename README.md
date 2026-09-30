# Always-On Multi-Bank Liquidity Bridge

End-to-end fintech hackathon prototype for cross-bank payment interoperability.

## Features
- Scenario-based interoperability friction analysis
- Smart route discovery and selection
- Configurable compliance checks
- Liquidity-aware routing
- Tokenised-value simulation
- Modular Drunix ledger adapter with local mock fallback
- Settlement/audit record
- Interactive dashboard

## Run

```bash
docker compose up --build
```

Dashboard: http://localhost:8501  
API docs: http://localhost:8000/docs

## Prototype disclaimer
This project simulates banking networks, tokenised value and settlement. It does not move real funds or claim live connectivity to Citi, SWIFT, NPCI, Drunix or other networks unless separately configured and verified.

## Demo
Default scenario: USD 10M from Citi New York to Bank X Singapore. Analyse the payment, compare eligible routes, then execute a simulated settlement.
