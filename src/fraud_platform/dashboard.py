import os
import requests
import streamlit as st

st.set_page_config(page_title="Fraud Detection", layout="centered")
st.title("Real-Time Fraud Detection")
st.caption("Submit a transaction to the FastAPI model endpoint.")
with st.form('transaction'):
    step=st.number_input('Step',min_value=0,value=1)
    kind=st.selectbox('Transaction type',['PAYMENT','TRANSFER','CASH_OUT','CASH_IN','DEBIT'])
    amount=st.number_input('Amount',min_value=0.0,value=1000.0)
    old_org=st.number_input('Origin balance before',min_value=0.0,value=5000.0)
    new_org=st.number_input('Origin balance after',min_value=0.0,value=4000.0)
    old_dest=st.number_input('Destination balance before',min_value=0.0,value=0.0)
    new_dest=st.number_input('Destination balance after',min_value=0.0,value=1000.0)
    submitted=st.form_submit_button('Score transaction')
if submitted:
    payload={'step':step,'type':kind,'amount':amount,'oldbalanceOrg':old_org,'newbalanceOrig':new_org,'oldbalanceDest':old_dest,'newbalanceDest':new_dest}
    try:
        r=requests.post(os.getenv('API_URL','http://localhost:8000')+'/predict',json=payload,timeout=15); r.raise_for_status(); result=r.json()
        st.metric('Fraud probability',f"{result['fraud_probability']:.2%}")
        if result['is_fraud']: st.error('Flagged for review')
        else: st.success('Not flagged by current threshold')
        st.json(result)
    except requests.RequestException as e: st.error(f'API unavailable: {e}')
