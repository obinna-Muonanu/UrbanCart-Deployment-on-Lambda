import streamlit as st
import requests

API_URL = "https://w6sgoz4cgbwdjivtngvymiwyva0drahm.lambda-url.us-east-1.on.aws/predict"  # replace with your actual URL

st.title("UrbanCart Churn Predictor")
st.write("Enter customer details to predict churn risk.")

months_active = st.number_input("Months Active", min_value=0, value=8)
avg_order_value = st.number_input("Average Order Value", min_value=0.0, value=45.20)
num_orders = st.number_input("Orders Last Quarter", min_value=0, value=3)
days_since_last_order = st.number_input("Days Since Last Order", min_value=0, value=40)
support_tickets = st.number_input("Support Tickets Filed", min_value=0, value=2)

if st.button("Predict"):
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
        label = "Will churn" if result["churn_prediction"] == 1 else "Will not churn"
        st.subheader(f"Prediction: {label}")
        st.write(f"Churn probability: {result['churn_probability']:.2%}")
    else:
        st.error(f"Request failed ({response.status_code}): {response.text}")