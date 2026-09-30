import os, requests, streamlit as st
API_URL=os.getenv("API_URL","http://localhost:8000")
st.set_page_config(page_title="Always-On Liquidity Bridge",page_icon="↔",layout="wide")
st.title("Always-On Multi-Bank Liquidity Bridge")
st.caption("Interoperability Friction Analyzer · Prototype / Simulated")
with st.sidebar:
    st.header("Payment Scenario")
    source=st.selectbox("Sending bank",["Citi New York","Bank Alpha London","Bank Delta Frankfurt"])
    destination=st.selectbox("Receiving bank",["Bank X Singapore","Bank Y Tokyo","Bank Z Dubai"])
    currency=st.selectbox("Currency",["USD","EUR","GBP","SGD"])
    amount=st.number_input("Amount",min_value=1000.0,value=10000000.0,step=100000.0)
    country=st.selectbox("Destination country",["Singapore","Japan","UAE","United Kingdom"])
    purpose=st.text_input("Payment purpose","Corporate treasury transfer")
    objective=st.selectbox("Routing objective",["balanced","speed","cost"])
    analyse_btn=st.button("Analyse Payment",type="primary",use_container_width=True)
    execute_btn=st.button("Execute Simulated Payment",use_container_width=True)
payload={"source_bank":source,"destination_bank":destination,"currency":currency,"amount":amount,"country":country,"purpose":purpose,"objective":objective}
if analyse_btn or execute_btn:
    try:
        response=requests.post(API_URL+("/execute" if execute_btn else "/analyze"),json=payload,timeout=10); data=response.json()
        if response.status_code>=400: st.error(data.get("detail","Request failed"))
        else:
            c1,c2,c3,c4=st.columns(4); c1.metric("Payment",f"{currency} {amount:,.0f}")
            if data.get("selected"):
                fr=data["selected"]["friction"]; c2.metric("Estimated latency",f'{fr["estimated_latency_seconds"]:,} s'); c3.metric("Intermediaries",fr["intermediaries"]); c4.metric("Estimated fee",f'{currency} {fr["estimated_fee"]:,.2f}')
            st.subheader("Compliance"); st.success("Prototype policy checks passed.") if data["compliance"]["passed"] else st.error("Prototype policy checks failed.")
            for name,passed in data["compliance"]["checks"].items(): st.write(("✓ " if passed else "✕ ")+name.replace("_"," ").title())
            st.subheader("Eligible Routes")
            for item in data.get("candidates",[]):
                r=item["route"]; f=item["friction"]; selected=(data.get("selected") or {}).get("route",{}).get("id")==r["id"]
                with st.container(border=True):
                    a,b,c=st.columns([2,1,1]); a.write(f'**{r["name"]}** · {r["network_type"]}'); b.write(f'Latency: {f["estimated_latency_seconds"]:,}s'); c.write(f'Fee: {currency} {f["estimated_fee"]:,.2f}')
                    st.write(f'Steps: {f["steps"]} · Intermediaries: {f["intermediaries"]} · 24/7: {"Yes" if f["operating_24x7"] else "No"}')
                    if selected: st.info(f'Selected for this scenario · score {data["decision"]["score"]}')
            if data.get("settlement"): st.subheader("Settlement"); st.success("Simulated settlement recorded."); st.json(data["settlement"])
    except requests.RequestException as exc: st.error(f"API unavailable: {exc}")
else: st.markdown("### Demo scenario\n**USD 10M** · Citi New York → Bank X Singapore\n\nUse the sidebar to analyse routes and execute a simulated settlement.")
