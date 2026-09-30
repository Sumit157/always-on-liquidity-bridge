from .models import ComplianceResult, PaymentRequest

class ComplianceEngine:
    def evaluate(self, payment: PaymentRequest) -> ComplianceResult:
        checks = {
            "supported_currency": payment.currency.upper() in {"USD", "EUR", "GBP", "SGD"},
            "positive_amount": payment.amount > 0,
            "amount_limit": payment.amount <= 50_000_000,
            "source_destination_distinct": payment.source_bank != payment.destination_bank,
            "purpose_present": bool(payment.purpose.strip()),
        }
        reasons = []
        if not checks["supported_currency"]: reasons.append("Currency is not supported by prototype policy.")
        if not checks["amount_limit"]: reasons.append("Amount exceeds configured prototype limit.")
        if not checks["source_destination_distinct"]: reasons.append("Source and destination banks must differ.")
        return ComplianceResult(all(checks.values()), checks, reasons)
