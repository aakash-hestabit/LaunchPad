import streamlit as st
import pandas as pd

st.title("Loan Prediction Monitor")

logs = pd.read_csv("prediction_logs.csv")
logs['timestamp'] = pd.to_datetime(logs['timestamp']) 

st.metric("Total Loan Requests", len(logs))

st.subheader("Approval (1) vs Rejection (0)")
st.bar_chart(logs["prediction"].value_counts())

st.subheader("Traffic Over Time")
logs_over_time = logs.set_index("timestamp").resample("1min").count()
st.line_chart(logs_over_time["prediction"])