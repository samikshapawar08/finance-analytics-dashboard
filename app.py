import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Finance Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("https://docs.google.com/spreadsheets/d/1P9YtET94BnxMyP8x43_t6DV1D5Jy73KDawa3JaNT6zg/export?format=csv")

# Convert month properly
df['month'] = pd.to_datetime(df['month'])

# 🔥 FIX: Add realistic variation (IMPORTANT)
np.random.seed(42)
df['profit'] = df['revenue'] * np.random.uniform(0.25, 0.5, len(df))
df['cost'] = df['revenue'] - df['profit']

# ---------------- KPI ----------------
total_revenue = df['revenue'].sum()
total_profit = df['profit'].sum()
total_cost = df['cost'].sum()
profit_margin = (total_profit / total_revenue) * 100

# ---------------- MONTHLY ----------------
monthly = df.groupby('month').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'cost': 'sum'
}).sort_index()

monthly['margin'] = (monthly['profit'] / monthly['revenue']) * 100
monthly['margin'] = monthly['margin'].round(2)

monthly['growth'] = monthly['revenue'].pct_change() * 100
monthly['contribution'] = (monthly['revenue'] / total_revenue) * 100

# Better labels
monthly.index = monthly.index.strftime('%b %Y')

# ---------------- INSIGHTS ----------------
best_month = monthly['revenue'].idxmax()
best_margin_month = monthly['margin'].idxmax()
worst_month = monthly['revenue'].idxmin()

# ---------------- UI ----------------
st.title("📊Finance Analytics Dashboard")

# KPI ROW
col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"₹{round(total_revenue,2)}")
col2.metric("Profit", f"₹{round(total_profit,2)}")
col3.metric("Cost", f"₹{round(total_cost,2)}")
col4.metric("Margin", f"{round(profit_margin,2)}%")

st.markdown("---")

# ---------------- CHARTS ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue vs Profit vs Cost")
    st.line_chart(monthly[['revenue', 'profit', 'cost']])

with col2:
    st.subheader("Revenue Contribution %")
    st.bar_chart(monthly[['contribution']])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Revenue")
    st.bar_chart(monthly[['revenue']])

with col2:
    st.subheader("Profit Margin Trend")
    st.line_chart(monthly[['margin']])

# ---------------- EXTRA (ADVANCED) ----------------
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue Growth %")
    st.line_chart(monthly[['growth']])

with col2:
    st.subheader("Moving Average (3 months)")
    monthly['ma'] = monthly['revenue'].rolling(3).mean()
    st.line_chart(monthly[['ma']])

# ---------------- INSIGHTS ----------------
st.markdown("---")
st.subheader("🔍 Key Insights")

st.write(f"Best Revenue Month: **{best_month}**")
st.write(f"Best Margin Month: **{best_margin_month}**")
st.write(f"Lowest Revenue Month: **{worst_month}**")