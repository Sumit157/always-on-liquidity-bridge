# Architecture

The dashboard calls FastAPI. FastAPI validates the payment, runs compliance, filters eligible routes, scores them with SmartRouter and exposes scenario friction metrics. Execute mode passes the selected route to a ledger adapter that records a simulated settlement.

The default ledger implementation is `MockDrunixLedger`. It is isolated behind `LedgerAdapter` so a verified Drunix integration can be added later without changing routing logic.
