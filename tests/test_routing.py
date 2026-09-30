from services.models import PaymentRequest
from services.routing import SmartRouter
from services.simulator import DEFAULT_ROUTES

def test_balanced_route_selects_token_route():
    p=PaymentRequest("Citi","Bank X","USD",10_000_000,"Singapore","Treasury")
    assert SmartRouter(DEFAULT_ROUTES).decide(p).route_id=="R-A"

def test_no_route_when_liquidity_is_insufficient():
    p=PaymentRequest("Citi","Bank X","USD",60_000_000,"Singapore","Treasury")
    assert SmartRouter(DEFAULT_ROUTES).decide(p) is None
