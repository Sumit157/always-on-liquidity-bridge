from dataclasses import dataclass

@dataclass(frozen=True)
class PaymentRequest:
    source_bank: str
    destination_bank: str
    currency: str
    amount: float
    country: str
    purpose: str
    urgency: str = "standard"

@dataclass(frozen=True)
class Route:
    id: str
    name: str
    network_type: str
    latency_seconds: int
    fee: float
    liquidity_available: float
    available_24x7: bool
    currencies: tuple[str, ...]
    compliance_ready: bool = True
    settlement_capable: bool = True

@dataclass(frozen=True)
class RouteDecision:
    route_id: str
    score: float
    reasons: list[str]

@dataclass(frozen=True)
class ComplianceResult:
    passed: bool
    checks: dict[str, bool]
    reasons: list[str]
