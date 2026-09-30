from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from services.compliance import ComplianceEngine
from services.ledger import MockDrunixLedger
from services.models import PaymentRequest
from services.routing import SmartRouter
from services.simulator import DEFAULT_ROUTES

app=FastAPI(title="Always-On Multi-Bank Liquidity Bridge API",version="0.1.0")
router=SmartRouter(DEFAULT_ROUTES); compliance=ComplianceEngine(); ledger=MockDrunixLedger()

class PaymentIn(BaseModel):
    source_bank:str; destination_bank:str; currency:str=Field(min_length=3,max_length=3); amount:float=Field(gt=0); country:str; purpose:str; urgency:str="standard"; objective:str="balanced"

@app.get("/health")
def health(): return {"status":"ok","service":"bridge-api","ledger":"mock-drunix"}
@app.get("/routes")
def routes(): return [r.__dict__ for r in DEFAULT_ROUTES]

def analyse(payment_in:PaymentIn):
    p=PaymentRequest(payment_in.source_bank,payment_in.destination_bank,payment_in.currency.upper(),payment_in.amount,payment_in.country,payment_in.purpose,payment_in.urgency)
    comp=compliance.evaluate(p)
    if not comp.passed: return {"status":"REJECTED","payment":p.__dict__,"compliance":comp.__dict__,"candidates":[],"decision":None,"selected":None}
    candidates=router.eligible_routes(p); decision=router.decide(p,payment_in.objective); views=[]
    for r in candidates:
        views.append({"route":r.__dict__,"friction":{"steps":3 if r.network_type=="TOKEN" else 4 if r.network_type=="RTP" else 8,"intermediaries":0 if r.network_type=="TOKEN" else 1 if r.network_type=="RTP" else 3,"estimated_latency_seconds":r.latency_seconds,"estimated_fee":r.fee,"operating_24x7":r.available_24x7,"liquidity_headroom":max(r.liquidity_available-p.amount,0),"baseline_latency_seconds":86400}})
    selected=next((x for x in views if decision and x["route"]["id"]==decision.route_id),None)
    return {"status":"ELIGIBLE","payment":p.__dict__,"compliance":comp.__dict__,"candidates":views,"decision":decision.__dict__ if decision else None,"selected":selected}

@app.post("/analyze")
def analyze(payment_in:PaymentIn): return analyse(payment_in)
@app.post("/execute")
def execute(payment_in:PaymentIn):
    result=analyse(payment_in)
    if result["status"]!="ELIGIBLE" or not result["selected"]: raise HTTPException(400,"Payment is not eligible for execution")
    return {**result,"settlement":ledger.register_transfer({"payment":result["payment"],"route":result["selected"]["route"],"status":"SIMULATED_SETTLEMENT"})}
