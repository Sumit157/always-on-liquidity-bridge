from datetime import datetime, timezone
from uuid import uuid4

class LedgerAdapter:
    def register_transfer(self, payload: dict) -> dict: raise NotImplementedError

class MockDrunixLedger(LedgerAdapter):
    def register_transfer(self, payload: dict) -> dict:
        return {"transaction_id":f"DRX-{uuid4().hex[:12].upper()}","ledger":"drunix-mock","timestamp":datetime.now(timezone.utc).isoformat(),"status":"RECORDED","payload":payload}
