import streamlit as st
import requests

API_URL = "https://w6sgoz4cgbwdjivtngvymiwyva0drahm.lambda-url.us-east-1.on.aws/predict"  # keep your real URL here

st.set_page_config(page_title="UrbanCart Churn Predictor", page_icon="🛒", layout="centered")

st.title("🛒 UrbanCart Churn Predictor")
st.markdown("##### Predict whether a customer is likely to churn, based on their activity.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    months_active = st.number_input("Months Active", min_value=0, value=8)
    num_orders = st.number_input("Orders Last Quarter", min_value=0, value=3)
    support_tickets = st.number_input("Support Tickets Filed", min_value=0, value=2)

with col2:
    avg_order_value = st.number_input("Average Order Value ($)", min_value=0.0, value=45.20)
    days_since_last_order = st.number_input("Days Since Last Order", min_value=0, value=40)

if st.button("Predict", type="primary", use_container_width=True):
    payload = {
        "MonthsActive": months_active,
        "AvgOrderValue": avg_order_value,
        "NumOrdersLastQuarter": num_orders,
        "DaysSinceLastOrder": days_since_last_order,
        "SupportTicketsFiled": support_tickets,
    }

    with st.spinner("Getting prediction..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        st.divider()

        if result["churn_prediction"] == 1:
            st.error("This customer is likely to churn")
        else:
            st.success("This customer is likely to stay")

        st.metric("Churn Probability", f"{result['churn_probability']:.1%}")
    else:
        st.error(f"Request failed ({response.status_code}): {response.text}")