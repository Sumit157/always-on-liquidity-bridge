from services.compliance import ComplianceEngine
from services.models import PaymentRequest

def test_normal_payment_passes():
    p=PaymentRequest("Citi","Bank X","USD",10_000_000,"Singapore","Treasury")
    assert ComplianceEngine().evaluate(p).passed

def test_same_bank_rejected():
    p=PaymentRequest("Citi","Citi","USD",10_000_000,"Singapore","Treasury")
    assert not ComplianceEngine().evaluate(p).passed
