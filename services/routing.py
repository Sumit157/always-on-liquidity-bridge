from .models import PaymentRequest, Route, RouteDecision

class SmartRouter:
    def __init__(self, routes: list[Route]): self.routes = routes
    def eligible_routes(self, payment: PaymentRequest) -> list[Route]:
        return [r for r in self.routes if payment.currency in r.currencies and r.compliance_ready and r.settlement_capable and r.liquidity_available >= payment.amount]
    def decide(self, payment: PaymentRequest, objective: str = "balanced") -> RouteDecision | None:
        candidates = self.eligible_routes(payment)
        if not candidates: return None
        scored=[]
        for r in candidates:
            latency=max(0.0,100.0-min(r.latency_seconds/60.0,100.0))
            fee=max(0.0,100.0-min((r.fee/max(payment.amount,1))*100000,100.0))
            liquidity=min(r.liquidity_available/payment.amount*20,100.0)
            availability=100.0 if r.available_24x7 else 40.0
            if objective=="speed": score=.55*latency+.15*fee+.15*liquidity+.15*availability
            elif objective=="cost": score=.55*fee+.15*latency+.15*liquidity+.15*availability
            else: score=.35*latency+.25*fee+.20*liquidity+.20*availability
            reasons=[f"Estimated latency: {r.latency_seconds}s",f"Estimated fee: {payment.currency} {r.fee:,.2f}","24/7 operating window" if r.available_24x7 else "Restricted operating window","Sufficient route liquidity"]
            scored.append((r,round(score,2),reasons))
        scored.sort(key=lambda x:x[1],reverse=True)
        r,score,reasons=scored[0]
        return RouteDecision(r.id,score,reasons)
