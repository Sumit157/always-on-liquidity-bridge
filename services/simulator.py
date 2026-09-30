from .models import Route

DEFAULT_ROUTES = [
    Route("R-A", "Token Network A", "TOKEN", 15, 35, 50_000_000, True, ("USD", "SGD")),
    Route("R-B", "Real-Time Rail B", "RTP", 90, 18, 20_000_000, True, ("USD", "EUR", "GBP", "SGD")),
    Route("R-C", "Legacy Correspondent Rail", "LEGACY", 86_400, 125, 100_000_000, False, ("USD", "EUR", "GBP", "SGD")),
]
